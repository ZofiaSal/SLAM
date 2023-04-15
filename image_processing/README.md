# SLAM - image processing

## Finding matches

Firstly, find feature points using SuperGlue solution.

Clone their repo: https://github.com/magicleap/SuperGluePretrainedNetwork

Our current command:

`./match_pairs.py --input_dir ../image_processing/test_data_sets/circle_with_chess/ --output_dir ../image_processing/test_data_sets/circle_with_chess/pairs_data/ --input_pairs ../image_processing/test_data_sets/circle_with_chess/description.txt --viz --fast_viz --resize -1 --match_threshold 0.3 --shuffle --max_keypoints 50 --nms_radius 30`

Previous description: 
`./match_pairs.py --input_dir arg --output_dir arg --input_pairs arg --viz --resize -1 --match_threshold 0.2 --max_keypoints 100`

`--input_dir` - directory with imput photos

`--output_dir` - directory to dump .npz results

`--input_pairs` - path to text description file: one line contains one pair, example: im1.jpg im2.jpg

`--viz` - put this option to visualize results (optional)

`--resize -1` - for not changing the output photo size!

`--match_threshold 0.2` - pairs accuracy tolerance

`--max_keypoints 100` - maximum number of keypoints to process