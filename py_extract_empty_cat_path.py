ids = set()
fd= open('query_bing_empty_cat_id_list.txt')
for line in fd:
	line = line.strip()
	ids.add(int(line))
fd.close()
fd= open('new_wiki_subject_hierarchy_with_path_id.xml')
fd_w = open('query_bing_continue_tasks.xml', 'w')
fd_w.write('<?xml version="1.0" encoding="utf-8" ?>\n')
fd_w.write('\t<taxonomy id="-1"  keyword=""  name="SEEUWO_Training_Data"  path="SEEUWO_Training_Data" >\n')
#<topic id="1291"  keyword="Sports medicine"  name="Sports medicine"  path="SEEUWO_Training_Data/Professions_and_Applied_sciences/Human_physical_performance_and_recreation*/Sports_medicine" >
for line in fd:
	line = line.strip()
	if line.find('<topic') != -1:		
		a = line.index('id="')
		b = line[a+4:].index('"')
		tid = line[a+4:][:b]
		if line.find('name') != -1:
			a = line.index('name="')
			b = line[a+6:].index('"')
			name = line[a+6:][:b]
		if line.find('keyword') != -1:
			a = line.index('keyword="')
			b = line[a+9:].index('"')
			keyword = line[a+9:][:b]
		if int(tid) in ids:
			a = line.index('path="')
			b = line[a+6:].index('"')
			path = line[a+6:][:b]
			b = path.split('|')		
			for bb in b:
				fd_w.write('\t\t<topic name="'+name+'" keyword="'+keyword+'" path="' + path+ '"/>\n')				
fd.close()
fd_w.write('\t</taxonomy>')
fd_w.close()
