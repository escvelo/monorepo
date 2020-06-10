
"""
    References
        [1] Tordoff, B; Murray, DW. "Guided sampling and consensus for motion estimation." European Conference n Computer Vision, 2002.
        [2] Lee, KY; Chuang, YY; Chen, BY; Ouhyoung, M. "Video Stabilization using Robust Feature Trajectories." National Taiwan University, 2009.
        [3] Litvin, A; Konrad, J; Karl, WC. "Probabilistic video stabilization using Kalman filtering and mosaicking." IS&T/SPIE Symposium on Electronic Imaging, Image and Video Communications and Proc., 2003.
        [4] Matsushita, Y; Ofek, E; Tang, X; Shum, HY. "Full-frame Video Stabilization." Microsoft® Research Asia. CVPR 2005. 
"""


from visualization_helper import visualize_points, plot3Dview, draw_epipolar_lines, show_correspondences, show_imgsLeftRight, show_cornerpoints
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


#cap = cv2.VideoCapture(filename)
ImgLeft = Image.open('./data/picLeft.jpg')
ImgRight = Image.open('./data/picRight.jpg')
#tform = AffineTransform(scale=(0.9, 0.9), rotation=0.2, translation=(20, -10))
#ImgLeft = np.array(ImgLeft.resize(newsize, Image.BILINEAR))
#ImgRight= np.array(ImgRight.resize(newsize, Image.BILINEAR))
#ImgRight = warpImg(tform, ImgLeft)
ImgLeft = np.array(ImgLeft)
ImgRight = np.array(ImgRight)

model_robust, Points_Left, Points_Right, inliers, outliers = estimateStabTform(ImgLeft, ImgRight)
model_robust = convertTGenAffineToSRT(model_robust)
#import ipdb; ipdb.set_trace()
ImgRight_corrected = warpImg(model_robust, ImgRight)
ImgRight_corrected = np.array(ImgRight_corrected)

# print("Ground truth:")
# print(f"Scale: ({tform.scale[1]:.4f}, {tform.scale[0]:.4f}), "
#       f"Translation: ({tform.translation[1]:.4f}, "
#       f"{tform.translation[0]:.4f}), "
#       f"Rotation: {-tform.rotation:.4f}")
# print("Affine transform:")
# print(f"Scale: ({model.scale[0]:.4f}, {model.scale[1]:.4f}), "
#       f"Translation: ({model.translation[0]:.4f}, "
#       f"{model.translation[1]:.4f}), "
#       f"Rotation: {model.rotation:.4f}")
print("RANSAC:")
print(f"Scale: ({model_robust.scale[0]:.4f}, {model_robust.scale[1]:.4f}), "
      f"Translation: ({model_robust.translation[0]:.4f}, "
      f"{model_robust.translation[1]:.4f}), "
      f"Rotation: {model_robust.rotation:.4f}")





#import ipdb; ipdb.set_trace()
show_imgsLeftRight(ImgLeft, ImgRight, title='dest frame (right) rotated/translated/scaled')
show_imgsLeftRight(ImgLeft, ImgRight_corrected, title='dest frame corrected')
show_cornerpoints(ImgLeft, ImgRight, Points_Left[inliers], Points_Right[inliers], title='corners detected', n_disp_pts=10)
show_correspondences(ImgLeft, ImgRight, Points_Left[inliers], Points_Right[inliers], title='inlier correspondences', n_disp_pts = 20)
show_correspondences(ImgLeft, ImgRight, Points_Left[outliers], Points_Right[outliers], title='outlier correspondences', n_disp_pts = 20)
#F_matrix = estimate_normalized_fundamental_matrix(Points_Left[inliers], Points_Right[inliers])
#draw_epipolar_lines(F_matrix, ImgLeft, ImgRight, Points_Left[inliers][0:10], Points_Right[inliers][0:10])
plt.show()