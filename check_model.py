def check_model_weight(model_fname, reverse_dict):
	#skip model parameter
	lines = []
	fd = open(model_fname)
	for line in fd:
		lines.append(line.strip())
	fd.close()
	#begin read weight
	weights = [float(l) for l in lines[6:]]
	
	z=[(weights[i], reverse_dict[i+1]) for i in range(len(weights)) if weights[i] != 0]
	z = sorted(z, key=lambda s:s[0], reverse=True)
	return z

def check_example_weight(dataset, id, reverse_dict):			
	fd = open(dataset)
	for line in fd:
		a = line.index(' ')
		if line[:a] == id:
			print line
			break
	fd.close()
	words = []
	line = line.strip().split(' ')
	for l in line[1:]:
		wd, v = l.split(':')
		words.append((int(wd), reverse_dict[int(wd)], v))
	return words
	
if __name__ == '__main__':
	#987, 4254, 17943, 53199, 89213, 105489, 123323, 124218, 124338, 128547, 129285, 129610, 134774, 137472, 139081, 140509, 142975, 144397, 150656, 151428, 153123, 154123, 156725, 157512, 158156, 161586, 163094, 164505, 164952, 168398, 168738, 254030, 254031, 576402, 1551619, 1596309, 1596963, 1599111, 1600893, 1602467, 1603349, 1603891, 1606190, 1607709, 1608592, 1609492, 1610817, 1622692, 1622698, 1687825, 1727941, 1736358, 1738366, 1779821, 1789478, 1793285, 1855553, 1965656
	from help_tools import read_dict, build_reverse_dict, restore_words_from_stem, read_stem_to_words
	from make_tf_idf import read_idf_table
	dict_fname = 'adv_uwo_full_dict'
	uwo_dataset = 'uwo_food_tf_idf.txt'
	stem2words = 'adv_uwo_stem_to_voc.txt'
	food_idf_fname = 'food_idf.txt'
	model_fname = 'food_model'
	model_word_fname = 'food_model_word'
	my_dict = read_dict(dict_fname)
	fd_idf = read_idf_table(food_idf_fname)
	reverse_dict = build_reverse_dict(my_dict)
	
	
	fd_idf_dict = {}
	for wd in fd_idf.keys():
		fd_idf_dict[reverse_dict[int(wd)]] = fd_idf[wd]
		
	stem2voc = read_stem_to_words(stem2words)
	model_weight = check_model_weight('food_model', reverse_dict)
	fd = open(model_word_fname, 'w')
	for m in model_weight:
		fd.write(('%.6f' % m[0]) + ' ' + m[1] + '\n')
	fd.close()
	"""
	model_weight_dict = {}
	for m in model_weight:
		model_weight_dict[m[1]] = m[0]
	actual_words = restore_words_from_stem([m[1] for m in model_weight], stem2voc)
	
	words = check_example_weight(uwo_dataset, '987', reverse_dict)
	
	words_dict = {}
	for wd in words:
		words_dict[wd[1]] = wd[2]
	
	score = 0
	for wd in words:
		if wd[1] in model_weight_dict:
			v = model_weight_dict[wd[1]] * float(wd[2])
			print wd[1], v
			score += v
	"""
