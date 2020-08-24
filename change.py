import cv2
import numpy as np
import os
import sys


index = 0
for l in range(1199):
    if(((l-3)%4)==0):
        continue
    img1 = cv2.imread('im0/out_' + str(l) + '.jpg')
    cv2.imwrite('im0/out_' + str(index) + '.jpg', img1)
    index+=1
