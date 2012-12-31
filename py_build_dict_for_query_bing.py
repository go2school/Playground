def merge_dict(ids, folder, fileext, outfname):
	cut_dict ={}
	for id in ids:
		fd = open(folder + '/' + str(id)+'_' + fileext)
		for line in fd:
			line = line.strip().split(' ')
			wd = line[0]
			occ = int(line[1])
			if wd not in cut_dict:
				cut_dict[wd] = occ
			else:
				cut_dict[wd] += occ
		fd.close()
	words = cut_dict.keys()
	words.sort()
	fd = open(folder + '/' + outfname, 'w')
	for w in words:
		fd.write(str(w) + ' ' + str(cut_dict[w]) + '\n')
	fd.close()
	
def read_raw_dict(fname):
	cur_dict = {}	
	fd=open(fname)
	for line in fd:
		line = line.strip().split(' ')
		wd = line[0]
		occ = int(line[1])
		cur_dict[wd] = occ
	fd.close()	
	return cur_dict
	
def remove_rare_words(dict_fname, out_dict_fname, threshold):
	#read dict <word, occ>
	bing_dict = {}	
	fd = open(dict_fname)	
	for line in fd:	
		line = line.strip()
		line = line.split(' ')
		word = line[0]
		occ = int(line[1])		
		bing_dict[word] = occ
	fd.close()
	#sort words
	words = bing_dict.keys()
	words.sort()
	#write dict <word, occ, id>
	fd_w = open(out_dict_fname, 'w')
	n = 1
	for w in words:
		if bing_dict[w] >= threshold:
			fd_w.write(w + ' ' + str(bing_dict[w]) + ' ' + str(n) + '\n')
			n += 1
	fd_w.close()
	

if __name__ == '__main__':
	in_folder = '/home/mpi/query_bing_project'
	in_dict_fname = 'query_bing_dictionary0102.txt'
	merged_dict_base = 'query_bing_merged_dictionary0102.txt'
	out_dict_fname = 'query_bing_rare_removed'
	#merge_dict(range(6), in_folder, in_dict_fname, merged_dict_base)	
	#cur_dict = read_raw_dict(in_folder + '/' + merged_dict_base)
	#words = [(w, cur_dict[w]) for w in cur_dict]
	#words = sorted(words, key=lambda s:s[1], reverse=True)
	#for th in range(10):
	#	remove_rare_words(in_folder + '/' + merged_dict_base, in_folder + '/' + out_dict_fname + '_' + str(th) + '.txt', th)
