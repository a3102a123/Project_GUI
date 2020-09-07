from PyQt5.QtGui import QImage, QPixmap
import numpy as np
import cv2
import copy
import _pickle as cPickle
import sys
import os
import time

from enum import Enum,IntEnum
from PyQt5.QtWidgets import QWidget, QApplication, QLabel
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QGuiApplication
from munkres import Munkres, print_matrix

# return the number of image load from folder
def image_num():
    dir_path = "im0/"
    dir = os.listdir( dir_path)
    img_num = len(dir)
    return img_num

# show the opencv image
def show_im(name,im):
    cv2.imshow(name,im)
    # press any key to close the window
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# make the block bgr image.The size of image is as same as img
def mk_empty_img(img):
    if len(img.shape) > 2:
        height,width,channel = img.shape
        img_out = np.zeros((height,width,channel), dtype="uint8")
    else:
        height,width = img.shape
        img_out = np.zeros((height,width), dtype="uint8")
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

# apply the mask on rgb image
def apply_mask(img,mask):
    out_img = cv2.bitwise_and(img,img,mask = mask)
    return out_img
# extract the rectangle part of image from input image
def get_rect_img(img,rect):
    width = int(abs(rect[0] - rect[2]))
    height = int(abs(rect[1] - rect[3]))
    x = int(min(rect[0],rect[2]))
    y = int(min(rect[1],rect[3]))
    out_img = np.zeros((height,width,3),dtype="uint8")
    out_img = img[y:y + height,x:x + width]
    return out_img

# the dis is the distance out of rectangle
# which is used to select potential key points for match
# if dis = 0,0 return all key points' descripter
def compute_SIFT_des(img,kps,rect=[0,0,0,0],dis=[0,0]):
    sift = cv2.xfeatures2d.SIFT_create()
    new_kp,des = sift.compute(img,kps)
    # RootSIFT descriptor
    eps = 1e-7
    des /= (des.sum(axis=1, keepdims=True) + eps)
    des = np.sqrt(des)
    if dis == [0,0] :
        return des
    new_des = []
    count = 3
    max_x = max(rect[0],rect[2]) + count*abs(dis[0])
    min_x = min(rect[0],rect[2]) - count*abs(dis[0])
    max_y = max(rect[1],rect[3]) + count*abs(dis[1])
    min_y = min(rect[1],rect[3]) - count*abs(dis[1])
    
    print("expend1:", min(rect[0],rect[2]),min(rect[1],rect[3]),min(rect[0],rect[2]),max(rect[1],rect[3]))
    print("expend2:", min_x,min_y,max_x,max_y)
    for i in range(len(kps) - 1 , -1 , -1):
        kp = kps[i]
        x,y = kp.pt
        if x < min_x or x > max_x:
            new_kp.pop(i)
            continue
        if y < min_y or y > max_y:
            new_kp.pop(i)
            continue
        new_des.append(des[i])
    # to show the remain key points on image
    img_out = copy.deepcopy(img)
    cv2.drawKeypoints(img,new_kp,img_out)
    cv2.rectangle(img_out,(int(min_x),int(min_y)),(int(max_x),int(max_y)),(0,255,0),thickness=1)
    cv2.imshow("limited_key_points",img_out)
    # press any key to close the window
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    new_des.reverse()
    return new_kp,np.array(new_des)

# convert opencv image to Qimage
def convImg(img):
    height, width, channel = img.shape
    bytesPerline = 3 * width
    qImg = QImage(img.data, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
    return qImg

# the class to maintain QLabel image's infomation
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

    # draw the rectangle on image
    # is_img_coor determine whether the input rectangle is in image's coordinate
    # default assume input rect is in label's coordinate
    def draw_rect(self,rect,im_w,im_h,lb_w,lb_h,color,is_img_coor = False):
        img = copy.deepcopy(self.img)
        if not is_img_coor:
            w_ratio = im_w/lb_w
            h_ratio = im_h/lb_h
        else:
            w_ratio = 1
            h_ratio = 1
        p1 = (int(rect[0] * w_ratio),int(rect[1] * h_ratio))
        p2 = (int(rect[2] * w_ratio),int(rect[3] * h_ratio))
        cv2.rectangle(img,p1,p2,color)
        self.qImg = convImg(img)

    def show_img(self):
        cv2.imshow("temp",self.img)
        # press any key to close the window
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# the class for target image to additionally store rectangle info
class Target_Image(Image):
    def __init__(self,img,i):
        self.rect = [0,0,0,0]
        self.pre_rect = [0,0,0,0]
        self.motion = [30,30]

# The enum of result file type
class File_Type(IntEnum):
    BUS = 1
    CAR = 2
    CAR2 = 3
    AUTOBIKE = 4
    AUTOBIKE2 = 5

# 需手動更換GUI_template.py中的QLabel和import image.py
class MyLabel(QLabel):
    # dummy event function. implement in main.py
    def mousePressEvent(self,event):
        return
    
    def mouseReleaseEvent(self,event):
        return
    
    def mouseMoveEvent(self,event):
        return
    
    def mouseDoubleClickEvent(self,event):
        return

if __name__ == "__main__":
    import cv2
    import os
