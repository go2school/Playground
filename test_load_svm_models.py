from svm_server_util import load_model
from help_tools import read_platts_model

cats = range(662)
base_folder = '/home/mpi/see_all_models/'
base_model_file = 'model_SEE_0.2'
base_platts_fname = 'model_SEE_0.2_addtional.txt'
for c in cats:
	m = load_model(base_folder + str(c) + '_' + base_model_file)	
	mode, A, B = read_platts_model(base_folder +  str(c) + '_' + base_platts_fname)	 
	if mode == 0:
		print m.get_nr_class()
	else:
		print c, mode
