if __name__ == '__main__':
	import sys	
	from svm_checker_helper import *
	from see_probability_estimation import commpute_pav_probability			
	from active_learning import *
	root = Node().read_tree('dmoz_hierarchy.txt')
	len_threshold = 15
	threshold = 0.5
	repredict_other_threshold = 0.1
	tf_idf_method = 'tf-idf'
	n_cats = my_cats
	id = 345940
	example =  query_a_page_from_db(id)
	len_example = len(example.split(' ')) - 1
	#probs = example_based_multi_label_prediction_with_platts_pav_calibration_feature_shrinkage(example, n_cats, my_voc_maps, my_idfs, my_models, my_prob_model_choices, my_platts_models, my_pav_models, '', tf_idf_method)
	probs = adv_webserver_example_based_multi_label_prediction_with_platts_pav_calibration_feature_shrinkage(example, n_cats, my_voc_maps, my_idfs, my_models, my_prob_model_choices, my_platts_models, my_pav_models, '')
	#map the results into word space
	wt = [0,0,0,0]	
	wt[0] = probs[0]
	wt[1] = probs[1]
	wt[2] = map_svm_feature_list_by_id_to_words(my_cats, probs[2], my_inverse_voc_maps, inverse_dict)
	wt[3] = map_svm_feature_list_by_id_to_words(my_cats, probs[3], my_inverse_voc_maps, inverse_dict)
					
	#recompute score
	print id
	top_level_cats = [c.labelIndex for c in root.children]
	print [id2cat[str(w[0])] + ':' + str(w[1]) for w in wt[0] if w[1] > threshold]
	print [id2cat[str(w[0])] + ':' + str(w[1]) for w in wt[0] if w[0] in top_level_cats]	
	
	
	#print [id2cat[str(w)] + ':' + str(wt[0][w]) for w in wt[0].keys()]
	
	old_probs = wt[0]
	prob_dict = {}
	for p in old_probs:
		prob_dict[p[0]] = p[1]
		
	#make_modified_probability(prob_dict, threshold, len_threshold, repredict_other_threshold, root, wt[2], wt[3], my_platts_models, my_pav_models, my_prob_model_choices)
	score_dict = {}
	for c in root.children:
		#check if it is short example
		#if len(wt[2][c.labelIndex]) < len_threshold:			
		s_pos, s_neg = get_positive_and_negative_word_score(wt[2][c.labelIndex], wt[3][c.labelIndex])
		#cut the positive weight score by half, hopefully to predict more negative examples
		s = s_pos * 1.5 + s_neg 
		if my_prob_model_choices[c.labelIndex] == 'PLATTS':
			calibrated_prob = platts_calibration(s, my_platts_models[c.labelIndex][0], my_platts_models[c.labelIndex][1], my_platts_models[c.labelIndex][2])
		else:
			calibrated_prob = commpute_pav_probability(my_pav_models[c.labelIndex], s)
		prob_dict[c.labelIndex] = calibrated_prob
		score_dict[c.labelIndex] = s
		
	#output new probs
	wc = prob_dict.keys()
	wc.sort()
	print [str(w) + ':'+id2cat[str(w)] + ':' + str(prob_dict[w]) for w in wc if prob_dict[w] > threshold]	
	#print [str(w) + ':'+id2cat[str(w)] + ':' + str(score_dict[w]) for w in wc if score_dict[w] > 0]	

	"""
	new_probs = []
	for c in n_cats:
		wd = {}
		sd = {}
		for w in wt[2][c]:
			wd[w[0]] = w[1]
		for w in wt[3][c]:
			sd[w[0]] = w[1]
		s = 0
		s_pos = 0
		s_neg = 0
		wt_rs = []
		sm = sum(wd.values())
		for w in wd.keys():
			v = wd[w] * sd[w]
			if sd[w] < 0:
				if len_example < len_threshold:
					s_neg += 2 * v
				else:
					s_neg += v
			else:
				if is_other == True:
					s_pos += 2 * v
				else:
					s_pos += v
			wt_rs.append((w, v))
		wt_rs = sorted(wt_rs, key=lambda s:s[1], reverse=True)
		s = s_neg + s_pos
		#platts model
		p1 = commpute_pav_probability(my_pav_models[c], s)
		p2 = platts_calibration(s, my_platts_models[c][0], my_platts_models[c][1], my_platts_models[c][2])
		#print id2cat[str(c)], 'score', s, s_pos, s_neg
		#print id2cat[str(c)], 'prob', wt[0][c]
		#print 'calibrated prob', p1, p2
		#print '-----'
		if p1 > 0.5 or p2 > 0.5:
			new_probs.append((c, max(p1,p2)))
	for n in new_probs:
		print id2cat[str(n[0])], n[1]
	"""
