import numpy as np

# 'point' is a numpy array of shape (3,) representing a point in 3D space,
# with origin of the coordinate system in the (0, 0, 0) point.
# 'movement' is a numpy array of shape (3,) representing a movement of the
# coordinates system. The new origin of the coordinate system is calculated
# by applying the movement to the old origin of the coordinate system.
# We assume the rotation is performed first, then the translation.
# The rotation is performed around the Y axis.
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

# change to cylindrical coordinates, having X and Z as radius and Y as height.
# Y axis goes down, X axis goes right, Z axis goes forward.
def changeToCylindricalCoordinates(point):
    x = point[0]
    y = point[1]
    z = point[2]
    r = np.sqrt(x**2 + z**2)
    phi = -np.arctan2(x, z)
    return np.array([r, phi, y])

L1 = [-4.0, 10.0, 0.0]; L2 = [-4.0, -9.0, 0.0]; L3 = [3.0, -9.0, 0.0]; L4 = [3.0, 10.0, 0.0]; L5 = [-4.0, 8.0, -1.0]; L6 = [-4.0, 6.5, -1.0]; L7 = [-4.0, 8.0, 5.0]; L8 = [-4.0, 6.5, 5.0]; L9 = [4.5, 8.5, 1.8]; L10 = [3.5, 9.0, 1.8]
L11 = [4.5, 8.5, 3.5]; L12 = [3.5, 9.0, 3.5]; L13 = [0.06, 5.94, 0.82]; L14 = [-0.55, 6.52, 1.62]; L15 = [-0.85, 5.52, 2.12]; L16 = [-0.24, 4.94, 1.32]; L17 = [1.0, 6.0, 1.5]; L18 = [0.39, 6.58, 2.29]; L19 = [0.09, 5.58, 2.79]; L20 = [0.7, 5.0, 2.0]
L21 = [-2.0, -9.0, 0.35]; L22 = [-0.5, -9.0, 0.35]; L23 = [-2.0, -9.0, 1.55]; L24 = [-0.5, -9.0, 1.55]; L25 = [0.5, -9.0, 1.55]; L26 = [0.5, -9.0, 0.35]; L27 = [2.0, -9.0, 0.35]; L28 = [2.0, -9.0, 1.55]; L29 = [-3.5, -6.8, -0.5]; L30 = [-2.5, -8.8, -0.5]
L31 = [-3.5, -6.8, 2.5]; L32 = [-2.5, -8.8, 2.5]; L33 = [-2.5, -8.8, 1.0]; L34 = [-3.5, -6.8, 1.0]; L35 = [-3.0, -7.8, 0.25]; L36 = [-3.0, -7.8, 1.75]; L37 = [2.0, -4.0, 0.0]; L38 = [1.0, -5.0, 0.0]; L39 = [2.66, -4.66, 0.35]; L40 = [2.28, -4.28, 0.92]
L41 = [1.34, -3.34, 0.35]; L42 = [1.72, -3.72, -0.92]; L43 = [0.72, -4.72, -0.92]; L44 = [-3.0, -2.0, 0.2]; L45 = [-3.0, -2.0, 1.5]; L46 = [-3.0, -3.0, 1.0]; L47 = [-4.0, -3.0, 1.0]; L48 = [-3.55, -2.55, 1.22]; L49 = [-3.0, -2.62, 0.69]; L50 = [-3.0, -2.0, 0.68]
L51 = [-3.0, 3.0, -2.0]; L52 = [-4.0, 4.0, 0.0]; L53 = [-3.22, 3.22, -1.57]; L54 = [-3.66, 3.66, -0.69]; L55 = [-4.36, 4.36, 0.73]; L56 = [-4.74, 4.74, 1.48]; L57 = [-3.84, 3.84, -0.33]; L58 = [-3.0, 1.0, 0.0]; L59 = [-2.0, 2.0, 0.0]; L60 = [-3.5, 2.5, 0.5]
L61 = [-2.81, 2.78, 0.4]; L62 = [-3.61, 1.32, 0.23]; L63 = [3.62, 0.88, 0.85]; L64 = [4.0, 0.0, 0.56]; L65 = [3.85, 1.24, 1.19]; L66 = [3.86, -0.17, 1.69]; L67 = [5.06, 0.48, 1.8]; L68 = [-4.0, 0.5, 1.0]; L69 = [-4.0, 0.7, 0.5]; L70 = [-3.5, 0.5, -0.5]
L71 = [-3.7, -0.7, 0.5]; L72 = [4.0, -3.0, 1.0]; L73 = [4.0, 3.0, 0.0]; L74 = [4.0, 2.21, 0.13]; L75 = [4.0, 0.64, 0.39]; L76 = [4.0, -1.0, 0.67]; L77 = [4.0, -0.28, 0.55]; L78 = [0.9, 3.29, 0.0]; L79 = [1.4, 1.81, 0.0]; L80 = [1.4, 1.81, 0.0]
L81 = [1.75, 0.76, 0.0]

