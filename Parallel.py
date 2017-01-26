# -*- coding: utf-8 -*-
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
from multiprocessing import Process, Pipe
from multiprocessing import Pool

def fuga(idx, cpu_process, files, PATH): # 並列実行したい関数
    for file in files[idx::cpu_process]:
        print PATH + "/" + file




    #print p.map(fuga, files) # fugaに0,1,..のそれぞれを与えて並列演算

if __name__ == "__main__":

    PATH = "/home/ys/Share/01_AndeuxWorks/ver20170123"
    files = os.listdir(PATH)
    print len(files)

    cpu_process = 10
    process_list = []
    for idx in range(cpu_process):
        p = Process(target = fuga, args = (idx, cpu_process, files, PATH))
        process_list.append(p)

    #start process
    for p in process_list:
        p.start()

    # wait for process end
    for p in process_list:
        p.join()
