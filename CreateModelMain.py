# -*- coding: utf-8 -*-
import tensorflow as tf
import cv2
import numpy as np
import os
import math
import time
import Denoising as dn
import TrnMaking as trn
import AnsMaking as am
import AreaFinder as AF
import ImageUtitlity as Util
from multiprocessing import Process
import sys



def CreateTrainingModel(NEWPATH, PATH, mode):

    if os.path.isdir(NEWPATH) == False:
        os.mkdir(NEWPATH)

    if (os.path.isdir(PATH)):
        files = os.listdir(PATH)

        for file in files:
            img = cv2.imread(PATH + "/" + file)

            # create half image
            Height, Width = img.shape[:2]
            half_img = cv2.resize(img, (Width / 2, Height / 2))

            # add denoising
            #img = dn.Denoising(img)
            #half_img = dn.Denoising(half_img)
            if mode =="12A24" or mode == "12A32" or mode == "12B24" or mode =="12Z32":
                img = dn.Denoising_GaussianBlur_Thresh(img, 15, 20)
                half_img = dn.Denoising_GaussianBlur_Thresh(half_img, 15, 20)
            elif mode =="15B24" or mode =="8Z32":
                img = dn.Denoising_GaussianBlur_Thresh(img, 15, 40)
                half_img = dn.Denoising_GaussianBlur_Thresh(half_img, 15, 40)
            elif mode =="15A32":
                img = dn.Denoising_GaussianBlur_Thresh(img, 15, 45)
                half_img = dn.Denoising_GaussianBlur_Thresh(half_img, 15, 40)
            else:
                img = dn.Denoising_GaussianBlur_Thresh(img, 15, 30)
                half_img = dn.Denoising_GaussianBlur_Thresh(half_img, 15, 30)

            # left cut
            img = dn.Leftwiper(img, 19)
            half_img = dn.Leftwiper(half_img, 9)

            # add threshold
            #img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            #half_img_gray = cv2.cvtColor(half_img, cv2.COLOR_BGR2GRAY)

            #ret, thresh = cv2.threshold(img_gray, 25, 255, cv2.THRESH_TOZERO)
            #half_ret, half_thresh = cv2.threshold(half_img_gray, 25, 255, cv2.THRESH_TOZERO)

            cv2.imwrite(NEWPATH + "/" + file, img)
            cv2.imwrite(NEWPATH + "_half/" + file, half_img)

"""
Function CreateAnsModel(
Raw(half)Path = raw (half)img path(denoised image file Path)
Ans(half)Path = ans (half)img path
AnsLinePath = put on ans line to raw img
OrganAnsPath = Cut out organ area
CatheAnsPath = Cut out Cathe area
finalPath = put on catheter and organ information in one file
"""
def CreateAnsModel(RawPath, half_RawPath, AnsPath, half_AnsPath, AnsLinePath, OrganAnsPath, CatheAnsPath, finalPath):

    #st = time.time()
    print "Create AnsPath : "+AnsPath

    """create half image"""
    #Util.Img2half(AnsPath, half_AnsPath)

    """ put on ans line to denoised raw image """
    am.DrawAnsLine(AnsPath, RawPath, AnsLinePath)
    am.DrawAnsLine(half_AnsPath, half_RawPath, AnsLinePath+"_half")

    """Create Organ Answer image """
    # ラインより右側の組織領域を抽出する。(AreaFinder.py)
    AF.AllFile_AreaDesider(AnsLinePath, RawPath, OrganAnsPath)
    Util.AllFile_Img2half(OrganAnsPath,OrganAnsPath+"_half")
    #AF.AllFile_AreaDesider(AnsLinePath+"_half", half_RawPath, OrganAnsPath+"_half")

    """pick up catheter information"""
    AF.AllFile_CatheterFinder(AnsLinePath, CatheAnsPath)
    Util.AllFile_Img2half(CatheAnsPath, CatheAnsPath +"_half")
    #AF.AllFile_CatheterFinder(AnsLinePath+"_half", CatheAnsPath+"_half")

    """ Synthesis """
    AF.AllFile_OrganCatheSynthesis(OrganAnsPath, CatheAnsPath, finalPath)
    Util.AllFile_Img2half(finalPath, finalPath + "_half")
    #AF.AllFile_OrganCatheSynthesis(OrganAnsPath+"_half",CatheAnsPath+"_half", finalPath+"_half")


