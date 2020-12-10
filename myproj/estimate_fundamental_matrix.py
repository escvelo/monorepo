import numpy as np
from helpers import homogeneous_coord, upsample, nonhomogeneous_coord

def normalization_matrix(points):
    mean = np.mean(points, axis=0)
    centered = points - mean[None, :]
    variance = np.var(centered, axis = 0)
    std_deviation = np.sqrt(variance)
    prec = 1/ std_deviation
    S =    np.array([[prec[0],  0,        0   ], \
                     [  0,   prec[1],     0   ], \
                     [  0,      0,        1   ]])
    M =    np.array([[  1,      0,    -mean[0]], \
                     [  0,      1,    -mean[1]], \
                     [  0,      0,       1    ]])
    return np.dot(S,M)
def estimate_normalized_fundamental_matrix(points_a, points_b):
    Ta = normalization_matrix(points_a)
    points_a = homogeneous_coord(points_a)
    normalized_pt_a = np.transpose(np.dot(Ta, np.transpose(points_a)))

    Tb = normalization_matrix(points_b)
    points_b = homogeneous_coord(points_b)
    normalized_pt_b = np.transpose(np.dot(Tb, np.transpose(points_b)))

    a1 = normalized_pt_a
    a1_u = a1 * normalized_pt_b[:,0][:,None]
    a1_v = a1 * normalized_pt_b[:,1][:,None]
    A = np.hstack((a1_u, a1_v, a1))
    
    U, S, Vh = np.linalg.svd(A)

    f = Vh[-1,:]
    F = np.transpose(f.reshape((3,3)))
    
    F_matrix = np.dot(np.dot(np.transpose(Tb) , F), Ta)
    return F_matrix