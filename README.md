# SLAM
Bachelor's thesis project 


What do we need to change:

- abstract out getting controls and observations where each observation is [d,ang,z,i] where d is distance on XY plane, ang is angle between front of a robot and observation, z is the Z coord of landmark and i is and index of landmark.




What even is here?

*ekf_slam.py*

implementation of  ekf algorithm using  
https://github.com/AtsushiSakai/PythonRobotics/tree/405f3e79341356c4fa3f78dbe37bcd87f12d155b/SLAM/EKFSLAM

*image_processing.py*

Implementation for finding coordinates of feature points based on two pictures and the movement. 

*feature_points/*

TODO : clean it (feature_points/find_fundamental.py = ./find_matches_with_superglue.py ) 

*first_dataset/*

Set of photos made for testing image_processing and potentially in future also for slam.

*camera_calibration/*

Script for getting intrinsic and distortion of camera based on Charuko photos . 

*robot_connecting/*

Low level stuff for getting info from robot and moving it.

*synthetic_tests/*

All tests, to run use make test

TODO: info -- how to get npz
TODO: add camera calibration scritp ?
