from PyQt5 import QtWidgets
import GUI_template as GUI
from Class.image import *
import os
import sys
import _pickle as cPickle
if __name__ == "__main__":
    # global variable

    # create ui object
    ui = GUI.Ui_Dialog()
    img1 = Image(cv2.imread("im0/out_0.jpg"),0)
    img2 = Image(cv2.imread("im0/out_1.jpg"),1)
    img_dir_path = "im0/"
    img_name_arr = []
    img_kp_arr = []
    img_arr = []
    img_num = 0

    def dis_img():
        ui.img_label1.setPixmap( QPixmap.fromImage(img1.qImg))
        ui.img_label2.setPixmap( QPixmap.fromImage(img2.qImg))

    # direction -1 for left button, 1 for right button, 0 for check current image
    def change_image(direction):
        img1_idx = (img1.idx + direction) % img_num
        img2_idx = (img2.idx + direction) % img_num
        img1.set_img(img_arr , img1_idx , img_kp_arr)
        img2.set_img(img_arr, img2_idx , img_kp_arr)
        if ui.SIFT_Button.isChecked():
            draw_SIFT_kp()
        dis_img()
        text1 = img_name_arr[img1.idx]
        text2 = img_name_arr[img2.idx]
        ui.img_text1.setText(text1)
        ui.img_text2.setText(text2)

    # display SIFT key points on image
    def draw_SIFT_kp():
        img1_out = copy.deepcopy(img1.img)
        img2_out = copy.deepcopy(img2.img)
        cv2.drawKeypoints(img1.img,img1.kps,img1_out)
        cv2.drawKeypoints(img2.img,img2.kps,img2_out)
        img1.draw_img(img1_out)
        img2.draw_img(img2_out)
        
    def button_fun():
        ui.Right_Button.clicked.connect(lambda: change_image(1))
        ui.Left_Button.clicked.connect(lambda: change_image(-1))
        ui.SIFT_Button.clicked.connect(lambda: change_image(0))
    # load image
    def load_img(img_name_arr):
        img_name_arr[:] = os.listdir(img_dir_path)
        img_name_arr.sort(key = len)
        i = 0
        for filename in img_name_arr :
            img = cv2.imread(img_dir_path + filename)
            #store image 
            img_arr.append(img)
            i += 1
            #speed up for debug
            if i > 10:
                break
        return i
    # load key points data
    def load_data(img_kp_arr):
        data_path = "data/SIFT_kp.txt"
        f = open(data_path,"rb")
        data = cPickle.loads(f.read())
        for kp_arr in data:
            temp_arr = []
            for point in kp_arr:
                temp = cv2.KeyPoint(x=point[0][0],y=point[0][1],_size=point[1], _angle=point[2], 
                                _response=point[3], _octave=point[4], _class_id=point[5])
                temp_arr.append(temp)
            img_kp_arr.append(temp_arr)
    # init image entity
    def init():
        img1.set_img(img_arr,0,img_kp_arr)
        img2.set_img(img_arr,1,img_kp_arr)
    
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui.setupUi(Dialog)
    # init
    img_num = load_img(img_name_arr)
    load_data(img_kp_arr)
    init()
    button_fun()
    Dialog.show()
    sys.exit(app.exec_())