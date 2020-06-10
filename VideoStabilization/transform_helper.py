from extract_features import detectFASTFeatures

import cv2
import numpy as np
from PIL import Image
from skimage.transform import resize, AffineTransform, warp
from skimage.measure import ransac

def convertTGenAffineToSRT(Trafo_aff):
    """ 
    @param arg1: generat affine transform, data type is the matrix returned by 
                 AffineTransform(mat)
    @return: scale, rotation and tranlation equivalent.
    
    @brief
      Input is the matrix defining generalized affine transform. For numerical 
      stability we convert it into only matrix defining only scale, rotation and 
      translation equivalent. The new matrix will look like:
          |s*cos(ang)   s*sin(ang)  t_x|
          |s*-sin(ang)  s*cos(ang)  t_y|
          |   0            0         1 |
    """
    
    # Extract scale and rotation sub-matrix
    H = Trafo_aff.params
    R= H[:-1,:-1]
    # compute mean theta using 
    theta = np.mean([np.arctan2(R[0,1],R[0,0]), np.arctan2(-R[1,0], R[1,1])])
    scale = np.mean(np.diagonal(R)/np.cos(theta))
    t = H[:,-1][:-1]
    HsRt = np.array([[scale*np.cos(theta)  ,  scale* np.sin(theta),   t[0]], \
                     [scale *-np.sin(theta),  scale * np.cos(theta),  t[1]], \
                     [       0,               0,                        1]])
    return AffineTransform(HsRt)

def estimateStabTform(imgA, imgB):
    """
    @param arg1: input numpy image array at t frame in video sequence. 
    @param arg2: input numpy image array at t+1 frame in video sequence.
    
    @return: 
        Tranform: stabilized genrelized affine transform of form
          |a_0  a_2  t_x|
          |a_1  a_3  t_y|
          | 0    0    1 |
    parameter a_* define scale, rotation and shear and t_* represents translations.
        PointsLeft: Corner points in arg1. For visualization.
        PointsRight: Corner points in arg2. For visualization.
        inliers: clean correspondence from PointsLeft to PointsRight
        outliers: not clean correspondence from PointsLeft and PointsRight
    """

    PointsA, image_corner_ptsA = detectFASTFeatures(imgA, threshold=20)
    PointsB, image_corner_ptsB = detectFASTFeatures(imgB, threshold=20)
    freakExtractor = cv2.xfeatures2d.FREAK_create()
    pointsA,descriptorsA= freakExtractor.compute(imgA, PointsA)
    pointsB,descriptorsB= freakExtractor.compute(imgB, PointsB)

    # create BFMatcher object
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    # Match descriptors.
    matches = bf.match(descriptorsA,descriptorsB)

    A, B= [], []
    matches = sorted(matches, key = lambda x:x.distance)
    sel_matches = matches
    for m in sel_matches:
        A.append(list(pointsA[m.queryIdx].pt))
        B.append(list(pointsB[m.trainIdx].pt))
    Points_Left = np.array(A)
    Points_Right = np.array(B)

    model = AffineTransform()
    model.estimate(Points_Left, Points_Right)

    model_robust, inliers = ransac((Points_Right, Points_Left), AffineTransform, min_samples=3,
                                residual_threshold=2, max_trials=100)

    outliers = inliers == False

    return model_robust, Points_Left, Points_Right, inliers, outliers


def warpImg(tform, Img, newsize= None):
    if isinstance(Img, np.ndarray):
        newsize = Img.shape
        Img = Image.fromarray(Img)    
    if newsize is None:
        img_warped = warp(Img, tform.inverse, output_shape=newsize)
    else:
        img_warped = warp(Img, tform.inverse, output_shape=newsize)
    max_val = np.max(img_warped)
    #import ipdb; ipdb.set_trace()
    if max_val:
        img_warped = img_warped / max_val
    img_warped = 255 * img_warped
    img_warped = img_warped.astype(np.uint8)
    return img_warped
