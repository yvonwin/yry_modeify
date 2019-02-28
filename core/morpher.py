# -*- coding: utf-8 -*-
# @Time    : 2017/9/2 13:40

import cv2
import time
import numpy as np
import os
import PIL.Image

import core
import test



SCALE_FACTOR = 1
FEATHER_AMOUNT = 11


# 用procrustes分析对齐人脸
def transformation_points(src_img, src_points, dst_img, dst_points):
    start = time.time()
    src_points = src_points.astype(np.float64)
    dst_points = dst_points.astype(np.float64)

    c1 = np.mean(src_points, axis=0)
    c2 = np.mean(dst_points, axis=0)

    src_points -= c1
    dst_points -= c2

    s1 = np.std(src_points)
    s2 = np.std(dst_points)

    src_points /= s1
    dst_points /= s2

    u, s, vt = np.linalg.svd(src_points.T * dst_points)
    r = (u * vt).T

    m = np.vstack([np.hstack(((s2 / s1) * r, c2.T - (s2 / s1) * r * c1.T)), np.matrix([0., 0., 1.])])

    # 结果插入OpenCv的cv2.warpAffine函数，将函数二映射到图像一
    output = cv2.warpAffine(dst_img, m[:2],
                            (src_img.shape[1], src_img.shape[0]),
                            borderMode=cv2.BORDER_TRANSPARENT,
                            flags=cv2.WARP_INVERSE_MAP)
    stop = time.time()
    print("transformation用时",str(stop-start)+"秒")
    return output


#     # 未使用
# def tran_matrix(src_img, src_points, dst_img, dst_points):
#     h = cv2.findHomography(dst_points, src_points)
#     output = cv2.warpAffine(dst_img, h[0][:2], (src_img.shape[1], src_img.shape[0]),
#                             borderMode=cv2.BORDER_TRANSPARENT,
#                             flags=cv2.WARP_INVERSE_MAP)

#     return output


# def tran_similarity(src_img, src_points, dst_img, dst_points):
#     s60 = math.sin(60 * math.pi / 180)
#     c60 = math.cos(60 * math.pi / 180)

#     in_pts = np.copy(dst_points).tolist()
#     out_pts = np.copy(src_points).tolist()

#     x_in = c60 * (in_pts[0][0] - in_pts[1][0]) - s60 * (in_pts[0][1] - in_pts[1][1]) + in_pts[1][0]
#     y_in = s60 * (in_pts[0][0] - in_pts[1][0]) + c60 * (in_pts[0][1] - in_pts[1][1]) + in_pts[1][1]

#     in_pts.append([np.int(x_in), np.int(y_in)])

#     x_out = c60 * (out_pts[0][0] - out_pts[1][0]) - s60 * (out_pts[0][1] - out_pts[1][1]) + out_pts[1][0]
#     y_out = s60 * (out_pts[0][0] - out_pts[1][0]) + c60 * (out_pts[0][1] - out_pts[1][1]) + out_pts[1][1]

#     out_pts.append([np.int(x_out), np.int(y_out)])

#     m = cv2.estimateRigidTransform(np.array([in_pts]), np.array([out_pts]), False)

#     output = cv2.warpAffine(dst_img, m, (src_img.shape[1], src_img.shape[0]))

#     return output


# 校正颜色
def correct_color(img1, img2, landmark):
    blur_amount = 0.4 * np.linalg.norm(
        np.mean(landmark[core.LEFT_EYE_POINTS], axis=0)
        - np.mean(landmark[core.RIGHT_EYE_POINTS], axis=0)
    )
    blur_amount = int(blur_amount)

    if blur_amount % 2 == 0:
        blur_amount += 1

    img1_blur = cv2.GaussianBlur(img1, (blur_amount, blur_amount), 0)
    img2_blur = cv2.GaussianBlur(img2, (blur_amount, blur_amount), 0)

    img2_blur += (128 * (img2_blur <= 1.0)).astype(img2_blur.dtype)

    return img2.astype(np.float64) * img1_blur.astype(np.float64) / img2_blur.astype(np.float64)