def Parllel_ModelMaking(idx, cpu_process, files, PATH, choice): # 並列実行したい関数
    for file in files[idx::cpu_process]:

        # now there are only 2 files(Raw and Ans) under the dir of $file
        Raw_PATH = PATH + "/" + file + "/Raw"
        ANS_PATH = PATH + "/" + file + "/Ans"
        Denoised_PATH = PATH + "/" + file + "/trn"
        AnsLinePath = PATH + "/" + file + "/line_on"
        OrganAnsPath = PATH + "/" + file + "/Red"
        CatheAnsPath = PATH + "/" + file + "/Blue"
        finalPath = PATH + "/" + file + "/DL_Ans"

        if choice == 2 or choice == 3:
            # create half image
            Util.Img2half(Raw_PATH, Raw_PATH + "_half")
            print "fin to create raw image :elapsed time %f [sec]" % (time.time() - st)

            # create training data
            CreateTrainingModel(PATH + "/" + file + "/trn", Raw_PATH, file)
            print "fin to create training model :elapsed time %f [sec]" % (time.time() - st)

            half_AnsPath = PATH + "/" + file + "/Ans_half"
            am.AllFile_DrawAnsLine2halfImg(ANS_PATH, Raw_PATH + "_half", half_AnsPath)
            print "fin to create answer image: elapsed time %f [sec]" % (time.time() - st)

        if choice == 1 or choice == 3:
            # create half image
            Util.Img2half(Denoised_PATH, Denoised_PATH + "_half")
            print "fin to create raw image :elapsed time %f [sec]" % (time.time() - st)

            CreateAnsModel(Denoised_PATH, Denoised_PATH + "_half", ANS_PATH, ANS_PATH + "_half", AnsLinePath,
                           OrganAnsPath, CatheAnsPath, finalPath)
            print "fin to create all image: elapsed time %f [sec]" % (time.time() - st)


if __name__ == '__main__':
    #http://yura2.hateblo.jp/entry/2015/08/08/Python%E3%81%A7%E3%83%9E%E3%83%AB%E3%83%81%E3%83%97%E3%83%AD%E3%82%BB%E3%82%B9%E5%87%A6%E7%90%86

    choice = input("1: make only ans 2: make only training 3: make ans and training::")
    st = time.time()

    PATH = "/home/ys/Share/7_DL_model_set/ver20170413"
    if (os.path.isdir(PATH)):
        files = os.listdir(PATH)

        cpu_process = 12
        process_list = []
        for idx in range(cpu_process):
            p = Process(target=Parllel_ModelMaking, args=(idx, cpu_process, files, PATH, choice))
            process_list.append(p)

        # start process
        for p in process_list:
            p.start()

        # wait for process end
        for p in process_list:
            p.join()

    print "fin to create all image: elapsed time %f [sec]" % (time.time() - st)

'''
        for file in files:
            #now there are only 2 files(Raw and Ans) under the dir of $file
            Raw_PATH = PATH+ "/" + file + "/Raw"
            ANS_PATH = PATH+ "/" + file + "/Ans"
            Denoised_PATH = PATH + "/" + file + "/trn"
            AnsLinePath = PATH + "/" + file + "/line_on"
            OrganAnsPath = PATH + "/" + file + "/Red"
            CatheAnsPath = PATH + "/" + file + "/Blue"
            finalPath = PATH + "/" + file + "/DL_Ans"

            if choice ==2 or choice ==3:
                # create half image
                Util.Img2half(Raw_PATH, Raw_PATH + "_half")
                print "fin to create raw image :elapsed time %f [sec]" % (time.time() - st)

                # create training data
                CreateTrainingModel(PATH+ "/" + file + "/trn", Raw_PATH)
                print "fin to create training model :elapsed time %f [sec]" % (time.time() - st)

                half_AnsPath = PATH + "/" + file + "/Ans_half"
                am.AllFile_DrawAnsLine2halfImg(ANS_PATH, Raw_PATH +"_half", half_AnsPath)
                print "fin to create answer image: elapsed time %f [sec]" % (time.time() - st)

            if choice ==1 or choice ==3:

                # create half image
                Util.Img2half(Denoised_PATH, Denoised_PATH + "_half")
                print "fin to create raw image :elapsed time %f [sec]" % (time.time() - st)

                CreateAnsModel(Denoised_PATH, Denoised_PATH+"_half", ANS_PATH, ANS_PATH+"_half",AnsLinePath,OrganAnsPath,CatheAnsPath,finalPath)
                print "fin to create all image: elapsed time %f [sec]" % (time.time() - st)
'''
