from PyQt5.QtGui import QImage, QPixmap
import numpy as np
import cv2
import copy
# make the block bgr image.The size of image is as same as img
def mk_empty_img(img):
    width,height,channel = img.shape
    img_out = np.zeros((width,height,channel))
    return img_out

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

if __name__ == "__main__":
    import cv2
    import os
