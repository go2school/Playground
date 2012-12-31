def load_model(model_fname):
	from liblinearutil import load_model
	model = load_model(model_fname)	  
	return model	

def read_platts_model(fname):
	fd = open(fname)
	line0 = fd.readline()
	line1 = fd.readline()
	line0 = line0.strip()
	line1 = line1.strip()
	#extarct predict mode
	a = line0.rindex(' ')
	mode = int(line0[a+1:])
	#extract A and B
	line1 = line1.split(' ')
	A = float(line1[1])
	B = float(line1[2])
	fd.close()
	return mode, A, B
	
def extract_doc_id(doc):
	a = doc.index('_')
	return int(doc[:a])
	
def extract_cats(doc, n_cats):
	items = doc.split('_')
	#parse ID
	id = int(items[0])
	#parse categories
	cats = items[1]	
	cats = cats[1:len(cats)-1]	
	if len(cats) == 0:
		cats = []	
	else:
		cats = [int(c) for c in cats.split(',')]
	if -1 in cats:
		cats = range(n_cats)
	return cats
	
def extract_id_features(doc):
	items = doc.split('_')
	#parse ID
	id = int(items[0])
	#parse features
	words = {}
	for feature in items[2:]:
		if feature == '':
			break
		wd, v = feature.split(':')
		words[int(wd)] = float(v)				
	return id, words
	
def extract_id_cats_features(doc, n_cats):
	items = doc.split('_')
	#parse ID
	id = int(items[0])
	#parse categories
	cats = items[1]	
	cats = cats[1:len(cats)-1]	
	if len(cats) == 0:
		cats = []	
	else:
		cats = [int(c) for c in cats.split(',')]
	if -1 in cats:
		cats = range(n_cats)
	#parse features
	words = {}
	for feature in items[2:]:
		if feature == '':
			break
		wd, v = feature.split(':')
		words[int(wd)] = float(v)				
	return id, cats, words
	
def multi_label_load_model(my_cats, base_folder, base_model_fname):
	svm_models = {}
	from liblinearutil import load_model
	for c in my_cats:		
		model = load_model(base_folder +  str(c) + '_' + base_model_fname)	  
		svm_models[c] = model
	return svm_models

def multi_label_load_idf(my_cats, base_folder, base_idf_fname, sep):
	idfs = {}
	from help_tools import read_idf
	for c in my_cats:		
		idf = read_idf(base_folder +  str(c) + '_' + base_idf_fname, sep)	  
		idfs[c] = idf
	return idfs
		
def multi_label_load_feature_map(my_cats, base_folder, base_map_fname, sep):
	feature_maps = {}
	from help_tools import read_feature_map
	for c in my_cats:		
		di_map = read_feature_map(base_folder +  str(c) + '_' + base_map_fname, sep)	  
		feature_maps[c] = di_map
	return feature_maps

def multi_label_load_inverse_feature_map(my_cats, base_folder, base_map_fname, sep):
	inverse_feature_maps = {}
	from help_tools import read_inverse_feature_map
	for c in my_cats:		
		di_map = read_inverse_feature_map(base_folder +  str(c) + '_' + base_map_fname, sep)	  
		inverse_feature_maps[c] = di_map
	return inverse_feature_maps
	
def multi_label_load_platts_model(my_cats, base_folder, base_platts_fname):
	platts_models = {}	
	for c in my_cats:		
		mode, A, B = read_platts_model(base_folder +  str(c) + '_' + base_platts_fname)	  
		platts_models[c] = (mode, A, B)
	return platts_models
	
def get_multi_label_platts_model(platts_models, cats):
	"""
	modes = []
	A = []
	B = []
	for c in cats:
		if c in platts_models:
			modes.append((c, platts_models[c][0]))
			A.append((c, platts_models[c][1]))
			B.append((c, platts_models[c][2]))
	
	str_m = [str(m[0]) + ':' + str(m[1]) for m in modes]	
	str_a = [str(m[0]) + ':' + str(m[1]) for m in A]	
	str_b = [str(m[0]) + ':' + str(m[1]) for m in B]	
	
	str_m = '_'.join(str_m)
	str_a = '_'.join(str_a)
	str_b = '_'.join(str_b)
	print str_m, str_a, str_b
	"""
	modes = []
	A = []
	B = []
	for c in cats:
		if c in platts_models:
			modes.append(platts_models[c][0])
			A.append(platts_models[c][1])
			B.append(platts_models[c][2])
	return modes, A, B
	#return str_m, str_a, str_b
			
