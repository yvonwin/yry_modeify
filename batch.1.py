import argparse
import core
import glob
import os


def main():
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
    # types = ('*.jpg','*.png')
    source_path_list = glob.glob(os.path.join(sd,'*.png'))
    target_path_list = glob.glob(os.path.join(dd,'*.png'))

    source_path_list.sort(key=lambda x: int(x.split('.')[0].split('-')[-1]))
    target_path_list.sort(key=lambda x: int(x.split('.')[0].split('-')[-1]))

    for s, d in zip((glob.iglob(os.path.join(sd, '*.png'))), glob.iglob(os.path.join(dd, '*.png'))):
      core.face_merge(src_img=s, dst_img=d, out_img=os.path.join(od, 'output-{0}.jpg'.format(i)),face_area=[50, 30, 500, 485],
                    alpha=0.75,
                    k_size=(15, 10),
                    mat_multiple=0.95)
      i = i + 1


if __name__ == '__main__':
    main()