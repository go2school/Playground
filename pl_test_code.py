from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
from svm_server_util import extract_doc_id
from IPython.parallel import Client
from time import time
import BaseHTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from threading import Lock
import urllib
#global variable for model
mec = None
root = None
rc = None
#end global variables for model

#synchronized variable
lock = None

dict_fname = 'see_dmoz_dictionary0102.txt'
stop_fname = 'new_english.stop'
idf_fname = 'food_idf.txt'

#base_model_file = '/home/xiao/liblinear-1.8/python/food_model'
#n_cats = 3
"""
base_folder = '/home/mpi/see_all_models/'
base_prob_estimation_folder = '/home/mpi/SEE_Probability_Estimation/pav_model'
base_prob_estimation_choice_file = '/home/mpi/SEE_Probability_Estimation/best_parameter.txt'
"""
base_folder = '/home/xiao/see_all_models/'
base_prob_estimation_folder = '/home/xiao/SEE_Probability_Estimation/pav_model'
base_prob_estimation_choice_file = '/home/xiao/SEE_Probability_Estimation/best_parameter.txt'
base_model_file = 'model_SEE_0.2'
base_idf_file = 'idf_SEE_0.2'
base_local_dict_file = 'feature_indices_SEE_0.2'
base_model_para = 'model_SEE_0.2_addtional.txt'
base_pav_model_ext = 'SEE_0.2_pav_model'
n_cats = 4
cats = range(n_cats)

rc = Client()	
mec = rc[:]
mec.execute('import os')
mec.execute('os.chdir("/media/01CC16F5ED7072F0/seeuwo/query_bing")')	
mec.execute('from svm_server_util import multi_label_load_model, multi_label_load_idf, multi_label_load_feature_map, multi_label_load_platts_model, multi_label_prediction')
mec.execute('from help_tools import read_stop_list, read_dict')
mec.execute('from see_probability_estimation import read_model_choice, read_pav_parameters_by_ids')

#create lock variable
lock = Lock()

#init models
#each machines load parts of the models	
mec['base_model_file'] = base_model_file	
mec['base_folder'] = base_folder
mec['base_local_dict_file'] = base_local_dict_file
mec['base_idf_file'] = base_idf_file
mec['base_model_para'] = base_model_para
mec['stop_fname'] = stop_fname
mec['dict_fname'] = dict_fname
mec['predict_param'] = ''
mec['base_prob_estimation_folder'] = base_prob_estimation_folder
mec['base_prob_estimation_choice_file'] = base_prob_estimation_choice_file
mec['base_pav_model_ext'] = base_pav_model_ext
mec.scatter('my_cats', cats)
mec.execute('my_models = multi_label_load_model(my_cats, base_folder, base_model_file)')
mec.execute('my_idfs = multi_label_load_idf(my_cats, base_folder, base_idf_file, ":")')
mec.execute('my_voc_maps = multi_label_load_feature_map(my_cats, base_folder, base_local_dict_file, ":")')
mec.execute('my_platts = multi_label_load_platts_model(my_cats, base_folder, base_model_para)')
mec.execute('stop_words = read_stop_list(stop_fname)')
mec.execute('voc = read_dict(dict_fname, ",")')	
#read probability choice
#added by xiao 01242012
mec.execute('my_prob_model_choice = read_model_choice(base_prob_estimation_choice_file)')
mec.execute('my_pav_models = read_pav_parameters_by_ids(my_cats, base_prob_estimation_folder, base_pav_model_ext)')

import uuid
suffix_lst = [str(uuid.uuid4()).replace('-','') for i in range(10)]
var_html = 'html_' + suffix_lst[0]
var_title = 'title_' + suffix_lst[0]
var_body = 'body_' + suffix_lst[0]				
var_predicted_cats = 'predicted_cats_' + suffix_lst[1]
var_svm_vector = 'svm_vector_' + suffix_lst[2]
var_probs = 'probs_' + suffix_lst[3]
var_svm_len = 'len_svm_vectors_' + suffix_lst[4]

url = 'http://www.google.ca'
from url_util import download_webpage
html = download_webpage(url)
mec[var_html] = html	
mec[var_predicted_cats] = cats									
mec.execute('from svm_server_util import from_html_to_svm_vector, multi_label_prediction_with_platts_pav_calibration_feature_shrinkage')																			
mec.execute(var_svm_vector + ' = from_html_to_svm_vector(' + var_html + ', voc, stop_words)')

mec.execute(var_probs + ', ' + var_svm_len + ' = multi_label_prediction_with_platts_pav_calibration_feature_shrinkage('+var_svm_vector+', '+var_predicted_cats+', my_voc_maps, my_idfs, my_models, my_prob_model_choice, my_platts, my_pav_models, predict_param)')			
