from IPython.parallel import Client
from time import time

#end global variables for model

dict_fname = 'see_dmoz_dictionary0102.txt'
stop_fname = 'new_english.stop'

base_folder = '/home/mpi/see_all_models/'
base_prob_estimation_folder = '/home/mpi/SEE_Probability_Estimation/pav_model'
base_prob_estimation_choice_file = '/home/mpi/SEE_Probability_Estimation/best_parameter.txt'

base_model_file = 'model_SEE_0.2'
base_idf_file = 'idf_SEE_0.2'
base_local_dict_file = 'feature_indices_SEE_0.2'
base_model_para = 'model_SEE_0.2_addtional.txt'
base_pav_model_ext = 'SEE_0.2_pav_model'

n_cats = 662
cats = range(n_cats)

#enlarge positive weight by two
#pos_factors = [0.25, 0.5, 4]
pos_factors = [1, 0.5, 2]

#cats = [2, 39, 410, 447, 300, 555]
#prediction parameters
"""
input_svm = '/home/mpi/uwo_svm.txt'
output_dir = '/home/mpi/uwo_prediction/'
output_prob_postfix = 'uwo_probability.txt'

input_svm = '/home/mpi/uwo_schulich_svm.txt'
output_dir = '/home/mpi/uwo_schulich_prediction/'
output_prob_postfix = 'uwo_probability.txt'
"""

input_svm = '/home/mpi/uwo_new_svm.txt'
output_dir = '/home/mpi/uwo_parameter_prediction/'
output_prob_postfix = 'uwo_parameter_probability.txt'

input_svm = '/home/mpi/westernmustangs_svm.txt'
output_dir = '/home/mpi/mustangs_parameter_prediction/'
output_prob_postfix = 'mustangs_parameter_probability.txt'

input_svm = '/home/mpi/uwo_to_do_svm.txt'
output_dir = '/home/mpi/uwo_to_do_prediction/'
output_prob_postfix = 'to_do_parameter_probability.txt'

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
mec['stop_fname'] = stop_fname
mec['dict_fname'] = dict_fname
mec['predict_param'] = ''
mec['output_dir'] = output_dir
mec['base_prob_estimation_folder'] = base_prob_estimation_folder
mec['base_prob_estimation_choice_file'] = base_prob_estimation_choice_file
mec['base_pav_model_ext'] = base_pav_model_ext
mec['input_svm'] = input_svm
mec['output_prob_postfix'] = output_prob_postfix
mec['pos_factors'] = pos_factors

#dispatch jobs
mec.scatter('my_cats', cats)

mec.execute('my_models = multi_label_load_model(my_cats, base_folder, base_model_file)')
mec.execute('my_idfs = multi_label_load_idf(my_cats, base_folder, base_idf_file, ":")')
mec.execute('my_voc_maps = multi_label_load_feature_map(my_cats, base_folder, base_local_dict_file, ":")')
mec.execute('my_platts = multi_label_load_platts_model(my_cats, base_folder, base_model_para)')
mec.execute('stop_words = read_stop_list(stop_fname)')
mec.execute('voc = read_dict(dict_fname, ",")')	
#read probability choice
#added by xiao 01242012
mec.execute('my_prob_model_choices = read_model_choice(base_prob_estimation_choice_file)')
mec.execute('my_pav_models = read_pav_parameters_by_ids(my_cats, base_prob_estimation_folder, base_pav_model_ext)')	

#do svm prediction
mec.execute('file_based_parameter_multi_label_prediction_with_platts_pav_calibration_feature_shrinkage(input_svm, output_dir, output_prob_postfix, pos_factors, my_cats, my_voc_maps, my_idfs, my_models, my_prob_model_choices, my_platts, my_pav_models, "")')

end = time()

print 'using time as ' + str(end - start) + ' seconds'
