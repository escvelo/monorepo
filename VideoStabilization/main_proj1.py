
from estimate_proj_matrix import calculate_projection_matrix, compute_camera_center
from evaluate_points import evaluate_points
from visualization_helper import visualize_points, plot3Dview
import matplotlib.pyplot as plt
import numpy as np
import re
def read_lines(filename):
    with open(filename,'r') as f :
        all_lines = ''.join( f.readlines() )
    values = np.array( re.findall('[\d.E+-]+', all_lines), float)
    return values, len(values)

arr, num = read_lines('./data/pts2d-pic_b.txt')
Points_2D = arr.reshape((int(num/2),2)) 
arr, num = read_lines('./data/pts3d.txt')
Points_3D = arr.reshape((int(num/3),3))

M = calculate_projection_matrix(Points_2D, Points_3D)
residual, Projected_2D_Pts= evaluate_points(M, Points_2D, Points_3D)
print(f"Residual: {residual}")
visualize_points(Points_2D,Projected_2D_Pts)
camera_center = compute_camera_center(M)
plot3Dview(Points_3D, camera_center)
plt.show()