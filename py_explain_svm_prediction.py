if __name__ == '__main__':
	import sys	
	from svm_checker_helper import *
	from see_probability_estimation import commpute_pav_probability			
	from active_learning import *
	
	n_cats= 2
	#cats = [0, 85, 157, 224, 275, 304, 349, 369, 466, 564, 627, 423, 189]
	#cats = [0, 85, 157, 224, 275, 304, 349, 369, 466, 564, 627]
	#cats = [0, 85, 157, 304, 349, 369, 564, 627, 423]
	#cats = [0, 1, 5, 6, 2, 3, 4]
	#cats = [0, 1, 2, 157, 184, 186]
	cats = [157]
	#cats = [0, 564]
	#cats = range(662)
	my_cats = cats
	#setup configuration
	dmoz_id2cat_fname = 'dmoz_id2cat.js'
	dict_fname = 'see_dmoz_dictionary0102.txt'
	stop_fname = 'new_english.stop'	
	base_folder = '/home/mpi/see_all_models/'
	base_model_file = 'model_SEE_0.2'
	base_idf_file = 'idf_SEE_0.2'
	base_local_dict_file = 'feature_indices_SEE_0.2'
	base_model_para = 'model_SEE_0.2_addtional.txt'
	base_prob_estimation_folder = '/home/mpi/SEE_Probability_Estimation/pav_model'
	base_prob_estimation_choice_file = '/home/mpi/SEE_Probability_Estimation/best_parameter.txt'	
	base_pav_model_ext = 'SEE_0.2_pav_model'
	#read cat mapping
	fd = open(dmoz_id2cat_fname)
	ct = fd.read()
	fd.close()
	id2cat = json.loads(ct)
	#read dictionary
	inverse_dict = read_inverse_dict(dict_fname, ',')
	#load model parameters
	from see_probability_estimation import read_model_choice, read_pav_parameters_by_ids	
	my_models = multi_label_load_model(my_cats, base_folder, base_model_file)	
	my_idfs = multi_label_load_idf(my_cats, base_folder, base_idf_file, ':')
	my_voc_maps = multi_label_load_feature_map(my_cats, base_folder, base_local_dict_file, ':')
	my_inverse_voc_maps = multi_label_load_inverse_feature_map(my_cats, base_folder, base_local_dict_file, ':')
	my_platts_models = multi_label_load_platts_model(my_cats, base_folder, base_model_para)
	my_prob_model_choices = read_model_choice(base_prob_estimation_choice_file)
	my_pav_models = read_pav_parameters_by_ids(my_cats, base_prob_estimation_folder, base_pav_model_ext)
	
