# -*- coding: utf-8 -*-
import tensorflow as tf
import cv2
import numpy as np
import os
import math
import time


#find red point and create answer
def DrawAnsLine2halfImg(ans_img, raw_img):

    #img=cv2.imread(path+"/"+filename)

    height = ans_img.shape[0]
    width = ans_img.shape[1]
    black_img = np.zeros((height, width, 3), np.uint8)

    for y in range(height):
        for x in range(width):
            B = ans_img[y, x, 0]
            G = ans_img[y, x, 1]
            R = ans_img[y, x, 2]


            # find Red
            if B<50 and G<50 and R>200:
                halfx = int(math.ceil(x / 2))
                halfy = int(math.ceil(y / 2))

                # to avoid error
                if halfx >= width / 2: halfx = (width / 2) - 1
                if halfy >= height / 2: halfy = (height / 2) - 1

                #input Organ Ans in black image
                raw_img[halfy, halfx, 0]= 0
                raw_img[halfy, halfx, 1]= 0
                raw_img[halfy, halfx, 2]= 255

            # find Blue
            if B>200 and G<50 and R<50:
                halfx = int(math.ceil(x / 2))
                halfy = int(math.ceil(y / 2))

                # to avoid error
                if halfx >= width / 2: halfx = (width / 2) - 1
                if halfy >= height / 2: halfy = (height / 2) - 1

                #input cathe Ans in black image
                raw_img[halfy, halfx, 0]= 255
                raw_img[halfy, halfx, 1]= 0
                raw_img[halfy, halfx, 2]= 0

    return raw_img

#: """ to make half answer image
"""
AnsPath      : Default size image
halfRaw_Path : half size raw image
NEWPath      : Path for save image
"""
def AllFile_DrawAnsLine2halfImg(AnsPath, halfRaw_Path, NEWPATH):
    if os.path.isdir(NEWPATH) == False:
        os.mkdir(NEWPATH)

    if (os.path.isdir(AnsPath)):
        files = os.listdir(AnsPath)
        for file in files:

            raw_img = cv2.imread(halfRaw_Path + "/" + file)
            ans_img = cv2.imread(AnsPath + "/" + file)
            new_img = DrawAnsLine2halfImg(ans_img, raw_img)
            cv2.imwrite(NEWPATH + "/" + file, new_img)


#:回答のラインを引く
#引数（答えがあるフォルダ、
#　　　生データがあるフォルダ、
#　　　新たに答えを入れるフォルダ、
#　  ）
def DrawAnsLine(ans_path, raw_path, NEWPATH):
    if os.path.isdir(NEWPATH) == False:
        os.mkdir(NEWPATH)

    if (os.path.isdir(ans_path)):
        files = os.listdir(ans_path)
        for file in files:

            raw_img = cv2.imread(raw_path + "/" + file)
            ans_img = cv2.imread(ans_path + "/" + file)
            Height, Width = ans_img.shape[:2]

            for y in range(Height):
                for x in range(Width):
                    B = ans_img[y, x, 0]
                    G = ans_img[y, x, 1]
                    R = ans_img[y, x, 2]

                    if B < 50 and G < 50 and R > 150:
                        raw_img[y, x, 0] = 0
                        raw_img[y, x, 1] = 0
                        raw_img[y, x, 2] = 255

                    if B > 150 and G <50 and R <50:
                        raw_img[y, x, 0] = 255
                        raw_img[y, x, 1] = 0
                        raw_img[y, x, 2] = 0

            cv2.imwrite(NEWPATH + "/" + file, raw_img)



