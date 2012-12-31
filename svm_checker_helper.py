from svm_server_util import *
from help_tools import *
import simplejson as json
def extract_related_svm_weight(feature_ids, svm_model):
	weights = []
	for f in feature_ids:
		#svm weight index should be minus by one
		#as it is started at zero
		weights.append((f, svm_model.w[f-1]))
	return weights
		
def map_svm_feature_id_to_words(cats, my_vectors, my_inverse_voc_maps, inverse_dict):
	words = {}
	for c in cats:
		if c in my_vectors:
			new_word_list = []
			old_words = my_vectors[c]
			for w in old_words:
				new_word_list.append((inverse_dict[my_inverse_voc_maps[c][w[0]]], w[1]))
			words[c] = new_word_list
	return words
	
def map_svm_feature_list_by_id_to_words(cats, my_vectors, my_inverse_voc_maps, inverse_dict):
	words = {}
	for c in cats:
		for vector in my_vectors:
			if vector[0] == c:
				new_word_list = []
				old_words = vector[1]
				for w in old_words:
					new_word_list.append((inverse_dict[my_inverse_voc_maps[c][w[0]]], w[1]))
				words[c] = new_word_list
	return words
		
def query_a_page_from_db(id):
	import MySQLdb
	con   =   MySQLdb.connect(host="192.168.0.2",  port=3306, user="root",  passwd="see",  db="uwo")  
	cursor   =   con.cursor()  
	sql  ='select * from uwo.uwo_new_nutch_svm_vector where id =' + str(id)	
	cursor.execute(sql)
	row = cursor.fetchone()
	cursor.close()
	con.close()
	if row != None:
		return str(row[0]) + ' ' + row[1]
	else:
		return ''	

def query_a_page_from_db_query_bing(schema, table, id):
	import MySQLdb
	con   =   MySQLdb.connect(host="192.168.0.2",  port=3306, user="root",  passwd="see",  db="uwo")  
	cursor   =   con.cursor()  
	sql  ='select * from '+schema+'.'+table+' where id =' + str(id)	
	cursor.execute(sql)
	row = cursor.fetchone()
	cursor.close()
	con.close()
	if row != None:
		return str(row[0]) + ' ' + row[1]
	else:
		return ''
				
def query_a_page_from_clueweb09_db(id):
	import MySQLdb
	con   =   MySQLdb.connect(host="192.168.0.2",  port=3306, user="root",  passwd="see",  db="clueweb09")  
	cursor   =   con.cursor()  
	sql  ='select svm_feature from clueweb09.webpages where id ="' + str(id)	 + '"'
	cursor.execute(sql)
	row = cursor.fetchone()
	cursor.close()
	con.close()
	if row != None:
		return row[0]
	else:
		return ''			
	
def example_based_multi_label_prediction_with_platts_pav_calibration_feature_shrinkage(str_example, cats, voc_maps, idfs, models, prob_model_choices, platts_models, pav_models, predict_param, tf_or_tf_idf):
	from make_tf_idf import compute_tf_idf_by_vector, compute_tf_by_vector
	from see_probability_estimation import commpute_pav_probability		
	probs = {}
	scores = {}
	tf_idfs = {}
	svm_weights = {}
	features_c = {}
	for c in cats:
		if c in models:
			#read and predict features
			line = str_example.strip().split(' ')			
			id = line[0]
			svm_vector = []
			for l in line[1:]:
				word, occ = l.split(':')
				svm_vector.append((int(word), int(occ)))	
			#map the input vector to the shrinked vector space							
			shrinked_vector = [(voc_maps[c][v[0]], v[1]) for v in svm_vector if v[0] in voc_maps[c]]			
			#make tf idf
			if tf_or_tf_idf == 'tf':
				tf_idf = compute_tf_by_vector(shrinked_vector, idfs[c])
			else:
				tf_idf = compute_tf_idf_by_vector(shrinked_vector, idfs[c])				
			#make SVM feature
			features = {}
			feature_ids = []
			for wd in tf_idf:
				features[wd[0]] = wd[1]
				feature_ids.append(wd[0])
			#extract related svm weight		
			if platts_models[c][0] == 0:				
				svm_weight = extract_related_svm_weight(feature_ids, models[c])
			else:
				svm_weight = []
			#do prediction
			p_label, p_acc, p_val = do_svm_prediction(models[c], platts_models[c], 1, features, predict_param)				
			#make probability
			if prob_model_choices[c] == 'PLATTS':
				calibrated_prob = platts_calibration(p_val[0][0], platts_models[c][0], platts_models[c][1], platts_models[c][2])
			else:
				calibrated_prob = commpute_pav_probability(pav_models[c], p_val[0][0])
			#book results
			probs[c] = calibrated_prob
			#sort feature by positive weight
			tf_idfs[c] = sorted(tf_idf, key=lambda s:s[1], reverse=True)
			svm_weights[c] = sorted(svm_weight, key=lambda s:s[1], reverse=True)
			scores[c] = p_val[0][0]
			features_c[c] = features
	return probs, scores, tf_idfs, svm_weights, features_c
	
