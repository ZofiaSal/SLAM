from ctypes import cdll
lib = cdll.LoadLibrary('./libcalibration.so')
  
class Calibration(object):
    def __init__(self):
        self.obj = lib.Calibration_new()
  
    def myCalibration(self):
        lib.Calibration_myCalibration(self.obj)
  
f = Calibration()
f.myCalibration()


import numpy as np
import sys
sys.path.append('./')
import photos_from_realsense.description as desc

print( "\n\n\n PART 1:")

A = []
b = []

len = 0
for point in desc.points2D_im1:
    A.append(desc.points3D[point[0]])
    b.append(point[1][0])
    len += 1

A = np.array(A)
b = np.array(b)

x, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
x = np.array([round(xi, 5) for xi in x])

print("1. Solution for A:"); print(A); print(" b: "); print(b); print(" is:")
print(x)

print("\n\n\n checker")
for i in range(len):
    b1 = A[i] @ x
    print(round(b1, 0), end = ' ')
print()
for i in range(len):
    print(round(desc.points2D_im1[i][1][0] + 0.1, 0), end = ' ')
print()
for i in range(len):
    b1 = A[i] @ x
    print(abs(round(b1, 0) - round(desc.points2D_im1[i][1][0] + 0.1, 0)), end = ' ')



##############################################################################

print( "\n\n\n PART 2:")

A = []
b = []
for point in desc.points2D_im1:
    A.append(desc.points3D[point[0]])
    b.append(point[1][1])


A = np.array(A)
b = np.array(b)

x, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
x = np.array([round(xi, 5) for xi in x])

print("2. Solution for A:"); print(A); print(" b: "); print(b); print(" is:")
print(x)

print("\n\n\n checker")
for i in range(len):
    b1 = A[i] @ x
    print(round(b1, 0), end = ' ')
print()
for i in range(len):
    b1 = A[i] @ x
    print(round(desc.points2D_im1[i][1][1] + 0.1, 0), end = ' ')
print()
for i in range(len):
    b1 = A[i] @ x
    print(abs(round(b1, 0) - round(desc.points2D_im1[i][1][1] + 0.1, 0)), end = ' ')

##############################################################################

print( "\n\n\n PART 3:")

A = []
b = []
for point in desc.points2D_im1:
    A.append(desc.points3D[point[0]])
    b.append(1)


A = np.array(A)
b = np.array(b)

x, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
x = np.array([round(xi, 5) for xi in x])


print("3. Solution for A:"); print(A); print(" b: "); print(b); print(" is:")
print(x)

##############################################################################

print("\n\n\n checker")
for i in range(len):
    b1 = A[i] @ x
    print(round(b1, 0), end = ' ')
print()