def multi_label_prediction(doc, my_cats, svm_models):
	from liblinearutil import predict		
	#extract id, categories and features
	id, features = extract_id_features(doc)	
	probs = []		
	for c in my_cats:
		if c in svm_models:
			p_label, p_acc, p_val = predict([1], [features], svm_models[c], '-b 1')
			probs.append((c, p_val[0][0]))			
			print c, p_val[0][0]		
	return probs

def platts_calibration(f, mode, A, B):
	import math	
	if mode == 1:
		return 0.5
	elif mode == 2:
		return 1
	elif mode == 3:
		return 0
	else:
		try:
			return 1.0/(1+math.exp(A*f+B));
		except Exception:
			return 0

def do_svm_prediction(model, platt_model, y, x, predict_param):
	from liblinearutil import predict
	if platt_model[0] == 0:
		return predict([y], [x], model, predict_param)	
	elif platt_model[0] == 1:
		import random
		p = random.uniform(-1000,1000)
		if p>=0:
			label = 1
		else:
			label = -1
		acc = 0					
		return [label], acc, [[p]]
	elif platt_model[0] == 2:
		p = 1000
		label = 1
		acc = 0
		return [label], acc, [[p]]
	else:
		p = -1000
		label = -1
		acc = 0
		return [label], acc, [[p]]
				
def extract_features(title, body, keywords, desc, cur_dict, stop_words):	
	from nltk.probability import FreqDist
	from nltk.tokenize import regexp_tokenize	
	from help_tools import remove_stop, stem_words	
	
	#to lowercase
	title = title.lower()
	desc = desc.lower()
	keywords = keywords.lower()
	body = body.lower()
		
	#feature vector
	vector = []
		
	#extract title
	if len(title)>0:
		title_wordlist = regexp_tokenize(title, '[a-zA-Z]+')
		title_removed = remove_stop(title_wordlist, stop_words)
		title_stemmed = stem_words(title_removed)						
		title_stemmed = [t + '_t' for t in title_stemmed]									
		#compute freq
		cp = FreqDist(title_stemmed).items()
		for c in cp:
			arg_term = c[0]
			if arg_term in cur_dict:
				vector.append((cur_dict[c[0]], c[1]))
	
	#merge body, desc and keywords
	body = body + ' ' + desc + ' ' + keywords					
				
	#extract body text		
	if len(body)>0:
		body_wordlist = regexp_tokenize(body, '[a-zA-Z]+')
		body_removed = remove_stop(body_wordlist, stop_words)
		body_stemmed = stem_words(body_removed)		
		body_stemmed = [t + '_b' for t in body_stemmed]	
		
		cp =FreqDist(body_stemmed).items()
		for c in cp:
			arg_term = c[0]
			if arg_term in cur_dict:
				vector.append((cur_dict[c[0]], c[1]))
	
	return vector