def webserver_example_based_multi_label_prediction_with_platts_pav_calibration_feature_shrinkage(str_example, cats, voc_maps, idfs, models, prob_model_choices, platts_models, pav_models, predict_param):
	from make_tf_idf import compute_tf_idf_by_vector
	from see_probability_estimation import commpute_pav_probability		
	probs = []
	len_vectors = []
	for c in cats:
		if c in models:
			#read and predict features
			line = str_example.strip().split(' ')			
			id = line[0]
			svm_vector = []
			for l in line[1:]:
				word, occ = l.split(':')
				svm_vector.append((int(word), int(occ)))	
			#map the input vector to the shrinked vector space							
			shrinked_vector = [(voc_maps[c][v[0]], v[1]) for v in svm_vector if v[0] in voc_maps[c]]			
			#make tf idf			
			tf_idf = compute_tf_idf_by_vector(shrinked_vector, idfs[c])				
			#make SVM feature
			features = {}
			for wd in tf_idf:
				features[wd[0]] = wd[1]
			#do prediction
			p_label, p_acc, p_val = do_svm_prediction(models[c], platts_models[c], 1, features, predict_param)				
			#make probability
			if prob_model_choices[c] == 'PLATTS':
				calibrated_prob = platts_calibration(p_val[0][0], platts_models[c][0], platts_models[c][1], platts_models[c][2])
			else:
				calibrated_prob = commpute_pav_probability(pav_models[c], p_val[0][0])
			#book results
			probs.append((c, calibrated_prob))
			len_vectors.append((c, len(features)))					
	return probs, len_vectors

def adv_example_based_multi_label_prediction_with_platts_feature_shrinkage(str_example, cats, voc_maps, idfs, models, platts_models, predict_param):
	from make_tf_idf import compute_tf_idf_by_vector	
	probs = []
	len_vectors = []
	example_weights = []
	svm_weights = []
	for c in cats:
		if c in models:
			#read and predict features
			line = str_example.strip().split(' ')			
			id = line[0]
			svm_vector = []
			for l in line[1:]:
				word, occ = l.split(':')
				svm_vector.append((int(word), int(occ)))	
			#map the input vector to the shrinked vector space							
			shrinked_vector = [(voc_maps[c][v[0]], v[1]) for v in svm_vector if v[0] in voc_maps[c]]			
			#make tf idf			
			tf_idf = compute_tf_idf_by_vector(shrinked_vector, idfs[c])				
			#make SVM feature
			features = {}
			feature_ids = []
			for wd in tf_idf:
				features[wd[0]] = wd[1]
				feature_ids.append(wd[0])
			#extract related svm weight
			if platts_models[c][0] == 0:				
				svm_weight = extract_related_svm_weight(feature_ids, models[c])
			else:
				svm_weight = []
			#do prediction
			p_label, p_acc, p_val = do_svm_prediction(models[c], platts_models[c], 1, features, predict_param)				
			#make probability			
			calibrated_prob = platts_calibration(p_val[0][0], platts_models[c][0], platts_models[c][1], platts_models[c][2])			
			#book results
			probs.append((c, calibrated_prob))
			len_vectors.append((c, len(features)))					
			example_weights.append((c, tf_idf))
			svm_weights.append((c, svm_weight))			
	return probs, len_vectors, example_weights, svm_weights
		
