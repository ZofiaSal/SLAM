import numpy as np
from give_only_seen import only_seen_points

# 'point' is a numpy array of shape (3,) representing a point in 3D space,
# with origin of the coordinate system in the (0, 0, 0) point.
# 'movement' is a numpy array of shape (3,) representing a movement of the
# coordinates system. The new origin of the coordinate system is calculated
# by applying the movement to the old origin of the coordinate system.
# We assume the rotation is performed first, then the translation.
# The rotation is performed around the Y axis.
def changeCoordinates(point, movement):
    angle = - movement[2]
    x_translation = - movement[0]
    z_translation = - movement[1]
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

def changeCoordinatesOfAll(points, movement):
    for i in range(len(points)):
        points[i] = changeCoordinates(points[i], movement)
    return points

# change to cylindrical coordinates, having X and Z as radius and Y as height.
# Y axis goes down, X axis goes right, Z axis goes forward.
def changeToCylindricalCoordinates(point):
    x = point[0]
    y = point[1]
    z = point[2]
    r = np.sqrt(x**2 + z**2)
    phi = -np.arctan2(x, z)
    return np.array([r, phi * 180 / np.pi, y])

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

# movement leading (from [0, 0, 0]) to starting position [X, Z, ROTATION]
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

R = 0.9
MOVEMENT = [- 2 * R * np.sin(10 * np.pi / 180) * np.sin(20 * np.pi / 180), 
            2 * R * np.sin(10 * np.pi / 180) * np.cos(20 * np.pi / 180), 
            - 20 * np.pi / 180]

MOVEMENTS = []

for i in range(1, 10):
    MOVEMENTS.append(MOVEMENT)

def get_ids(all_points, taken_points):
    result = []
    n = 0
    i = 0
    while i < len(taken_points):
        if taken_points[i][0] == all_points[n][0] and \
           taken_points[i][1] == all_points[n][1] and \
           taken_points[i][2] == all_points[n][2]:
            result.append(n + 1)
            i += 1
        n += 1
    return result

all_points = []
all_points_ids = []
points_to_append = only_seen_points(points_from_staircase)
all_points_ids.append(get_ids(points_from_staircase, points_to_append))
for j in range(len(points_to_append)):
    points_to_append[j] = changeToCylindricalCoordinates(points_to_append[j])
all_points.append(points_to_append)

for i in range (len(MOVEMENTS)):
    points_from_staircase = changeCoordinatesOfAll(points_from_staircase, MOVEMENTS[i])
    points_to_append = only_seen_points(points_from_staircase)
    all_points_ids.append(get_ids(points_from_staircase, points_to_append))
    for j in range(len(points_to_append)):
        points_to_append[j] = changeToCylindricalCoordinates(points_to_append[j])
    all_points.append(points_to_append)

with open("points.csv", "w") as file:
    forward = round(2 * R * np.sin(10 * np.pi / 180), 3)
    angle = round(- 20 * np.pi / 180, 3)
    file.write(str(forward) + "," + str(angle) + "\n")
    file.write("81\n")
    for points, ids in zip(all_points, all_points_ids):
        # Write IDs separated by commas
        ids_str = ",".join(str(id) for id in ids)
        file.write(ids_str + "\n")
        
         # Round x, y, and z coordinates to three decimal places
        x_coords = [round(point[0], 3) for point in points]
        y_coords = [round(point[1], 3) for point in points]
        z_coords = [round(point[2], 3) for point in points]
        
        x_coords_str = ",".join(str(coord) for coord in x_coords)
        y_coords_str = ",".join(str(coord) for coord in y_coords)
        z_coords_str = ",".join(str(coord) for coord in z_coords)
        
        file.write(x_coords_str + "\n")
        file.write(y_coords_str + "\n")
        file.write(z_coords_str)
        
        # Add an empty line between each set of data
        file.write("\n")