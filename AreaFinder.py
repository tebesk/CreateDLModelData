# -*- coding: utf-8 -*-
import tensorflow as tf
import cv2
import numpy as np
import os
import math
import time

#: check the pixel is the organ or not
def OrgorNot(img, x, y):
    B = img[y, x, 0]
    G = img[y, x, 1]
    R = img[y, x, 2]
    if B > 10 and G > 10 and R > 10:
        return 1
    else:
        return 0

#: Organ check
def OrganCheker(img, img_area, Width, Height, x, y, border, B, G, R):
    # 上、下、右上、右下、右の画素が10以上であれば
    if border == 1:
        if R > 10:
            org = 0
            if x < (Width - 1):
                org += OrgorNot(img, x + 1, y)
                if y > 0:
                    org += OrgorNot(img, x, y - 1)
                    org += OrgorNot(img, x + 1, y - 1)
                if y < (Height - 1):
                    org += OrgorNot(img, x, y + 1)
                    org += OrgorNot(img, x + 1, y + 1)
            if org > 0:
                B = img_area[y, x, 0] = 255
                G = img_area[y, x, 1] = 255
                R = img_area[y, x, 2] = 255

    return img_area

#: deside where is the organ area in images
def AreaDesider(img, raw_img):
    Height, Width = img.shape[:2]
    img_area = np.zeros((Height, Width, 3), np.uint8)

    for y in range(Height):
        border = 0

        for x in range(Width):
            B = img[y, x, 0]
            G = img[y, x, 1]
            R = img[y, x, 2]
            # find red
            if B < 50 and G < 50 and R > 200:
                border = 1
            img_area = OrganCheker(raw_img, img_area, Width, Height, x, y, border, B, G, R)

    return img_area


""" AreaDesider for all files """
#: anslinepaht: line-one, BasePath: raw img, NewPath: for save path
def AllFile_AreaDesider(AnsLinePath, BasePath, NewPath):
    if os.path.isdir(NewPath) == False:
        os.mkdir(NewPath)

    if (os.path.isdir(AnsLinePath)):
        files = os.listdir(AnsLinePath)

        for file in files:
            img = cv2.imread(AnsLinePath + "/" + file)
            raw_img = cv2.imread(BasePath + "/" + file)
            ans_img = AreaDesider(img, raw_img)
            cv2.imwrite(NewPath + "/" + file, ans_img)


""" Catherter finder """
def BlueChecker(img, black_img, x, y, border):
    B = img[y, x, 0]
    G = img[y, x, 1]
    R = img[y, x, 2]

    if B > 200 and G < 50 and R < 50:
        border = 1
        black_img[y, x, 0] = 255
        black_img[y, x, 1] = 0
        black_img[y, x, 2] = 0

    if border == 1:
        black_img[y, x, 0] = 255
        black_img[y, x, 1] = 0
        black_img[y, x, 2] = 0
    return  black_img, border


def CatheterFinderFromTop(img):
    Height, Width = img.shape[:2]
    black_img = np.zeros((Height, Width, 3), np.uint8)
    for x in range(Width):
        border = 0
        for y in range(Height):
            black_img, border = BlueChecker(img, black_img, x, y, border)

    return black_img

def CatheterFinderFromBelow(img):
    Height, Width = img.shape[:2]
    black_img = np.zeros((Height, Width, 3), np.uint8)

    for x in range(Width):
        border = 0
        for y in reversed(range(Height)):
            black_img, border = BlueChecker(img, black_img, x, y, border)

    return  black_img

def CatheterFinderFromRight(img):
    Height, Width = img.shape[:2]
    black_img = np.zeros((Height, Width, 3), np.uint8)

    for y in reversed(range(Height)):
        border = 0
        for x in reversed(range(Width)):
            black_img, border = BlueChecker(img, black_img, x, y, border)

    return black_img


