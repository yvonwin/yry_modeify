# -*- coding: utf-8 -*-
# @Time    : 2017/9/2 13:40
# @Author  : 郑梓斌

import json
import os

import requests
import numpy as np
import  dlib
import cv2

from time import time

PREDICTOR_PATH = "./shape_predictor_68_face_landmarks.dat"
SCALE_FACTOR = 1
FEATHER_AMOUNT = 11

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(PREDICTOR_PATH)


FACE_POINTS = list(range(17, 68))
JAW_POINTS = list(range(0, 17))
LEFT_EYE_POINTS = list(range(36, 42))
LEFT_BROW_POINTS = list(range(22, 27))
MOUTH_POINTS = list(range(48, 61))
LIP_POINTS = list(range(49,65))
NOSE_POINTS = list(range(27, 35))
RIGHT_EYE_POINTS = list(range(42, 48))
RIGHT_BROW_POINTS = list(range(17,22))

LEFT_FACE = list(range(0, 9)) + list(range(18, 22))
RIGHT_FACE = list(range(9, 17)) + list(range(23, 27))


JAW_END = 17
FACE_START = 0
FACE_END = 68

OVERLAY_POINTS = [
    LEFT_FACE,
    RIGHT_FACE,
    LIP_POINTS,
    JAW_POINTS,
    MOUTH_POINTS
]

class TooManyFace(Exception):
    pass
class NoFaces(Exception):
    pass

def matrix_marks(image):
    pointer = []
    txt = image + ".txt"
    image = cv2. image = cv2.imread(image,cv2.IMREAD_COLOR)

    fp = open(txt,'w+')
    rects = detector(image,1)
    matrix_list = np.matrix([[p.x,p.y] for p in (predictor(image, rects[0]).parts())])
    # print(matrix_list)
    for p in matrix_list.tolist():
        fp.write(str(p[0])+' '+str(p[1]))
        fp.write('\n')
        # print(p[0],p[1])
    return matrix_list

def face_points(image):
    points  = []
    # matrix_list = matrix_marks(image)
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
        return matrix_list,points
    # return matrix_list, point_list, err


# def landmarks_by_face__(image):
#     url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
#     params = {
#         'api_key': 'LdQT9TzbQBYttnQ6wGeblcW1UT0UhWDx',
#         'api_secret': 'NBRWDCTKnraBu7kygsoAMv5seFZSe3e7',
#         'return_landmark': 1
#     }
#     file = {'image_file': open(image, 'rb')}
#
#     r = requests.post(url=url, files=file, data=params)
#
#     if r.status_code == requests.codes.ok:
#         return r.content.decode('utf-8')
#     else:
#         return r.conten


def matrix_rectangle(left, top, width, height):
    pointer = [
        (left, top),
        (left + width / 2, top),
        (left + width - 1, top),
        (left + width - 1, top + height / 2),
        (left, top + height / 2),
        (left, top + height - 1),
        (left + width / 2, top + height - 1),
        (left + width - 1, top + height - 1)
    ]

    return pointer