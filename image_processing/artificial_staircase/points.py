import math
import numpy as np


def changeCoordinates(point, movement):
    angle = -movement[2]
    x_translation = -movement[0]
    z_translation = -movement[1]
    Rxz = np.array(
        [
            [np.cos(angle), 0, -np.sin(angle)],
            [0, 1, 0],
            [np.sin(angle), 0, np.cos(angle)],
        ]
    )

    # Apply the rotation matrix to point P
    point_rotated = np.dot(Rxz, point)

    # Translate the coordinates of P by x and z
    return point_rotated + np.array([x_translation, 0, z_translation])


# points = np.array(
#     [
#         [0. ,0. ,0],
#         START
#     ])

# print("movement:")
# print(np.round(START_MOVEMENT, 3))

# print("test:")
# print(points)

# for i in range(len(points)):
#     points[i] = changeCoordinates(points[i], START_MOVEMENT)

# print("after movement1:")
# # print points rounded to 2 decimal places
# print(np.round(points, 3))

# ### TEST <- ROTATION FIRST THEN TRANSLATION

# points = np.array([[1.0, 102.0, 0.0]])
# TEST_MOVEMENT = [1.0, 0.0, - 45 * np.pi / 180]

# for i in range(len(points)):
#     points[i] = changeCoordinates(points[i], TEST_MOVEMENT)

# print("after movement:")
# # print points rounded to 2 decimal places
# print(np.round(points, 3))

# # [[  0.707 102.      0.707]]


# change to cylindrical coordinates, having X and Z as radius and Y as height.
# Y axis goes down, X axis goes right, Z axis goes forward.
def changeToCylindricalCoordinates(point):
    x = point[0]
    y = point[1]
    z = point[2]
    r = np.sqrt(x**2 + z**2)
    phi = -np.arctan2(x, z)
    return np.array([r, y, phi * 180 / np.pi])


# points_art_coords_test = np.array([[1.0, 1.0, - 1.0]])

# for i in range(len(points_art_coords_test)):
#     points_art_coords_test[i] = changeToCylindricalCoordinates(points_art_coords_test[i])

# print("points_art_coords_test:")
# print(np.round(points_art_coords_test, 3))

