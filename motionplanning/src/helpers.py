from custom_types import Point2D

def Point2D_to_tuple_list(point2D_list):
    mat = []
    for pt in point2D_list:
        mat.append(pt.toTuple())
    return mat 
def Point2D_to_x_y_list(point2D_list):
    x, y = [], []
    for pt in point2D_list:
        x.append(pt.x)
        y.append(pt.y)
    return x, y