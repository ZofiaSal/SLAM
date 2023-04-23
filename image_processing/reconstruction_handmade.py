from cmath import pi
import subprocess
import sys
import numpy as np
import os
import cv2
import argparse

# OUR FINAL CAMERA CALIBRATION MATRIX
calibration = 0.6442544274536695
cameraMatrix = np.array([[932.35252209,   0.,         657.24325896],
 [  0.,         930.23581552, 357.42939289],
 [  0.,           0.,           1.        ]])
distCoeffs = np.array([[ 1.76279343e-01, -6.07952723e-01, -4.64176532e-04, -4.96839648e-04, 6.04867450e-01]])

HOW_MANY_POINTS_DEFAULT = 1000

# points1 - characteristic points from first picture 
# points2 - characteristic points for corresponding points from picture two
# movement - the change from where picture 1 was taken to where picture 2 was taken [x,z,alpha] where alpha is a clockwise rotation in XY
def triangulatePoints(points1, points2, movement, intrinsicCamera = cameraMatrix):
    print("triangulate1: ", end="")
    print(repr(points1))
    print("triangulate2: ", end="")
    print(repr(points2))
    print("movement: ", end="")
    print(movement)

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

# Writes to '/debug_handmade_matches/' images with the matches drawn on them for all pairs of photos listed in '/pairs_data/description.txt' 
def debugImage(directory_path, points_sets):

    pathCount = 0
    with open(directory_path + '/pairs_data/description.txt', 'r') as f:
        for line in f:
            # Split the line into a list of image names
            image_names = line.strip().split()
            
            # Assign the image names to two separate variables
            img1_name = image_names[0]
            img2_name = image_names[1]

            img1 = cv2.imread(directory_path + '/source_photos/' + img1_name)
            img2 = cv2.imread(directory_path + '/source_photos/' + img2_name)
            try :
                points1, points2 = points_sets[pathCount]

                print("debug_image1: ", end="")
                print(repr(points1))
                print("debug_image2: ", end="")
                print(repr(points2))

                colors = [[0, 0, 255], [0, 255, 0], [255, 0, 0], [255, 255, 0], [255, 0, 255], [0, 255, 255], [255, 255, 255], [0, 0, 0]]

                for i in range(len(points1)):
                    x = int(points1[i][0])
                    y = int(points1[i][1])
                    
                    cv2.circle(img1, (x, y), 5, colors[i % len(colors)], -1)
                    cv2.putText(img1, str(i) + ":" + str(x) + "," + str(y), (x+10, y+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA)
                    
                    x = int(points2[i][0])
                    y = int(points2[i][1])
                    cv2.circle(img2, (x, y), 5, colors[i % len(colors)], -1)
                    cv2.putText(img2, str(i) + ":" + str(x) + "," + str(y), (x+10, y+10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA)

                # draw the chessboard coordinate system
                img1 = cv2.drawFrameAxes(img1, cameraMatrix, distCoeffs, np.array([0.0, 0.0, 0.0]), np.array([0.0, 0.0, 1.0]), 0.1)
                img2 = cv2.drawFrameAxes(img2, cameraMatrix, distCoeffs, np.array([0.0, 0.0, 0.0]), np.array([0.0, 0.0, 1.0]), 0.1)
                
                # concatenate the images horizontally
                debug_image = np.concatenate((img1, img2), axis=1)
                cv2.imwrite(directory_path + '/debug_handmade_matches/' + img1_name[:-4] + '_' + img2_name[:-4] + '.png', debug_image)
                
            except Exception as e:
                print("For pictures " + img1_name + " and " + img2_name + " occured an error: " + str(e))
                
            pathCount += 1

# File needs to be called points_pairs.py 
# and have a variable called points which is an array of pairs (array1, array2) where array1 are points from first image and array2 are points from second image.
# File movement.py needs to have a variable called MOVEMENTS which is an array of movements (x, y, angle) for each pair of images.
def calculatePointsFromFile(directory_path):
    
    sys.path.append(directory_path + "/handmade_matches")
    import points_pairs as pp  

    sys.path.append(directory_path + "/source_photos")
    import movement 
   
    MOVEMENTS = movement.MOVEMENTS

    points_sets = pp.points 
    
    debugImage(directory_path, points_sets)

    points3D = []
    
    for i in range(len(points_sets)): 
        try :
            (points1, points2) = points_sets[i]
            if points1.size != points2.size:
                raise Exception("The number of points in the two images is not the same")

            HOW_MANY_POINTS = min(HOW_MANY_POINTS_DEFAULT, len(points1))

            POINTS = triangulatePoints(points1[:HOW_MANY_POINTS,:],
                                points2[:HOW_MANY_POINTS,:], 
                                MOVEMENTS[i]) 
            POINTS = cv2.convertPointsFromHomogeneous(POINTS.T)
            POINTS_SHAPED = POINTS[:, 0, :]

            print("Points from triangulation: " + repr(POINTS_SHAPED))

            for j in range(HOW_MANY_POINTS):
                POINTS_SHAPED[j] = changeCoordinates(POINTS_SHAPED[j], MOVEMENTS[0])

            points3D.append(np.array(POINTS_SHAPED))
        except Exception as e:
            print("In test number " + str(i) + " occured an error: " + str(e))
            continue
    
    return points3D

def main():
    # Create the parser
    parser = argparse.ArgumentParser(description='3d reconstruction')

    # Add the arguments
    parser.add_argument('--data', type=str, help='Data set directory name')

    # Parse the arguments
    args = parser.parse_args()
    data_set = args.data

    current_path = os.path.dirname(os.path.abspath(__file__))
    directory_path = current_path + "/test_data_sets/" + data_set
    
    print(calculatePointsFromFile(directory_path))

if __name__ == '__main__':
    main()