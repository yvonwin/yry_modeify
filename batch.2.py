import argparse
import core
import glob
import os
from time import time

# 一张图片替换
def main():
    # os.environ['CUDA_VISIBLE_DEVICES'] = 0
    ap = argparse.ArgumentParser(description='batch face swap routine')
    ap.add_argument('-s', '--source_dir', type=str, help='input source directory')
    ap.add_argument('-d', '--dest_dir', type=str, help='input destination directory')
    ap.add_argument('-o', '--output_dir', type=str, help='output directory')

    args = ap.parse_args()
    sd = args.source_dir
    dd = args.dest_dir
    od = args.output_dir
    i = 0
    
    source_path_list = []
    target_path_list = []
    if not os.path.exists(od):
        os.mkdir(od)
    types = ('*.jpg','*.png')
    for files in types:
        source_path_list.extend(glob.glob(os.path.join((sd),files)))
        # target_path_list.extend(glob.glob(os.path.join((dd),files)))
    # source_path_list = glob.glob(sd)
    # target_path_list = glob.glob(dd)
    # source_path_list = glob.glob(os.path.join(sd,'*.png'))
    # target_path_list = glob.glob(os.path.join(dd,'*.png'))

    source_path_list.sort(key=lambda x: int(x.split('.')[1].split('-')[-1]))
    # target_path_list.sort(key=lambda x: int(x.split('.')[1].split('-')[-1]))
    # print(source_path_list)
    d = './C/jin-02.png'
    for s in source_path_list:
      core.face_merge(src_img=s, dst_img=d, out_img=os.path.join(od, 'output-{0}.jpg'.format(i)),face_area=[50, 30, 500, 485],
                    alpha=0.75,
                    k_size=(15, 10),
                    mat_multiple=0.95)
      i = i + 1
      print("已处理",i,"张图片")


if __name__ == '__main__':
    start = time()
    main()
    stop  = time()
    print("总共用时"+str(stop-start)+"秒")