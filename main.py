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
    img_target = Target_Image(mk_empty_img(img1.img),-1)
    img_dir_path = "im0/"
    img_name_arr = []
    img_kp_arr = []
    BF_match_arr = []
    img_arr = []
    img_num = 0
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
    def is_meet_ratio(m1,m2):
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
            if not is_meet_ratio(m[0],m[1]):
                continue
            cv2.arrowedLine(img1_out,(int(kp1_pt[0]),int(kp1_pt[1])),(int(kp2_pt[0]),int(kp2_pt[1])),(0,0,255),1)
            cv2.arrowedLine(img2_out,(int(kp1_pt[0]),int(kp1_pt[1])),(int(kp2_pt[0]),int(kp2_pt[1])),(0,0,255),1)
        img1.draw_img(img1_out)
        img2.draw_img(img2_out)
    
    # input a Dmatch and then return the pair of matched key points
    def get_match_kp(match,kps1,kps2):
        if isinstance(match,tuple) or isinstance(match,list):
            kp1 = kps1[match[0].queryIdx]
            kp2 = kps2[match[0].trainIdx]
        else:
            kp1 = kps1[match.queryIdx]
            kp2 = kps2[match.trainIdx]
        return kp1,kp2
    
    # draw the line of match on combined image 
    def draw_match_line(matches,img_out,wA,kps1,kps2):
        for m in matches:
            kp1,kp2 = get_match_kp(m,kps1,kps2)
            kp1_pt = np.array( kp1.pt )
            kp2_pt = np.array( kp2.pt )
            if not is_meet_dis(kp1_pt,kp2_pt):
                continue
            cv2.line(img_out, ( int(kp1_pt[0]) , int(kp1_pt[1]) ), ( int(kp2_pt[0] + wA) , int(kp2_pt[1]) ), (0,0,255), 1)

    # draw the line of BF match on two images
    def draw_BF_match_line():
        # prepare combined image
        img_out = combine_img(img1.img,img2.img)
        raw_matches = BF_match_arr[img1.idx]
        matches = []
        hA, wA = img1.img.shape[:2]
        for i in range(len(raw_matches) - 1 , -1 , -1):
            m = raw_matches[i]
            if is_meet_ratio(m[0],m[1]):
                matches.append(m)
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
    
    # create GMM foreground mask of img2
    def GMM(img_GMM1,img_GMM2):
        fgbg_gmm = cv2.createBackgroundSubtractorMOG2(detectShadows=True)
        #the kernel for morphologyEx
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
        fgbg_gmm.apply(img_GMM1.img)
        fgmask = fgbg_gmm.apply(img_GMM2.img)
        fgmask = cv2.erode(fgmask,kernel,iterations = 2)
        fgmask = cv2.dilate(fgmask,kernel,iterations = 5)
        return fgmask
    
    # using the mask and SIFT key point match to find the target's contour on img2
    def find_target_contour(kps_t,kps2,matches,mask):
        _,contours, hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        temp = []
        count_arr = [0 for i in range(len(contours))]
        count = 0

        next_p = np.array([512.0, 512.0, 0.0, 0.0]) 
        # determine which contour is pointed by key point
        for m in matches:
            kp1,kp2 = get_match_kp(m,kps_t,kps2)
            pt = kp2.pt
            for i,c in enumerate( contours ):
                if cv2.pointPolygonTest(c,pt,False) >= 0:
                    count += 1
                    count_arr[i] += 1
            temp.append(kp2)
        show_im("mask",mask)
        out_mask = mk_empty_img(mask)
        # find the rectangle coordinate of pointed contour
        for i in range(0,len(contours)):
            if count_arr[i] > 0:
                x,y,w,h = cv2.boundingRect(contours[i])
                cv2.rectangle(img2.img,(x,y),(x+w,y+h),(0,255,0),2)

                if((img_target.rect[0]<=(x+w/2)<=img_target.rect[2])&(img_target.rect[1]<=(y+h/2)<=img_target.rect[3])):
                    next_p[0] = min(next_p[0],x)
                    next_p[1] = min(next_p[1],y)
                    next_p[2] = max(next_p[2],x+w)
                    next_p[3] = max(next_p[3],y+h)
                    out_mask[y:y+h, x:x+w] = mask[y:y+h, x:x+w]
                    #print(x,y,x+w,y+h)
                    #show_im("out"+str(i),out_mask)
        print("next_p 1:",next_p)
        img_target.rect = next_p 
        cv2.rectangle(out_mask,(int(next_p[0]),int(next_p[1])),(int(next_p[2]),int(next_p[3])),255,thickness=1)
        return out_mask

    # finding the SIFT key points of target image
    def SIFT_target_img():
        sift = cv2.xfeatures2d.SIFT_create()
        kp = sift.detect(img_target.img, None)
        img_target.kps = kp

    # set the bounded image(rad rectangle) in img1 to img_target
    # compute on image's coordinate
    def set_target_img():
        if not sum(img_target.rect):
            print("No bounded area!")
            return

        print(img_target.rect)

        width = int(abs(img_target.rect[0] - img_target.rect[2]))
        height = int(abs(img_target.rect[1] - img_target.rect[3]))
        x = int(min(img_target.rect[0],img_target.rect[2]))
        y = int(min(img_target.rect[1],img_target.rect[3]))
        temp_img = np.zeros((height,width,3),dtype="uint8")
        temp_img = img1.img[y:y + height,x:x + width]
        img_target.draw_img(np.copy(temp_img))
        SIFT_target_img()
        ui.target_label.setPixmap(QPixmap.fromImage(img_target.qImg))
        ui.target_label.setFixedSize(width*2,height*2)

    # BF match target image with img2
    def BF_target_match():
        ori_img2 = img_arr[img2.idx]
        des_t = compute_SIFT_des(img_target.img,img_target.kps)
        if ui.Target_Limit_Button.isChecked():
            kps2,des_2 = compute_SIFT_des(ori_img2,img2.kps,img_target.rect,30)
        else:
            des_2 = compute_SIFT_des(ori_img2,img2.kps)
            kps2 = img2.kps
        matcher = cv2.DescriptorMatcher_create("BruteForce")
        matches = matcher.knnMatch(des_t,des_2,2)
        img_out = combine_img(img_target.img,ori_img2)
        hA,wA = img_target.img.shape[:2]
        # draw the line on target image and img1
        draw_match_line(matches,img_out,wA,img_target.kps,kps2)
        return kps2,matches,img_out
    
    # create the graph for Hungarian algorithm
    def kp_feature_distance_graph(des1,des2):
        print(len(des1),len(des2))
        graph = []
        for i in range(0,len(des1)):
            temp_dict = []
            des1_pt = np.array(des1[i])
            for j in range(0,len(des2)):
                des2_pt = np.array(des2[j])
                dis = np.linalg.norm(des1_pt - des2_pt)
                temp_dict.append(dis)
            graph.append(temp_dict)
        return graph
    
    # Hungarian algorithm to match target image with img2
    def Hungarian_match():
        ori_img2 = img_arr[img2.idx]
        des_t = compute_SIFT_des(img_target.img,img_target.kps)
        if ui.Target_Limit_Button.isChecked():
            kps2,des_2 = compute_SIFT_des(ori_img2,img2.kps,img_target.rect,30)
        else:
            des_2 = compute_SIFT_des(ori_img2,img2.kps)
            kps2 = img2.kps
        graph = kp_feature_distance_graph(des_t, des_2)
        matches = []
        hungarian = Munkres()
        print("Computing...")
        index = hungarian.compute(graph)
        print("Finish!")
        for row,column in index:
            dis = graph[row][column]
            temp = cv2.DMatch(row,column,dis)
            matches.append(temp)
        img_out = combine_img(img_target.img,ori_img2)
        hA,wA = img_target.img.shape[:2]
        # draw the line on target image and img1
        draw_match_line(matches,img_out,wA,img_target.kps,kps2)
        return kps2,matches,img_out
    
    # find the target in next image & move img1,img2 to next image
    # input rect is a list of 4 element (index 0,1 for first point, index 2,3 for second point)
    # (the left top & right bottom point of target rectangle's coordinate)
    def find_next_target(rect):
        # draw the rectangle on next image to highlight the target
        change_image(1)
        im_h,im_w,c = img1.img.shape
        lb_w = ui.img_label1.width()
        lb_h = ui.img_label1.height()
        img1.draw_rect(rect,im_w,im_h,lb_w,lb_h,(0,255,0),True)
        dis_img()
        # set the rectangle highlight part of img1 as the next target image
        set_target_img()
        
    # display the match result in subwindows
    # mode determine which match algorithm to use 
    def show_match_result(mode):
        if ui.target_label.pixmap() == None:
            print("No target image.")
            return
        # mode 0 use BF match
        if mode == 0 :
            kps2,matches,img_out = BF_target_match()
        # mode 1 use Hungarian algorithm
        elif mode == 1:
            _,_,BF_img = BF_target_match()
            kps2,matches,Hungarian_img = Hungarian_match()
            img_out = combine_img(BF_img,Hungarian_img)
        # find the GMM mask contour of target
        mask = GMM(img1,img2)
        
        # show_im("fgmask",mask)
        out_mask = find_target_contour(img_target.kps,kps2,matches,mask)
        img_out = np.hstack((img_out,cv2.cvtColor( out_mask, cv2.COLOR_GRAY2RGB)))
        # set image to subwindow's label
        qImg = convImg(np.copy(img_out))
        sub_ui.Image_Label.setPixmap(QPixmap.fromImage(qImg))
        # show subwindow
        Dialog2.show()
        find_next_target(img_target.rect)
    
    # mouse trigger function
    ###########################################

    # draw rectagle on image1
    def img_label1_mousePressEvent(self,event):
        global draing_flag
        draing_flag = True
        img_target.rect[0] = event.x()
        img_target.rect[1] = event.y()
    
    def img_lable1_mouseReleaseEvent(self,event):
        global draing_flag
        draing_flag = False
        # convert the target rectangle's coordinate to image's coordinate
        im_h,im_w,c = img1.img.shape
        lb_w = ui.img_label1.width()
        lb_h = ui.img_label1.height()
        w_ratio = im_w/lb_w
        h_ratio = im_h/lb_h
        img_target.rect[0] = img_target.rect[0] * w_ratio
        img_target.rect[1] = img_target.rect[1] * h_ratio
        img_target.rect[2] = img_target.rect[2] * w_ratio
        img_target.rect[3] = img_target.rect[3] * h_ratio
    
    def img_label1_mouseMoveEvent(self,event):
        if draing_flag:
            im_h,im_w,c = img1.img.shape
            lb_w = ui.img_label1.width()
            lb_h = ui.img_label1.height()
            img_target.rect[2] = event.x()
            img_target.rect[3] = event.y()
            img1.draw_rect(img_target.rect,im_w,im_h,lb_w,lb_h,(0,0,255))
            dis_img()
    
    def img_Label1_mouseDoubleClickEvent(self,event):
        img_target.rect[0] = 0
        img_target.rect[1] = 0
        img_target.rect[2] = 0
        img_target.rect[3] = 0
        img1.draw_img(img1.img)
        dis_img()
    
    def bind_img_lable1_func(obj):
        funcType = type(obj.mousePressEvent)
        obj.mousePressEvent = funcType(img_label1_mousePressEvent,obj)
        funcType = type(obj.mouseReleaseEvent)
        obj.mouseReleaseEvent = funcType(img_lable1_mouseReleaseEvent,obj)
        funcType = type(obj.mouseMoveEvent)
        obj.mouseMoveEvent = funcType(img_label1_mouseMoveEvent, obj)
        funcType = type(obj.mouseDoubleClickEvent)
        obj.mouseDoubleClickEvent = funcType(img_Label1_mouseDoubleClickEvent, obj)

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
        ui.Target_BF_Button.clicked.connect(lambda: show_match_result(0))
        ui.Target_Hungarian_Button.clicked.connect(lambda: show_match_result(1))

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
