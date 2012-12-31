#<topic classifier="yes"  id="22"  keyword="Languages"  name="Languages"  path="SEEUWO_Training_Data/Humanities/Linguistics/Languages" >
def read_in_id_path_table():
	fname = 'new_wiki_subject_hierarchy_with_path_id.xml'
	path2id = {}
	fd=  open(fname)	
	for line in fd:
		line = line.strip()
		if line.startswith('<topic'):
			a = line.index('id=')
			b = line[a:].index(' ')
			cid = line[a:][4:b-1]
			a = line.index('path=')
			b = line[a:].index(' ')
			path = line[a:][6:b-1]		
			if path in path2id:
				print line
			if path != '':
				path2id[path] = cid			
	fd.close()
	return path2id

if __name__ == '__main__': 
	svm_hier = 'new_wiki_subject_svm_hierarchy.txt'
	#root = Node().read_tree(svm_hier)
	ret = read_in_id_path_table()
