import numpy as np
import cv2
import sys
sys.path.append('../')
import image_processing.image_processing as imp

translationX = 1.
translationY = 1.
angle1 = np.pi/4
print(f'kosinus {np.cos(angle1)}')
sample3DPoint = np.array([5., 2., 0.5, 1.]).T

K = np.array([
    [1000., 5., 200.],
    [0., 1000., 200.],
    [0., 0., 1.]], dtype = np.float64)

rotation0 = np.identity(3)

Rt0 = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0]], dtype = np.float64)

print('tu')
print(Rt0[:3, :3])
print('tu2')
print(rotation0)

Rt0[:3, :3] = rotation0

rotation1 = np.array([
    [np.cos(angle1), np.sin(angle1), 0],
    [-np.sin(angle1), np.cos(angle1), 0],
    [0, 0, 1]
], dtype = np.float64)

Rt1 = np.array([
    [1, 0, 0, -translationX],
    [0, 1., 0, -translationY],
    [0, 0, 1., 0]], dtype = np.float64)

Rt1[:3, :3] = rotation1

print('tu3')
print(Rt1)

projection_matrix0 = K @ Rt0
print(f'projection:\n {projection_matrix0}')
projection_matrix1 = K @ Rt1

def projectionTo2D(projection_matrix, point):
    a = projection_matrix @ point
    print(f'aaa: {a}')
    a /= a[-1]
    return a[:-1]

pixels1 = np.array([projectionTo2D(projection_matrix0, sample3DPoint)])
pixels2 = np.array([projectionTo2D(projection_matrix1, sample3DPoint)])

result = imp.calculatePoints3D(
    pixels1,
    pixels2,
    [translationX, translationY, angle1],
    K).T[0]

print(result)

def fromHomogenous(point):
    return (point / point[-1])[:-1]

result = fromHomogenous(result)

print(result)


