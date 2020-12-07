from PyQt5.QtGui import QImage, QPixmap
import numpy as np
import cv2
import copy
import _pickle as cPickle
import sys
import getopt
import os
import time
import math
import matplotlib.pyplot as plt

from enum import Enum,IntEnum
from PyQt5.QtWidgets import QWidget, QApplication, QLabel
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QGuiApplication, qRed, qGreen, qBlue
from munkres import Munkres, print_matrix
from filterpy.kalman import KalmanFilter
from filterpy.common import Q_discrete_white_noise
from skimage.measure import compare_ssim

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
def compute_SIFT_des(img,kps,rect=[0,0,0,0],dis=[0,0],is_show = True):
    sift = cv2.xfeatures2d.SIFT_create()
    new_kp,des = sift.compute(img,kps)
    # if the target image too small return nothing
    if(not isinstance(des,np.ndarray)):
        return
    # RootSIFT descriptor
    eps = 1e-7
    des /= (des.sum(axis=1, keepdims=True) + eps)
    des = np.sqrt(des)
    if dis == [0,0] :
        return des
    new_des = []
    count = 2
    max_x = max(rect[0],rect[2]) + count*abs(dis[0])
    min_x = min(rect[0],rect[2]) - count*abs(dis[0])
    max_y = max(rect[1],rect[3]) + count*abs(dis[1])
    min_y = min(rect[1],rect[3]) - count*abs(dis[1])
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
    cv2.rectangle(img_out,(int(min(rect[0],rect[2])),int(min(rect[1],rect[3]))),(int(max(rect[0],rect[2])),int(max(rect[1],rect[3]))),(0,0,255),thickness=1)
    cv2.rectangle(img_out,(int(min_x),int(min_y)),(int(max_x),int(max_y)),(0,255,0),thickness=1)
    if is_show:
        cv2.imshow("limited_key_points",img_out)
    # press any key to close the window
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    new_des.reverse()
    return new_kp,np.array(new_des)

