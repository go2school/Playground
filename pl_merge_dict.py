def merge_voc(ids, fname_dict):	
	#merge dict
	whole_dict = set()
	for id in range(ids):	
		fd = open(fname_dict + '_' + str(id))
		for line in fd:
			line = line.strip().split(' ')
			whole_dict.add(line[0])
		fd.close()
		
	"""
	#remove single stem
	for i in range(26):
		z = chr(i + ord('a'))
		if z + '_b' in whole_dict:
			print z + '_b'
			whole_dict.remove(z + '_b')
		if z + '_u' in whole_dict:
			print z + '_u'
			whole_dict.remove(z + '_u')
		if z + '_kd' in whole_dict:
			print z + '_kd'
			whole_dict.remove(z + '_kd')
	"""
		
	whole_dict = list(whole_dict)
	whole_dict.sort()
	n = 1	
	fd = open(fname_dict, 'w')
	for kk in whole_dict:
		fd.write(kk + ' ' + str(n) + '\n')
		n += 1
	fd.close()

def merge_freq(ids, fname_freq):	
	#merge dict
	whole_dict = {}
	for id in range(ids):	
		fd = open(fname_freq + '_' + str(id))
		for line in fd:
			line = line.strip().split(' ')
			if line[0] not in whole_dict:
				whole_dict[line[0]] = int(line[1])
			else:
				whole_dict[line[0]] += int(line[1])			
		fd.close()
	
	#remove single stem
	stems = whole_dict.keys()
	"""
	for i in range(26):
		z = chr(i + ord('a'))
		if z + '_b' in whole_dict:
			print z + '_b'
			stems.remove(z + '_b')
		if z + '_u' in whole_dict:
			print z + '_u'
			stems.remove(z + '_u')
		if z + '_kd' in whole_dict:
			print z + '_kd'
			stems.remove(z + '_kd')
	"""
			
	stems.sort()
	n = 1	
	fd = open(fname_freq, 'w')
	for kk in stems:
		fd.write(kk + ' ' + str(whole_dict[kk]) + '\n')
		n += 1
	fd.close()

def merge_voc_to_stem(ids, fname_voc_2_stem):
	#merge dict
	whole_dict = {}
	for id in range(ids):	
		fd = open(fname_voc_2_stem + '_' + str(id))
		for line in fd:
			line = line.strip().split(' ')		
			whole_dict[line[0]] = line[1]
		fd.close()
						
	stems = whole_dict.keys()
	stems.sort()
	fd = open(fname_voc_2_stem, 'w')
	for kk in stems:
		fd.write(kk + ' ' + str(whole_dict[kk]) + '\n')		
	fd.close()
	
def merge_stem_to_voc(ids, fname_stem_2_voc):
	#merge dict
	whole_dict = {}
	for id in range(ids):	
		fd = open(fname_stem_2_voc + '_' + str(id))
		for line in fd:
			line = line.strip().split(' ')	
			if line[0] not in whole_dict:
				whole_dict[line[0]] = []
			else:
				for l in line[1:]:
					whole_dict[line[0]].append(l)
		fd.close()
		
	#remove single stem
	stems = whole_dict.keys()
	"""
	for i in range(26):
		z = chr(i + ord('a'))
		if z + '_b' in whole_dict:
			print z + '_b'
			stems.remove(z + '_b')
		if z + '_u' in whole_dict:
			print z + '_u'
			stems.remove(z + '_u')
		if z + '_kd' in whole_dict:
			print z + '_kd'
			stems.remove(z + '_kd')
	"""
			
	stems.sort()	
	fd = open(fname_stem_2_voc, 'w')
	for kk in stems:
		fd.write(kk)
		for k in whole_dict[kk]:
			fd.write(' ' + k)
		fd.write('\n')		 		
	fd.close()
	
def merge_features(ids, name, toname):
	datas = []
	for id in range(ids):
		fd = open(name + '_' + str(id) + '.txt')
		for line in fd:
			line = line.strip()
			a = line.index(' ')
			id = line[:a]
			datas.append((id, line))
		fd.close()
	datas = sorted(datas, key = lambda s:s[0])
	fd = open(toname, 'w')
	for data in datas:
		fd.write(data[1] + '\n')
	fd.close()

if __name__ == '__main__':
	fname_stop = 'new_english.stop'
	fname_dict = 'new_uwo_dict'
	fname_freq = 'new_uwo_freq'
	local_trunk_size = 10000
	fname_voc_2_stem = 'new_uwo_voc_to_stem'
	fname_stem_2_voc = 'new_uwo_stem_to_voc'
	ids = 3
	merge_voc(ids, fname_dict)
	merge_freq(ids, fname_freq)
	merge_voc_to_stem(ids, fname_voc_2_stem)
	merge_stem_to_voc(ids, fname_stem_2_voc)
