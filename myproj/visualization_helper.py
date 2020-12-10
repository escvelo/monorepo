import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from helpers import homogeneous_coord
import cv2
def visualize_points( Actual_Pts, Project_Pts):
    plt.figure()

    plt.plot(Actual_Pts[:,0],Actual_Pts[:,1],'ro', label = 'Actual points')
    plt.plot(Project_Pts[:,0],Project_Pts[:,1], '+', label = 'Projected points')
    plt.legend()
    

def plot3Dview(Points_3D, camera_center):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(Points_3D[:,0], Points_3D[:,1], Points_3D[:,2], s=30,marker='o')
    C = camera_center
    ax.scatter(C[0], C[1], C[2], s=30,c='r',marker='+')
    zmin = np.min(Points_3D[:,-1])
    zmax = np.max(Points_3D[:,-1])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_zlim(zmin, zmax)
    for p in np.vstack((Points_3D,C)):
        pts= np.vstack((p,[p[0],p[1],zmin]))
        ax.plot(pts[:,0], pts[:,1], pts[:,2])

def plot_epipolarLine(axes, epipolar_line, left_line, right_line, Img):
    PL = np.cross(epipolar_line.flatten(), left_line)
    PR = np.cross(epipolar_line.flatten(), right_line)
    x = [PL[0]/PL[2], PR[0]/PR[2]]
    y = [PL[1]/PL[2], PR[1]/PR[2]]
    plt.xlim([0,Img.shape[1]])
    plt.ylim([Img.shape[0],0])
    axes.plot(x, y)

def draw_epipolar_lines(F_matrix, ImgLeft, ImgRight, PtsLeft, PtsRight):
    fig = plt.figure()
    ax = fig.add_subplot(122)
    Pul = [1,1,1]
    Pbl = [1, ImgLeft.shape[0], 1]
    Pur=[ImgLeft.shape[1], 1, 1]
    Pbr = [ImgLeft.shape[1], ImgLeft.shape[0], 1]

    lL = np.cross(Pul, Pbl)
    lR = np.cross(Pur,Pbr)
    ax.imshow(ImgRight)
    for i in range(PtsRight.shape[0]):
        e = np.dot(F_matrix, np.transpose(homogeneous_coord(PtsLeft[i])))
        plot_epipolarLine(ax, e, lL, lR, ImgLeft)
    ax = fig.add_subplot(121)
    ax.imshow(ImgLeft)
    for i in range(PtsRight.shape[0]):
        e = np.dot(np.transpose(F_matrix), np.transpose(homogeneous_coord(PtsRight[i])))
        plot_epipolarLine(ax, e, lL, lR, ImgLeft)

def show_correspondences(imgA_bgr, imgB_bgr, ptA, ptB, title = None, n_disp_pts = None):
    if n_disp_pts is not None:
        if n_disp_pts < ptA.shape[0]:
            indexes = np.random.permutation(n_disp_pts)
            ptA = ptA[indexes]
            ptB = ptB[indexes]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    h1, w1 = imgA_bgr.shape[:2]
    h2, w2 = imgB_bgr.shape[:2]
    view = np.zeros((max(h1, h2), w1 + w2, 3), np.uint8)
    view[:h1, :w1, :] = imgA_bgr  
    view[:h2, w1:, :] = imgB_bgr
    view[:, :, 1] = view[:, :, 0]  
    view[:, :, 2] = view[:, :, 0]
    #import ipdb; ipdb.set_trace()
    ax.imshow(view)
    for i in range(ptA.shape[0]):
        # draw the keypoints
    # print m.queryIdx, m.trainIdx, m.distance
        color = tuple([np.random.randint(0, 255) for _ in range(3)])
        A,B = ptA[i], ptB[i]
        #cv2.line(view, (int(A[0]), int(A[1])) , (int(B[0] + w1), int(B[1])), color)
        ax.plot([int(A[0]), int(B[0]) + w1], [int(A[1]), int(B[1])])
    ax.scatter(ptA[:,0], ptA[:,1])
    ax.scatter(ptB[:,0] + w1,ptB[:,1])
    if title is not None:
        ax.set_title(title)
    else:
        ax.set_title('correspondances')
    ax.axis('off')
    
def show_imgsLeftRight(imgA_bgr, imgB_bgr, title = None):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    h1, w1 = imgA_bgr.shape[:2]
    h2, w2 = imgB_bgr.shape[:2]
    view = np.zeros((max(h1, h2), w1 + w2, 3), np.uint8)
    view[:h1, :w1, :] = imgA_bgr  
    view[:h2, w1:, :] = imgB_bgr
    view[:, :, 1] = view[:, :, 0]  
    view[:, :, 2] = view[:, :, 0]
    #import ipdb; ipdb.set_trace()
    ax.imshow(view)
    if title is not None:
        ax.set_title(title)
    else:
        ax.set_title('correspondances')
    ax.axis('off')

def show_cornerpoints(imgA_bgr, imgB_bgr, ptA, ptB, title = None, n_disp_pts = None):
    if n_disp_pts is not None:
        if n_disp_pts < ptA.shape[0]:
            indexes = np.random.permutation(n_disp_pts)
            ptA = ptA[indexes]
            ptB = ptB[indexes]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    h1, w1 = imgA_bgr.shape[:2]
    h2, w2 = imgB_bgr.shape[:2]
    view = np.zeros((max(h1, h2), w1 + w2, 3), np.uint8)
    view[:h1, :w1, :] = imgA_bgr  
    view[:h2, w1:, :] = imgB_bgr
    view[:, :, 1] = view[:, :, 0]  
    view[:, :, 2] = view[:, :, 0]
    #import ipdb; ipdb.set_trace()
    ax.imshow(view)
    ax.scatter(ptA[:,0], ptA[:,1], c = 'r')
    ax.scatter(ptB[:,0] + w1,ptB[:,1], c = 'g')
    if title is not None:
        ax.set_title(title)
    else:
        ax.set_title('correspondances')
    ax.axis('off')

def rgb2gray(arr):
    return cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)

def imfuse(imgA_uint8,imgB_uint8, show=True):
    imgA_ = rgb2gray(imgA_uint8) # Read first frame into imgA
    imgB_ = rgb2gray(imgB_uint8) # Read second frame into imgB
    C = np.dstack((imgB_,imgA_,imgB_))
    #cv2.imshow("imfuse",C)
    #cv2.waitKey(0)
    #if show:
     #   cv2.imshow(C)
    return C