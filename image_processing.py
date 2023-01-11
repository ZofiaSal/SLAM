from gettext import translation
import numpy as np
import cv2
import find_matches_with_superglue as matches

# intrinsic = np.matrix([[1.10137417e+03, 0.00000000e+00, 2.89506647e+02],
#  [0.00000000e+00, 1.07474733e+03, 1.84718234e+02],
#  [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]],dtype = np.float64)

# distortion = np.matrix([[ 7.46597504e-01,  7.89619631e+01, -2.26703831e-02,  1.18290186e-01,
#   -3.06426901e+03]], dtype = np.float64)

intrinsic = np.matrix([[915.18878362,   0.,         239.58328874],
 [  0.,         911.09442479, 194.90084703],
 [  0.,          0.,           1.        ]], dtype = np.float64)

distortion = np.matrix([[-4.36931096e-01,  2.52126992e+00, -7.28634641e-03, -5.15932592e-03,
  -2.62649369e+01]], dtype = np.float64)

def getRotationsInXY(angle):
    Rz = np.zeros(shape = (3, 3))
    Rz[0, 0] = np.cos(angle)
    Rz[0, 1] = -np.sin(angle)
    Rz[1, 0] = np.sin(angle)
    Rz[1, 1] = np.cos(angle)
    Rz[2, 2] = 1
    
    return Rz

# points1 - characteristic points from first picture 
# points2 - characteristic points for corresponding points from picture two
# distance - the change from where picture 1 was taken to where picture 2 was taken [x,y,alpha] where a lpha is rotation in XY
def calculatePoints3D(points1, points2, distance):
    
    #calculate extrinsic matrix
    rotation1 = np.identity(4, dtype = np.float64)
    rotation1[:3, :3] = getRotationsInXY(-distance[2]) # with minus ?
    rotation2 = np.identity(4, dtype = np.float64)

    translation1 = np.identity(4, dtype = np.float64)
    translation1[:2, 3] = [value * -1 for value in distance] [:2]
    translation2 = np.identity(4, dtype = np.float64)

    extrinsic1 = np.linalg.inv(rotation1 @ translation1)
    extrinsic2 = np.linalg.inv(rotation2 @ translation2)

    # remove last row of Extrinsic -> (3,4)
    extrinsic1 = extrinsic1[:-1, :]
    extrinsic2 = extrinsic2[:-1, :]

    projectionMatrix1 = intrinsic @ extrinsic1
    projectionMatrix2 = intrinsic @ extrinsic2

    points_undist1 = cv2.undistortPoints(points1.astype(np.float64), intrinsic, distortion)
    points_undist2 = cv2.undistortPoints(points2.astype(np.float64), intrinsic, distortion)
    
    print(points_undist1)
    print(points_undist2)
    return cv2.triangulatePoints(projectionMatrix1, projectionMatrix2, points1.astype(np.float64).T, points2.astype(np.float64).T)

    

def main():
    (points1, points2) = matches.find_matches()
    print(points1, points2)
    X = calculatePoints3D(points1[:10,:],points2[:10,:],[5.0,0.0,0.0])
    X = cv2.convertPointsFromHomogeneous(X.T)
    print(X)


if __name__ == '__main__':
    main()