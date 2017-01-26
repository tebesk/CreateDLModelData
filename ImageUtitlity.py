# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os

""" image to half """
def Img2half(ImgPath, NewPath):
    if os.path.isdir(NewPath) == False:
        os.mkdir(NewPath)

    if (os.path.isdir(ImgPath)):
        files = os.listdir(ImgPath)
        for file in files:
            img = cv2.imread(ImgPath + "/" + file)
            if not (img is None):
                width = img.shape[0]
                hight = img.shape[1]
                half_img = cv2.resize(img, (hight / 2, width / 2))
                name, ext = os.path.splitext(file)
                cv2.imwrite(NewPath + "/" + name + ".bmp", half_img)
            else:
                print 'Not exist'
    else:
        print "there is no image folder"

def AllFile_Img2half(ImgPath, NewPath):
    if os.path.isdir(NewPath) == False:
        os.mkdir(NewPath)

    if (os.path.isdir(ImgPath)):
        files = os.listdir(ImgPath)
        for file in files:
            img = cv2.imread(ImgPath + "/" + file)
            if not (img is None):
                width = img.shape[0]
                hight = img.shape[1]
                half_img = cv2.resize(img, (hight / 2, width / 2))
                name, ext = os.path.splitext(file)
                cv2.imwrite(NewPath + "/" + name + ".bmp", half_img)
            else:
                print 'Not exist'
    else:
        print "there is no image folder"
