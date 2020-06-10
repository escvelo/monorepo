from helpers import homogeneous_coord, nonhomogeneous_coord
import numpy as np
from estimate_proj_matrix import Project_3d_to_2d

def evaluate_points( M, points_2d, points_3d):
    proj_2d = Project_3d_to_2d( M, points_2d, points_3d) 
    u, v = proj_2d[:,0], proj_2d[:,1]
    residual = np.sum(((u-points_2d[:,0])**2+(v-points_2d[:,1])**2)**0.5)

    return residual, proj_2d