from Class.image import *
#show the image until user press any key to continue
def show_im(name,im):
    cv2.imshow(name,im)
    # press any key to close the window
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# To store all images in folder "im0"
img_arr = []
img_gray_arr = []
img_out = []
# read the folder
dir_path = "im0/"
dir = os.listdir( dir_path)
dir.sort(key = len)
i = 0
for filename in dir :
    img = cv2.imread(dir_path + filename)
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #store image 
    img_arr.append(img)
    i += 1
    #speed up for debug
    if i >= image_num():
        break
#SIFT
sift = cv2.xfeatures2d.SIFT_create()
f = open("data/SIFT_kp.txt","wb")
img_kp_arr = []
print("Creating SIFT_kp.txt")
for i in range(0,len( img_arr)) :
    #extract key point & descriptor of courrent image's foreground and previous image
    kp1,des1 = sift.detectAndCompute(img_arr[i],None)
    kp_arr = []
    for point in kp1:
        temp = (point.pt, point.size, point.angle, point.response, point.octave, point.class_id)
        kp_arr.append(temp)
    img_kp_arr.append(kp_arr)
    sys.stdout.write("\rprogress:\t{}/{}".format((i+1),len(img_arr)))
    sys.stdout.flush()
# save key points to txt file
if not os.path.isdir("data/"):
    os.mkdir("data/")
f.write(cPickle.dumps(img_kp_arr))
f.close()
print("\nDown")