def extract_features_with_feature_shrinkage(title, body, keywords, desc, cur_dict, dict_map, stop_words, idf_table):	
	from nltk.probability import FreqDist
	from nltk.tokenize import regexp_tokenize	
	from help_tools import remove_stop, stem_words
	from make_tf_idf import compute_tf_idf_by_vector
	
	#to lowercase
	title = title.lower()
	desc = desc.lower()
	keywords = keywords.lower()
	body = body.lower()
		
	#feature vector
	vector = []
		
	#extract title
	if len(title)>0:
		title_wordlist = regexp_tokenize(title, '[a-zA-Z]+')
		title_removed = remove_stop(title_wordlist, stop_words)
		title_stemmed = stem_words(title_removed)						
		title_stemmed = [t + '_t' for t in title_stemmed]									
		#compute freq
		cp = FreqDist(title_stemmed).items()
		for c in cp:
			arg_term = c[0]
			if arg_term in cur_dict:
				vector.append((cur_dict[c[0]], c[1]))
	
	#merge body, desc and keywords
	body = body + ' ' + desc + ' ' + keywords					
				
	#extract body text		
	if len(body)>0:
		body_wordlist = regexp_tokenize(body, '[a-zA-Z]+')
		body_removed = remove_stop(body_wordlist, stop_words)
		body_stemmed = stem_words(body_removed)		
		body_stemmed = [t + '_b' for t in body_stemmed]	
		
		cp =FreqDist(body_stemmed).items()
		for c in cp:
			arg_term = c[0]
			if arg_term in cur_dict:
				vector.append((cur_dict[c[0]], c[1]))
	
	#map feature (shrinkage)	
	shrinked_vector = [(dict_map[v[0]], v[1]) for v in vector if v[0] in dict_map]
			
	#write down result
	svm_vector = ''			
	if len(shrinked_vector) != 0:		
		shrinked_vector = compute_tf_idf_by_vector(shrinked_vector, idf_table)		
		shrinked_vector.sort()		
		shrinked_vector = [str(v[0]) + ':' + ('%.6f' % v[1]) for v in shrinked_vector]
		svm_vector += '_'.join(shrinked_vector)
	return svm_vector
	
def from_html_to_svm_feature_with_shrinkage(html, voc, voc_map, stop_words, idf):
	from url_util import extract_content
	from help_tools import read_dict, read_stop_list, read_idf			
	title, body, keyword, description, charcode = extract_content(html)
	svm_vector = extract_features_with_feature_shrinkage(title, body, keyword, description, voc, voc_map, stop_words, idf)
	return svm_vector
	
def from_html_to_svm_feature(html, voc, voc_map, stop_words, idf):
	from url_util import extract_content
	from help_tools import read_dict, read_stop_list, read_idf			
	title, body, keyword, description, charcode = extract_content(html)
	svm_vector = extract_features(title, body, keyword, description, voc, stop_words, idf)
	return svm_vector
	
def from_html_to_svm_vector(html, voc, stop_words):
	from url_util import extract_content		
	title, body, keyword, description, charcode = extract_content(html)
	svm_vector = extract_features(title, body, keyword, description, voc, stop_words)
	return svm_vector

def from_title_body_to_svm_vector(title, body, voc, stop_words):
	from url_util import remove_nontext
	body = remove_nontext(body)
	keyword = ""
	description = ""
	svm_vector = extract_features(title, body, keyword, description, voc, stop_words)
	return svm_vector
				
def shrinking_svm_vector(svm_vector, voc_map):
	return [(voc_map[v[0]], v[1]) for v in svm_vector if v[0] in voc_map]
				
def make_tf_idf_vector(svm_vector, idfs):
	from make_tf_idf import compute_tf_idf_by_vector
	return compute_tf_idf_by_vector(svm_vector, idfs)				
		
def multi_label_prediction_with_feature_shrinkage(svm_vector, cats, voc_maps, idfs, models, platts_models, predict_param):	
	from make_tf_idf import compute_tf_idf_by_vector
	from liblinearutil import predict
	probs = []
	for c in cats:
		if c in models:
			#shrink features
			print 'classify ' + str(c)
			shrinked_vector = [(voc_maps[c][v[0]], v[1]) for v in svm_vector if v[0] in voc_maps[c]]
			print shrinked_vector
			#make tf idf
			tf_idf = compute_tf_idf_by_vector(shrinked_vector, idfs[c])
			print 'tf', tf_idf
			#make SVM feature
			features = {}
			for wd in tf_idf:
				features[wd[0]] = wd[1]			
			#p_label, p_acc, p_val = do_svm_prediction(models[c], platts_models[c], 1, features, predict_param)
				
			p_label, p_acc, p_val = predict([1], [features], models[c], predict_param)
			probs.append((c, p_val[0][0]))			
	return probs			

