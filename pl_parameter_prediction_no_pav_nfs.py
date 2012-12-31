from IPython.parallel import Client
from time import time

#end global variables for model

base_folder = '/home/mpi/shareddir/query_bing_models/'

base_model_file = 'model_query_bing'
base_idf_file = 'idf_query_bing'
base_local_dict_file = 'feature_indices_query_bing'
base_model_para = 'model_query_bing_addtional.txt'

used_cats_fname = '/home/mpi/uwo_query_bing_workingspace/used_tree_nodes.txt'
cats = []
fd = open(used_cats_fname)
for line in fd:
	cats.append(int(line.strip()))
fd.close()

#enlarge positive weight by half, one, two
pos_factors = [1, 0.5, 2]

input_svm = '/home/mpi/uwo_query_bing_workingspace/uwo_query_bing_id_svm.txt'
output_dir = '/home/mpi/shareddir/uwo_query_bing_parameter_prediction/'
output_prob_postfix = 'uwo_query_bing_parameter_probability.txt'

#init library	
#with global variables
from help_tools import read_id_cat			
from active_learning import Node		

start = time()

rc = Client()

#set up as blocking mode	
mec = rc[:]
mec.block = True

mec.execute('import os')
mec.execute('os.chdir("/home/mpi/query_search_project/")')	
mec.execute('from svm_server_util import *')
mec.execute('from svm_checker_helper import *')
mec.execute('from help_tools import read_stop_list, read_dict')
mec.execute('from see_probability_estimation import read_model_choice, read_pav_parameters_by_ids')

#init models
#each machines load parts of the models	
mec['base_model_file'] = base_model_file	
mec['base_folder'] = base_folder
mec['base_local_dict_file'] = base_local_dict_file
mec['base_idf_file'] = base_idf_file
mec['base_model_para'] = base_model_para
mec['predict_param'] = ''
mec['output_dir'] = output_dir
mec['input_svm'] = input_svm
mec['output_prob_postfix'] = output_prob_postfix
mec['pos_factors'] = pos_factors

#dispatch jobs
mec.scatter('my_cats', cats)

mec.execute('my_models = multi_label_load_model(my_cats, base_folder, base_model_file)')
mec.execute('my_idfs = multi_label_load_idf(my_cats, base_folder, base_idf_file, ":")')
mec.execute('my_voc_maps = multi_label_load_feature_map(my_cats, base_folder, base_local_dict_file, ":")')
mec.execute('my_platts = multi_label_load_platts_model(my_cats, base_folder, base_model_para)')
#read probability choice
#added by xiao 01242012
#mec.execute('my_prob_model_choices = read_model_choice(base_prob_estimation_choice_file)')
#mec.execute('my_pav_models = read_pav_parameters_by_ids(my_cats, base_prob_estimation_folder, base_pav_model_ext)')	

#do svm prediction
mec.execute('file_based_parameter_multi_label_prediction_with_platts_calibration_feature_shrinkage(input_svm, output_dir, output_prob_postfix, pos_factors, my_cats, my_voc_maps, my_idfs, my_models, my_platts, "")')

end = time()

print 'using time as ' + str(end - start) + ' seconds'
