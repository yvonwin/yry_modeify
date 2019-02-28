# -*- coding: utf-8 -*-
# @Time    : 2017/9/2 13:40

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


def gen_frames(movie, dir_name):
  '''generate frames in temporal order'''
  import os
  if not os.path.exists(dir_name):
    os.mkdir(dir_name)
  else:
    return
  os.system('ffmpeg -i {0} {1}'.format(movie, os.path.join(dir_name, 'frame-%0d.png')))



def movie_swap(temp_movie, dst_movie):
  import glob, os
  # gen frames for temp and dst
 
  start = time()

  gen_frames(temp_movie, 'A2')
  gen_frames(dst_movie, 'B2')
  if not os.path.exists('out'):
    os.mkdir('out')
  # swap every face
  framesA = sorted(glob.glob('A2/*.png'), key=lambda x:int(os.path.basename(x).split('.')[0].split('-')[-1]))
  framesB = sorted(glob.glob('B2/*.png'), key=lambda x:int(os.path.basename(x).split('.')[0].split('-')[-1]))
  i = 0
  for f_a, f_b in zip(framesA, framesB):
    core.face_merge(src_img=f_a,
                    dst_img=f_b,
                    out_img='out/frame-{0}.png'.format(i),
                    face_area=[50, 30, 500, 485],
                    alpha=0.95,
                    k_size=(15, 10),
                    mat_multiple=0.95)
    i = i + 1
    print("已处理",i,"张图片")
  stop = time()
  print("总共用时"+str(stop-start)+"秒")
  # composite movie
  os.system('ffmpeg -i out/frame-%0d.png -c:v libx264 -vf "fps=25,format=yuv420p" out/out.mp4')


def main():
  start = time()
  core.face_merge(src_img='./target/sen-00015.png',
                  dst_img='./shiyuan/shiyuan-6.png',
                  out_img='output/1.png',
                  face_area=[50, 30, 500, 485],
                  alpha=0.75,
                  k_size=(15, 10),
                  mat_multiple=0.95)
  stop = time()
  print(str(stop - start) + "秒")



if __name__ == '__main__':
    # start = time()
    movie_swap('movies/zjk-480.mp4', 'movies/news_1.mp4')
    # stop  = time()