def adv_webserver_example_based_multi_label_prediction_with_platts_pav_calibration_feature_shrinkage(str_example, cats, voc_maps, idfs, models, prob_model_choices, platts_models, pav_models, predict_param):
	from make_tf_idf import compute_tf_idf_by_vector
	from see_probability_estimation import commpute_pav_probability		
	probs = []
	len_vectors = []
	example_weights = []
	svm_weights = []
	for c in cats:
		if c in models:
			#read and predict features
			line = str_example.strip().split(' ')			
			id = line[0]
			svm_vector = []
			for l in line[1:]:
				word, occ = l.split(':')
				svm_vector.append((int(word), int(occ)))	
			#map the input vector to the shrinked vector space							
			shrinked_vector = [(voc_maps[c][v[0]], v[1]) for v in svm_vector if v[0] in voc_maps[c]]			
			#make tf idf			
			tf_idf = compute_tf_idf_by_vector(shrinked_vector, idfs[c])				
			#make SVM feature
			features = {}
			feature_ids = []
			for wd in tf_idf:
				features[wd[0]] = wd[1]
				feature_ids.append(wd[0])
			#extract related svm weight
			if platts_models[c][0] == 0:				
				svm_weight = extract_related_svm_weight(feature_ids, models[c])
			else:
				svm_weight = []
			#do prediction
			p_label, p_acc, p_val = do_svm_prediction(models[c], platts_models[c], 1, features, predict_param)				
			#make probability
			if prob_model_choices[c] == 'PLATTS':
				calibrated_prob = platts_calibration(p_val[0][0], platts_models[c][0], platts_models[c][1], platts_models[c][2])
			else:
				calibrated_prob = commpute_pav_probability(pav_models[c], p_val[0][0])
			#book results
			probs.append((c, calibrated_prob))
			len_vectors.append((c, len(features)))					
			example_weights.append((c, tf_idf))
			svm_weights.append((c, svm_weight))			
	return probs, len_vectors, example_weights, svm_weights
		
def get_positive_and_negative_word_score(examples_weight, svm_weight):
	wd = {}#word weight table
	sd = {}#svm weight table
	for w in examples_weight:
		wd[w[0]] = w[1]
	for w in svm_weight:
		sd[w[0]] = w[1]	
	s_pos = sum([wd[w] * sd[w] for w in wd.keys() if sd[w] > 0])
	s_neg = sum([wd[w] * sd[w] for w in wd.keys() if sd[w] < 0])	
	return s_pos, s_neg		

def make_modified_probability(old_probs, threshold, len_threshold, repredict_other_threshold, node, examples_weights, svm_models, platts_models, pav_models, prob_model_choices):
	from see_probability_estimation import commpute_pav_probability	
	from svm_server_util import platts_calibration
	
	#check if it is short
	for c in node.children:
		#check if it is short example
		if len(examples_weights[c.labelIndex]) < len_threshold:	
			print 'short doc'
			s_pos, s_neg = get_positive_and_negative_word_score(examples_weights[c.labelIndex], svm_models[c.labelIndex])
			#cut the positive weight score by half, hopefully to predict more negative examples
			s = s_pos * 0.5 + s_neg
			if prob_model_choices[c.labelIndex] == 'PLATTS':
				calibrated_prob = platts_calibration(s, platts_models[c.labelIndex][0], platts_models[c.labelIndex][1], platts_models[c.labelIndex][2])
			else:
				calibrated_prob = commpute_pav_probability(pav_models[c.labelIndex], s)
			old_probs[c.labelIndex] = calibrated_prob
	#check if this example does not predict any category (check if it is other)
	is_other = True
	for c in node.children:
		if old_probs[c.labelIndex] >= threshold:
			is_other = False
			break
	if is_other == False:
		for c in node.children:			
			x = 0
			#make_modified_probability(old_probs, threshold, len_threshold, c.labelIndex, examples_weights, svm_models, platts_models, pav_models, prob_model_choices, new_probs)	
	else:
		print 'other doc'
		#increase the positive score		
		for c in node.children:
			#check if it is too small
			if old_probs[c.labelIndex] >= repredict_other_threshold:
				s_pos, s_neg = get_positive_and_negative_word_score(examples_weights[c.labelIndex], svm_models[c.labelIndex])
				#cut the positive weight score by half, hopefully to predict more negative examples
				s = s_pos * 2 + s_neg
				if prob_model_choices[c.labelIndex] == 'PLATTS':
					calibrated_prob = platts_calibration(s, platts_models[c.labelIndex][0], platts_models[c.labelIndex][1], platts_models[c.labelIndex][2])
				else:
					calibrated_prob = commpute_pav_probability(pav_models[c.labelIndex], s)
				old_probs[c.labelIndex] = calibrated_prob				
	