def multi_label_prediction_with_platts_calibration_feature_shrinkage(svm_vector, cats, voc_maps, idfs, models, platts_models, predict_param):
	from make_tf_idf import compute_tf_idf_by_vector
	probs = []
	len_vectors = []
	for c in cats:
		if c in models:
			#shrink features
			print 'classify ' + str(c)
			shrinked_vector = [(voc_maps[c][v[0]], v[1]) for v in svm_vector if v[0] in voc_maps[c]]			
			#make tf idf
			tf_idf = compute_tf_idf_by_vector(shrinked_vector, idfs[c])				
			#make SVM feature
			features = {}
			for wd in tf_idf:
				features[wd[0]] = wd[1]
			p_label, p_acc, p_val = do_svm_prediction(models[c], platts_models[c], 1, features, predict_param)				
			#make probability
			calibrated_prob = platts_calibration(p_val[0][0], platts_models[c][0], platts_models[c][1], platts_models[c][2])
			probs.append((c, calibrated_prob))	
			len_vectors.append((c, len(features)))				
	return probs, len_vectors
	
def multi_label_prediction_with_platts_pav_calibration_feature_shrinkage(svm_vector, cats, voc_maps, idfs, models, prob_model_choices, platts_models, pav_models, predict_param):
	from make_tf_idf import compute_tf_idf_by_vector
	from see_probability_estimation import commpute_pav_probability
	probs = []
	len_vectors = []
	for c in cats:
		if c in models:
			#shrink features
			print 'classify ' + str(c)
			shrinked_vector = [(voc_maps[c][v[0]], v[1]) for v in svm_vector if v[0] in voc_maps[c]]			
			#make tf idf
			tf_idf = compute_tf_idf_by_vector(shrinked_vector, idfs[c])				
			#make SVM feature
			features = {}
			for wd in tf_idf:
				features[wd[0]] = wd[1]
			p_label, p_acc, p_val = do_svm_prediction(models[c], platts_models[c], 1, features, predict_param)				
			#make probability
			if prob_model_choices[c] == 'PLATTS':
				calibrated_prob = platts_calibration(p_val[0][0], platts_models[c][0], platts_models[c][1], platts_models[c][2])
			else:
				calibrated_prob = commpute_pav_probability(pav_models[c], p_val[0][0])
			probs.append((c, calibrated_prob))	
			len_vectors.append((c, len(features)))				
	return probs, len_vectors
	
def file_based_multi_label_prediction_with_platts_pav_calibration_feature_shrinkage(in_fname, out_dir, out_fname_pattern, cats, voc_maps, idfs, models, prob_model_choices, platts_models, pav_models, predict_param):
	from make_tf_idf import compute_tf_idf_by_vector
	from see_probability_estimation import commpute_pav_probability		
	for c in cats:
		if c in models:
			#read and predict features
			fd = open(in_fname)
			fd_w = open(out_dir + '/' + str(c)+ '_' + out_fname_pattern, 'w')			
			for line in fd:
				line = line.strip().split(' ')
				id = line[0]
				svm_vector = []
				for l in line[1:]:
					word, occ = l.split(':')
					svm_vector.append((int(word), int(occ)))								
				shrinked_vector = [(voc_maps[c][v[0]], v[1]) for v in svm_vector if v[0] in voc_maps[c]]			
				#make tf idf
				tf_idf = compute_tf_idf_by_vector(shrinked_vector, idfs[c])				
				#make SVM feature
				features = {}
				for wd in tf_idf:
					features[wd[0]] = wd[1]
				p_label, p_acc, p_val = do_svm_prediction(models[c], platts_models[c], 1, features, predict_param)				
				#make probability
				if prob_model_choices[c] == 'PLATTS':
					calibrated_prob = platts_calibration(p_val[0][0], platts_models[c][0], platts_models[c][1], platts_models[c][2])
				else:
					calibrated_prob = commpute_pav_probability(pav_models[c], p_val[0][0])
				fd_w.write(('%.5f' % calibrated_prob) + '\n')				
			fd.close()
			fd_w.close()			
			
