#chunk a list into pieces
def chunks(l, n):
    return [l[i:i+n] for i in range(0, len(l), n)]
	
#read stop words into list
def read_stop_list(fname):
	stops = set()
	fd = open(fname)
	for line in fd:
		line = line.strip()
		stops.add(line)
	fd.close()
	return stops
	
#filter stop words from list
def remove_stop(word_list, stop_set):		
	word_list = [w for w in word_list if w not in stop_set]	
	return 	word_list

#stem words from list
def stem_words(word_list):
	from nltk.stem import PorterStemmer	
	stm = PorterStemmer()
	word_list = [stm.stem(w) for w in word_list]
	return word_list	

#make vocabulary to stemming words mapping and vice verse
def make_voc2stem(word_list, stem_word_list, voc2stem, stem2voc):
	for i in range(len(word_list)):
		voc2stem[word_list[i]] = stem_word_list[i]
		if stem_word_list[i] not in stem2voc:
			stem2voc[stem_word_list[i]] = set([word_list[i]])
		else:
			stem2voc[stem_word_list[i]].add(word_list[i])
			
#read dictionary from file			
def read_dict(fname, sep):
	cur_dict = {}
	fd = open(fname)
	for line in fd:
		line = line.strip()
		line = line.split(sep)
		word = line[0]
		id = int(line[1])
		cur_dict[word] = id
	fd.close()
	return cur_dict

def read_dict_query_bing(fname, sep):
	cur_dict = {}
	fd = open(fname)
	for line in fd:
		line = line.strip()
		line = line.split(sep)
		word = line[0]
		id = int(line[2])
		cur_dict[word] = id
	fd.close()
	return cur_dict

def read_dict_query_bing_freq(fname, sep):
	cur_dict = {}
	fd = open(fname)
	for line in fd:
		line = line.strip()
		line = line.split(sep)
		word = line[0]
		occ = int(line[1])
		id = int(line[2])
		cur_dict[word] = (id, occ)
	fd.close()
	return cur_dict
		
#read dictionary from file			
def read_inverse_dict(fname, sep):
	inverse_cur_dict = {}
	fd = open(fname)
	for line in fd:
		line = line.strip()
		line = line.split(sep)
		word = line[0]
		id = int(line[1])
		inverse_cur_dict[id] = word
	fd.close()
	return inverse_cur_dict

def read_inverse_dict_query_bing(fname, sep):
	inverse_cur_dict = {}
	fd = open(fname)
	for line in fd:
		line = line.strip()
		line = line.split(sep)
		word = line[0]
		id = int(line[2])
		inverse_cur_dict[id] = word
	fd.close()
	return inverse_cur_dict
		
def read_feature_map(fname, sep):
	cur_map = {}
	fd = open(fname)
	for line in fd:
		line = line.strip()
		line = line.split(sep)
		word = int(line[0])
		to = int(line[1])
		cur_map[word] = to
	fd.close()
	return cur_map

def read_inverse_feature_map(fname, sep):
	cur_map = {}
	fd = open(fname)
	for line in fd:
		line = line.strip()
		line = line.split(sep)
		from_word = int(line[0])
		to_word = int(line[1])
		cur_map[to_word] = from_word
	fd.close()
	return cur_map
		
def read_idf(fname, sep):
	cur_idf = {}
	fd = open(fname)
	for line in fd:
		line = line.strip()
		line = line.split(sep)
		word = line[0]
		v = float(line[1])
		cur_idf[int(word)] = v
	fd.close()
	return cur_idf
	
def build_reverse_dict(my_dict):
	reverse_dict = {}
	for k in my_dict.keys():
		reverse_dict[my_dict[k]] = k
	return reverse_dict
		
#write dictionary into file	
def write_dict(term_freq, fname):
	terms = term_freq.keys()
	terms.sort()
	id = 1
	fd = open(fname, 'w')	
	for term in terms:
		fd.write(term + ' ' + str(id) + '\n')
		id += 1
	fd.close()
	
def write_dict_with_occ(term_freq, fname):
	terms = term_freq.keys()
	terms.sort()
	fd = open(fname, 'w')	
	for term in terms:
		fd.write(term + ' ' + str(term_freq[term]) + '\n')		
	fd.close()
	
#write term frenquency into file
def write_term_freq(term_freq, fname):
	terms = term_freq.keys()
	terms.sort()
	fd = open(fname, 'w')
	for term in terms:
		fd.write(term + ' ' + str(term_freq[term]) + '\n')
	fd.close()
	
#write vocabulary to stemming mapping	
def write_voc_2_stem(voc2stem, stem2voc, fname_voc_2_stem, fname_stem_2_voc):
	fd = open(fname_voc_2_stem, 'w')
	for word in voc2stem:
		fd.write(word + ' ' + voc2stem[word] + '\n')
	fd.close()
	fd = open(fname_stem_2_voc, 'w')
	for stem in stem2voc:
		fd.write(stem)
		for v in stem2voc[stem]:
			fd.write(' ' + v)
		fd.write('\n')
	fd.close()

def read_stem_to_words(fname):
	stem2voc = {}
	fd = open(fname)
	for line in fd:
		line = line.strip().split(' ')
		stem2voc[line[0]] = line[1:]
	fd.close()
	return stem2voc

def restore_words_from_stem(stmes, stem2voc):
	words = [stem2voc[st][0] for st in stmes if st in stem2voc]
	return words

def read_id_cat(fname):
	id2cat = {}
	fd = open(fname)
	for line in fd:
		line = line.strip().split(' ')
		id2cat[line[0]] = line[1]
	fd.close()
	return id2cat
	
	
	
if __name__ == '__main__': 	
	mode, A, B = read_platts_model('/home/xiao/dmoz_models/dmoz_multiclass_full_models/0_model_dmoz_multiclass_full_addtional.txt')
