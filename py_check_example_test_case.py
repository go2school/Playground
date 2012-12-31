if __name__ == '__main__':
	import sys	
	from svm_checker_helper import query_a_page_from_db, example_based_multi_label_prediction_with_platts_pav_calibration_feature_shrinkage, map_svm_feature_id_to_words
	from see_probability_estimation import commpute_pav_probability			
	len_threshold = 10
	tf_idf_method = 'tf-idf'
	n_cats = my_cats#[157]
	example =  query_a_page_from_db(id)
	len_example = len(example.split(' ')) - 1
	probs = example_based_multi_label_prediction_with_platts_pav_calibration_feature_shrinkage(example, n_cats, my_voc_maps, my_idfs, my_models, my_prob_model_choices, my_platts_models, my_pav_models, '', tf_idf_method)
	#map the results into word space
	wt = [0,0,0,0]
	is_other = True
	wt[0] = probs[0]
	for c in n_cats:
		if wt[0][c] > 0.5:
			is_other = False
	wt[1] = probs[1]
	wt[2] = map_svm_feature_id_to_words(my_cats, probs[2], my_inverse_voc_maps, inverse_dict)
	wt[3] = map_svm_feature_id_to_words(my_cats, probs[3], my_inverse_voc_maps, inverse_dict)
	#recompute score
	print id
	print wt[0], wt[1]
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
