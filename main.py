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
    img_optical_flow_arr = []
    img_arr = []
    img_num = 0
    draing_flag = False
    erode_num = 3
    dilate_num = 5
    saved_result_arr = []
    # function
    ###########################################

    # display image
    def dis_img():
        ui.img_label1.setPixmap( QPixmap.fromImage(img1.qImg))
        ui.img_label2.setPixmap( QPixmap.fromImage(img2.qImg))
        # refresh the mainwindow
        QApplication.processEvents()

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
        if ui.Optical_Flow_Button.isChecked():
            img1.set_img(img_optical_flow_arr , img1_idx , img_kp_arr)
            img2.set_img(img_optical_flow_arr, img2_idx , img_kp_arr)
        else:
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
    
    # select the perticular image to change
    def select_image():
        img_id = ui.Image_Selector.value()
        direction = img_id - img1.idx
        change_image(direction)
    
    # change the image with saved result data
    def change_image_with_result(direction):
        change_image(direction)
        if len(saved_result_arr) != 0:
            find_next_target(0,saved_result_arr[img1.idx])
            dis_img()
        else :
            print("Haven't loaded result data.")

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
        fgmask = cv2.erode(fgmask,kernel,iterations = erode_num)
        fgmask = cv2.dilate(fgmask,kernel,iterations = dilate_num)
        return fgmask
    
    # using the mask and SIFT key point match to find the target's contour on img2
    def find_target_contour(kps_t_arr,kps2_arr,matches_arr,mask,is_show):
        _,contours, hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        temp = []
        count_arr = [0 for i in range(len(contours))]
        count = 0
        next_p = np.array([512.0, 512.0, 0.0, 0.0]) 
        # determine which contour is pointed by key point
        for m_idx,matches in enumerate(matches_arr):
            for m in matches:
                kp1,kp2 = get_match_kp(m,kps_t_arr[m_idx],kps2_arr[m_idx])
                pt = kp2.pt
                for i,c in enumerate( contours ):
                    if cv2.pointPolygonTest(c,pt,False) >= 0:
                        count += 1
                        count_arr[i] += 1
                temp.append(kp2)
        if is_show:
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
        cv2.rectangle(out_mask,(int(next_p[0]),int(next_p[1])),(int(next_p[2]),int(next_p[3])),255,thickness=1)
        # return the target contour of mask and rectangle coordinate
        return out_mask,next_p

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
        temp = [img_target.rect[0],img_target.rect[1],img_target.rect[2],img_target.rect[3]]
        img_target.rect[0] = min(temp[0],temp[2])
        img_target.rect[1] = min(temp[1],temp[3]) 
        img_target.rect[2] = max(temp[0],temp[2]) 
        img_target.rect[3] = max(temp[1],temp[3]) 
        width = int(abs(img_target.rect[0] - img_target.rect[2]))
        height = int(abs(img_target.rect[1] - img_target.rect[3]))
        print(width*height)
        global erode_num
        global dilate_num
        if(width*height < 15000):
            erode_num = 2
            dilate_num = 3
        else:
            erode_num = 4
            dilate_num = 8
        temp_img = get_rect_img(img1.img,img_target.rect)
        img_target.draw_img(np.copy(temp_img))
        SIFT_target_img()
        ui.target_label.setPixmap(QPixmap.fromImage(img_target.qImg))
        ui.target_label.setFixedSize(width*2,height*2)

    # BF match target image with img2
    def BF_target_match():
        ori_img2 = img_arr[img2.idx]
        des_t = compute_SIFT_des(img_target.img,img_target.kps)
        if ui.Target_Limit_Button.isChecked():
            kps2,des_2 = compute_SIFT_des(ori_img2,img2.kps,img_target.rect,[30,30])
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
    
    # match the previous target image with img2
    def pre_target_BF_match():
        pre_img_idx = (img1.idx - 1)%img_num
        pre_img = img_arr[pre_img_idx]
        pre_target_img = get_rect_img(pre_img,img_target.pre_rect)
        sift = cv2.xfeatures2d.SIFT_create()
        kp_t,des_t = sift.detectAndCompute(pre_target_img,None)
        # use the target velocity(target's motion attribute) to limit key point on img2
        ori_img2 = img_arr[img2.idx]
        # the move distance should be two times of motion
        predict_motion = (img_target.motion[0] * 2,img_target.motion[1] * 2)
        kps2,des_2 = compute_SIFT_des(ori_img2,img2.kps,img_target.pre_rect,predict_motion)
        # match
        matcher = cv2.DescriptorMatcher_create("BruteForce")
        matches = matcher.knnMatch(des_t,des_2,2)
        img_out = combine_img(pre_target_img,ori_img2)
        hA,wA = pre_target_img.shape[:2]
        # draw the line on target image and img1
        draw_match_line(matches,img_out,wA,kp_t,kps2)
        return kps2,matches,img_out,kp_t
    
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
            kps2,des_2 = compute_SIFT_des(ori_img2,img2.kps,img_target.rect,[30,30])
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
    # set up the rect attribute of img_target which is a list of 4 element (index 0,1 for first point, index 2,3 for second point)
    # (the left top & right bottom point of target rectangle's coordinate)
    # dir is the direction of next image(also can set 0 to let image unchanged)
    def find_next_target(dir,next_rect):
        # draw the rectangle on next image to highlight the target
        change_image(dir)
        img_target.pre_rect = copy.deepcopy(img_target.rect)
        img_target.rect = next_rect
        im_h,im_w,c = img1.img.shape
        lb_w = ui.img_label1.width()
        lb_h = ui.img_label1.height()
        img1.draw_rect(img_target.rect,im_w,im_h,lb_w,lb_h,(0,255,0),True)
        # set the rectangle highlight part of img1 as the next target image
        set_target_img()
    
    # Dector main function
    # display the match result in subwindows and detect result on next image
    # mode determine which match algorithm to use
    # is_show flag determine whether the process is showed 
    def show_detect_result(mode,is_show):
        # store the two kind of match result and used key point
        kps2_arr = []
        kps_t_arr = []
        matches_arr = []
        if ui.target_label.pixmap() == None:
            print("No target image.")
            return
        # mode 0 use BF match
        if mode == 0 :
            kps2,matches,img_out = BF_target_match()
            sub_ui.textBrowser_2.setText("Result mask")
        # mode 1 use Hungarian algorithm
        elif mode == 1:
            _,_,BF_img = BF_target_match()
            kps2,matches,Hungarian_img = Hungarian_match()
            img_out = combine_img(BF_img,Hungarian_img)
            sub_ui.textBrowser_2.setText("Hungarian")
        kps2_arr.append(kps2)
        kps_t_arr.append(img_target.kps)
        matches_arr.append(matches)
        # use the previous rectangle to reinforce match result
        if sum(img_target.pre_rect) != 0:
            kps2,matches,pre_img_out,kps_t = pre_target_BF_match()
            kps2_arr.append(kps2)
            kps_t_arr.append(kps_t)
            matches_arr.append(matches)
            temp = np.hstack((img_out,pre_img_out))
            show_im("two match result",temp)
        # find the GMM mask contour of target
        print("e d:", erode_num,dilate_num)
        mask = GMM(img1,img2)
        # use mask and match restult to find the target in next image
        out_mask,next_rect = find_target_contour(kps_t_arr,kps2_arr,matches_arr,mask,is_show)
        # draw the finding result on match result image
        _,target_width,_ = img_target.img.shape
        cv2.rectangle(img_out,(int(next_rect[0] + target_width),int(next_rect[1])),(int(next_rect[2] + target_width),int(next_rect[3])),(0,255,0),thickness=1)
        # combine the match result and final GMM mask
        img_out = np.hstack((img_out,cv2.cvtColor( out_mask, cv2.COLOR_GRAY2RGB)))
        # set image of result to subwindow's label
        qImg = convImg(np.copy(img_out))
        sub_ui.Image_Label.setPixmap(QPixmap.fromImage(qImg))
        sub_ui.textBrowser.setText("BF Match")
        # show subwindow
        if is_show:
            Dialog2.show()
        # update the next target's coordinate of rectangle
        find_next_target(1,next_rect)
        dis_img()
        return next_rect
    
    # save the match result 
    def save_detect_result():
        # check dir exist
        data_dir = "result_data"
        if not os.path.isdir(data_dir):
            os.mkdir(data_dir)
        filename = ui.FileName.toPlainText()
        # check filename isn't empty
        if filename == "":
            print("The filename is empty!")
            return
        # check whether the target exist
        if ui.target_label.pixmap() == None:
            print("No target image!")
            return
        # check img1 is first image
        if img1.idx != 0 :
            print("The left image is not the first image!")
            return
        # run detect to find target on all image
        result_rect_arr = [img_target.rect]
        for i in range(len(img_arr) - 1):
            result_rect = show_detect_result(0,False)
            result_rect_arr.append(result_rect)
        # store the result
        f = open(data_dir + "/" + filename,"wb")
        f.write(cPickle.dumps(result_rect_arr))
        f.close()
        print("Already save result into the file: " + filename + "!")
    
    # display the detect result file of selected type of vehicle 
    def display_select_result():
        # intial the image to first image
        img1.set_img(img_arr,0,img_kp_arr)
        img2.set_img(img_arr,1,img_kp_arr)
        select_data = ui.Result_Data.currentText()
        if select_data == "Bus":
            load_detect_result(File_Type.BUS)
        elif select_data == "Car1":
            load_detect_result(File_Type.CAR)
        elif select_data == "Car2":
            load_detect_result(File_Type.CAR2)
        elif select_data == "Autobike1":
            load_detect_result(File_Type.AUTOBIKE)
        elif select_data == "Autobike2":
            load_detect_result(File_Type.AUTOBIKE2)
        if len(saved_result_arr) == 0:
            return
        for i,rect in enumerate(saved_result_arr):
            if i == 0:
                find_next_target(0,rect)
            else:
                find_next_target(1,rect)
            dis_img()
            time.sleep(.500)

    # load the detect result file and store the detect result data into global array
    def load_detect_result(type):
        dir_path = "result_data"
        if type == File_Type.BUS:
            file_path = dir_path + "/" + "bus.txt"
        elif type == File_Type.CAR:
            file_path = dir_path + "/" + "car.txt"
        elif type == File_Type.CAR2:
            file_path = dir_path + "/" + "car_left.txt"
        elif type == File_Type.AUTOBIKE:
            file_path = dir_path + "/" + "moto.txt"
        elif type == File_Type.AUTOBIKE2:
            file_path = dir_path + "/" + "moto_right.txt"
        else:
            file_path = dir_path + "/" + ""
        if not os.path.isfile(file_path):
            print("The result file doesn't exist!!")
            return
        saved_result_arr.clear()
        f = open(file_path,"rb")
        data = cPickle.loads(f.read())
        for rect_data in data:
            saved_result_arr.append(rect_data)
        f.close()
    
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
        ui.Target_BF_Button.clicked.connect(lambda: show_detect_result(0,True))
        ui.Target_Hungarian_Button.clicked.connect(lambda: show_detect_result(1,True))
        ui.Optical_Flow_Button.clicked.connect(lambda: change_image(0))
        ui.SaveFileButton.clicked.connect(save_detect_result)
        ui.Dispaly_Button.clicked.connect(display_select_result)
        ui.Result_Left_Button.clicked.connect(lambda: change_image_with_result(-1))
        ui.Result_Right_Button.clicked.connect(lambda: change_image_with_result(1))
        ui.Image_Selector.valueChanged.connect(select_image)

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
        if not os.path.isfile(dir_path + "optical_flow.txt"):
            import create_data.Optical_Flow
    
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
    
    # load optical flow data
    def load_optical_flow():
        data_path = "data/optical_flow.txt"
        f = open(data_path,"rb")
        data = cPickle.loads(f.read())
        for img in data:
            img_optical_flow_arr.append(img)
    
    # load data
    def load_data(img_kp_arr):
        check_data_file()
        load_SIFT_kp()
        load_BF_match()
        load_optical_flow()
    
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
