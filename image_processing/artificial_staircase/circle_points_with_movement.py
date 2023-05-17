from matplotlib import pyplot as plt
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
    result = point_rotated + np.array([x_translation, 0, z_translation])

    return result

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
    d = np.sqrt(x ** 2 + z ** 2)
    phi = -np.arctan2(x, z)
    return np.array([d, phi, y])

points_from_staircase = []
XCOORS = [0.7, 2.34, 3.26, 4.39, 4.99, 4.59, 2.66, 1.17, -1.37, -2.26, -3.48, -4.64]

for i in range(len(XCOORS)):
    mul = -1.
    if i < 5:
        mul = 1.
    points_from_staircase.append([XCOORS[i], mul * np.sqrt(25 - XCOORS[i] * XCOORS[i]), 0.5])

# Extract X and Y coordinates from the points
XCOORSPLOT = [point[0] for point in points_from_staircase]
YCOORSPLOT = [point[1] for point in points_from_staircase]

print(points_from_staircase)

print(len(points_from_staircase))

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

with open("circle_points.csv", "w") as file:
    forward = round(2 * R * np.sin(10 * np.pi / 180), 3)
    angle = round(- 20 * np.pi / 180, 3)
    file.write(str(forward) + "," + str(angle) + "\n")
    file.write("81\n")
    if len(all_points) == 0:
        print("ALERT\n")
    for points, ids in zip(all_points, all_points_ids):
        # Write IDs separated by commas
        ids_str = ",".join(str(id) for id in ids)
        for id in ids:
            if id == 13:
                print("ID ALERT")
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

ROBOT_POINTS = []

for i in range(12):
    ang = 20 * (i + 1)
    last_position = [-R * np.cos(ang * np.pi / 180), 
                    0.0, 
                    R * np.sin(ang * np.pi / 180)]
    ROBOT_POINTS.append(last_position)

X_ROBOT = [point[0] for point in ROBOT_POINTS]
Y_ROBOT = [point[2] for point in ROBOT_POINTS]
for i in range(len(X_ROBOT)):
    XCOORSPLOT.append(X_ROBOT[i])
    YCOORSPLOT.append(Y_ROBOT[i])

# Plot the points with equal aspect ratio
plt.scatter(XCOORSPLOT, YCOORSPLOT)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Points on XY Plane')
plt.grid(True)
plt.gca().set_aspect('equal', adjustable='box')  # Set equal aspect ratio
plt.show()