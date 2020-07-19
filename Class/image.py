from PyQt5.QtGui import QImage, QPixmap
import numpy as np
import cv2
import copy
import _pickle as cPickle
import sys
import os

from PyQt5.QtWidgets import QWidget, QApplication, QLabel
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QGuiApplication

# return the number of image load from folder
def image_num():
    return 10

# make the block bgr image.The size of image is as same as img
def mk_empty_img(img):
    height,width,channel = img.shape
    img_out = np.zeros((height,width,channel))
    return img_out

# return the horizontally combined image of img1 & img2
def combine_img(img1,img2):
    (hA, wA) = img1.shape[:2]
    (hB, wB) = img2.shape[:2]
    img_out = np.zeros((max(hA, hB), wA + wB, 3), dtype="uint8")
    img_out[0:hA, 0:wA] = img1
    img_out[0:hB, wA:] = img2
    return img_out

# split the combined image to two image with origin size
def split_combined_img(img_out,img1,img2):
    (hA, wA) = img1.shape[:2]
    (hB, wB) = img2.shape[:2]
    img1_out = img_out[0:hA, 0:wA]
    img2_out = img_out[0:hB, wA:]
    return img1_out,img2_out

# convert opencv image to Qimage
def convImg(img):
    height, width, channel = img.shape
    bytesPerline = 3 * width
    qImg = QImage(img.data, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
    return qImg

class Image():
    
    def __init__(self,img,i):
        self.idx = i
        self.img = copy.deepcopy(img)
        self.kps = []
        self.qImg = convImg(img)
    
    def set_img(self,img_arr,i,kp_arr):
        self.idx = i
        self.img = copy.deepcopy(img_arr[i])
        self.kps = kp_arr[i]
        self.qImg = convImg(self.img)
    
    def draw_img(self,img):
        self.img = copy.deepcopy(img)
        self.qImg = convImg(img)

    def draw_rect(self,rect,im_w,im_h,lb_w,lb_h):
        img = copy.deepcopy(self.img)
        w_ratio = im_w/lb_w
        h_ratio = im_h/lb_h
        p1 = (int(rect[0] * w_ratio),int(rect[1] * h_ratio))
        p2 = (int(rect[2] * w_ratio),int(rect[3] * h_ratio))
        cv2.rectangle(img,p1,p2,(0,0,255))
        self.qImg = convImg(img)

    def show_img(self):
        cv2.imshow("temp",self.img)
        # press any key to close the window
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# 需手動更換GUI_template.py中的QLabel和import image.py
class MyLabel(QLabel):
    # dummy event function. implement in main.py
    def mousePressEvent(self,event):
        return
    
    def mouseReleaseEvent(self,event):
        return
    
    def mouseMoveEvent(self,event):
        return

if __name__ == "__main__":
    import cv2
    import os
