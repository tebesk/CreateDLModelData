# -*- coding: utf-8 -*-
import tensorflow as tf
import cv2
import numpy as np
import os
import math
import time


def Synthesis(Ans_Path, Raw_Path, Save_Path):
    if os.path.isdir(Save_Path) == False:
        os.mkdir(Save_Path)

    # get directory list
    Large_dirs = getdirs(Ans_Path) ## ex. 12A32
    for L_dir in Large_dirs:
        st = time.time()
        if os.path.isdir(Save_Path+"/"+L_dir) == False:
            os.mkdir(Save_Path+"/"+L_dir)

        Middle_dirs = getdirs(Ans_Path+"/"+L_dir)  ## ex. 160824167101(.BMP)
        for M_dir in Middle_dirs:

            ### Read answer image
            Ansfiles = os.listdir(Ans_Path + "/" + L_dir + "/" + M_dir)

            for file in Ansfiles:
                path, ext = os.path.splitext(file)  # check kakucho-shi
                if ext == ".bmp":
                    # save ans files
                    ans_img = cv2.imread(Ans_Path + "/" + L_dir + "/" + M_dir +"/"+ file, 1)  # 第二引数：カラータイプ　-1: RGBA, 0: グレースケール, 1: RGB
                    ans_tmp_dir = Save_Path + "/" + L_dir + "/Ans/"
                    if os.path.isdir(ans_tmp_dir) == False:
                        os.mkdir(ans_tmp_dir)

                    cv2.imwrite(ans_tmp_dir + M_dir + "_" + file, ans_img)

                    # save raw files
                    raw_img = cv2.imread(Raw_Path + "/" + L_dir + "/" + M_dir +"/rt/"+ file, 1)
                    raw_tmp_dir = Save_Path + "/" + L_dir + "/Raw/"
                    if os.path.isdir(raw_tmp_dir) == False:
                        os.mkdir(raw_tmp_dir)
                    cv2.imwrite(raw_tmp_dir + M_dir + "_"+ file, raw_img)
        print L_dir+" is finish. elapsed time:" + (time.time() - st)


##get only directory list(http://lightson.dip.jp/blog/seko/1876)
def getdirs(path):
    dirs = []
    for item in os.listdir(path):
        if os.path.isdir(os.path.join(path, item)):
            dirs.append(item)
    return dirs

'''
def CopyAndSaveImgFiles(read_path, save_path, right_ext):
    for item in os.listdir(path):
        if os.path.isdir(os.path.join(path, item)):
            dirs.append(item)
'''

if __name__ == '__main__':

    st = time.time()

    Synthesis("/home/ys/Share/01_AndeuxWorks/ver20170413",
              "/home/ys/Share/11_IMG2BMP",
              "/home/ys/Share/7_DL_model_set/ver20170413")

    print "fin to create all image: elapsed time %f [sec]" % (time.time() - st)