#given an example, find positive weight and negative weight of svm
#reprdict its probability
#assume the cat is in my model
def make_calibrated_prediction(c, old_prob, str_example, pos_factor, repredict_other_threshold, voc_maps, idfs, svm_models, platts_models, pav_models, prob_model_choices):
	from make_tf_idf import compute_tf_idf_by_vector
	from see_probability_estimation import commpute_pav_probability		
	from svm_server_util import platts_calibration
	
	#check if its model existed
	#if it uses platts calibration but it does not have model, we directly return the old prob
	if prob_model_choices[c] == 'PLATTS' and platts_models[c][0] != 0:
		calibrated_prob = old_prob
	else:
		#read and predict features
		line = str_example.strip().split(' ')			
		id = line[0]
		svm_vector = []
		for l in line[1:]:
			word, occ = l.split(':')
			svm_vector.append((int(word), int(occ)))	
		#map the input vector to the shrinked vector space							
		shrinked_vector = [(voc_maps[c][v[0]], v[1]) for v in svm_vector if v[0] in voc_maps[c]]			
		#make tf idf			
		tf_idf = compute_tf_idf_by_vector(shrinked_vector, idfs[c])				
		#make SVM feature
		features = {}
		feature_ids = []
		for wd in tf_idf:
			features[wd[0]] = wd[1]
			feature_ids.append(wd[0])
		#extract related svm weight					
		svm_weight = extract_related_svm_weight(feature_ids, models[c])
		#get positive weight and negative weight
		s_pos, s_neg = get_positive_and_negative_word_score(tf_idf, svm_weight)
		#cut the positive weight score by half, hopefully to predict more negative examples
		s = s_pos * pos_factor + s_neg	
		if prob_model_choices[c] == 'PLATTS':
			calibrated_prob = platts_calibration(s, platts_models[c][0], platts_models[c][1], platts_models[c][2])
		else:
			calibrated_prob = commpute_pav_probability(pav_models[c], s)
	return (c, calibrated_prob)
		
def file_based_positive_enlarged_multi_label_prediction_with_platts_pav_calibration_feature_shrinkage(in_fname, out_dir, out_fname_pattern, pos_factor, cats, voc_maps, idfs, models, prob_model_choices, platts_models, pav_models, predict_param):
	from make_tf_idf import compute_tf_idf_by_vector
	from see_probability_estimation import commpute_pav_probability		
	for c in cats:
		if c in models:
			#read and predict features
			fd = open(in_fname)
			fd_w = open(out_dir + '/' + str(c)+ '_' + out_fname_pattern, 'w')
			for line in fd:
				#if I use platts but without model, then I predict it as 0, 1 or 0.5
				if prob_model_choices[c] == 'PLATTS' and platts_models[c][0] != 0:
					calibrated_prob = platts_calibration(0, platts_models[c][0], platts_models[c][1], platts_models[c][2])
				else:
					#extract SVM example features
					line = line.strip().split(' ')
					id = line[0]
					svm_vector = []
					for l in line[1:]:
						word, occ = l.split(':')
						svm_vector.append((int(word), int(occ)))								
					#mapping features to SVM feature space
					shrinked_vector = [(voc_maps[c][v[0]], v[1]) for v in svm_vector if v[0] in voc_maps[c]]			
					#make tf idf
					tf_idf = compute_tf_idf_by_vector(shrinked_vector, idfs[c])				
					#make SVM dictionary feature
					features = {}
					feature_ids = []
					for wd in tf_idf:
						features[wd[0]] = wd[1]
						feature_ids.append(wd[0])
					#extract related svm weight	in model
					svm_weight = extract_related_svm_weight(feature_ids, models[c])
					#get positive score and negative score
					s_pos, s_neg = get_positive_and_negative_word_score(tf_idf, svm_weight)
					#change positive score
					s = s_pos * pos_factor + s_neg
					#make probability
					if prob_model_choices[c] == 'PLATTS':
						calibrated_prob = platts_calibration(s, platts_models[c][0], platts_models[c][1], platts_models[c][2])
					else:
						calibrated_prob = commpute_pav_probability(pav_models[c], s)
				fd_w.write(('%.5f' % calibrated_prob) + '\n')
			fd.close()
			fd_w.close()

