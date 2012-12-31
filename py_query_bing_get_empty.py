def sperate_ids():
	fd_w = open('query_bing_used_id_list.txt', 'w')
	fd_w2 = open('query_bing_empty_id_list.txt', 'w')
	fd = open('query_bing_id_categories_list.txt')
	for line in fd:
		line = line.strip().split(' ')		
		if len(line) != 1:
			fd_w.write(line[0] + '\n')
		else:
			fd_w2.write(line[0] + '\n')
	fd.close()
	fd_w.close()
	fd_w2.close()

sperate_ids()

ids = set()
fd = open('query_bing_empty_id_list.txt')
for line in fd:
	ids.add(int(line.strip()))
fd.close()
pathes = set()
fd = open('query_bing_id_path_list.txt')
fd_w = open('query_bing_empty_id_path_list.txt', 'w')
for line in fd:
	line = line.strip().split('|')
	if int(line[0]) in ids:
		path = line[1]
		if path.endswith('.xml'):
			b = path.rindex('/')
			path = path[:b]		
		"""
		prefixes = ['/media/d/SEEUWO_Training_Data/', 'SEEUWO_Training_Data/', '/home/xiao/wiki_subject_hierarchy/SEEUWO_Training_Data_top_two/']
		new_path = 'SEEUWO_Training_Data/'
		if path.startswith(prefixes[0]):
			new_path += path[len(prefixes[0]):]
		elif path.startswith(prefixes[1]):
			new_path += path[len(prefixes[1]):]
		elif path.startswith(prefixes[2]):
			new_path += path[len(prefixes[2]):]
		"""
		pathes.add(path)
		fd_w.write(line[0] + '|' + line[1] + '\n')
fd.close()
fd_w.close()
pathes = list(pathes)
pathes.sort()
fd_w = open('query_bing_empty_folder_list.txt', 'w')
for p in pathes:
	fd_w.write(p + '\n')
fd_w.close()
