def read_id_list(fname):
	ids = []
	fd = open(fname)
	for line in fd:
		ids.append(int(line.strip()))
	fd.close()
	return ids

def chunks(l, n):
    return [l[i:i+n] for i in range(0, len(l), n)]
    
def path2catID(path, path2id):
	#remove file part
	if path.endswith('.xml'):
		b = path.rindex('/')
		path = path[:b]		
	prefixes = ['/media/d/SEEUWO_Training_Data/', 'SEEUWO_Training_Data/', '/home/xiao/wiki_subject_hierarchy/SEEUWO_Training_Data_top_two/']
	
	v = ''	
	if path.startswith(prefixes[0]):
		v = path[len(prefixes[0]):]
	elif path.startswith(prefixes[1]):
		v = path[len(prefixes[1]):]
	elif path.startswith(prefixes[2]):
		v = path[len(prefixes[2]):]	
	
	#print 'SEEUWO_Training_Data/' + v
	
	#print new_path
	if 'SEEUWO_Training_Data/' + v in path2id:
		return path2id['SEEUWO_Training_Data/' + v]
	elif path in path2id:
		print 'xxxxxxx'
		return path2id[path]
	else:
		#print new_path
		return -1
			
def read_in_id_path_table(fname):	
	path2id = {}
	fd=  open(fname)
	ids = []
	fd_w = open('tmp.txt', 'w')	
	for line in fd:
		line = line.strip()
		if line.startswith('<topic'):
			a = line.index('id=')
			b = line[a:].index(' ')
			cid = line[a:][4:b-1]
			a = line.index('path=')
			b = line[a:].index(' ')
			path = line[a:][6:b-1]	
			path = path.split('|')	
			fd_w.write('|'.join(path) + '\n')
			if len(path) > 1:
				print 'multiple path for single node found', path
			for p in path:				
				if p in path2id:
					print line
				path2id[p] = cid
				if p.endswith('*'):
					print 'find * ' + p
					p = p[:len(p)-1]
					path2id[p] = cid
				
			ids.append(cid)
	fd.close()
	fd_w.close()
	return path2id

def read_in_id_path_list(fname):
	id2path = {}
	fd = open(fname)
	for line in fd:
		line = line.strip().split('|')
		id2path[int(line[0])] = line[1]
	fd.close()	
	return id2path

def read_in_id_path_list(fname):
	id2path = {}
	fd = open(fname)
	for line in fd:
		line = line.strip()
		a = line.index(' ')
		id = line[:a]
		path = line[a+1:]
		id2path[int(id)] = path
	fd.close()	
	return id2path
		
def get_all_ancestor(id, id2node):
	ans = [id]
	if id in id2node:
		nd = id2node[id]
		n = nd.parent
		while n.labelIndex != -1:
			ans.append(n.labelIndex)
			n = n.parent
		ans.sort()
	return ans	

def update_svm_cats(schema, table, cats):
	import MySQLdb
	con   =   MySQLdb.connect(host="192.168.0.2",  port=3306, user="root",  passwd="see",  db=schema)  
	cursor   =   con.cursor()  
	for cat in cats:
		sql = 'update ' + table + ' set categories="' + cat[1] + '" where id='+ str(cat[0])
		#sql = 'insert into ' + table + ' (id,categories) values(' + str(cat[0]) + ',"' + cat[1] + '")'
		#print sql
		cursor.execute(sql)
	con.commit()	
	cursor.close()
	con.close()	
		
def pl_build_categories(IDs, id2path, path2id, id2nodes, trunk_size, schema, table):	
	from time import time
	from help_tools import chunks
	from db_util import get_docs_in_set_query_search_engine
	start = time()	
	all_trunks = chunks(IDs, trunk_size)
	fd_w = open('tmp.tmp', 'w')
	for trunk in all_trunks:
		start_id = trunk[0]
		end_id = trunk[len(trunk) - 1]
		print 'start making SVM features from ' + str(start_id) + ' to ' + str(end_id)
		cats = []
		for id in trunk:
			if id in id2path:
				path = id2path[id]				
				catid = int(path2catID(path, path2id))				
				if catid != -1:
					nodes = get_all_ancestor(catid, id2nodes)
					nodes = ','.join([str(nd) for nd in nodes])
					#print catid, id,nodes
					cats.append((id, nodes))				
				else:
					fd_w.write(path + '\n')
		update_svm_cats(schema, table, cats)
		print 'finish making SVM features from ' + str(start_id) + ' to ' + str(end_id)		
	end = time()
	fd_w.close()
	print 'Finish tasks in ' + str(int(end - start)) + ' seconds'
	
if __name__ == '__main__': 
	from active_learning import *
	db_id_list = 'query_bing_id_list.txt'
	xmlfname = 'new_wiki_subject_hierarchy_with_path_id.xml'
	svm_hier = 'new_wiki_subject_svm_hierarchy.txt'
	id_path_list = 'query_bing_id_path_list.txt'
	schema = 'query_search_engine'
	table = 'svm_text_tokens'
	
	empty_id_list = 'query_bing_empty_id_list.txt'
	id2path = read_in_id_path_list(id_path_list)
	all_ids = read_id_list(db_id_list)	
	root = Node().read_tree(svm_hier)
	catid2nodes = {}
	root.get_id_to_node_map(catid2nodes)
	path2catid = read_in_id_path_table(xmlfname)
	local_trunk_size = 500
	
	pl_build_categories(all_ids, id2path, path2catid, catid2nodes, local_trunk_size, schema, table)
	#pl_build_categories([7791], id2path, path2catid, catid2nodes, local_trunk_size, schema, table)
	
	"""
	from IPython.parallel import Client
	from time import time
	from build_dict_and_stem_map_query_search_engine_project import *
	#end global variables for model

	db_id_list = 'sorted_unique_query_bing_actual_id_list.txt'
	base_dict_fname = '/home/mpi/query_bing_project/query_bing_dictionary0102_rare_removed_4.txt'		
	#base_folder = '.'
	stop_fname = 'new_english.stop'
	schema_name = 'query_search_engine'
	table_name = 'svm_text_tokens'
	global_trunk_size = 100000
	local_trunk_size = 250
	start = time()

	rc = Client()

	#set up as blocking mode	
	mec = rc[:]
	mec.block = True

	mec.execute('import os')
	mec.execute('os.chdir("/home/mpi/query_search_project/")')	
	mec.execute('from build_dict_and_stem_map_query_search_engine_project import *')
	mec.execute('from help_tools import read_stop_list, read_dict_query_bing')	

	#init models
	#each machines load parts of the models	
	mec['base_dict_fname'] = base_dict_fname
	mec['stop_fname'] = stop_fname
	mec['local_trunk_size']	= local_trunk_size		
	mec['schema'] = schema_name
	mec['table'] = table_name
		
	mec.execute('stop_words = read_stop_list(stop_fname)')
	mec.execute('word_dict = read_dict_query_bing(base_dict_fname, " ")')
	print 'finish reading stopwords and dictionary'
	#read all ids
	all_ids = read_id_list(db_id_list)	
	mec.scatter('my_trunk', all_ids)	
	print 'starting jobs'
	mec.execute('pl_build_svm_features_new(my_trunk, local_trunk_size, schema, table, stop_words, word_dict)')	
	
	end = time()

	print 'using time as ' + str(end - start) + ' seconds'
	"""
		
		
	
