# -*- coding: utf-8 -*-
import numpy as np
import os
import math
import time
import cv2, matplotlib
import numpy as np
import matplotlib.pyplot as plt

def Thresh(PATH, NEWPATH):
    st = time.time()

    if os.path.isdir(NEWPATH) == False:
        os.mkdir(NEWPATH)

    if (os.path.isdir(PATH)):
        files = os.listdir(PATH)

    for file in files:
        img = cv2.imread(PATH + "/" + file)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(img_gray, 30, 255, cv2.THRESH_TOZERO)
        cv2.imwrite(NEWPATH + "/" + file, thresh)


def Denoising(img):
    # 4近傍の定義
    # neiborhood4 = np.array([[0, 1, 0],[1, 1, 1],[0, 1, 0]],np.uint8)
    # 8近傍の定義
    neiborhood8 = np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]], np.uint8)

    # 近傍8のオープニング
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, neiborhood8)
    # 近傍8のクロージング
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, neiborhood8)
    return img

#: 2017.1.25 renew
def Denoising_GaussianBlur_Thresh(img, gauss_num, thresh_num):
    img_blur_small = cv2.GaussianBlur(img, (gauss_num, gauss_num), 0)
    ret, thresh = cv2.threshold(img_blur_small, thresh_num, 255, cv2.THRESH_TOZERO)
    return thresh


# 画像の左端を黒くする
def Leftwiper(img, num):
    orgHeight, orgWidth = img.shape[:2]
    for y in range(orgHeight):
        for x in range(num):
            img[y, x, 0] = 0
            img[y, x, 1] = 0
            img[y, x, 2] = 0
    return img



if __name__ == '__main__':
    img = cv2.imread("/home/ys/Share/7_DL_model_set/ver20170123/12A32/Raw/160824164038_0.bmp")
    img_blur_small = cv2.GaussianBlur(img, (15, 15), 0)
    ret, thresh = cv2.threshold(img_blur_small, 20, 255, cv2.THRESH_TOZERO)
    cv2.imwrite("/home/ys/Undeux/3.bmp", thresh)
    cv2.imwrite("/home/ys/Undeux/4.bmp",img_blur_small)



