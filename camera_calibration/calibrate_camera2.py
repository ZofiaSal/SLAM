import cv2
import glob
import cv2.aruco as aruco

RELATIVE_PATH = './chessboard_photos_for_calibration/nie_dziala/*.jpg'
ROW_COUNT = 6
COLUMN_COUNT = 5
SIZE_FULL_SQUARE =  0.0184
SIZE_SQUARE = 0.015
IMG_SIZE  = (1280,720)

# RELATIVE_PATH = "./chessboard_photos_for_calibration/images_of_charuco_second_attempt_realsense/*.jpg"
# ROW_COUNT = 7
# COLUMN_COUNT = 5
# SIZE_FULL_SQUARE =  0.0285
# SIZE_SQUARE = 0.023
# IMG_SIZE  = (1280,720)

# RELATIVE_PATH = './images_of_charuco_from_Krystyna_phone/*.jpg'
# ROW_COUNT = 8
# COLUMN_COUNT = 9
# SIZE_FULL_SQUARE =  0.0137
# SIZE_SQUARE = 0.011
# IMG_SIZE  = (4608,3456)

images = sorted(glob.glob(RELATIVE_PATH))
dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)

img_points = []
corners_all = []
good_images = []
for iname in images:
    img = cv2.imread(iname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    board = aruco.CharucoBoard((ROW_COUNT, COLUMN_COUNT), SIZE_FULL_SQUARE, SIZE_SQUARE, dictionary)

    detector = aruco.CharucoDetector(board)
    charuco_corners, charuco_ids, marker_corners, marker_ids = detector.detectBoard(
            image = gray)

    if charuco_corners is None:
        print("Didn't find board on ", iname)
        continue

    img = aruco.drawDetectedMarkers(
            image = img, 
            corners = marker_corners)

    img = aruco.drawDetectedCornersCharuco(
            image = img,
            charucoCorners = charuco_corners,
            charucoIds = charuco_ids)

    counter = (ROW_COUNT - 1) * (COLUMN_COUNT -1 )
    if len(charuco_corners) == counter:
        good_images.append(iname)
        img_points.append(charuco_corners)
        assert tuple(charuco_ids) == tuple([[i] for i in range(counter)])
        corners_all.append(board.getChessboardCorners())

calibration, cameraMatrix, distCoeffs, rvecs, tvecs = cv2.calibrateCamera(
        objectPoints = corners_all,
        imagePoints = img_points,
        imageSize = IMG_SIZE,
        cameraMatrix = None,
        distCoeffs = None)

print(calibration) #Error should be as close to zero as possible ideally in range(0.1, 1)
print(cameraMatrix)
print(distCoeffs)