def CatheterFinder(img):
    Height, Width = img.shape[:2]
    black_img = np.zeros((Height, Width, 3), np.uint8)
    for y in range(Height):
        border = 0
        for x in range(Width):
            black_img, border = BlueChecker(img, black_img, x, y, border)

    return black_img


    '''
    for y in range(height):
        OnOff = 0
        blue_x = 0

        for x in range(width):
            B = img[y, x, 0]
            G = img[y, x, 1]
            R = img[y, x, 2]

            if x == width-1:
                continue

            if B > 200 and G < 50 and R < 50:
                # when mode is Off mode
                if OnOff == 0:
                    OnOff =1
                    blue_x = x
                    black_img[y, x, 0] = 255
                    black_img[y, x, 1] = 0
                    black_img[y, x, 2] = 0
                    continue

                # when mode is On mode
                elif OnOff ==1:
                    dif = x- blue_x
                    if dif > 1:
                        for num in range(blue_x, x):
                            # input ans in black image
                            black_img[y, num, 0] = 255
                            black_img[y, num, 1] = 0
                            black_img[y, num, 2] = 0
                        OnOff = 0

                    if dif == 1:
                        blue_x = x
                        black_img[y, x, 0] = 255
                        black_img[y, x, 1] = 0
                        black_img[y, x, 2] = 0


                        nextB = img[y, x+1, 0]
                        nextG = img[y, x+1, 1]
                        nextR = img[y, x+1, 2]
                        if nextB < 200 and nextG > 200 and nextR > 200:
                            OnOff =0
    '''


def FourCatheCheck_Synthesis(img1, img2, img3, img4):
    Height, Width = img1.shape[:2]
    black_img = np.zeros((Height, Width, 3), np.uint8)
    for x in range(Width):
        for y in range(Height):
            img1B= img1[y, x, 0]
            img2B= img2[y, x, 0]
            img3B= img3[y, x, 0]
            img4B= img4[y, x, 0]

            if img1B > 200 and img2B > 200 and img3B > 200 and img4B > 200:
                black_img[y, x, 0] = 255
                black_img[y, x, 1] = 0
                black_img[y, x, 2] = 0
    return black_img


""" After FourCatheCheck Sythesis"""
def WallSide_CatheCheck_Blow(img):
    Height, Width = img.shape[:2]
    new_img = img
    for x in range(Width):

        blue_y = 0
        border = 0
        renzoku = 0
        for y in range(Height):
            B = img[y, x, 0]
            G = img[y, x, 1]
            R = img[y, x, 2]

            if B > 200 and G < 50 and R < 50: # if the point is blue...
                if border ==0: # for the first case
                    border = 1
                    blue_y = y

                if border >0:
                    dif = y - blue_y
                    if dif == 1:
                        blue_y = y
                        border= border +1
                    if dif > 1:
                        blue_y = y
                        border = 1

        if border < 10 and blue_y > Height*0.9:#連続4回以下は既存のカテではないと判断(is collect?)
            for i in range(blue_y, Height):
                new_img[i, x, 0] = 255
                new_img[i, x, 1] = 0
                new_img[i, x, 2] = 0

    return new_img

def WallSide_CatheCheck_FromBelow(img):
    Height, Width = img.shape[:2]
    new_img = img
    for x in range(Width):
        blue_y = 0
        border = 0
        for y in reversed(range(Height)):
            B = img[y, x, 0]
            G = img[y, x, 1]
            R = img[y, x, 2]

            if B > 200 and G < 50 and R < 50: # if the point is blue...
                if border ==0: # for the first case
                    border = 1
                    blue_y = y

                if border >0:
                    dif = blue_y - y
                    if dif == 1:
                        blue_y = y
                        border= border +1
                    if dif > 1:
                        blue_y = y
                        border = 1

        if border > 0 and border < 5 and blue_y < Height*0.1:#連続4回以下は既存のカテではないと判断(is collect?)
            for i in range(0, blue_y+1):
                new_img[i, x, 0] = 255
                new_img[i, x, 1] = 0
                new_img[i, x, 2] = 0

    return new_img


""" Catheter Finder for all files """

def AllFile_CatheterFinder(AnsLinePath, NewPath):
    if os.path.isdir(NewPath) == False:
        os.mkdir(NewPath)

    if (os.path.isdir(AnsLinePath)):
        files = os.listdir(AnsLinePath)

        for file in files:
            img = cv2.imread(AnsLinePath + "/" + file)
            height, width = img.shape[:2]

            # 上下反転
            xAxis = cv2.flip(img, 0)
            img_vv = cv2.vconcat([xAxis, img])
            img_vvv = cv2.vconcat([img_vv, xAxis])

            #４つの画像を合わせて確認
            img1 = CatheterFinder(img_vvv)
            img2 = CatheterFinderFromTop(img_vvv)
            img3 = CatheterFinderFromBelow(img_vvv)
            img4 = CatheterFinderFromRight(img_vvv)
            img5 = FourCatheCheck_Synthesis(img1, img2, img3, img4)

            #画像を切り抜き
            clp = img5[height:height * 2, 0:width]

            cv2.imwrite(NewPath + "/" + file, clp)


