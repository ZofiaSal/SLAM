import numpy as np
import cv2
import sys
sys.path.append('../')
import image_processing as imp

translationX = 0
translationY = 0.5

K = np.array([
    [1000, 0, 0],
    [0, 1000, 0],
    [0, 0, 1]])

rotation0 = np.identity(3)

Rt0 = np.array([
    [1, 0, 0, 0],    
    [0, 1, 0, 0],
    [0, 0, 1, 0]])

print('tu')
print(Rt0[:3, :3])
print('tu2')
print(rotation0)

Rt0[:3, :3] = rotation0

angle1 = -np.pi/2
rotation1 = np.array([
    [np.cos(angle1), -np.sin(angle1), 0],
    [np.sin(angle1), np.cos(angle1), 0],
    [0, 0, 1]
])

Rt1 = np.array([
    [1, 0, 0, translationX],
    [0, 1, 0, translationY],
    [0, 0, 1, 0]])

Rt1[:3, :3] = rotation1

projection_matrix0 = K @ Rt0
projection_matrix1 = K @ Rt1

sample3DPoint = np.array([1, 2, 0.3, 1]).T

def projectionTo2D(projection_matrix, point):
    a = projection_matrix @ point
    a /= a[-1]
    return a[:-1]

pixels1 = np.array([projectionTo2D(projection_matrix0, sample3DPoint)])
pixels2 = np.array([projectionTo2D(projection_matrix1, sample3DPoint)])

result = imp.calculatePoints3D(
    pixels1,
    pixels2,
    [translationX, translationY, -angle1],
    K)

print(result)
