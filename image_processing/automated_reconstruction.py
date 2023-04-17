import subprocess

# data set directory
# put the photos in 'data_set' directory,
# put the 'pairs_data' directory inside (for the putput)
# put the 'description.txt' file inside 'pairs_data'
data_set = 'circle_with_chess'

# Run the SuperGluePretrainedNetwork

subprocess.run([
                'python', 
                '../SuperGluePretrainedNetwork/match_pairs.py', 
                '--input_dir', './test_data_sets/' + data_set, 
                '--output_dir', './test_data_sets/' + data_set + '/pairs_data',
                '--input_pairs', './test_data_sets/' + data_set + '/pairs_data/description.txt', 
                '--viz', '--fast_viz', # visualize the matches
                '--resize', '-1', # must be (do not resize the image)
                '--match_threshold', '0.3', # match tolerance: the more the more tolerant
                '--shuffle', # shuffle the pairs before cutting off the list
                '--max_keypoints', '50', # before matching
                '--nms_radius', '30' # don't allow keypoints to be too close to each other
                ])