L1 = [-4.0, 10.0, 0.0]
L2 = [-4.0, -9.0, 0.0]
L3 = [3.0, -9.0, 0.0]
L4 = [3.0, 10.0, 0.0]
L5 = [-4.0, 8.0, -1.0]
L6 = [-4.0, 6.5, -1.0]
L7 = [-4.0, 8.0, 5.0]
L8 = [-4.0, 6.5, 5.0]
L9 = [4.5, 8.5, 1.8]
L10 = [3.5, 9.0, 1.8]
L11 = [4.5, 8.5, 3.5]
L12 = [3.5, 9.0, 3.5]
L13 = [0.06, 5.94, 0.82]
L14 = [-0.55, 6.52, 1.62]
L15 = [-0.85, 5.52, 2.12]
L16 = [-0.24, 4.94, 1.32]
L17 = [1.0, 6.0, 1.5]
L18 = [0.39, 6.58, 2.29]
L19 = [0.09, 5.58, 2.79]
L20 = [0.7, 5.0, 2.0]
L21 = [-2.0, -9.0, 0.35]
L22 = [-0.5, -9.0, 0.35]
L23 = [-2.0, -9.0, 1.55]
L24 = [-0.5, -9.0, 1.55]
L25 = [0.5, -9.0, 1.55]
L26 = [0.5, -9.0, 0.35]
L27 = [2.0, -9.0, 0.35]
L28 = [2.0, -9.0, 1.55]
L29 = [-3.5, -6.8, -0.5]
L30 = [-2.5, -8.8, -0.5]
L31 = [-3.5, -6.8, 2.5]
L32 = [-2.5, -8.8, 2.5]
L33 = [-2.5, -8.8, 1.0]
L34 = [-3.5, -6.8, 1.0]
L35 = [-3.0, -7.8, 0.25]
L36 = [-3.0, -7.8, 1.75]
L37 = [2.0, -4.0, 0.0]
L38 = [1.0, -5.0, 0.0]
L39 = [2.66, -4.66, 0.35]
L40 = [2.28, -4.28, 0.92]
L41 = [1.34, -3.34, 0.35]
L42 = [1.72, -3.72, -0.92]
L43 = [0.72, -4.72, -0.92]
L44 = [-3.0, -2.0, 0.2]
L45 = [-3.0, -2.0, 1.5]
L46 = [-3.0, -3.0, 1.0]
L47 = [-4.0, -3.0, 1.0]
L48 = [-3.55, -2.55, 1.22]
L49 = [-3.0, -2.62, 0.69]
L50 = [-3.0, -2.0, 0.68]
L51 = [-3.0, 3.0, -2.0]
L52 = [-4.0, 4.0, 0.0]
L53 = [-3.22, 3.22, -1.57]
L54 = [-3.66, 3.66, -0.69]
L55 = [-4.36, 4.36, 0.73]
L56 = [-4.74, 4.74, 1.48]
L57 = [-3.84, 3.84, -0.33]
L58 = [-3.0, 1.0, 0.0]
L59 = [-2.0, 2.0, 0.0]
L60 = [-3.5, 2.5, 0.5]
L61 = [-2.81, 2.78, 0.4]
L62 = [-3.61, 1.32, 0.23]
L63 = [3.62, 0.88, 0.85]
L64 = [4.0, 0.0, 0.56]
L65 = [3.85, 1.24, 1.19]
L66 = [3.86, -0.17, 1.69]
L67 = [5.06, 0.48, 1.8]
L68 = [-4.0, 0.5, 1.0]
L69 = [-4.0, 0.7, 0.5]
L70 = [-3.5, 0.5, -0.5]
L71 = [-3.7, -0.7, 0.5]
L72 = [4.0, -3.0, 1.0]
L73 = [4.0, 3.0, 0.0]
L74 = [4.0, 2.21, 0.13]
L75 = [4.0, 0.64, 0.39]
L76 = [4.0, -1.0, 0.67]
L77 = [4.0, -0.28, 0.55]
L78 = [0.9, 3.29, 0.0]
L79 = [1.4, 1.81, 0.0]
L80 = [1.55, 1.35, 0.0]
L81 = [1.75, 0.76, 0.0]
L_TEST = [1.0, 2.0, 3.0]

points_from_staircase = np.array(
    [
        L1,
        L2,
        L3,
        L4,
        L5,
        L6,
        L7,
        L8,
        L9,
        L10,
        L11,
        L12,
        L13,
        L14,
        L15,
        L16,
        L17,
        L18,
        L19,
        L20,
        L21,
        L22,
        L23,
        L24,
        L25,
        L26,
        L27,
        L28,
        L29,
        L30,
        L31,
        L32,
        L33,
        L34,
        L35,
        L36,
        L37,
        L38,
        L39,
        L40,
        L41,
        L42,
        L43,
        L44,
        L45,
        L46,
        L47,
        L48,
        L49,
        L50,
        L51,
        L52,
        L53,
        L54,
        L55,
        L56,
        L57,
        L58,
        L59,
        L60,
        L61,
        L62,
        L63,
        L64,
        L65,
        L66,
        L67,
        L68,
        L69,
        L70,
        L71,
        L72,
        L73,
        L74,
        L75,
        L76,
        L77,
        L78,
        L79,
        L80,
        L81,
        L_TEST,
    ]
)

for i in range(len(points_from_staircase)):
    x = points_from_staircase[i][0]
    y = points_from_staircase[i][1]
    z = points_from_staircase[i][2]
    points_from_staircase[i] = np.array([x, -z, y])

# standing at the point (X, Y, Z):
START = [-np.cos(20 * np.pi / 180) * 0.9, 0.03, np.sin(20 * np.pi / 180) * 0.9]
START_MOVEMENT = [
    -np.cos(10 * np.pi / 180) * 0.9,
    -np.sin(10 * np.pi / 180) * 0.9,
    -30 * np.pi / 180,
]

# change coordinates to start position
for i in range(len(points_from_staircase)):
    points_from_staircase[i] = changeCoordinates(
        points_from_staircase[i], START_MOVEMENT
    )

