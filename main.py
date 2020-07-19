from PyQt5 import QtWidgets
import GUI_template as GUI
import GUI_subwindow as subwindow
from Class.image import *

if __name__ == "__main__":
    # global variable
    ###########################################

    # create ui object
    ui = GUI.Ui_Dialog()
    sub_ui = subwindow.Ui_Dialog()
    img1 = Image(cv2.imread("im0/out_0.jpg"),0)
    img2 = Image(cv2.imread("im0/out_1.jpg"),1)
    img_target = Image(mk_empty_img(img1.img),-1)
    img_dir_path = "im0/"
    img_name_arr = []
    img_kp_arr = []
    BF_match_arr = []
    img_arr = []
    img_num = 0
    img_rect = [0,0,0,0]
    draing_flag = False

    # function
    ###########################################

    # display image
    def dis_img():
        ui.img_label1.setPixmap( QPixmap.fromImage(img1.qImg))
        ui.img_label2.setPixmap( QPixmap.fromImage(img2.qImg))

    # determine whether the match meets the distance limit
    def is_meet_dis(kp1_pt,kp2_pt):
        if not ui.Limit_Button.isChecked():
            return True
        else:
            limit_dis = ui.Distance_Limit.value()
            dis = np.linalg.norm(kp1_pt - kp2_pt)
            if dis > limit_dis:
                return False
            else:
                return True

    # determine whether the match meets the ration test
    def is_meet_ration(m1,m2):
        ratio = ui.Ratio_Test_Display.value()
        if m1.distance < m2.distance * ratio:
            return True
        else:
            return False

    # direction -1 for left button, 1 for right button, 0 for check current image
    def change_image(direction):
        img1_idx = (img1.idx + direction) % img_num
        img2_idx = (img2.idx + direction) % img_num
        img1.set_img(img_arr , img1_idx , img_kp_arr)
        img2.set_img(img_arr, img2_idx , img_kp_arr)
        if ui.SIFT_Button.isChecked():
            draw_SIFT_kp()
        if ui.BF_Flow_Button.isChecked():
            draw_BF_match_flow()
        if ui.BF_Line_Button.isChecked():
            draw_BF_match_line()
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
    
    # draw the flow of BF match
    def draw_BF_match_flow():
        img1_out = copy.deepcopy(img1.img)
        img2_out = copy.deepcopy(img2.img)
        matches = BF_match_arr[img1.idx]
        for m in matches:
            kp1 = img1.kps[m[0].queryIdx]
            kp2 = img2.kps[m[0].trainIdx]
            kp1_pt = np.array( kp1.pt )
            kp2_pt = np.array( kp2.pt )
            if not is_meet_dis(kp1_pt,kp2_pt):
                continue
            if not is_meet_ration(m[0],m[1]):
                continue
            cv2.arrowedLine(img1_out,(int(kp1_pt[0]),int(kp1_pt[1])),(int(kp2_pt[0]),int(kp2_pt[1])),(0,0,255),1)
            cv2.arrowedLine(img2_out,(int(kp1_pt[0]),int(kp1_pt[1])),(int(kp2_pt[0]),int(kp2_pt[1])),(0,0,255),1)
        img1.draw_img(img1_out)
        img2.draw_img(img2_out)
    
    # draw the line of match on combined image
    def draw_match_line(matches,img_out,wA,kps1,kps2):
        for m in matches:
            kp1 = kps1[m[0].queryIdx]
            kp2 = kps2[m[0].trainIdx]
            kp1_pt = np.array( kp1.pt )
            kp2_pt = np.array( kp2.pt )
            if not is_meet_dis(kp1_pt,kp2_pt):
                continue
            if not is_meet_ration(m[0],m[1]):
                continue
            cv2.line(img_out, ( int(kp1_pt[0]) , int(kp1_pt[1]) ), ( int(kp2_pt[0] + wA) , int(kp2_pt[1]) ), (0,0,255), 1)

    # draw the line of BF match on two images
    def draw_BF_match_line():
        # prepare combined image
        img_out = combine_img(img1.img,img2.img)
        matches = BF_match_arr[img1.idx]
        hA, wA = img1.img.shape[:2]
        # draw line
        draw_match_line(matches,img_out,wA,img1.kps,img2.kps)
        # split combined image to two image
        img1_out,img2_out = split_combined_img(img_out,img1.img,img2.img)
        img1.draw_img( np.copy(img1_out) )
        img2.draw_img( np.copy(img2_out) )

    # trigger this function when limit distance is changed
    def change_limit_distance():
        if ui.Limit_Button.isChecked():
            change_image(0)
    
    # trigger this function when ration test is changed
    def change_ratio_test():
        # display changed number
        value = float(ui.Ratio_Test.value())
        max_value = float(ui.Ratio_Test.maximum())
        ui.Ratio_Test_Display.display(value / max_value)
        change_image(0)

    # finding the SIFT key points of target image
    def SIFT_target_img():
        sift = cv2.xfeatures2d.SIFT_create()
        kp = sift.detect(img_target.img, None)
        img_target.kps = kp

    # set the bounded image(rad rectangle) in img1 to img3
    def set_target_img():
        if not sum(img_rect):
            print("No bounded area!")
            return
        im_h,im_w,c = img1.img.shape
        lb_w = ui.img_label1.width()
        lb_h = ui.img_label1.height()
        w_ratio = im_w/lb_w
        h_ratio = im_h/lb_h
        width = int(abs(img_rect[0] - img_rect[2]) * w_ratio)
        height = int(abs(img_rect[1] - img_rect[3]) * h_ratio)
        x = int(min(img_rect[0],img_rect[2]) * w_ratio)
        y = int(min(img_rect[1],img_rect[3]) * h_ratio)
        temp_img = np.zeros((height,width,3),dtype="uint8")
        temp_img = img1.img[y:y + height,x:x + width]
        img_target.draw_img(np.copy(temp_img))
        SIFT_target_img()
        ui.target_label.setPixmap(QPixmap.fromImage(img_target.qImg))
        ui.target_label.setFixedSize(width*2,height*2)

    # BF match target image with img1 and img2
    def BF_target_match():
        sift = cv2.xfeatures2d.SIFT_create()
        ori_img1 = img_arr[img1.idx]
        ori_img2 = img_arr[img2.idx]
        des_t = sift.compute(img_target.img,img_target.kps)
        des_1 = sift.compute(ori_img1,img1.kps)
        des_2 = sift.compute(ori_img2,img2.kps)
        matcher = cv2.DescriptorMatcher_create("BruteForce")
        matches = matcher.knnMatch(des_t[1],des_1[1],2)
        img_out = combine_img(img_target.img,ori_img1)
        hA,wA = img_target.img.shape[:2]
        # draw the line on target image and img1
        draw_match_line(matches,img_out,wA,img_target.kps,img1.kps)
        # set image to subwindow's label
        qImg = convImg(np.copy(img_out))
        sub_ui.Image_Label.setPixmap(QPixmap.fromImage(qImg))
        # show subwindow
        Dialog2.show()
    
    # mouse trigger function
    ###########################################

    # draw rectagle on image1
    def img_label1_mousePressEvent(self,event):
        global draing_flag
        draing_flag = True
        img_rect[0] = event.x()
        img_rect[1] = event.y()
    
    def img_lable1_mouseReleaseEvent(self,event):
        global draing_flag
        draing_flag = False
    
    def img_label1_mouseMoveEvent(self,event):
        if draing_flag:
            im_h,im_w,c = img1.img.shape
            lb_w = ui.img_label1.width()
            lb_h = ui.img_label1.height()
            img_rect[2] = event.x()
            img_rect[3] = event.y()
            img1.draw_rect(img_rect,im_w,im_h,lb_w,lb_h)
            dis_img()
    
    def bind_img_lable1_func(obj):
        funcType = type(obj.mousePressEvent)
        obj.mousePressEvent = funcType(img_label1_mousePressEvent,obj)
        funcType = type(obj.mouseReleaseEvent)
        obj.mouseReleaseEvent = funcType(img_lable1_mouseReleaseEvent,obj)
        funcType = type(obj.mouseMoveEvent)
        obj.mouseMoveEvent = funcType(img_label1_mouseMoveEvent, obj)

    # initial function
    ###########################################
    
    # connect button function    
    def button_fun():
        ui.Right_Button.clicked.connect(lambda: change_image(1))
        ui.Left_Button.clicked.connect(lambda: change_image(-1))
        ui.SIFT_Button.clicked.connect(lambda: change_image(0))
        ui.BF_Flow_Button.clicked.connect(lambda: change_image(0))
        ui.BF_Line_Button.clicked.connect(lambda: change_image(0))
        ui.Limit_Button.clicked.connect(lambda: change_image(0))
        ui.Distance_Limit.valueChanged.connect(change_limit_distance)
        ui.Ratio_Test.valueChanged.connect(change_ratio_test)
        ui.Target_Button.clicked.connect(set_target_img)
        ui.Target_Find_Button.clicked.connect(BF_target_match)

    # overwrite mouse trigger function of label
    def Qlabel_fun():
        bind_img_lable1_func(ui.img_label1)
        
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
            if i >= image_num():
                break
        return i
    
    # check whether the data files exist
    def check_data_file():
        dir_path = "data/"
        if not os.path.isfile(dir_path + "SIFT_kp.txt"):
            import create_data.SIFT_kp
        if not os.path.isfile(dir_path + "SIFT_BF_match.txt"):
            import create_data.SIFT_BF_match
    
    # load key points data
    def load_SIFT_kp():
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
        f.close()
    
    # load BF match data
    def load_BF_match():
        data_path = "data/SIFT_BF_match.txt"
        f = open(data_path,"rb")
        data = cPickle.loads(f.read())
        for match_arr in data:
            temp_arr = []
            for m in match_arr:
                m1 = cv2.DMatch(m[0][0],m[0][1],m[0][2])
                m2 = cv2.DMatch(m[1][0],m[1][1],m[1][2])
                temp_arr.append((m1,m2))
            BF_match_arr.append(temp_arr)
        f.close()
    
    # load data
    def load_data(img_kp_arr):
        check_data_file()
        load_SIFT_kp()
        load_BF_match()
    
    # init image entity
    def init():
        img1.set_img(img_arr,0,img_kp_arr)
        img2.set_img(img_arr,1,img_kp_arr)
    
    # main
    ###########################################
    # create main window
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui.setupUi(Dialog)
    # create subwindow
    Dialog2 = QtWidgets.QDialog()
    sub_ui.setupUi(Dialog2)
    # init
    img_num = load_img(img_name_arr)
    load_data(img_kp_arr)
    init()
    button_fun()
    Qlabel_fun()
    Dialog.show()
    sys.exit(app.exec_())
