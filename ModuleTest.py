# -*- coding: utf-8 -*-
# @Time    : 2017/9/2 13:40
# @Author  : 郑梓斌

import core
from time import time
# src-img ---- 模特图片
# dst_img ---- 带融合图片
# out_img ---- 结果图片输出路径
# face_area ---- 指定模板图中进行人脸融合的人脸框位置。四个正整数数组，依次代表人脸框左上角纵坐标（top），左上角横坐标（left），
# 人脸框宽度（width），人脸框高度（height），通过设定改参数可以减少结果的大范围变形，把变形风险控制在人脸框区域
# alpha —— 融合比例，范围 [0,1]。数字越大融合结果包含越多融合图 (dst_img) 特征。
# blur_size—— 模糊核大小，用于模糊人脸融合边缘，减少融合后的违和感
# mat_multiple —— 缩放获取到的人脸心型区域

if __name__ == '__main__':
    start = time()    
    core.face_merge(src_img='./images/b.jpg',
                    dst_img='./images/aa.jpg',
                    out_img='output/output_test_source.png',
                    face_area=[50, 30, 500, 485],
                    alpha=0.75,
                    k_size=(15, 10),
                    mat_multiple=0.95)
    stop = time()
    print(str(stop-start)+"秒")
    