# convert opencv image to Qimage
def convImg(img):
    height, width, channel = img.shape
    bytesPerline = 3 * width
    qImg = QImage(img.data, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
    return qImg

def print_bar():
    print("======================================")

def arrange_rect(rect):
    x1 = min(rect[0],rect[2])
    y1 = min(rect[1],rect[3])
    x2 = max(rect[0],rect[2])
    y2 = max(rect[1],rect[3])
    return [x1,y1,x2,y2]

def print_rect(img,rect,color):
    cv2.rectangle(img,(int(min(rect[0],rect[2])),int(min(rect[1],rect[3]))),(int(max(rect[0],rect[2])),int(max(rect[1],rect[3]))),color,thickness=1)

def calc_rect_area(rect):
    rect = arrange_rect(rect)
    x = rect[2] - rect[0]
    y = rect[3] - rect[1]
    return x*y

# check the rect center is out of the eliminate region
def check_in_elim_region(rect):
    x = (rect[2] + rect[0]) / 2
    y = (rect[3] + rect[1]) / 2
    if (( x - 2*y - 180 > 0) or (2 * x - 5 * y + 1500 < 0) ):
        return True
    return False

# the class to maintain QLabel image's infomation
class Image():
    
    def __init__(self,img,i):
        self.idx = i
        self.img = copy.deepcopy(img)
        self.drew_img = copy.deepcopy(img)
        self.kps = []
        self.qImg = convImg(img)
    
    def set_img(self,img_arr,i,kp_arr):
        self.idx = i
        self.img = copy.deepcopy(img_arr[i])
        self.drew_img = copy.deepcopy(img_arr[i])
        self.kps = kp_arr[i]
        self.qImg = convImg(self.img)
    
    # is_set flag to determine whether set img to object img
    def draw_img(self,img,is_set = False):
        if is_set:
            self.img = copy.deepcopy(img)
        self.drew_img = copy.deepcopy(img)
        self.qImg = convImg(img)

    def reset_drew_img(self):
        self.drew_img = copy.deepcopy(self.img)
        self.qImg = convImg(self.img)

    # draw the rectangle on image
    # is_img_coor determine whether the input rectangle is in image's coordinate
    # is_new flag determine whether the rectangle is drew on new image(default is drew on new image)
    def draw_rect(self,rect,im_w,im_h,lb_w,lb_h,color,is_img_coor = False,is_new = True):
        if is_new:
            img = copy.deepcopy(self.img)
        else :
            img = self.drew_img
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
    
    def show_drew_img(self):
        cv2.imshow("temp",self.drew_img)
        # press any key to close the window
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# the class for target image to additionally store rectangle info
class Target_Image(Image):
    def __init__(self,img,i):
        self.rect = [0,0,0,0]
        self.motion = [30,30]
        #previous trustable target image information
        self.pre_rect = [0,0,0,0]   #可靠
        self.pre_idx = i
        self.predict_pre_rect = [0,0,0,0]   #可能不可靠
        self.is_predict = False #means current target image ism't trustable
        # kalman filter
        self.kl = cv2.KalmanFilter(4,2)
        self.kl_init_f = False
        # using for GMM to eliminate spot noise
        self.erode_num = 0
        self.dilate_num = 0
        # using for determine object size & motion calculation
        self.mul = 0
        # the flag to determine whether the target image comes from yolo
        self.is_yolo = False

    def set_rect(self,new_rect):
        self.rect = arrange_rect(new_rect)

    def set_pre_rect(self,new_rect):
        self.pre_rect = arrange_rect(new_rect)
    
    def set_predict_pre_rect(self,new_rect):
        self.predict_pre_rect = arrange_rect(new_rect)
    # rect attribute need clear by additionally assign [0,0,0,0]
    def clear(self):
        self.motion = [30,30]
        self.pre_rect = [0,0,0,0]
        self.pre_idx = -1
        self.is_predict = False
        self.predict_pre_rect = [0,0,0,0]
        self.kl_init_f = False

    def check_range(self,time):
        target_rect = copy.deepcopy(self.rect)
        if(self.motion[0] >= 0 ):
            target_rect[2] += (self.motion[0] * time)
        else:
            target_rect[0] += (self.motion[0] * time)
        if(self.motion[1] >= 0 ):
            target_rect[3] += (self.motion[1] * time)
        else:
            target_rect[1] += (self.motion[1] * time)
        return target_rect
    # initial the kalman filter
    def kl_init(self,new_motion):
        self.kl = cv2.KalmanFilter(4,2)
        self.kl.measurementMatrix = np.array([[1,0,0,0],[0,1,0,0]],np.float32)
        self.kl.transitionMatrix = np.array([[1,0,1,0],[0,1,0,1],[0,0,1,0],[0,0,0,1]], np.float32)
        self.kl.processNoiseCov = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]], np.float32) * 0.003
        self.kl.measurementNoiseCov = np.array([[1,0],[0,1]], np.float32) * 1
        x_center = ((self.pre_rect[2] - self.pre_rect[0]) / 2) + self.pre_rect[0]
        y_center = ((self.pre_rect[3] - self.pre_rect[1]) / 2) + self.pre_rect[1]
        # print("Initial kalman filter [",x_center,",",y_center,"] motion : ",new_motion)
        self.kl.statePre =  np.array([x_center,y_center,new_motion[0],new_motion[1]],np.float32)
        self.kl_init_f = True
    
    def get_legal_region(self):
        # target image in first detect
        if self.pre_idx == -1:
            x1 = self.rect[0] - abs(self.motion[0])
            x2 = self.rect[2] + abs(self.motion[0])
            y1 = self.rect[1] - abs(self.motion[1])
            y2 = self.rect[3] + abs(self.motion[1])
        else : 
            x1 = self.rect[0] + self.motion[0]
            x2 = self.rect[2] + self.motion[0]
            y1 = self.rect[1] + self.motion[1]
            y2 = self.rect[3] + self.motion[1]
            # if self.motion[0] > 0:
            #     x1 = self.rect[0]
            #     x2 = self.rect[2] + self.motion[0]
            # else :
            #     x1 = self.rect[0] + self.motion[0]
            #     x2 = self.rect[2]
            # if self.motion[1] > 0:
            #     y1 = self.rect[1]
            #     y2 = self.rect[3] + self.motion[1]
            # else:
            #     y1 = self.rect[1] + self.motion[1]
            #     y2 = self.rect[3]
        return [x1,y1,x2,y2]
    
    def check_in_legal_region(self,rect):
        x = (rect[0] + rect[2]) / 2
        y = (rect[1] + rect[3]) / 2
        region = self.get_legal_region()

        if(region[0] <= x <= region[2]) and (region[1] <= y <= region[3]):
            return True
        else:
            return False

    def check_overlap(self,rect,motion_mul):
        x = (rect[0] + rect[2]) / 2
        y = (rect[1] + rect[3]) / 2
        motion_x = abs(self.motion[0] * motion_mul)
        motion_y = abs(self.motion[1] * motion_mul)
        region = self.rect
        if((region[0] - motion_x) <= x <= (region[2] + motion_x)) and ((region[1] - motion_y) <= y <= (region[3] + motion_y)):
            return True
        else:
            return False

# The enum of result file type
class File_Type(IntEnum):
    File50 = 1
    CAR = 2
    CAR2 = 3
    AUTOBIKE = 4
    AUTOBIKE2 = 5

# The enum of motion type
class Motion_Type(IntEnum):
    ORIGIN = 1
    KALMAN = 2
    COMPLEX = 3

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
