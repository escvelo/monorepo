import numpy as np
from helpers import homogeneous_coord, upsample, nonhomogeneous_coord
from visualization_helper import visualize_points

def calculate_projection_matrix(Points_2D, Points_3D):
 
    # To solve for the projection matrix. You need to set up a system of
    # % equations using the corresponding 2D and 3D points:

    # %                                                     [M11       [ u1
    # %                                                      M12         v1
    # %                                                      M13         .
    # %                                                      M14         .
    # %[ X1 Y1 Z1 1 0  0  0  0 -u1*X1 -u1*Y1 -u1*Z1          M21         .
    # %  0  0  0  0 X1 Y1 Z1 1 -v1*X1 -v1*Y1 -v1*Z1          M22         .
    # %  .  .  .  . .  .  .  .    .     .      .          *  M23   =     .
    # %  Xn Yn Zn 1 0  0  0  0 -un*Xn -un*Yn -un*Zn          M24         .
    # %  0  0  0  0 Xn Yn Zn 1 -vn*Xn -vn*Yn -vn*Zn ]        M31         .
    # %                                                      M32         un
    # %                                                      M33         vn ]
    # % AM = b (solve for M, using regresssion)

    Points_3D = homogeneous_coord(Points_3D)
    a1 = upsample(Points_3D, 2,1)
    a2 = upsample(Points_3D,2)
    a3 = a1 + a2
    a3 = a3[:,:-1]

    b1 = upsample(Points_2D[:,0][:,None],2,1)
    b2 = upsample(Points_2D[:,1][:,None],2)
    b3= b1 + b2
    b4= np.repeat(b3,3, axis=1)
    b5 = np.multiply(-b4 , a3)
    A = np.hstack((a1, a2, b5))
    b=b3
    M= np.dot(np.linalg.pinv(A),b)
    return np.vstack((M,1)).reshape((3,4))

def Project_3d_to_2d( M, points_2d, points_3d):
    projection = np.transpose(np.dot(M, np.transpose(homogeneous_coord(points_3d))))
    proj_2d = nonhomogeneous_coord(projection) 
    u, v = proj_2d[:,0], proj_2d[:,1]
    Projected_2D_Pts = np.hstack((u[:,None], v[:,None]))
    return Projected_2D_Pts


def compute_camera_center(M):
    Rot = M[:3,:3]
    translation = M[:,-1]
    return - np.dot(np.linalg.inv(Rot), translation)
