import points
import numpy as np
from points import changeCoordinates
from points import changeToCylindricalCoordinates

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

# points_art_coords_test = np.array([[1.0, 1.0, - 1.0]])

# for i in range(len(points_art_coords_test)):
#     points_art_coords_test[i] = changeToCylindricalCoordinates(points_art_coords_test[i])

# print("points_art_coords_test:")
# print(np.round(points_art_coords_test, 3))