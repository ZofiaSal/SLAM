import time
import pyrealsense2.pyrealsense2 as rs
import numpy as np
import cv2
from datetime import date

pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8,15)

profile = pipeline.start(config)

# Get the sensor once at the beginning. (Sensor index: 1)
sensor = pipeline.get_active_profile().get_device().query_sensors()[1]

# Set the exposure anytime during the operation
# Outside partly cloudy day -> sensor.set_option(rs.option.exposure, 1.000)
# Inside quite bright -> sensor.set_option(rs.option.exposure, 150.000)
sensor.set_option(rs.option.exposure, 750.000)

align_to = rs.stream.color
align = rs.align(align_to)


message = "Press only enter to make another photo, press anything and enter to exit\n"

def int_to_three_digit_string(i):
    # Convert the integer to a string
    s = str(i)
    
    # If the string is already 3 characters long, return it
    if len(s) == 3:
        return s
    
    # If the string is less than 3 characters long, pad it with leading zeros
    elif len(s) < 3:
        return s.zfill(3)
    
    # If the string is more than 3 characters long, return the last 3 characters
    else:
        return s[-3:]

i = 0; 
key =  input(message)
while(key == ""):

    frames = pipeline.wait_for_frames()

    aligned_frames = align.process(frames)
    frame = aligned_frames.get_color_frame()

    image = np.asanyarray(frame.get_data())

    # Filename 
    imageName = './' + 'photo_' + int_to_three_digit_string(i) + "_"+str(date.today())+'.jpg'

    # Saving the image 
    cv2.imwrite(imageName, image) 

    key = input(message)

    i = i+1



pipeline.stop()