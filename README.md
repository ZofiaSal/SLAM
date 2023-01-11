# SLAM
Bachelor's thesis project 
implementation of  ekf algorithm copied from 
https://github.com/AtsushiSakai/PythonRobotics/tree/405f3e79341356c4fa3f78dbe37bcd87f12d155b/SLAM/EKFSLAM

What do we need to change :

- abstract out getting controls and observations where each observation is [d,ang,z,i] where d is distance on XY plane, ang is angle between front of a robot and observation, z is the Z coord of landmark and i is and index of landmark.


What even is here ?

*feature_points*

*first_dataset*
Set of photos made for testing image_processing and potentially in future also out slam.

*images_prev*
Script for getting intrinsic and distortion of camera based on Charuko photos . 

*robot_connecting*
Low level stuff for getting info from robot and moving it.