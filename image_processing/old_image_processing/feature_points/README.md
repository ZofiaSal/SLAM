# SLAM

## Finding fundamental matrix


Finding fundamental matrix. Feature points and matches are found using SuperGlue solution (credits: Magic Leap, Inc.).

To execute type: `./find_fundamental.py`.


The points are taken from `./dump_match_pairs/scene0711_00_frame-001680_scene0711_00_frame-001995_matches.npz`. This file is the result of `match_pairs.py` script from SuperGlue project: https://github.com/magicleap/SuperGluePretrainedNetwork
Example file is already here.


To execute `match_pairs.py` script clone SuperGlue repo and run:

`./match_pairs.py --input_dir dir_with_images_to_compare --output_dir path_to_dump_match_pairs_dir`

"You can provide your own list of pairs `--input_pairs` for images contained in `--input_dir`. [...] Each line corresponds to one pair and is structured as follows:

```
path_image_A path_image_B 
```
"
Example in `assets/phototourism_test_pairs.txt` in SuperGlue repository.

`--viz` -> outputs a visualisation of those pairs 

`--resize -1` -> for not changing the size of the pictures!!

`--match_threshold 0.2`  


np:
./SuperGluePretrainedNetwork/match_pairs.py --input_dir ./ --output_dir ./ --input_pairs ./pairs_super_glue.txt --resize -1 --viz --match_threshold 0.6
## References

https://sourishghosh.com/2016/fundamental-matrix-from-camera-matrices/

https://www.robots.ox.ac.uk/~vgg/hzbook/hzbook1/HZepipolar.pdf
