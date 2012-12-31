#if url already in global list
#change ID to fit global list
#or else
#add a large number on the ID to avoid redundancy
def update_id_url(id_urls, max_id, global_id_urls):
	global_dict = {}
	for i in range(len(global_id_urls)):
		global_dict[global_id_urls[i][1]] = global_id_urls[i][0]
	new_id_urls = []
	old2new = {}
	for i in range(len(id_urls)):	
		if id_urls[i][1] in global_dict:
			new_id_urls.append((global_dict[id_urls[i][1]], id_urls[i][1]))
			old2new[id_urls[i][0]] = global_dict[id_urls[i][1]]
		else:
			new_id_urls.append((id_urls[i][0] + max_id, id_urls[i][1]))
			old2new[id_urls[i][0]] = id_urls[i][0] + max_id
	return new_id_urls, old2new
	
if __name__ == '__main__':	
	
	from util import read_id_urls, sample_id_by_check_exist
	from db_util import get_id_url_from_query, get_max_id
	from db_util import get_docs_in_set, get_docs_in_set_uwo
	from build_dict_and_stem_map import extract_doc_features
	from help_tools import read_stop_list, read_dict

	all_id_url_fname = 'uwo_id_urls.txt'
	
	stop_fname = 'new_english.stop'
	#customized stop words
	augmented_stop_fname = 'new_english_university.stop'
	
	dict_fname = 'adv_uwo_full_dict'
	feature_fname = 'food_features.txt'
	label_fname = 'food_labels.txt'
	id_fname = 'food_id.txt'
	db = 'query_search_engine.webs'
	global_db = 'uwo.webs'
	global_feature_fname = 'uwo_features.txt'
	n = 10000
	site_list = ['site:uwo.ca','site:uwaterloo.ca','site:uottawa.ca','site:mcmaster.ca','site:queensu.ca']
	word_list = ['food', 'meal', 'grill', 'cheese', 'dessert', 'fries', 'chicken', 'salad', 'lunch', 'dinner', 'dining', 'cuisine', 'eating', 'nutrition', 'beer', 'drink']

	#make positive ids
	all_id_urls = read_id_urls(all_id_url_fname)
	max_id = get_max_id(global_db)
	existed_id_urls =  []
	for site in site_list:
		for word in word_list:
			query = word + ' ' + site
			tmp = get_id_url_from_query(db, query)
			existed_id_urls += tmp	
	new_existed_id_urls, old2new = update_id_url(existed_id_urls, max_id, all_id_urls)
	
	positive_ids = [r[0] for r in existed_id_urls]
	positive_ids.sort()
	
	#sampled n examples from database as negative examples
	negative_ids = sample_id_by_check_exist([r[0] for r in all_id_urls], [r[0] for r in new_existed_id_urls], n)
	negative_ids.sort()

	#read stop words and dictionary
	stop_words = read_stop_list(stop_fname)
	#read university stop words
	university_stop_words = read_stop_list(augmented_stop_fname)
	stop_words = stop_words.union(university_stop_words)
	#read dictionary
	cur_dict = read_dict(dict_fname)

	fd_feature_w = open(feature_fname, 'w')
	actual_pos_ids = []
	actual_neg_ids = []
	#get positive features
	pos_docs = get_docs_in_set(db, positive_ids)
	features = extract_doc_features(pos_docs, stop_words, cur_dict)
	#write positive features
	for vector in features:	
		fd_feature_w.write(str(old2new[vector[0]]))
		actual_pos_ids.append(old2new[vector[0]])
		for wd in vector[1]:
			fd_feature_w.write(' ' + str(wd[0]) + ':' + str(wd[1]))
		fd_feature_w.write('\n')
		
	#get and write negative features	
	fd = open(global_feature_fname)
	m = 0
	for line in fd:
		a = line.index(' ')
		id = int(line[:a])	
		if id in negative_ids and m < len(negative_ids):
			actual_neg_ids.append(id)
			fd_feature_w.write(line)
			m += 1
	fd.close()
	fd_feature_w.close()
			
	#write labels	
	fd_label_w = open(label_fname, 'w')
	for id in actual_pos_ids:
		fd_label_w.write(str(id) + ' 1\n')
	for id in actual_neg_ids:
		fd_label_w.write(str(id) + ' -1\n')
	fd_label_w.close()	
		
	fd = open(id_fname, 'w')
	for id in actual_pos_ids + actual_neg_ids:
		fd.write(str(id) + '\n')
	fd.close()
	
	print 'build dataset done'