def file_based_parameter_multi_label_prediction_with_platts_pav_calibration_feature_shrinkage(in_fname, out_dir, out_fname_pattern, pos_factors, cats, voc_maps, idfs, models, prob_model_choices, platts_models, pav_models, predict_param):
	from make_tf_idf import compute_tf_idf_by_vector
	from see_probability_estimation import commpute_pav_probability		
	for c in cats:
		if c in models:
			#read and predict features
			fd = open(in_fname)
			fd_w_list = []
			for i in range(len(pos_factors)):
				fd_w = open(out_dir + '/' + str(c)+ '_pos_' + str(pos_factors[i]) + '_' + out_fname_pattern, 'w')
				fd_w_list.append(fd_w)
			for line in fd:
				#if I use platts but without model, then I predict it as 0, 1 or 0.5
				calibrated_prob_list = []
				if prob_model_choices[c] == 'PLATTS' and platts_models[c][0] != 0:
					calibrated_prob = platts_calibration(0, platts_models[c][0], platts_models[c][1], platts_models[c][2])
					for i in range(len(pos_factors)):
						calibrated_prob_list.append(calibrated_prob)
				else:
					#extract SVM example features
					line = line.strip().split(' ')
					id = line[0]
					svm_vector = []
					for l in line[1:]:
						word, occ = l.split(':')
						svm_vector.append((int(word), int(occ)))								
					#mapping features to SVM feature space
					shrinked_vector = [(voc_maps[c][v[0]], v[1]) for v in svm_vector if v[0] in voc_maps[c]]			
					#make tf idf
					tf_idf = compute_tf_idf_by_vector(shrinked_vector, idfs[c])				
					#make SVM dictionary feature
					features = {}
					feature_ids = []
					for wd in tf_idf:
						features[wd[0]] = wd[1]
						feature_ids.append(wd[0])
					#extract related svm weight	in model
					svm_weight = extract_related_svm_weight(feature_ids, models[c])
					#get positive score and negative score
					s_pos, s_neg = get_positive_and_negative_word_score(tf_idf, svm_weight)
					#change positive score
					for i in range(len(pos_factors)):
						s = s_pos * pos_factors[i] + s_neg
						#make probability
						if prob_model_choices[c] == 'PLATTS':
							calibrated_prob = platts_calibration(s, platts_models[c][0], platts_models[c][1], platts_models[c][2])
						else:
							calibrated_prob = commpute_pav_probability(pav_models[c], s)
						calibrated_prob_list.append(calibrated_prob)
				for i in range(len(pos_factors)):
					fd_w_list[i].write(('%.5f' % calibrated_prob_list[i]) + '\n')
			fd.close()
			for i in range(len(pos_factors)):
				fd_w_list[i].close()

