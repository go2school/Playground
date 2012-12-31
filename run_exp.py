import os
"""
execfile('make_dataset.py')
execfile('make_tf_idf.py')
execfile('dataset_util.py')
"""
os.system('/home/xiao/liblinear-1.8/train -s 6 food_training_data.txt food_model')
os.system('/home/xiao/liblinear-1.8/predict -b 1 food_training_data.txt food_model food_prediction.txt')
os.system('/home/xiao/liblinear-1.8/predict -b 1 uwo_food_tf_idf.txt food_model uwo_food_prediction.txt')
execfile('compute_loss.py')
