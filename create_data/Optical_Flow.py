from Class.image import *

def draw_dense_flow(img, flow):
    # Creates an image filled with zero intensities with the same dimensions as the frame
    mask = np.zeros_like(img)
    # Sets image saturation to maximum
    mask[..., 2] = 255
    # Computes the magnitude and angle of the 2D vectors
    magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    # Sets image hue according to the optical flow direction
    mask[..., 0] = angle * 180 / np.pi / 2
    # Sets image value according to the optical flow magnitude (normalized)
    mask[..., 1] = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
    # Converts HSV to RGB (BGR) color representation
    rgb = cv2.cvtColor(mask, cv2.COLOR_HSV2BGR)
    return rgb

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
    img_gray_arr.append(img_gray)
    i += 1
    #speed up for debug
    if i >= image_num():
        break
# optical flow
pre_gray = img_gray_arr[0]
f = open("data/optical_flow.txt","wb")
optical_flow_arr = []
print("Creating optical_flow.txt")
for i in range(0,len( img_gray_arr )) :
    gray = img_gray_arr[i]
    flow = cv2.calcOpticalFlowFarneback(pre_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    pre_gray = gray
    img = draw_dense_flow(img_arr[i],flow)
    optical_flow_arr.append(img)
    sys.stdout.write("\rprogress:\t{}/{}".format((i+1),len(img_arr)))
    sys.stdout.flush()
# save the result image to txt file
if not os.path.isdir("data/"):
    os.mkdir("data/")
f.write(cPickle.dumps(optical_flow_arr))
f.close()
print("\nDown")