
import cv2
import numpy as np

def detectFASTFeatures(imgA_uint8, threshold=30):
    fast = cv2.FastFeatureDetector_create(threshold)
    keypoints_with_nonmax = fast.detect(imgA_uint8, None)
    image_with_nonmax = np.copy(imgA_uint8)
    cv2.drawKeypoints(imgA_uint8, keypoints_with_nonmax, image_with_nonmax,color=(0,255,0), flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    #plt.show()
    return keypoints_with_nonmax, image_with_nonmax