def tran_src(src_img, src_points, dst_points, face_area=None):
    # jaw = core.JAW_END

    dst_list = dst_points \
               + core.matrix_rectangle(face_area[0], face_area[1], face_area[2], face_area[3]) \
               + core.matrix_rectangle(0, 0, src_img.shape[1], src_img.shape[0])

    src_list = src_points \
               + core.matrix_rectangle(face_area[0], face_area[1], face_area[2], face_area[3]) \
               + core.matrix_rectangle(0, 0, src_img.shape[1], src_img.shape[0])

    # jaw_points = []

    # for i in range(0, jaw):
    #     jaw_points.append(dst_list[i])
    #     jaw_points.append(src_list[i])

    # warp_jaw = cv2.convexHull(np.array(jaw_points), returnPoints=False)
    # warp_jaw = warp_jaw.tolist()

    # for i in range(0, len(warp_jaw)):
    #     warp_jaw[i] = warp_jaw[i][0]

    # warp_jaw.sort()

    # if len(warp_jaw) <= jaw:
    #     dst_list = dst_list[jaw - len(warp_jaw):]
    #     src_list = src_list[jaw - len(warp_jaw):]
    #     for i in range(0, len(warp_jaw)):
    #         dst_list[i] = jaw_points[int(warp_jaw[i])]
    #         src_list[i] = jaw_points[int(warp_jaw[i])]
    # else:
    #     for i in range(0, jaw):
    #         if len(warp_jaw) > jaw and warp_jaw[i] == 2 * i and warp_jaw[i + 1] == 2 * i + 1:
    #             warp_jaw.remove(2 * i)

    #         dst_list[i] = jaw_points[int(warp_jaw[i])]

    dt = core.measure_triangle(src_img.shape, dst_list)

    res_img = np.zeros(src_img.shape, dtype=src_img.dtype)

    for i in range(0, len(dt)):
        t_src = []
        t_dst = []

        for j in range(0, 3):
            t_src.append(src_list[dt[i][j]])
            t_dst.append(dst_list[dt[i][j]])

        core.affine_triangle(src_img, res_img, t_src, t_dst)

    return res_img


def merge_img(src_img, dst_img, dst_matrix, dst_points, k_size=None, mat_multiple=None):
    '''
    获得面部遮罩
    '''
    start  = time.time()
    face_mask = np.zeros(src_img.shape, dtype=src_img.dtype)
    # OVERLAY_POINTS是一组特征点，对每个特征点用draw_conex_hul用白色填充（color=1)
    for group in core.OVERLAY_POINTS:
        cv2.fillConvexPoly(face_mask, cv2.convexHull(dst_matrix[group]), (255, 255, 255))

    r = cv2.boundingRect(np.float32([dst_points[:core.FACE_END]]))

    center = (r[0] + int(r[2] / 2), r[1] + int(r[3] / 2))

    if mat_multiple:
        mat = cv2.getRotationMatrix2D(center, 0, mat_multiple)
        face_mask = cv2.warpAffine(face_mask, mat, (face_mask.shape[1], face_mask.shape[0]))

    if k_size:
        face_mask = cv2.blur(face_mask, k_size, center)

    return cv2.seamlessClone(np.uint8(dst_img), src_img, face_mask, center, cv2.NORMAL_CLONE)
    stop = time.time()
    print("merge_img用时:"+str(stop-start)+"秒")

#图片变形
def morph_img(src_img, src_points, dst_img, dst_points, alpha=0.5,show_bg=None):
    # test time 
    start = time.time()

    src_img = src_img.astype(np.float32)
    dst_img = dst_img.astype(np.float32)

    morph_points = []

    if show_bg:
        res_img = src_img.copy()
    else:
        res_img = np.zeros(src_img.shape, src_img.dtype)

    for i in range(0, len(src_points)):
        x = (1 - alpha) * src_points[i][0] + alpha * dst_points[i][0]
        y = (1 - alpha) * src_points[i][1] + alpha * dst_points[i][1]
        morph_points.append((x, y))
    

    # dt = core.measure_triangle(src_img, morph_points)
    dt = core.measure_triangle(src_img, src_points)

    for i in range(0, len(dt)):
        t1 = []
        t2 = []
        t = []

        for j in range(0, 3):
            t1.append(src_points[dt[i][j]])
            t2.append(dst_points[dt[i][j]])
            t.append(morph_points[dt[i][j]])

        core.morph_triangle(src_img, dst_img, res_img, t1, t2, t, alpha)
    stop = time.time()
    print("morph_img用时"+str(stop-start)+"秒")
    
    return res_img


