from PyQt5 import QtWidgets
import GUI_template as GUI
import GUI_subwindow as subwindow
from Class.image import *
from skimage.measure import compare_ssim
if __name__ == "__main__":
    # global variable
    ###########################################

    # create ui object
    ui = GUI.Ui_Dialog()
    sub_ui = subwindow.Ui_Dialog()
    img1 = Image(cv2.imread("im0/out_0.jpg"),0)
    img2 = Image(cv2.imread("im0/out_1.jpg"),1)
    img_target_arr = []
    img_target = Target_Image(mk_empty_img(img1.img),-1)
    img_dir_path = "im0/"
    img_name_arr = []
    img_kp_arr = []
    BF_match_arr = []
    img_optical_flow_arr = []
    img_arr = []
    img_num = 0
    draing_flag = False
    saved_result_arr = []
    yolo_data_arr = []

    # the record list of kalman filter
    x1_arr = []
    x2_arr = []
    y1_arr = []
    y2_arr = []
    x_arr = []
    y_arr = []
    xv_arr = []
    yv_arr = []
    xv_new_arr = []
    yv_new_arr = []
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
        img1_out = copy.deepcopy(img1.drew_img)
        img2_out = copy.deepcopy(img2.drew_img)
        cv2.drawKeypoints(img1.img,img1.kps,img1_out)
        cv2.drawKeypoints(img2.img,img2.kps,img2_out)
        img1.draw_img(img1_out)
        img2.draw_img(img2_out)
    
    # draw the flow of BF match
    def draw_BF_match_flow():
        img1_out = copy.deepcopy(img1.drew_img)
        img2_out = copy.deepcopy(img2.drew_img)
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
        img_out = combine_img(img1.drew_img,img2.drew_img)
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
        fgbg_gmm.apply(img_GMM1)
        fgmask = fgbg_gmm.apply(img_GMM2)
        fgmask = cv2.erode(fgmask,kernel,iterations = img_target.erode_num)
        fgmask = cv2.dilate(fgmask,kernel,iterations = img_target.dilate_num)
        return fgmask
    
    # using the mask and SIFT key point match to find the target's contour on img2
    def find_target_contour(kps_t_arr,kps2_arr,matches_arr,mask):
        print("Finding target contour......")
        print_bar()
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
                #print("pt:" + str(pt))
                for i,c in enumerate( contours ):
                    if cv2.pointPolygonTest(c,pt,False) >= 0:
                        count += 1
                        count_arr[i] += 1
                temp.append(kp2)
        out_mask = mk_empty_img(mask)
        test_range = img_target.check_range(2)
        print("test rectangle range:" + str(test_range))
        print("motion:" + str(img_target.motion))
        # find the rectangle coordinate of pointed contour
        for i in range(0,len(contours)):
            if count_arr[i] > 0:
                x,y,w,h = cv2.boundingRect(contours[i])
                #cv2.rectangle(img2.img,(x,y),(x+w,y+h),(0,255,0),2)
                count = 1
                print("current contour rectangle:",x,y,x+w,y+h)
                if((test_range[0]<=(x+w/2)<=test_range[2])&(test_range[1]<=(y+h/2)<=test_range[3])):
                    next_p[0] = min(next_p[0],x)
                    next_p[1] = min(next_p[1],y)
                    next_p[2] = max(next_p[2],x+w)
                    next_p[3] = max(next_p[3],y+h)
                    out_mask[y:y+h, x:x+w] = mask[y:y+h, x:x+w]
                    print("Adopt!")
                    #show_im("out"+str(i),out_mask)
        print("next target's rectangle:",next_p)
        print_bar()
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
    def set_target_img(is_init=False):
        if not sum(img_target.rect):
            print("No bounded area!")
            return
        if is_init:
            img_target.clear()
            kl_record_list_init()
        temp = [img_target.rect[0],img_target.rect[1],img_target.rect[2],img_target.rect[3]]
        img_target.set_rect(temp)
        width = int(abs(img_target.rect[0] - img_target.rect[2]))
        height = int(abs(img_target.rect[1] - img_target.rect[3]))
        if(width*height < 15000):
            img_target.erode_num = 2
            img_target.dilate_num = 3
        else:
            img_target.erode_num = 4
            img_target.dilate_num = 8
        temp_img = get_rect_img(img1.img,img_target.rect)
        img_target.draw_img(np.copy(temp_img),is_set = True)
        SIFT_target_img()
        ui.target_label.setPixmap(QPixmap.fromImage(img_target.qImg))
        ui.target_label.setFixedSize(width*2,height*2)

    # draw all target in img_target_arr on img1
    def draw_target_arr():
        for i in range(len(img_target_arr)):
            im_h,im_w,c = img1.img.shape
            lb_w = ui.img_label1.width()
            lb_h = ui.img_label1.height()
            img1.draw_rect(img_target_arr[i].rect,im_w,im_h,lb_w,lb_h,(0,255,0),is_img_coor = True,is_new = False)
        dis_img()

    # set up all the yolo labeled target to image target type
    def set_yolo_target():
        img_target_arr.clear()
        img1.reset_drew_img()
        yolo_data = yolo_data_arr[img1.idx]
        for rect in yolo_data:
            temp = Target_Image(mk_empty_img(img1.img),-1)
            temp.set_rect(rect)
            img_target_arr.append(temp)
        global img_target
        temp = img_target
        for i in range(len(img_target_arr)):
            img_target = img_target_arr[i]
            find_next_target(0,img_target.rect)
        img_target = temp
        draw_target_arr()

    # BF match target image with img2
    def BF_target_match():
        ori_img2 = img_arr[img2.idx]
        des_t = compute_SIFT_des(img_target.img,img_target.kps)
        # use target motion to match
        predict_motion = (img_target.motion[0] * 2,img_target.motion[1] * 2)
        kps2,des_2 = compute_SIFT_des(ori_img2,img2.kps,img_target.rect,predict_motion)
        matcher = cv2.DescriptorMatcher_create("BruteForce")
        raw_matches = matcher.knnMatch(des_t,des_2,2)
        matches = []
        # the ratio test of match
        for i in range(len(raw_matches) - 1 , -1 , -1):
            m = raw_matches[i]
            if is_meet_ratio(m[0],m[1]):
                matches.append(m)
        img_out = combine_img(img_target.img,ori_img2)
        hA,wA = img_target.img.shape[:2]
        # draw the line on target image and img1
        draw_match_line(matches,img_out,wA,img_target.kps,kps2)
        return kps2,matches,img_out
    
    # match the previous target image with img2
    def pre_target_BF_match():
        pre_img = img_arr[img_target.pre_idx]
        pre_target_img = get_rect_img(pre_img,img_target.pre_rect)
        sift = cv2.xfeatures2d.SIFT_create()
        kp_t,des_t = sift.detectAndCompute(pre_target_img,None)
        # use the target velocity(target's motion attribute) to limit key point on img2
        ori_img2 = img_arr[img2.idx]
        # the move distance should be two times of motion
        predict_motion = (img_target.motion[0],img_target.motion[1])
        kps2,des_2 = compute_SIFT_des(ori_img2,img2.kps,img_target.rect,predict_motion)
        # match
        matcher = cv2.DescriptorMatcher_create("BruteForce")
        raw_matches = matcher.knnMatch(des_t,des_2,2)
        matches = []
        # the ratio test of match
        for i in range(len(raw_matches) - 1 , -1 , -1):
            m = raw_matches[i]
            if is_meet_ratio(m[0],m[1]):
                matches.append(m)
        img_out = combine_img(pre_target_img,ori_img2)
        hA,wA = pre_target_img.shape[:2]
        # draw the line on target image and img1
        draw_match_line(matches,img_out,wA,kp_t,kps2)
        return kps2,matches,img_out,kp_t

    def det_motion_type():
        select_motion = ui.Motion_Type.currentText()
        if select_motion == "Kalman":
            return Motion_Type.KALMAN
        elif select_motion == "Complex":
            return Motion_Type.COMPLEX
        # default compute motion with our simple way
        else:
            return Motion_Type.ORIGIN
    
    def kl_record_list_init():
        x1_arr.clear()
        x2_arr.clear()
        y1_arr.clear()
        y2_arr.clear()
        x_arr.clear()
        y_arr.clear()
        xv_arr.clear()
        yv_arr.clear()
        xv_new_arr.clear()
        yv_new_arr.clear()
    
    # show the plot of kalman info
    def show_kl_chart():
        if(len(y1_arr) == 0) or not ui.KL_Chart_Button.isChecked():
            return
        idx_arr = range(len(y1_arr))
        plt.figure()
        plt.plot(idx_arr,x_arr,marker='o',label = "Detected X")
        plt.plot(idx_arr,x1_arr,marker='o',label = "Kalman X")
        plt.plot(idx_arr,y_arr,marker='o',label = "Detected Y")
        plt.plot(idx_arr,y1_arr,marker='o',label = "Kalman Y")
        plt.legend()
        plt.figure()
        plt.plot(idx_arr,xv_arr,marker='o',label = "Detected X velocity")
        plt.plot(idx_arr,x2_arr,marker='o',label = "Kalman X velocity")
        plt.plot(idx_arr,xv_new_arr,marker='o',label = "New X velocity")
        plt.plot(idx_arr,yv_arr,marker='o',label = "Detected Y velocity")
        plt.plot(idx_arr,y2_arr,marker='o',label = "Kalman Y velocity")
        plt.plot(idx_arr,yv_new_arr,marker='o',label = "New Y velocity")
        plt.legend()
        # display the chart,if the kl showing option is checked
        plt.show()

    # count motion
    def motion():
        new_motion = [0,0]
        if img_target.is_predict:
            new_motion[0] = (img_target.rect[0] - img_target.predict_pre_rect[0] + img_target.rect[2] - img_target.predict_pre_rect[2]) / 2 
            new_motion[1] = (img_target.rect[1] - img_target.predict_pre_rect[1] + img_target.rect[3] - img_target.predict_pre_rect[3]) / 2 
        else:
            new_motion[0] = (img_target.rect[0] - img_target.pre_rect[0] + img_target.rect[2] - img_target.pre_rect[2]) / 2 
            new_motion[1] = (img_target.rect[1] - img_target.pre_rect[1] + img_target.rect[3] - img_target.pre_rect[3]) / 2 
        # kalman filter
        x_center = ((img_target.rect[2] - img_target.rect[0]) / 2) + img_target.rect[0]
        y_center = ((img_target.rect[3] - img_target.rect[1]) / 2) + img_target.rect[1]
        x = np.array([x_center,y_center],np.float32)
        if not img_target.kl_init_f:
            img_target.kl_init(new_motion)
        img_target.kl.correct(x)
        # predict the xy coordinate & velocity ([x,y,xv,yv])
        kl_pre = img_target.kl.predict()
        # compute new motion of target
        motion_type = det_motion_type()
        if motion_type == Motion_Type.ORIGIN:
            img_target.motion[0] = new_motion[0]
            img_target.motion[1] = new_motion[1]
        elif motion_type == Motion_Type.KALMAN:
            img_target.motion[0] = kl_pre[2]
            img_target.motion[1] = kl_pre[3]
        elif motion_type == Motion_Type.COMPLEX:
            img_target.motion[0] = (new_motion[0] + kl_pre[2]) / 2
            img_target.motion[1] = (new_motion[1] + kl_pre[3]) / 2
        # draw the motion vector on image
        motion_img = copy.deepcopy(img_arr[img1.idx])
        pt1 = (int(x_center), int(y_center))
        pt2 = (int(x_center + img_target.motion[0]), int(y_center + img_target.motion[1]))
        cv2.arrowedLine(motion_img, pt1,pt2,[0,0,255],2,8,0,0.5)
        show_im("motion vector",motion_img)
        # store kalman data into record list
        x1_arr.append(kl_pre[0])
        x2_arr.append(kl_pre[2])
        y1_arr.append(kl_pre[1])
        y2_arr.append(kl_pre[3])
        x_arr.append(x_center)
        xv_arr.append(new_motion[0])
        xv_new_arr.append(img_target.motion[0])
        y_arr.append(y_center)
        yv_arr.append(new_motion[1])
        yv_new_arr.append(img_target.motion[1])
        # draw the chart of kalman info
        show_kl_chart()

    def predict_next(mask):
        result = copy.deepcopy(img_target.rect)
        if(img_target.motion[0] >= 0 ):
            result[2] += (img_target.motion[0] * 1.5)
        else:
            result[0] += (img_target.motion[0] * 1.5)
        if(img_target.motion[1] >= 0 ):
            result[3] += (img_target.motion[1] * 1.5)
        else:
            result[1] += (img_target.motion[1] * 1.5)


        check = 0

        #print("o_rect" + str(img_target.rect))
        #print("n_rect" + str(next_rect))            
        _,contours, hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

        x = (result[2] - result[0]) / 25
        y = (result[3] - result[1]) / 25
        next_pt = []
        for i in range(25):
            for j in range(25):
                next_pt.append((int(result[0] + x * i), int(result[1] + y * j)))
            
        #print("next pt :" + str(next_pt))

        count_arr = [0 for i in range(len(contours))]
        count = 0
        for j in range(625):
            pt = next_pt[j]
            #print("pt:" + str(pt))
            for i,c in enumerate( contours ):
                if cv2.pointPolygonTest(c,pt,False) >= 0:
                    count += 1
                    count_arr[i] += 1
                    check = 1
        out_mask = mk_empty_img(mask)
        #cv2.rectangle(out_mask,(int(result[0]),int(result[1])),(int(result[2]),int(result[3])),255,thickness=1)
        #show_im("next_" + str(index), out_mask)
        next_p = np.array([512.0, 512.0, 0.0, 0.0])
        for i in range(0,len(contours)):
            if count_arr[i] > 0:
                x,y,w,h = cv2.boundingRect(contours[i])
                cv2.rectangle(img2.img,(x,y),(x+w,y+h),(0,255,0),2)

                next_p[0] = min(next_p[0],x)
                next_p[1] = min(next_p[1],y)
                next_p[2] = max(next_p[2],x+w)
                next_p[3] = max(next_p[3],y+h)
                out_mask[y:y+h, x:x+w] = mask[y:y+h, x:x+w]
                #print(x,y,x+w,y+h)
                #show_im("out"+str(i),out_mask)
        print("next predicted rectangle:",next_p)
        cv2.rectangle(out_mask,(int(next_p[0]),int(next_p[1])),(int(next_p[2]),int(next_p[3])),255,thickness=1)
        #img_target.rect = next_p
        print("check:", check)
        print_bar()
        if(check == 1): 
            return next_p
        else:
            return result

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
        # use default motion to match
        kps2,des_2 = compute_SIFT_des(ori_img2,img2.kps,img_target.rect,[30,30])
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
        if not img_target.is_predict:
            img_target.set_pre_rect(img_target.rect)
            img_target.pre_idx = img1.idx
        else:
            img_target.set_predict_pre_rect(img_target.rect)
        change_image(dir)
        img_target.set_rect(next_rect)
        im_h,im_w,c = img1.img.shape
        lb_w = ui.img_label1.width()
        lb_h = ui.img_label1.height()
        img1.draw_rect(img_target.rect,im_w,im_h,lb_w,lb_h,(0,255,0),is_img_coor = True,is_new = False)
        # set the rectangle highlight part of img1 as the next target image
        set_target_img()
    
    def yolo_match(kps_t_arr,kps2_arr,matches_arr):
        yolo_data = yolo_data_arr[img2.idx]
        yolo_img_arr = []
        temp = copy.deepcopy(img2.img)
        for i,kps_t in enumerate(kps_t_arr):
            kps_t = kps_t_arr[i]
            kps2 = kps2_arr[i]
            matches = matches_arr[i]
            for d in yolo_data:
                out_img = get_rect_img(img2.img,arrange_rect(d))
                yolo_img_arr.append(copy.deepcopy(out_img))
                print_rect(temp,arrange_rect(d),(0,0,255))
            if img_target.is_predict:
                pre_img = img_arr[img_target.pre_idx]
                target_img = get_rect_img(pre_img,img_target.pre_rect)
            else :
                target_img = img_target.img
            count_arr = [0 for i in range(len(yolo_data))] 
            # determine which contour is pointed by key point
            for m in matches:
                kp1,kp2 = get_match_kp(m,kps_t,kps2)
                pt = kp2.pt
                cv2.circle(temp,(int(pt[0]),int(pt[1])),1,(0,0,255),4)
                for i,d in enumerate(yolo_data):
                    d = arrange_rect(d)
                    if (d[0] <= pt[0] <= d[2]) and (d[1] <= pt[1] <= d[3]):
                        count_arr[i] += 1
            print_rect(temp,img_target.get_legal_region(),(0,255,0))
            show_im("Yolo match used data",temp)
            max_c = 0
            max_idx = -1
            for i,count in enumerate(count_arr):
                if count > max_c:
                    max_c = count
                    max_idx = i
            if max_idx == -1:
                return [0,0,0,0]
            match_num_thrs = int(len(matches) / 2)
            print("Yolo match Threshould : ",match_num_thrs)
            print("max match number : ",max_c)
            if max_c >= match_num_thrs:
                rect = yolo_data[max_idx]
                if(img_target.check_in_legal_region(rect)):
                    print("Using yolo data as detect result!")
                    return rect
                else :
                    return [0,0,0,0]
            else:
                return [0,0,0,0]
            # compute target descriptors & key points
            # sift = cv2.xfeatures2d.SIFT_create()
            # matcher = cv2.DescriptorMatcher_create("BruteForce")
            # des_t = compute_SIFT_des(target_img,kps_t)
            # for img in yolo_img_arr:
            #     img_out = combine_img(img,target_img)
            #     hA, wA = img.shape[:2]
            #     kps,des = sift.detectAndCompute(img,None)
            #     raw_matches = matcher.knnMatch(des,des_t,2)
            #     draw_match_line(raw_matches,img_out,wA,kps,kps_t)
            #     show_im("Yolo Data Image",img_out)
            # using compare ssim
            # for img in yolo_img_arr:
            #     w1,h1,c1 = target_img.shape
            #     w2,h2,c2 = img.shape
            #     r_target_img = cv2.resize(target_img, (max(h1,h2),max(w1,w2)) , interpolation=cv2.INTER_CUBIC)
            #     r_img = cv2.resize(img, (max(h1,h2),max(w1,w2)) , interpolation=cv2.INTER_CUBIC)
            #     show_im("Temp",np.hstack((r_target_img,r_img)))
            #     s = compare_ssim(r_target_img, r_img,multichannel=True)
            #     print(s)

    # Dector enter point
    def detector(mode,dir,is_show):
        if len(img_target_arr):
            global img_target
            temp = img_target
            for i in range(len(img_target_arr)):
                img_target = img_target_arr[i]
                show_detect_result(mode,0,is_show)
            img_target = temp
        # if ui.target_label.pixmap() == None:
        if not sum(img_target.rect):
            print("No target image.")
            change_image(1)
            draw_target_arr()
            return
        show_detect_result(mode,dir,is_show)
        draw_target_arr()

    # 如果圖片突然變大,可能是抓到兩輛車的前景,那我們從抓到的圖片找有沒有和原本圖相似的部分
    # 輸出為目標在原圖上的[x1 y1 x2 y2]
    def find_item_InBigImage(simg, bimg, next):
        print("InBigImage\n")
        maxy = bimg.shape[0] - simg.shape[0]
        maxx = bimg.shape[1] - simg.shape[1]
        h = simg.shape[0]
        w = simg.shape[1]
        result = [0.0]*5
        for i in range(maxy):
            for j in range(maxx):
                s1 = bimg[ i : i + h , j : j + w ]
                if( result[4] < compare_ssim(s1, simg, multichannel = True)):
                    result = [ (next[0] + j), (next[1] + i), (next[0] + j + w), (next[1] + i + h), compare_ssim(s1, simg, multichannel = True)]
                j += 3
            i += 3
        '''result[0] = (result[0]*2 + next[0]) / 3
        result[1] = (result[1]*2 + next[1]) / 3
        result[2] = (result[2]*2 + next[2]) / 3
        result[3] = (result[3]*2 + next[3]) / 3'''
        p1 = (int(result[0]), int(result[1]))
        p2 = (int(result[2]), int(result[3]))
        InBigImageShow = img2.img
        cv2.rectangle(InBigImageShow,p1,p2,(0,0,255), 2)
        cv2.imshow("find_item_InBigImage", InBigImageShow)
        return result[0:4]
    # Dector main function
    # display the match result in subwindows and detect result on next image
    # mode determine which match algorithm to use
    # dir is the control of direction for muitiple target
    # is_show flag determine whether the process is showed 
    def show_detect_result(mode,dir,is_show):
        # store the two kind of match result and used key point
        kps2_arr = []
        kps_t_arr = []
        matches_arr = []
        # current target image is trustable
        if not img_target.is_predict:
            # mode 0 use BF match
            if mode == 0 :
                kps2,matches,img_out = BF_target_match()
            # mode 1 use Hungarian algorithm
            elif mode == 1:
                _,_,BF_img = BF_target_match()
                kps2,matches,Hungarian_img = Hungarian_match()
                img_out = combine_img(BF_img,Hungarian_img)
            kps2_arr.append(kps2)
            kps_t_arr.append(img_target.kps)
            matches_arr.append(matches)
        # current target image isn't trustable
        # use the previous rectangle to match result
        else:
            kps2,matches,img_out,kps_t = pre_target_BF_match()
            kps2_arr.append(kps2)
            kps_t_arr.append(kps_t)
            matches_arr.append(matches)
        show_im("match result",img_out)
        # find the GMM mask contour of target
        mask = GMM(img1.img,img2.img)

        # using yolo detector data to find target
        next_rect = yolo_match(kps_t_arr,kps2_arr,matches_arr)
        # if no yolo reasonal data using tracker 
        if not sum(next_rect):
            # use mask and match restult to find the target in next image
            out_mask,next_rect = find_target_contour(kps_t_arr,kps2_arr,matches_arr,mask)
            # draw the finding result on match result image
            _,target_width,_ = img_target.img.shape
            cv2.rectangle(img_out,(int(next_rect[0] + target_width),int(next_rect[1])),(int(next_rect[2] + target_width),int(next_rect[3])),(0,255,0),thickness=1)
            # combine the match result and final GMM mask
            img_out = np.hstack((img_out,cv2.cvtColor( out_mask, cv2.COLOR_GRAY2RGB),cv2.cvtColor( mask, cv2.COLOR_GRAY2RGB)))
            # show Result
            if is_show:
                cv2.imshow("Detect Result",img_out)
            line_x = abs((next_rect[2] - next_rect[0]) / (img_target.rect[2] - img_target.rect[0]))
            line_y = abs((next_rect[3] - next_rect[1]) / (img_target.rect[3] - img_target.rect[1]))
            width = int(abs(img_target.rect[0] - img_target.rect[2]))
            height = int(abs(img_target.rect[1] - img_target.rect[3]))
            InBig_Check = 1.75
            if(width*height < 8500):
                print("InBig_Check change")
                InBig_Check = 1.3
            # The size of result doesn't meet the target using predict
            if ((next_rect[0] == 512.)&(next_rect[1] == 512.)&(next_rect[2] == 0.)&(next_rect[3] == 0.)):
                print("use motion to predict target rectangle...:", line_x*line_y)
                print_bar()
                img_target.is_predict = True
                next_rect = predict_next(mask)
            elif ((line_x*line_y > InBig_Check)&(width*height > 1000)):
                print("InBig_Check:" , InBig_Check)
                img_big = img2.img[int(next_rect[1]):int(next_rect[3]),int(next_rect[0]):int(next_rect[2])]
                next_rect = find_item_InBigImage(img_target.img, img_big, next_rect)
                img_target.is_predict = False
        else:
            img_target.is_predict = False
        # update the next target's coordinate of rectangle
        find_next_target(dir,next_rect)
        motion()
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
            result_rect = show_detect_result(0,1,False)
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
        img1.reset_drew_img()
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
        ui.Target_Button.clicked.connect(lambda: set_target_img(True))
        ui.Target_BF_Button.clicked.connect(lambda: detector(0,1,True))
        ui.Target_Hungarian_Button.clicked.connect(lambda: detector(1,1,True))
        ui.Optical_Flow_Button.clicked.connect(lambda: change_image(0))
        ui.SaveFileButton.clicked.connect(save_detect_result)
        ui.Dispaly_Button.clicked.connect(display_select_result)
        ui.Result_Left_Button.clicked.connect(lambda: change_image_with_result(-1))
        ui.Result_Right_Button.clicked.connect(lambda: change_image_with_result(1))
        ui.Image_Selector.valueChanged.connect(select_image)
        ui.KL_Chart_Button.clicked.connect(show_kl_chart)
        ui.Load_Yolo_Button.clicked.connect(set_yolo_target)

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
            if i >= img_num:
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
        for i,kp_arr in enumerate(data):
            temp_arr = []
            for point in kp_arr:
                temp = cv2.KeyPoint(x=point[0][0],y=point[0][1],_size=point[1], _angle=point[2], 
                                _response=point[3], _octave=point[4], _class_id=point[5])
                temp_arr.append(temp)
            img_kp_arr.append(temp_arr)
            if i >= img_num:
                break
        f.close()
    
    # load BF match data
    def load_BF_match():
        data_path = "data/SIFT_BF_match.txt"
        f = open(data_path,"rb")
        data = cPickle.loads(f.read())
        for i,match_arr in enumerate(data):
            temp_arr = []
            for m in match_arr:
                m1 = cv2.DMatch(m[0][0],m[0][1],m[0][2])
                m2 = cv2.DMatch(m[1][0],m[1][1],m[1][2])
                temp_arr.append((m1,m2))
            BF_match_arr.append(temp_arr)
            if i >= img_num:
                break
        f.close()
    
    # load optical flow data
    def load_optical_flow():
        data_path = "data/optical_flow.txt"
        f = open(data_path,"rb")
        data = cPickle.loads(f.read())
        for i,img in enumerate(data):
            img_optical_flow_arr.append(img)
            if i >= img_num:
                break
        f.close()
    
    # load yolo result data
    def load_yolo():
        data_path = "data/info.txt"
        f = open(data_path,"r")
        i = -1
        for data in f:
            temp = data.split(":")
            if len(temp) == 1 :
                i += 1
                yolo_data_arr.append([])
                continue
            temp = temp[1].split()
            temp = list(map(int,temp))
            yolo_data_arr[i].append([temp[0],temp[2],temp[1],temp[3]])
            if i >= img_num:
                break
        f.close()
    
    # load data
    def load_data(img_kp_arr):
        check_data_file()
        load_SIFT_kp()
        load_BF_match()
        load_optical_flow()
        load_yolo()
    
    # init image entity
    def init():
        img1.set_img(img_arr,0,img_kp_arr)
        img2.set_img(img_arr,1,img_kp_arr)

    def help_msg():
        print ("-h --help : get help information!")
        print("-d --debug : run GUI in more fast debug mode!")

    def parse_arg():
        argv = sys.argv[1:]
        try:
            opts, args = getopt.getopt(argv,"hd",["help","debug"])
        except getopt.GetoptError:
            help_msg()
            sys.exit(2)
        for opt, arg in opts:
            if opt in ("-h","--help"):
                help_msg()
                sys.exit(1)
            elif opt in("-d","--debug"):
                print("Run GUI in debug mode!")
                return 100
        return image_num()
    
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
    img_num = parse_arg()
    load_img(img_name_arr)
    load_data(img_kp_arr)
    init()
    button_fun()
    Qlabel_fun()
    Dialog.show()
    sys.exit(app.exec_())