def multi_label_prediction_without_feature_shrinkage(svm_vector, cats, idfs, models, platts_models, predict_param):	
	from make_tf_idf import compute_tf_idf_by_vector
	probs = []
	for c in cats:
		if c in models:	
			print 'classify ' + str(c)
			#make tf idf
			tf_idf = compute_tf_idf_by_vector(svm_vector, idfs[c])			
			#make SVM feature
			features = {}
			for wd in tf_idf:
				features[wd[0]] = wd[1]
			p_label, p_acc, p_val = do_svm_prediction(models[c], platts_models[c], 1, features, predict_param)
			probs.append((c, p_val[0][0]))			
	return probs
		
def test():	
	from url_util import download_webpage, extract_content
	from help_tools import read_dict, read_stop_list, read_idf	
	#url = 'http://www.google.ca/'
	url = 'http://mail.uwo.ca/'
	voc = read_dict('adv_uwo_full_dict')	
	stop_words = read_stop_list('new_english.stop')
	idf = read_idf('food_idf.txt')	
	svm_vector = from_url_to_svm_feature(url, voc, stop_words, idf)	
		
if __name__ == '__main__': 
	#test()
	#modes = multi_label_load_platts_model(range(5), '/home/mpi/dmoz_models/dmoz_multiclass_full_models/', 'model_dmoz_multiclass_full_addtional.txt')
	from dataset_util import read_multi_label
	#labels = read_multi_label('/media/01CC16F5ED7072F0/see_workingdirectory/svm_probs/dmoz_train_labels_12072011.txt')
	labels = read_multi_label('/home/xiao/label110629.txt')
	from help_tools import read_stop_list, read_dict
	import simplejson as json
	
	from active_learning import *
	
	hier = 'dmoz_hierarchy.txt'

	root = Node().read_tree(hier)

	n_cats= 2
	#cats = range(n_cats)
	#cats = [1,86,158,225,276,305,350,370,467,565,628]
	#cats = [c-1 for c in cats]
	#cats= range(500, 550)	
	cats = [0, 85, 157, 224, 275, 304, 349, 369, 466, 564, 627]
	cats = [0, 1, 2, 157, 184, 186]
	cats = [157]
	#cats = [0, 564]
	my_cats = cats
	dict_fname = '/home/mpi/dmoz_models/dictionary0102.txt'
	stop_fname = 'new_english.stop'
	idf_fname = 'food_idf.txt'
	base_folder = '/home/mpi/see_all_models/'
	base_model_file = 'model_SEE_0.2'
	base_idf_file = 'idf_SEE_0.2'
	base_local_dict_file = 'feature_indices_SEE_0.2'
	base_model_para = 'model_SEE_0.2_addtional.txt'
	base_prob_estimation_folder = '/home/mpi/SEE_Probability_Estimation/pav_model'
	base_prob_estimation_choice_file = '/home/mpi/SEE_Probability_Estimation/best_parameter.txt'	
	base_pav_model_ext = 'SEE_0.2_pav_model'
	from see_probability_estimation import read_model_choice, read_pav_parameters_by_ids	
	my_models = multi_label_load_model(my_cats, base_folder, base_model_file)	
	my_idfs = multi_label_load_idf(my_cats, base_folder, base_idf_file, ':')
	my_voc_maps = multi_label_load_feature_map(my_cats, base_folder, base_local_dict_file, ':')
	my_platts_models = multi_label_load_platts_model(my_cats, base_folder, base_model_para)
	my_prob_model_choices = read_model_choice(base_prob_estimation_choice_file)
	my_pav_models = read_pav_parameters_by_ids(my_cats, base_prob_estimation_folder, base_pav_model_ext)
	
	
	input_svm = '/home/mpi/clueweb09_svm.txt'
	output_dir = '/home/mpi/clueweb09_prediction/'
	output_prob_postfix = 'clueweb09_probability.txt'


	file_based_multi_label_prediction_with_platts_pav_calibration_feature_shrinkage(input_svm, output_dir, output_prob_postfix, my_cats, my_voc_maps, my_idfs, my_models, my_prob_model_choices, my_platts_models, my_pav_models, '')
	
