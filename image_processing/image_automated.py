import subprocess

subprocess.run([
                'python', 
                '../SuperGluePretrainedNetwork/match_pairs.py', 
                '--input_dir', './test_data_sets/circle_with_chess/', 
                '--output_dir', './test_data_sets/circle_with_chess/pairs_data/',
                '--input_pairs', './test_data_sets/circle_with_chess/pairs_data/description.txt', 
                '--viz', '--fast_viz', 
                '--resize', '-1', 
                '--match_threshold', '0.3', 
                '--shuffle', 
                '--max_keypoints', '50', 
                '--nms_radius', '30'
                ])