points_from_staircase = np.array(
    [
        L1, L2, L3, L4, L5, L6, L7, L8, L9, L10,
        L11, L12, L13, L14, L15, L16, L17, L18, L19, L20,
        L21, L22, L23, L24, L25, L26, L27, L28, L29, L30,
        L31, L32, L33, L34, L35, L36, L37, L38, L39, L40,
        L41, L42, L43, L44, L45, L46, L47, L48, L49, L50,
        L51, L52, L53, L54, L55, L56, L57, L58, L59, L60,
        L61, L62, L63, L64, L65, L66, L67, L68, L69, L70,
        L71, L72, L73, L74, L75, L76, L77, L78, L79, L80,
        L81
    ]
)

# change geogebra coordinates to our coordinates
for i in range(len(points_from_staircase)):
    x = points_from_staircase[i][0]
    y = points_from_staircase[i][1]
    z = points_from_staircase[i][2]
    points_from_staircase[i] = np.array([x, -z, y])

# starting position (X, Y, Z):
START = [- np.cos(20 * np.pi / 180) * 0.9, 0.03, np.sin(20 * np.pi / 180) * 0.9]

# movement leading to starting position [X, Z, ROTATION]
START_MOVEMENT = [
    - np.cos(10 * np.pi / 180) * 0.9,
    - np.sin(10 * np.pi / 180) * 0.9,
    - 30 * np.pi / 180,
]

# change coordinates to start position
for i in range(len(points_from_staircase)):
    points_from_staircase[i] = changeCoordinates(
        points_from_staircase[i], START_MOVEMENT
    )

# change coordinates from staircase to cylindrical
for i in range(len(points_from_staircase)):
    points_from_staircase[i] = changeToCylindricalCoordinates(points_from_staircase[i])

# capturing the result
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


# RESULT [distance, angle, height]
POINTS = np.array([
    [10.193, 48.027, 0.0], [9.828, -168.721, 0.0], [10.071, -127.551, 0.0], [10.427, 8.358, 0.0], [8.314, 52.297, 1.0], 
    [6.949, 56.994, 1.0], [8.314, 52.297, -5.0], [6.949, 56.994, -5.0], [9.782, -3.126, -1.8], [9.718, 3.437, -1.8], 
    [9.782, -3.126, -3.5], [9.718, 3.437, -3.5], [5.705, 20.864, -0.82], [6.219, 27.275, -1.62], [5.212, 30.047, -2.12], 
    [4.672, 22.55, -1.32], [5.984, 12.034, -1.5], [6.393, 18.855, -2.29], [5.355, 19.936, -2.79], [4.94, 11.767, -2.0], 
    [9.379, -157.069, -0.35], [9.314, -147.873, -0.35], [9.379, -157.069, -1.55], [9.314, -147.873, -1.55], [9.405, -141.773, -1.55], 
    [9.405, -141.773, -0.35], [9.733, -133.0, -0.35], [9.733, -133.0, -1.55], [7.587, -170.477, 0.5], [9.257, -160.295, 0.5], 
    [7.587, -170.477, -2.5], [9.257, -160.295, -2.5], [9.257, -160.295, -1.0], [7.587, -170.477, -1.0], [8.389, -164.88, -0.25], 
    [8.389, -164.88, -1.75], [5.163, -116.551, 0.0], [5.62, -130.826, 0.0], [6.08, -114.79, -0.35], [5.551, -115.733, -0.92], 
    [4.253, -119.071, -0.35], [4.776, -117.503, 0.92], [5.266, -132.703, 0.92], [3.157, 166.971, -0.2], [3.157, 166.971, -1.5], 
    [3.947, 176.925, -1.0], [4.571, 166.361, -1.0], [3.934, 166.581, -1.22], [3.635, 173.655, -0.69], [3.157, 166.971, -0.68], 
    [3.448, 68.667, 2.0], [4.856, 70.508, 0.0], [3.757, 69.19, 1.57], [4.377, 70.015, 0.69], [5.364, 70.934, -0.73], 
    [5.9, 71.304, -1.48], [4.631, 70.288, 0.33], [2.263, 102.187, 0.0], [2.048, 64.299, 0.0], [3.443, 80.447, -0.5], 
    [3.158, 68.469, -0.4], [2.944, 99.889, -0.23], [4.502, -52.699, -0.85], [4.855, -63.635, -0.56], [4.787, -48.772, -1.19], 
    [4.73, -65.798, -1.69], [5.908, -58.33, -1.8], [3.16, 116.513, -1.0], [3.179, 112.913, -0.5], [2.661, 115.859, 0.5], 
    [3.027, 139.448, -0.5], [5.867, -94.318, -1.0], [5.543, -30.944, 0.0], [5.206, -38.568, -0.13], [4.857, -56.078, -0.39], 
    [5.019, -75.104, -0.67], [4.881, -66.917, -0.55], [3.456, -0.344, 0.0], [2.702, -26.221, 0.0], [2.702, -26.221, 0.0], 
    [2.635, -50.118, 0.0], 
])

print(POINTS.shape)