import numpy as np

def get_points_box(points, type='polygon', width=2):
    points = np.array(points)
    if type == 'point' and len(points) == 1:
        box = [points[0][0] - width / 2, points[0][1] - width / 2, points[0][0] + width / 2, points[0][1] + width / 2]
        return box
    if type == 'circle' and len(points) == 2:
        r = np.sqrt((points[0][0] - points[1][0]) ** 2 + (points[0][1] - points[1][1]) ** 2)
        box = [points[0][0] - r, points[0][1] - r, points[0][0] + r, points[0][1] + r]
        return box
    box = [min(points[:, 0]), min(points[:, 1]), max(points[:, 0]), max(points[:, 1])]
    print(box)



if __name__ == '__main__':
    points = [[131.0, 5890.0],
              [129.0, 5635.0],
              [133.0, 5665.0],
              [135.0, 5748.0],
              [132.0, 5835.0],
              [131.0, 5891.0],
              [128.0, 5892.0],
              [128.0, 5891.0]]
    get_points_box(points,  type='polygon')

