from gettext import translation
import numpy as np
import cv2
import find_matches_with_superglue as matches

intrinsic = np.matrix([[1.10137417e+03, 0.00000000e+00, 2.89506647e+02],
 [0.00000000e+00, 1.07474733e+03, 1.84718234e+02],
 [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]],float)

distortion = np.matrix([[ 2.33589358e+00, -6.07874111e+01, -2.29399415e-02,  8.79756112e-02, -1.45708167e-01]], float)


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
    rotation1 = np.identity(4)
    rotation1[:3, :3] = getRotationsInXY(-distance[2]) # with minus ?
    rotation2 = np.identity(4)

    translation1 = np.identity(4)
    translation1[:2, 3] = [value * -1 for value in distance] [:2]
    translation2 = np.identity(4)

    extrinsic1 = np.linalg.inv(rotation1 @ translation1)
    extrinsic2 = np.linalg.inv(rotation2 @ translation2)

    # remove last row of Extrinsic -> (3,4)
    extrinsic1 = extrinsic1[:-1, :]
    extrinsic2 = extrinsic2[:-1, :]

    projectionMatrix1 = intrinsic @ extrinsic1
    projectionMatrix2 = intrinsic @ extrinsic2

    return cv2.triangulatePoints(projectionMatrix1, projectionMatrix2, points1[:,:15], points2[:,:15])

    

def main():
    (points1, points2) = matches.find_matches()
    X = calculatePoints3D(points1.T,points2.T,[5,0,0])
    X //= X[3]
    print(X.T)


if __name__ == '__main__':
    main()