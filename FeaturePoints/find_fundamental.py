import numpy as np
import cv2 as cv
import argparse

path = 'dump_match_pairs/scene0711_00_frame-001680_scene0711_00_frame-001995_matches.npz'
npz = np.load(path)
npz.files
['keypoints0', 'keypoints1', 'matches', 'match_confidence']

points0 = np.array([[2,3]])
points1 = np.array([[2,3]])

tab0 = npz['keypoints0']
tab1 = npz['keypoints1']
tab2 = npz['matches']

for x in range(tab2.size):
	if (tab2[x] != -1):
		points0 = np.insert(points0, points0.size // 2, tab0[x], 0);
		points1 = np.insert(points1, points1.size // 2, tab1[tab2[x]], 0);
		 
		 
points0 = np.delete(points0, 0, 0);
points1 = np.delete(points1, 0, 0);

if (points0.size < 8 or points1.size < 8):
	print("To few points to produce fundamental matrix.");
elif (points0.size != points1.size):
	print("Sizes don't match! Suspicious...");
else:

	F, mask = cv.findFundamentalMat(cv.UMat(points0), cv.UMat(points1),cv.FM_8POINT)

	print("F:");
	print(F);
	print("mask:");
	print(mask);