""" Catheter & Organ area synthesis"""
def OrganCatheSynthesis(red_img, blue_img):
    height = red_img.shape[0]
    width = red_img.shape[1]
    black_img = np.zeros((height, width, 3), np.uint8)

    for y in range(height):
        for x in range(width):
            redB = red_img[y, x, 0]
            redG = red_img[y, x, 1]
            redR = red_img[y, x, 2]

            blueB = blue_img[y, x, 0]
            blueG = blue_img[y, x, 1]
            blueR = blue_img[y, x, 2]

            if redB > 200 and redG > 200 and redR > 200:
                black_img[y, x, 0] = 0
                black_img[y, x, 1] = 0
                black_img[y, x, 2] = 255

            if blueB > 200 and blueG < 50 and blueR < 50:
                black_img[y, x, 0] = 255
                black_img[y, x, 1] = 0
                black_img[y, x, 2] = 0

    return black_img


""" Catheter & Organ area synthesis for all files """
def AllFile_OrganCatheSynthesis(OrganAns_Path, CatheAns_Path, New_Path):

    if os.path.isdir(New_Path) == False:
        os.mkdir(New_Path)

    if (os.path.isdir(OrganAns_Path)):
        files = os.listdir(OrganAns_Path)

    for file in files:
        red_img = cv2.imread(OrganAns_Path + "/" + file)
        blue_img = cv2.imread(CatheAns_Path + "/" + file)

        img = OrganCatheSynthesis(red_img, blue_img)

        cv2.imwrite(New_Path + "/" + file, img)


#: For Debug
if __name__ == '__main__':
    AnsLinePath = "/home/ys/Share/7_DL_model_set/ver20170123/8A24/line_on"
    BluePath = "/home/ys/Share/7_DL_model_set/ver20170123/8A24/Blue"
    start = time.time()
    if (os.path.isdir(AnsLinePath)):
        files = os.listdir(AnsLinePath)
        # file = "/home/ys/Share/7_DL_model_set/ver20170123/8A24/line_on/160914150823_0.bmp"

        for file in files:
            print file

            img = cv2.imread(AnsLinePath+"/"+file)
            height, width = img.shape[:2]

            xAxis = cv2.flip(img, 0)
            img_vv = cv2.vconcat([xAxis, img])
            img_vvv = cv2.vconcat([img_vv, xAxis])

            img1 = CatheterFinder(img_vvv)
            img2 = CatheterFinderFromTop(img_vvv)
            img3 = CatheterFinderFromBelow(img_vvv)
            img4 = CatheterFinderFromRight(img_vvv)
            Synthesis = FourCatheCheck_Synthesis(img1, img2, img3, img4)
            clp = Synthesis[height:height * 2, 0:width]
            cv2.imwrite(BluePath + "/" + file, clp)
    elapsed_time = time.time() - start
    print ("elapsed_time:{0}".format(elapsed_time)) + "[sec]"
    '''
    cv2.imwrite("/home/ys/Undeux/1.bmp", img_vvv)
    cv2.imwrite("/home/ys/Undeux/2.bmp", Synthesis)a
    cv2.imwrite("/home/ys/Undeux/3.bmp", clp)
    '''



    '''test
    img = cv2.imread("/home/ys/Share/7_DL_model_set/ver20161118/8A32/Ans_half/160914150507_100.bmp")
    img1 = CatheterFinder(img)
    img2 = CatheterFinderUppder(img)
    img3 = CatheterFinderFromBelow(img)
    img4 = CatheterFinderFromRight(img)
    img5 = FourCatheCheck_Synthesis(img1, img2, img3, img4)
    img6 = WallSide_CatheCheck_Blow(img5)
    img7 = WallSide_CatheCheck_FromBelow(img6)
    path = "/home/ys/Undeux/right.bmp"
    cv2.imwrite("/home/ys/Undeux/1.bmp", img1)
    cv2.imwrite("/home/ys/Undeux/2.bmp", img2)
    cv2.imwrite("/home/ys/Undeux/3.bmp", img3)
    cv2.imwrite("/home/ys/Undeux/4.bmp", img4)
    cv2.imwrite("/home/ys/Undeux/5.bmp", img5)
    cv2.imwrite("/home/ys/Undeux/6.bmp", img6)
    cv2.imwrite("/home/ys/Undeux/7.bmp", img7)
    '''
    #cv2.imwrite