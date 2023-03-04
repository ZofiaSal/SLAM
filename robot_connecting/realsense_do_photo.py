# Based on code from https://support.intelrealsense.com/hc/en-us/community/posts/360052346893-RGB-image-captured-by-Intel-realsense-camera-is-dark-using-python-code-

import pyrealsense2 as rs
import numpy as np
import time
import cv2

pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)

profile = pipeline.start(config)

# Get the sensor once at the beginning. (Sensor index: 1)
sensor = pipeline.get_active_profile().get_device().query_sensors()[1]

# Set the exposure anytime during the operation
sensor.set_option(rs.option.exposure, 500.000)

align_to = rs.stream.color
align = rs.align(align_to)

frames = pipeline.wait_for_frames()

aligned_frames = align.process(frames)
frame = aligned_frames.get_color_frame()

image = np.asanyarray(frame.get_data())

cv2.namedWindow('Align Example', cv2.WINDOW_AUTOSIZE)

# Filename 
imageName1 = 'photos/callibration/' + str(time.strftime("%Y_%m_%d_%H_%M_%S")) + 'photo.jpg'

# Saving the image 
cv2.imwrite(imageName1, image) 

key = cv2.waitKey(1)
# Press esc or 'q' to close the image window
cv2.destroyAllWindows()

pipeline.stop()