def face_merge(dst_img, src_img, out_img,
               face_area, alpha=0.75,
               k_size=None, mat_multiple=None):
    # 获取两张图片的人脸关键点（矩阵格式与数组格式）
    # src_matrix, src_points = core.face_points(src_img)
    # dst_matrix, dst_points = core.face_points(dst_img)
    #
    #
    # print(test)
    print(src_img)
    dst_name = dst_img.split('.')[1].split('/')[-1]
    # print(src_name)

    start = time.time() 
    src_matrix,src_points = core.face_points(src_img)
    dst_matrix,dst_points = core.face_points(dst_img)

    # opencv读取图片
    start_read = time.time()

    src_img = cv2.imread(src_img, cv2.IMREAD_COLOR)
    dst_img = cv2.imread(dst_img, cv2.IMREAD_COLOR)

    # stop_read = time.time()
    # print("读两张图片用时"+str(stop_read-start_read)+"秒")
    src_img = cv2.resize(src_img,(src_img.shape[1] * SCALE_FACTOR,
                          src_img.shape[0] * SCALE_FACTOR))

    dst_img = cv2.resize(dst_img,(dst_img.shape[1] * SCALE_FACTOR,
                          dst_img.shape[0] * SCALE_FACTOR))
    # # print(src_img1)
    print("********************")
    # 获取两张图片的人脸关键点（矩阵格式与数组格式）
    # src_matrix,src_points = core.face_points(src_img)
    # dst_matrix, dst_points = core.face_points(dst_img)

    dst_img = transformation_points(src_img=src_img, src_points=src_matrix[core.FACE_POINTS],
                                    dst_img=dst_img, dst_points=dst_matrix[core.FACE_POINTS])

    # print(dst_img)
    trans_file = 'temp/' + dst_name + str(time.time()) + '_trans.jpg'
    if ((os.path.isfile(trans_file))== False):
        cv2.imwrite(trans_file, dst_img)
    # print(trans_file)
    # trans_img = cv2.imread(trans_file,cv2.IMREAD_COLOR)

    # test del
    dst_matrix,dst_points = core.face_points(trans_file)

    # print(dst_points)
    # print(len(dst_points))
    # 再次取点后融合脸部
    start_morph = time.time()
    dst_img = morph_img(src_img, src_points, dst_img, dst_points, alpha)
    stop_morph = time.time()
    print("morph用时"+str(stop_morph-start_morph)+"秒")

    # morph_file = 'temp/' + dst_name +str(int(time.time() * 1000))+ '_morph.jpg'
    morph_file = 'temp/' + dst_name +str(time.time()) + '_morph.jpg'
    
    if((os.path.isfile(morph_file))==False):
        cv2.imwrite(morph_file, dst_img)
    # morph_img1 = cv2.imread(morph_file,cv2.IMREAD_COLOR)
    
    # print(morph_file)
    
    #test del
    # dst_matrix,dst_points = core.face_points(morph_file)

    # 再次对上一部的结果进行取点，然后运用三角放射将模特图片脸部轮廓、关键点变形成上一部得到的关键点
    # src_img = tran_src(src_img, src_points, dst_points, face_area)
    
    # 将融合后的新图片脸部区域用泊松融合算法贴合到模特图上
    start_merge = time.time()
    dst_img = merge_img(src_img, dst_img, dst_matrix, dst_points, k_size, mat_multiple)
    stop_merge = time.time()
    print("merge用时"+str(stop_merge-start_merge)+"秒")
    # os.remove(trans_file)
    # os.remove(trans_file + '.txt')

    # os.remove(morph_file)
    # os.remove(morph_file + '.txt')

    cv2.imwrite(out_img, dst_img)
    stop =time.time()
    print("这张用时"+str(stop-start)+"秒")