def file_based_parameter_multi_label_prediction_with_platts_calibration_feature_shrinkage(in_fname, out_dir, out_fname_pattern, pos_factors, cats, voc_maps, idfs, models, platts_models, predict_param):
	from make_tf_idf import compute_tf_idf_by_vector
	from see_probability_estimation import commpute_pav_probability		
	for c in cats:
		if c in models:
			#read and predict features
			fd = open(in_fname)
			fd_w_list = []
			for i in range(len(pos_factors)):
				fd_w = open(out_dir + '/' + str(c)+ '_pos_' + str(pos_factors[i]) + '_' + out_fname_pattern, 'w')
				fd_w_list.append(fd_w)
			for line in fd:
				#if I use platts but without model, then I predict it as 0, 1 or 0.5
				calibrated_prob_list = []
				if platts_models[c][0] != 0:
					calibrated_prob = platts_calibration(0, platts_models[c][0], platts_models[c][1], platts_models[c][2])
					for i in range(len(pos_factors)):
						calibrated_prob_list.append(calibrated_prob)
				else:
					#extract SVM example features
					line = line.strip().split(' ')
					id = line[0]
					svm_vector = []
					for l in line[1:]:
						word, occ = l.split(':')
						svm_vector.append((int(word), int(occ)))								
					#mapping features to SVM feature space
					shrinked_vector = [(voc_maps[c][v[0]], v[1]) for v in svm_vector if v[0] in voc_maps[c]]			
					#make tf idf
					tf_idf = compute_tf_idf_by_vector(shrinked_vector, idfs[c])				
					#make SVM dictionary feature
					features = {}
					feature_ids = []
					for wd in tf_idf:
						features[wd[0]] = wd[1]
						feature_ids.append(wd[0])
					#extract related svm weight	in model
					svm_weight = extract_related_svm_weight(feature_ids, models[c])
					#get positive score and negative score
					s_pos, s_neg = get_positive_and_negative_word_score(tf_idf, svm_weight)
					#change positive score
					for i in range(len(pos_factors)):
						s = s_pos * pos_factors[i] + s_neg
						#make probability						
						calibrated_prob = platts_calibration(s, platts_models[c][0], platts_models[c][1], platts_models[c][2])						
						calibrated_prob_list.append(calibrated_prob)
				for i in range(len(pos_factors)):
					fd_w_list[i].write(('%.5f' % calibrated_prob_list[i]) + '\n')
			fd.close()
			for i in range(len(pos_factors)):
				fd_w_list[i].close()
													
def simple_compute_svm(word_weight, svm_weight):
	wd = {}
	sd = {}
	for w in word_weight:
		wd[w[0]] = w[1]
	for w in svm_weight:
		sd[w[0]] = w[1]
	s = 0
	for w in wd.keys():
		 s += wd[w] * sd[w]
	return s
		
if __name__ == '__main__': 	
	from time import time
	n_cats= 2
	#cats = [0, 85, 157, 224, 275, 304, 349, 369, 466, 564, 627, 423, 189]
	cats = [0, 85, 157, 224, 275, 304, 349, 369, 466, 564, 627]
	#cats = [157]
	#cats = [0, 85, 157, 304, 349, 369, 564, 627, 423]
	#cats = [0, 1, 5, 6, 2, 3, 4]
	#cats = [0, 1, 2, 157, 184, 186]
	#cats = [157]
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
	
	input_svm = '/home/mpi/clueweb09_svm.txt'
	output_dir = '/home/mpi/clueweb09_prediction/'
	output_prob_postfix = 'clueweb09_probability.txt'
	file_based_parameter_multi_label_prediction_with_platts_pav_calibration_feature_shrinkage(input_svm, output_dir, output_prob_postfix, pos_factors, my_cats, my_voc_maps, my_idfs, my_models, my_prob_model_choices, my_platts, my_pav_models, "")
	
"""	
	uid = 'clueweb09-en0000-09-22554'
	from svm_checker_helper import query_a_page_from_clueweb09_db			
	bad_request = False						
	start_download = time()
	example =  query_a_page_from_clueweb09_db(uid)
	
	
	z=webserver_example_based_multi_label_prediction_with_platts_pav_calibration_feature_shrinkage(example, cats, my_voc_maps, my_idfs, my_models, my_prob_model_choices, my_platts_models, my_pav_models, '')
"""