# change coordinates from staircase to cylindrical
for i in range(len(points_from_staircase)):
    points_from_staircase[i] = changeToCylindricalCoordinates(points_from_staircase[i])

# why the result is not properly rounded?
print("points from staircase:")
print("POINTS = np.array([")
for i in range(len(points_from_staircase)):
    print(
        "    ["
        + str(np.round(points_from_staircase[i][0], 3))
        + ", "
        + str(np.round(points_from_staircase[i][1], 3))
        + ", "
        + str(np.round(points_from_staircase[i][2], 3))
        + "],",
        end=" ",
    )
    if (i + 1) % 5 == 0:
        print()
print("\n])")


# RESULT
POINTS = np.array(
    [
        [10.193, 0.0, 48.027],
        [9.828, 0.0, -168.721],
        [10.071, 0.0, -127.551],
        [10.427, 0.0, 8.358],
        [8.314, 1.0, 52.297],
        [6.949, 1.0, 56.994],
        [8.314, -5.0, 52.297],
        [6.949, -5.0, 56.994],
        [9.782, -1.8, -3.126],
        [9.718, -1.8, 3.437],
        [9.782, -3.5, -3.126],
        [9.718, -3.5, 3.437],
        [5.705, -0.82, 20.864],
        [6.219, -1.62, 27.275],
        [5.212, -2.12, 30.047],
        [4.672, -1.32, 22.55],
        [5.984, -1.5, 12.034],
        [6.393, -2.29, 18.855],
        [5.355, -2.79, 19.936],
        [4.94, -2.0, 11.767],
        [9.379, -0.35, -157.069],
        [9.314, -0.35, -147.873],
        [9.379, -1.55, -157.069],
        [9.314, -1.55, -147.873],
        [9.405, -1.55, -141.773],
        [9.405, -0.35, -141.773],
        [9.733, -0.35, -133.0],
        [9.733, -1.55, -133.0],
        [7.587, 0.5, -170.477],
        [9.257, 0.5, -160.295],
        [7.587, -2.5, -170.477],
        [9.257, -2.5, -160.295],
        [9.257, -1.0, -160.295],
        [7.587, -1.0, -170.477],
        [8.389, -0.25, -164.88],
        [8.389, -1.75, -164.88],
        [5.163, 0.0, -116.551],
        [5.62, 0.0, -130.826],
        [6.08, -0.35, -114.79],
        [5.551, -0.92, -115.733],
        [4.253, -0.35, -119.071],
        [4.776, 0.92, -117.503],
        [5.266, 0.92, -132.703],
        [3.157, -0.2, 166.971],
        [3.157, -1.5, 166.971],
        [3.947, -1.0, 176.925],
        [4.571, -1.0, 166.361],
        [3.934, -1.22, 166.581],
        [3.635, -0.69, 173.655],
        [3.157, -0.68, 166.971],
        [3.448, 2.0, 68.667],
        [4.856, 0.0, 70.508],
        [3.757, 1.57, 69.19],
        [4.377, 0.69, 70.015],
        [5.364, -0.73, 70.934],
        [5.9, -1.48, 71.304],
        [4.631, 0.33, 70.288],
        [2.263, 0.0, 102.187],
        [2.048, 0.0, 64.299],
        [3.443, -0.5, 80.447],
        [3.158, -0.4, 68.469],
        [2.944, -0.23, 99.889],
        [4.502, -0.85, -52.699],
        [4.855, -0.56, -63.635],
        [4.787, -1.19, -48.772],
        [4.73, -1.69, -65.798],
        [5.908, -1.8, -58.33],
        [3.16, -1.0, 116.513],
        [3.179, -0.5, 112.913],
        [2.661, 0.5, 115.859],
        [3.027, -0.5, 139.448],
        [5.867, -1.0, -94.318],
        [5.543, 0.0, -30.944],
        [5.206, -0.13, -38.568],
        [4.857, -0.39, -56.078],
        [5.019, -0.67, -75.104],
        [4.881, -0.55, -66.917],
        [3.456, 0.0, -0.344],
        [2.702, 0.0, -26.221],
        [2.613, 0.0, -36.49],
        [2.635, 0.0, -50.118],
        [2.504, -3.0, -17.485],
    ]
)

print(POINTS.shape)