# SLAM - image processing: 3D reconstruction

## Reconstruction 3D from handmade matches

Run the reconstruction:

`python reconstructionHandmade.py --data 'data_set_directory'`

Replace `data_set_directory` with the appropriate name.
The `data_set_directory` should be placed in _/SLAM/image_processing/test_data_sets_.
The _points_pairs.py_ file with source matches should be placed in _data_set_directory/handmade_matches_. The source photos (for debug output) should be placed in
_data_set_directory/source_photos_. The description of the movement should be placed in
_data_set_directory/source_photos/movement.py_ file. The debug output photos will be placed
in _data_set_directory/handmade_matches/debug_handmade_matches_. The output 3D points will be 
placed in the _data_set_directory/handmade_matches/output.py_ file.

See the _test_data_sets/_template_ directory for the model directory tree.

