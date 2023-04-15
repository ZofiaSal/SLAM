from cmath import pi
import numpy as np
import cv2

PATHS = [   
            './photo00_photo01_matches.npz',
            './photo01_photo02_matches.npz',
            './photo02_photo03_matches.npz',
            './photo03_photo04_matches.npz',
            './photo04_photo05_matches.npz',
            './photo05_photo06_matches.npz',
            './photo06_photo07_matches.npz',
            './photo07_photo08_matches.npz',
            './photo08_photo09_matches.npz',
            './photo09_photo10_matches.npz',
            './photo10_photo11_matches.npz',
            './photo11_photo12_matches.npz'
        ]

def extract_matches(path):
    data = np.load(path)
    matches = data['matches']
    keypoints0 = data['keypoints0']
    keypoints1 = data['keypoints1']
    points0 = keypoints0[matches != -1]
    points1 = keypoints1[matches[matches != -1]]
    if points0.size < 8 or points1.size < 8:
        print("Too few points to produce fundamental matrix.")
    else:
        return points0, points1
    
def main():
    for path in PATHS:
        print(path)
        points0, points1 = extract_matches(path)
        print(len(points0))

        if len(points0) < 15:
            print(points0)

if __name__ == '__main__':
    main()