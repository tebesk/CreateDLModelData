# -*- coding: utf-8 -*-
import cv2
import numpy as np
import os
import math
import time
import Denoising as dn

def TrainingModelMaking(NEWPATH, PATH):
    if os.path.isdir(NEWPATH) == False:
        os.mkdir(NEWPATH)

    if (os.path.isdir(PATH)):
        files = os.listdir(PATH)

        for file in files:
            img = cv2.imread(PATH + "/" + file)

            # create half image
            Height, Width = img.shape[:2]
            img = cv2.resize(img, (Width / 2, Height / 2))

            # add denoising
            img = dn.Denoising(img)

            # left cut
            img = dn.Leftwiper(img, 40)

            # add threshold
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(img_gray, 25, 255, cv2.THRESH_TOZERO)
            cv2.imwrite(NEWPATH + "/" + file, thresh)
