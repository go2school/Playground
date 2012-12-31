from time import time

#end global variables for model

base_folder = '/home/mpi/query_bing_models/'
base_model_file = 'model_query_bing'
base_idf_file = 'idf_query_bing'
base_local_dict_file = 'feature_indices_query_bing'
base_model_para = 'model_query_bing_addtional.txt'

dict_fname = '/home/mpi/query_bing_project/query_bing_rare_removed_3.txt'
stop_fname = 'new_english.stop'	
schema = 'uwo'
table = 'uwo_query_bing_nutch_svm_vector'

import simplejson as json
query_id2cat = 'query_other_id2name.js'
fd = open(query_id2cat)
ct = fd.read()
fd.close()
b = ct.index('=')
id2cat = json.loads(ct[b+1:])

#my_cats = [0,298,336,403,788,1060,1106,1162,1181,1209]
my_cats = [403]

#enlarge positive weight by half, one, two
pos_factors = [1, 0.5, 2]

input_svm = '/home/mpi/uwo_query_bing_workingspace/uwo_query_bing_id_svm.txt'
#output_dir = '/home/mpi/uwo_query_bing_parameter_prediction/'
#output_prob_postfix = 'uwo_query_bing_parameter_probability.txt'

#init library	
#with global variables
from help_tools import read_id_cat			
from active_learning import Node		

start = time()

import os
os.chdir("/home/mpi/query_search_project/")
from svm_server_util import *
from svm_checker_helper import *
from help_tools import read_stop_list, read_dict

inverse_dict = read_inverse_dict_query_bing(dict_fname, ' ')
whole_dict = read_dict_query_bing_freq(dict_fname, ' ')
predict_param = ''
my_models = multi_label_load_model(my_cats, base_folder, base_model_file)
my_idfs = multi_label_load_idf(my_cats, base_folder, base_idf_file, ":")
my_voc_maps = multi_label_load_feature_map(my_cats, base_folder, base_local_dict_file, ":")
my_platts = multi_label_load_platts_model(my_cats, base_folder, base_model_para)
my_inverse_voc_maps = multi_label_load_inverse_feature_map(my_cats, base_folder, base_local_dict_file, ':')

#read probability choice
#added by xiao 01242012
#mec.execute('my_prob_model_choices = read_model_choice(base_prob_estimation_choice_file)')
#mec.execute('my_pav_models = read_pav_parameters_by_ids(my_cats, base_prob_estimation_folder, base_pav_model_ext)')	

#do svm prediction
id = 345940
example =  query_a_page_from_db_query_bing(schema, table, id)
probs = adv_example_based_multi_label_prediction_with_platts_feature_shrinkage(example, my_cats, my_voc_maps, my_idfs, my_models, my_platts, predict_param)
#map the results into word space
wt = [0,0,0,0]	
wt[0] = probs[0]
wt[1] = probs[1]
vwt = [(id2cat[str(w[0])], w[1]) for w in wt[0]]
vlength = [(id2cat[str(w[0])], w[1]) for w in wt[1]]
wt[2] = map_svm_feature_list_by_id_to_words(my_cats, probs[2], my_inverse_voc_maps, inverse_dict)
wt[3] = map_svm_feature_list_by_id_to_words(my_cats, probs[3], my_inverse_voc_maps, inverse_dict)
				
				
pos_score = [wt[3][403][i][1] * wt[2][403][i][1] for i  in range(len(wt[3][403])) if wt[3][403][i][1] > 0]
pos_feature = [wt[3][403][i][0] for i  in range(len(wt[3][403])) if wt[3][403][i][1] > 0]
neg_score = [wt[3][403][i][1] * wt[2][403][i][1] for i  in range(len(wt[3][403])) if wt[3][403][i][1] <= 0]

