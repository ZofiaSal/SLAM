# SLAM

## Finding fundamental matrix


Finding fundamental matrix. Feature points and matches are found using SuperGlue solution (credits: Magic Leap, Inc.).

To execute type: `./find_fundamental.py`.


The points are taken from `./dump_match_pairs/scene0711_00_frame-001680_scene0711_00_frame-001995_matches.npz`. This file is the result of `match_pairs.py` script from SuperGlue project: https://github.com/magicleap/SuperGluePretrainedNetwork
Example file is already here.


To execute `match_pairs.py` script clone SuperGlue repo and run:

`./match_pairs.py --input_dir dir_with_images_to_compare --output_dir path_to_dump_match_pairs_dir`

## References

https://sourishghosh.com/2016/fundamental-matrix-from-camera-matrices/

https://www.robots.ox.ac.uk/~vgg/hzbook/hzbook1/HZepipolar.pdf
