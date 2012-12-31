
#read id to url
id2url = {}
url2ids = {}
fd = open('query_bing_id_url_list.txt')
for line in fd:
	a = line.index(' ')
	id = line[:a]
	url = line[a+1:].strip()
	id2url[id] = url
	if url in url2ids:
		url2ids[url].append(id)
	else:
		url2ids[url] = [id]
fd.close()
#merge cats
id2cats = {}
fd = open('query_bing_id_categories_list.txt')
for line in fd:
	line = line.strip().split(' ')
	id = line[0]
	cats = set(line[1].split(','))
	id2cats[id] = cats
fd.close()

done_ids = set()
fd_w = open('query_bing_id_merged_categories.txt', 'w')
ks = id2cats.keys()
ks = [int(k) for k in ks]
ks.sort()
v = set(ks)
for id in ks:
	id = str(id)
	if id not in done_ids:
		cats = id2cats[id]
		done_ids.add(id)#book it
		url = id2url[id]
		#get all related ids with same url
		ids = url2ids[url]
		for nid in ids:
			if int(nid) in v and nid not in done_ids and nid in id2cats:
				#merge set
				cats = cats | id2cats[nid]
				done_ids.add(nid)
		cats = list(cats)
		cats.sort()
		fd_w.write(str(id) + ' ' + ' '.join(cats) + '\n')			
fd_w.close()
