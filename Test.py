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
import  CreateModelMain as cmm
if __name__ == '__main__':

    PATH = input("input read path")
    NEWPATH = input("input save path")
    mode = input("input data model ex. 15B32")
    st = time.time()

    cmm.CreateTrainingModel(NEWPATH, PATH, mode)

    print "fin to create all image: elapsed time %f [sec]" % (time.time() - st)