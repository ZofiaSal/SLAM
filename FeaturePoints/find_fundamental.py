import numpy as np
import cv2 as cv
import argparse

path = 'dump_match_pairs/scene0711_00_frame-001680_scene0711_00_frame-001995_matches.npz'
npz = np.load(path)
npz.files
['keypoints0', 'keypoints1', 'matches', 'match_confidence']

# initialize the points here
points0 = np.array([[1,3]]);
points1 = np.array([[2,3]])

for x in range(d2):
	if (tab2[x] != -1):
		points0 = np.insert(points0, points0.size // 2, tab0[x], 0);
		points1 = np.insert(points1, points1.size // 2, tab1[tab2[x]], 0);
		 
		 
points0 = np.delete(points0, 0, 0);
points1 = np.delete(points1, 0, 0);

print("points0:");
print(points0);
print("points1:");
print(points1);
		 
# estimate fundamental matrix

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

#[F, mask] = cv.findFundamentalMat(cv.UMat(points0), cv.UMat(points1), 'Method','Ransac');  
  

'''
npz['keypoints0'].shape
(382, 2)
>>> npz['keypoints1'].shape
(391, 2)
>>> npz['matches'].shape
(382,)
>>> np.sum(npz['matches']>-1)
115
>>> npz['match_confidence'].shape
(382,)
'''
