def genrate_dict_file(folder, npcs, infname, outfname):
	ids = range(npcs)
	cur_dict = {}
	for id in ids:
		fd = open(folder + '/' + str(id) + '_' + infname)
		for line in fd:
			line = line.strip().split(' ')
			word = line[0]
			occ = int(line[1])
			if word not in cur_dict:
				cur_dict[word] = occ
			else:
				cur_dict[word] += occ
		fd.close()
	wds = cur_dict.keys()
	wds.sort()
	fd_w = open(folder + '/' + outfname, 'w')
	for wd in wds:
		fd_w.write(wd + ' ' + str(cur_dict[wd]) + '\n')
	fd_w.close()

def remove_rare_words(threshold, infname, outfname):	
	n = 1
	fd = open(infname)
	fd_w = open(outfname, 'w')
	for line in fd:
		old_line = line
		line = line.strip().split(' ')
		wd = line[0]
		occ = int(line[1])
		if occ >= threshold:
			fd_w.write(old_line.strip() + ' ' + str(n) + '\n')
			n += 1
	fd.close()
	fd_w.close()

def merge_voc2stem(folder, npcs, infname, outfname):
	ids = range(npcs)
	mapper = {}
	for id in ids:
		fd = open(folder + '/' + str(id) + '_' + infname)
		for line in fd:
			line = line.strip().split(' ')
			raw_word = line[0]
			stem_word = line[1]						
			mapper[raw_word] = stem_word	
	fd = open(folder + '/' + outfname, 'w')
	keys = mapper.keys()	
	keys.sort()
	for wd in keys:
		fd.write(wd + ' ' + str(mapper[wd]) + '\n')
	fd.close()
	

def merge_stem2voc(folder, npcs, infname, outfname):
	ids = range(npcs)
	mapper = {}
	for id in ids:
		fd = open(folder + '/' + str(id) + '_' + infname)
		for line in fd:
			line = line.strip().split(' ')
			stem_word = line[0]
			raw_words = set(line[1:])
			if stem_word not in mapper:
				mapper[stem_word] = raw_words
			else:
				mapper[stem_word] |= raw_words
	fd = open(folder + '/' + outfname, 'w')
	keys = mapper.keys()
	keys.sort()
	for wd in keys:
		fd.write(wd)
		wds = list(mapper[wd])
		wds.sort()
		for w in wds:
			fd.write(' ' + w)
		fd.write('\n')
	fd.close()
		
if __name__ == '__main__': 
	genrate_dict_file('/home/mpi/shareddir/query_bing_dictionary2', 17, 'query_bing_raw_dictionary0705.txt', 'query_bing_raw_dictionary0705.txt')	
	genrate_dict_file('/home/mpi/shareddir/query_bing_dictionary2', 17, 'query_bing_dictionary0705.txt', 'query_bing_dictionary0705.txt')	
	merge_voc2stem('/home/mpi/shareddir/query_bing_dictionary2', 17, 'query_bing_voc2stem.txt', 'query_bing_voc2stem.txt')	
	merge_stem2voc('/home/mpi/shareddir/query_bing_dictionary2', 17, 'query_bing_stem2voc.txt', 'query_bing_stem2voc.txt')	
	for th in range(2,4):
		remove_rare_words(th, '/home/mpi/shareddir/query_bing_dictionary2/query_bing_dictionary0705.txt', '/home/mpi/shareddir/query_bing_dictionary2/query_bing_dictionary0705_'+str(th)+'.txt')
