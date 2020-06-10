
import numpy as np
import cv2
def homogeneous_coord(points):
    if points.ndim == 1:
        points = points[None, :]
    ones = np.ones(points.shape[0])[:,None]
    return np.hstack((points,ones))

def nonhomogeneous_coord(points):
    if points.ndim == 1:
        points = points[None, :]
    points =  points / points[:,-1][:,None]
    return points[:,:-1]

def upsample(arr, n=2, phase = 0):
    '''
    @args
        n increases the sample rate of arr by inserting 
             n – 1 zeros between samples
        phase: specifies the number of samples by which to offset 
                  the upsampled sequence. currently only 0 and 1 supported

    @return upsampled array
    '''
    if phase > 1:
        raise ('pahse greater than 1 not supported')
    rows, cols = arr.shape
    out = np.zeros((rows * n,cols))
    if phase:
        row_indexes = np.array(range(0,out.shape[0], 2))
    else:
        row_indexes = np.array(range(1,out.shape[0]+1, 2))
    out[row_indexes,:] = arr
    return out

def bgr2gray(arr):
    return cv2.cvtColor(arr, cv2.COLOR_BGR2GRAY)