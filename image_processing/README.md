# SLAM - image processing: 3D reconstruction

## Finding matches

Clone the SuperGlue repo in the _/SLAM/_ directory: 

https://github.com/magicleap/SuperGluePretrainedNetwork

Run the reconstruction:

`python reconstruction3d.py --data 'data_set_directory' --fm`

Omit the `--fm` if the .npz files with matches are already generated.

Replace `data_set_directory` with the appropriate name.
In the */SLAM/image_processing/test_data_sets/data_set_directory* place the 
input photos and the *movement.py* file. In the *[...]/test_data_sets/data_set_directory/pairs_data/description.txt* place the pairs of photos (for SuperGlue). The debug output will be evaluated correctly only if you put them in alphabetical order. In the *movement.py* file put the description of the movements
between pairs of photos placed in the *description.txt* file. **See the example __template_ directory**. The .npz files and the visualization images will be stored in 
the *[...]/test_data_sets/data_set_directory/pairs_data* directory. The debug photos
showing found feature points will be placed in the *[...]/test_data_sets/data_set_directory/debug_matches* directory.


<!-- Our current command:

`./match_pairs.py --input_dir ../image_processing/test_data_sets/circle_with_chess/ --output_dir ../image_processing/test_data_sets/circle_with_chess/pairs_data/ --input_pairs ../image_processing/test_data_sets/circle_with_chess/description.txt --viz --fast_viz --resize -1 --match_threshold 0.3 --shuffle --max_keypoints 50 --nms_radius 30`

`./match_pairs.py --input_dir ../image_processing/test_data_sets/jbl_test_photos/ --output_dir ../image_processing/test_data_sets/jbl_test_photos/jbl_pairs/ --input_pairs ../image_processing/test_data_sets/jbl_test_photos/jbl_pairs/description.txt --viz --fast_viz --resize -1 --match_threshold 0.3 --shuffle --max_keypoints 50 --nms_radius 30`

Previous description: 
`./match_pairs.py --input_dir arg --output_dir arg --input_pairs arg --viz --resize -1 --match_threshold 0.2 --max_keypoints 100`

`--input_dir` - directory with imput photos

`--output_dir` - directory to dump .npz results

`--input_pairs` - path to text description file: one line contains one pair, example: im1.jpg im2.jpg

`--viz` - put this option to visualize results (optional)

`--resize -1` - for not changing the output photo size!

`--match_threshold 0.2` - pairs accuracy tolerance

`--max_keypoints 100` - maximum number of keypoints to process -->