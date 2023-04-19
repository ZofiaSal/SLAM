import subprocess
import numpy as np
import os
import cv2

# OUR FINAL CAMERA CALIBRATION MATRIX
calibration = 0.6442544274536695
cameraMatrix = np.array([[932.35252209,   0.,         657.24325896],
 [  0.,         930.23581552, 357.42939289],
 [  0.,           0.,           1.        ]])
distCoeffs = np.array([[ 1.76279343e-01, -6.07952723e-01, -4.64176532e-04, -4.96839648e-04, 6.04867450e-01]])

HOW_MANY_POINTS_DEFAULT = 1000

directory_path = './test_data_sets/' + data_set + '/pairs_data/'
PATHS = [os.path.join(directory_path, f) 
         for f in sorted(os.listdir(directory_path)) 
         if f.endswith('.npz')]

# points1 - characteristic points from first picture 
# points2 - characteristic points for corresponding points from picture two
# movement - the change from where picture 1 was taken to where picture 2 was taken [x,z,alpha] where alpha is a clockwise rotation in XY
def triangulatePoints(points1, points2, movement, intrinsicCamera = cameraMatrix):
    angle = movement[2]

    # R[I|-C]
    extrinsicCamera1 = [[1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 1, 0]]

    extrinsicCamera2 = [[np.cos(angle),     0,       np.sin(angle),  -movement[0]],
                        [0,                 1,      0,              0           ],
                        [-np.sin(angle),   0,      np.cos(angle),  -movement[1]]]

    projectionMatrix1 = intrinsicCamera @ extrinsicCamera1
    projectionMatrix2 = intrinsicCamera @ extrinsicCamera2

    return cv2.triangulatePoints(projectionMatrix1, projectionMatrix2, 
                                 points1.astype(np.float64).T, 
                                 points2.astype(np.float64).T)

def extract_matches(path):
    data = np.load(path)
    matches = data['matches']
    keypoints0 = data['keypoints0']
    keypoints1 = data['keypoints1']
    points0 = keypoints0[matches != -1]
    points1 = keypoints1[matches[matches != -1]]
    if points0.size < 8 or points1.size < 8:
        raise Exception('Not enough matches')
    else:
        return points0, points1

def debugImage():
    pathCount = 0
    with open('./test_data_sets/' + data_set + '/pairs_data/description.txt', 'r') as f:
        for line in f:
            # Split the line into a list of image names
            image_names = line.strip().split()
            
            # Assign the image names to two separate variables
            img1_name = image_names[0]
            img2_name = image_names[1]

            img1 = cv2.imread('./test_data_sets/' + data_set + '/source_photos/' + img1_name)
            img2 = cv2.imread('./test_data_sets/' + data_set + '/source_photos/' + img2_name)
            try :
                points1, points2 = extract_matches(PATHS[pathCount])

                for i in range(len(points1)):
                    x = int(points1[i][0])
                    y = int(points1[i][1])
                    cv2.circle(img1, (x, y), 5, (0,255,0), -1)
                    cv2.putText(img1, str(i) + ":" + str(x) + "," + str(y), (x+10, y+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA)
                    
                    x = int(points2[i][0])
                    y = int(points2[i][1])
                    cv2.circle(img2, (x, y), 5, (0,255,0), -1)
                    cv2.putText(img2, str(i) + ":" + str(x) + "," + str(y), (x+10, y+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA)

                # draw the chessboard coordinate system
                img1 = cv2.drawFrameAxes(img1, cameraMatrix, distCoeffs, np.array([0.0, 0.0, 0.0]), np.array([0.0, 0.0, 1.0]), 0.1)
                img2 = cv2.drawFrameAxes(img2, cameraMatrix, distCoeffs, np.array([0.0, 0.0, 0.0]), np.array([0.0, 0.0, 1.0]), 0.1)
                
                # concatenate the images horizontally
                debug_image = np.concatenate((img1, img2), axis=1)
                cv2.imwrite('./test_data_sets/' + data_set + '/debug_matches/' + img1_name[:-4] + '_' + img2_name[:-4] + '.png', debug_image)
                
            except Exception as e:
                print(e)
                
            pathCount += 1
            

def changeCoordinates(point, movement):
    angle = - movement[2]
    x_translation = - movement[0]
    z_translation = - movement[1]
    Rxz = np.array([[np.cos(angle), 0, -np.sin(angle)],
                    [0, 1, 0],
                    [np.sin(angle), 0, np.cos(angle)]])

    # Apply the rotation matrix to point P
    point_rotated = np.dot(Rxz, point)

    # Translate the coordinates of P by x and z
    return point_rotated + np.array([x_translation, 0, z_translation])

def calculatePointsFromPaths(PATHS):
    debugImage()
    points3D = []

    for i in range(len(PATHS)): 
        try :
            (points1, points2) = extract_matches(PATHS[i])
            HOW_MANY_POINTS = min(HOW_MANY_POINTS_DEFAULT, len(points1))

            POINTS = triangulatePoints(points1[:HOW_MANY_POINTS,:],
                                points2[:HOW_MANY_POINTS,:], 
                                movement.MOVEMENTS[i])
            POINTS = cv2.convertPointsFromHomogeneous(POINTS.T)
            POINTS_SHAPED = POINTS[:, 0, :]

            for j in range(HOW_MANY_POINTS):
                POINTS_SHAPED[j] = changeCoordinates(POINTS_SHAPED[j], movement.MOVEMENTS[i])

            points3D.append(np.array(POINTS_SHAPED))
        except Exception as e:
            print(e)
            continue
    
    return points3D

def main():
    # Calculate the 3D points from the paths

if __name__ == '__main__':
    main()