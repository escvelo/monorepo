
"""
    References
        [1] Tordoff, B; Murray, DW. "Guided sampling and consensus for motion estimation." European Conference n Computer Vision, 2002.
        [2] Lee, KY; Chuang, YY; Chen, BY; Ouhyoung, M. "Video Stabilization using Robust Feature Trajectories." National Taiwan University, 2009.
        [3] Litvin, A; Konrad, J; Karl, WC. "Probabilistic video stabilization using Kalman filtering and mosaicking." IS&T/SPIE Symposium on Electronic Imaging, Image and Video Communications and Proc., 2003.
        [4] Matsushita, Y; Ofek, E; Tang, X; Shum, HY. "Full-frame Video Stabilization." Microsoft® Research Asia. CVPR 2005. 
"""


from visualization_helper import visualize_points, plot3Dview, draw_epipolar_lines, show_correspondences, show_imgsLeftRight, show_cornerpoints, imfuse
from estimate_fundamental_matrix import estimate_normalized_fundamental_matrix
from transform_helper import convertTGenAffineToSRT, estimateStabTform, warpImg
import matplotlib.pyplot as plt
import numpy as np
import re
import cv2
from PIL import Image
import imshowpair
import numpy as np
from skimage.transform import resize, AffineTransform, warp
from skimage.measure import ransac


def readFrame():
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame

filename = './data/shaky2.mp4'
cap = cv2.VideoCapture(filename)
#cap = cv2.VideoCapture(filename)
#ImgLeft = Image.open('./data/picLeft.jpg')
#ImgRight = Image.open('./data/picRight.jpg')
totalFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
ImgLeft = readFrame()
#ImgRight = readFrame()

correctedMean = ImgLeft
ii = 40
Hcumulative = np.eye(3)
# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
out = cv2.VideoWriter('./data/corrected_shaky2.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))

frame = cv2.cvtColor(ImgLeft, cv2.COLOR_RGB2BGR)
out.write(frame)
print(totalFrames)

for i in range(totalFrames-1):
    print(i)
    ii = ii - 1
    if ii == 0:
        break
    ImgRight = readFrame()
    H, Points_Left, Points_Right, inliers, outliers = estimateStabTform(ImgLeft, ImgRight)
    HsRt = convertTGenAffineToSRT(H)
    Hcumulative = np.dot(HsRt.params, Hcumulative)
    model_robust = AffineTransform(Hcumulative)
    mo = convertTGenAffineToSRT(model_robust)
    print(f"Scale: ({model_robust.scale[0]:.4f}, {model_robust.scale[1]:.4f}), "
        f"Translation: ({model_robust.translation[0]:.4f}, "
        f"{model_robust.translation[1]:.4f}), "
        f"Rotation: {model_robust.rotation:.4f}")
    frame = warpImg(model_robust, ImgRight)
    
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    #frame = imfuse(ImgLeft, ImgRight)
    out.write(frame)
    ImgLeft = ImgRight
    # plt.figure(1); plt.clf()
    # print(ImgRight.shape)
    # plt.imshow(ImgRight)
    # plt.title('Number ' + str(ii))
    # plt.pause(3)
    
    #show_imgsLeftRight(ImgLeft, ImgRight, title='dest frame corrected')
    
    #plt.show()

out.release()
cap.release()
cv2.destroyAllWindows()

