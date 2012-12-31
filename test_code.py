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
n_cats = 662
cats = range(n_cats)

my_models = {}
my_cats = []
my_voc_maps = {}
my_idfs = {}
my_platts = {}

voc = {}
stop_words = {}
idf = {}
id2cat = {}

url = 'http://www.google.ca'
from svm_server_util import multi_label_load_model, multi_label_load_idf, multi_label_load_feature_map, multi_label_load_platts_model, multi_label_prediction, multi_label_prediction_with_platts_pav_calibration_feature_shrinkage
from help_tools import read_stop_list, read_dict
from see_probability_estimation import read_model_choice, read_pav_parameters_by_ids
	

voc = read_dict(dict_fname, ",")
stop_words = read_stop_list(stop_fname)
my_cats = range(2)	
my_models = multi_label_load_model(my_cats, base_folder, base_model_file)
my_idfs = multi_label_load_idf(my_cats, base_folder, base_idf_file, ":")
my_voc_maps = multi_label_load_feature_map(my_cats, base_folder, base_local_dict_file, ":")
my_platts = multi_label_load_platts_model(my_cats, base_folder, base_model_para)
my_prob_model_choice = read_model_choice(base_prob_estimation_choice_file)
my_pav_models = read_pav_parameters_by_ids(my_cats, base_prob_estimation_folder, base_pav_model_ext)

from url_util import download_webpage
html = download_webpage(url)

from svm_server_util import from_html_to_svm_vector, multi_label_prediction_with_platts_calibration_feature_shrinkage
var_svm_vector = from_html_to_svm_vector(html, voc, stop_words)
var_probs, var_svm_len = multi_label_prediction_with_platts_pav_calibration_feature_shrinkage(var_svm_vector, my_cats, my_voc_maps, my_idfs, my_models, my_prob_model_choice, my_platts, my_pav_models, '')
