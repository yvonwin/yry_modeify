import dlib
import numpy as np
import cv2
import os
from time import time
PREDICTOR_PATH = "./shape_predictor_68_face_landmarks.dat"

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(PREDICTOR_PATH)


def matrix_marks(image):
    pointer = []
    txt = image + ".txt"
    image = cv2.imread(image,cv2.IMREAD_COLOR)
    fp = open(txt,'w+')
    rects = detector(image,1)
    matrix_list = np.matrix([[p.x,p.y] for p in (predictor(image, rects[0]).parts())])
    print({"before matrix_marks"})
    # print(matrix_list)
    for p in matrix_list.tolist():
        fp.write(str(p[0])+' '+str(p[1]))
        fp.write('\n')
        # print(p[0],p[1]
    return matrix_list

def face_points(image):
    points  = []
    # matrix_list = matrix_marks(image)
    start = time()
    txt = image + '.txt'
    if os.path.isfile(txt):
        with open(txt) as file:
           for line in file:
            #   points =  line
            x,y = line.split()
            points.append((int(x),int(y)))
        # print(points)
        matrix_list = np.loadtxt(txt,dtype=int)
        matrix_list = np.mat(matrix_list)
        return matrix_list,points
    elif os.path.isfile(image):
        matrix_list = matrix_marks(image)
        if os.path.isfile(txt):
            with open(txt) as file:
                for line in file:
            #   points =  line
                 x,y = line.split()
                 points.append((int(x),int(y)))
        stop = time()
        print(str(stop-start))
        return matrix_list,points
    # print(points)
    # elif os.path.isfile(image):
    #     matrix_marks = matrix_marks(image)
        # print(matrix_marks)
        # with open(txt) as file:
        #    for line in file:
        #     #   points =  line
        #     x,y = line.split()
        #     points.append(int(x),int(y))
        # print(points)
        # return points
   
        # with open(txt, 'w') as file:
            # file.write(str(points))
    
if __name__ == '__main__':
    image = './sen/sen-2.png'
    # print(image)
    # matrix_list_1 = matrix_marks(image)
    matrix_list,points= face_points(image)
    print(points)
    print("********")
    # print(matrix_list)
    # print(matrix_list_1)


    trans_file = './sen/sen-1.png'
    trans_img = cv2.imread(trans_file,cv2.IMREAD_COLOR)
    print(trans_img)
    matrix_list = matrix_marks(trans_file)
    # # cv2.imwrite(trans_file, dst_img)
    # # print(trans_file)
    # matrix_list1,points1 = face_points(trans_file)
    # print(points

    # test_img = 'images/sen.png'
    # matrix_list1,points1 = face_points(test_img)
    # print(matrix_list1)
    # print(points1)
    