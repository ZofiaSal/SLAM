# SLAM - image processing

## Finding matches

Firstly, find feature points using SuperGlue solution.

Clone their repo: https://github.com/magicleap/SuperGluePretrainedNetwork

Run: 
`./match_pairs.py --input_dir arg --output_dir arg --input_pairs arg --viz --resize -1 --match_threshold 0.2 --max_keypoints 100`

`--input_dir` - directory with imput photos

`--output_dir` - directory to dump .npz results

`--input_pairs` - path to text description file: one line contains one pair, example: im1.jpg im2.jpg

`--viz` - put this option to visualize results (optional)

`--resize -1` - for not changing the output photo size!

`--match_threshold 0.2` - pairs accuracy tolerance

`--max_keypoints 100` - maximum number of keypoints to process