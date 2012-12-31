def read_id_list(fname):
	ids = []
	fd = open(fname)
	for line in fd:
		ids.append(line.strip())
	fd.close()
	return ids

def remove_nontext_2(body):
	import re
	body=body.replace("\n", " ")	
	body=re.sub("[^A-Za-z]"," ",body)	
	return body
		
def remove_nontext(body):
	import re
	body=body.replace("\n", " ")
	body=re.sub("&\S*;"," ",body)
	body=re.sub("[^A-Za-z,.;:'/]"," ",body)
	body=re.sub("\""," ",body)
	body=re.sub("\s+"," ",body)
	body=re.sub("\.+",".",body)
	body=re.sub("\.+",".",body)
	body=re.sub(",+",",",body)
	body=re.sub(";+",";",body)	
	return body
	
#build svm token vector
#based on the input dictionary
def extract_doc_features_new(docs, stop_words, cur_dict):
	from nltk.probability import FreqDist
	from nltk.tokenize import regexp_tokenize	
	from help_tools import remove_stop, stem_words
	vectors = []
	for doc in docs:
		
		id = doc[0]		
		title = doc[1]
		body = doc[2]
		
		if title == None:
			title = ''				
		if body == None:
			body = ''					
		
		#to lowercase
		title = title.lower()				
		body = body.lower()
				
		#remove none text
		title = remove_nontext(title)				
		body = remove_nontext(body)
			
		#feature vector
		vector = []
			
		#extract title
		if len(title)>0:
			title_wordlist = regexp_tokenize(title, '[a-zA-Z]+')
			title_removed = remove_stop(title_wordlist, stop_words)
			title_stemmed = stem_words(title_removed)			
			#add _t to the end of title
			title_removed = [t + '_t' for t in title_removed]
			title_stemmed = [t + '_t' for t in title_stemmed]									
			#compute freq
			cp = FreqDist(title_stemmed).items()
			for c in cp:
				arg_term = c[0]
				if arg_term in cur_dict:
					vector.append((cur_dict[c[0]], c[1]))
				
		#extract body text		
		if len(body)>0:
			body_wordlist = regexp_tokenize(body, '[a-zA-Z]+')
			body_removed = remove_stop(body_wordlist, stop_words)
			body_stemmed = stem_words(body_removed)
			
			#add _u to the end of title
			body_removed = [t + '_b' for t in body_removed]
			body_stemmed = [t + '_b' for t in body_stemmed]	
			
			cp =FreqDist(body_stemmed).items()
			for c in cp:
				arg_term = c[0]
				if arg_term in cur_dict:
					vector.append((cur_dict[c[0]], c[1]))
					
		if len(vector) != 0:
				vector.sort()
				vectors.append((id, vector))
	return vectors

def token_tuple_list_to_string(tuples):
	ret = []
	for t in tuples:
		ret.append(str(t[0]) + ':' + str(t[1]))
	return ' '.join(ret)
	
def insert_svm_features_into_db(schema, table, vectors):
	import MySQLdb
	con   =   MySQLdb.connect(host="192.168.0.2",  port=3306, user="root",  passwd="see",  db=schema)  
	cursor   =   con.cursor() 
	for vector in vectors:
		id = vector[0]
		features = token_tuple_list_to_string(vector[1])
		sql = 'insert into ' + table + ' values (' + str(id) + ', "' + features + '", "")'	
		cursor.execute(sql)
	con.commit()
	cursor.close()
	con.close()	

def insert_svm_features_into_uwo_db(schema, table, vectors):
	import MySQLdb
	con   =   MySQLdb.connect(host="192.168.0.2",  port=3306, user="root",  passwd="see",  db=schema)  
	cursor   =   con.cursor() 
	for vector in vectors:
		id = vector[0]
		features = token_tuple_list_to_string(vector[1])
		sql = 'insert into ' + table + ' values (' + str(id) + ', "' + features + '")'	
		cursor.execute(sql)
	con.commit()
	cursor.close()
	con.close()	
	
def update_svm_features_into_db(schema, table, vectors):
	import MySQLdb
	con   =   MySQLdb.connect(host="192.168.0.2",  port=3306, user="root",  passwd="see",  db=schema)  
	cursor   =   con.cursor() 
	for vector in vectors:
		id = vector[0]
		features = token_tuple_list_to_string(vector[1])
		sql = 'update ' + table + ' set tokens="' + features + '" where id=' + str(id)
		cursor.execute(sql)
	con.commit()
	cursor.close()
	con.close()	
		
#build dictionary		
def extract_term_freq_new(docs, stop_words, cur_dict, voc2stem, stem2voc):
	from nltk.probability import FreqDist
	from nltk.tokenize import regexp_tokenize	
	from help_tools import remove_stop, stem_words, make_voc2stem
	for doc in docs:
		
		id = doc[0]		
		title = doc[1]
		body = doc[2]
		
		if title == None:
			title = ''				
		if body == None:
			body = ''					
		
		#to lowercase
		title = title.lower()				
		body = body.lower()
				
		#remove none text
		title = remove_nontext(title)				
		body = remove_nontext(body)
		
		#extract title
		if len(title)>0:
			title_wordlist = regexp_tokenize(title, '[a-zA-Z]+')
			title_removed = remove_stop(title_wordlist, stop_words)
			title_stemmed = stem_words(title_removed)			
			#add _t to the end of title
			title_removed = [t + '_t' for t in title_removed]
			title_stemmed = [t + '_t' for t in title_stemmed]						
			#make voc to stem mapping
			make_voc2stem(title_removed, title_stemmed, voc2stem, stem2voc)			
			
			#compute freq
			cp = FreqDist(title_stemmed).items()
			for c in cp:
				arg_term = c[0]
				if arg_term not in cur_dict:
					cur_dict[arg_term] = 1
				else:
					cur_dict[arg_term] += 1
						
		#extract body text		
		if len(body)>0:
			body_wordlist = regexp_tokenize(body, '[a-zA-Z]+')
			body_removed = remove_stop(body_wordlist, stop_words)
			body_stemmed = stem_words(body_removed)
			
			#add _u to the end of title
			body_removed = [t + '_b' for t in body_removed]
			body_stemmed = [t + '_b' for t in body_stemmed]	
			
			make_voc2stem(body_removed, body_stemmed, voc2stem, stem2voc)			
			
			cp =FreqDist(body_stemmed).items()
			for c in cp:
				arg_term = c[0]
				if arg_term not in cur_dict:
					cur_dict[arg_term] = 1
				else:
					cur_dict[arg_term] += 1
		
	
def build_term_freq_list(max_id, trunks, stop_set):	
	from time import time
	from help_tools import chunks
	from db_util import get_docs_between
	start = time()
	cur_dict = {}
	voc2stem = {}
	stem2voc = {}
	#make trunks
	all_ids = range(max_id)
	all_trunks = chunks(all_ids, trunks)
	tot_trunks = len(all_trunks)
	for trunk in all_trunks:
		start_id = trunk[0]
		end_id = trunk[len(trunk) - 1]
		print 'start extract terms from ' + str(start_id) + ' to ' + str(end_id)
		docs = get_docs_between(start_id, end_id)
		extract_term_freq(docs, stop_set, cur_dict, voc2stem, stem2voc)
		print 'finish extract terms from ' + str(start_id) + ' to ' + str(end_id)
		tot_trunks -= 1
		print str(tot_trunks) + ' remained'		
	end = time()
	print 'Finish tasks in ' + str(int(end - start)) + ' seconds'
	return cur_dict, voc2stem, stem2voc

def pl_build_term_freq_list_new(IDs, trunk_size, stop_set, cur_dict, voc2stem, stem2voc):	
	from time import time
	from help_tools import chunks
	from db_util import get_docs_in_set_query_search_engine
	start = time()	
	all_trunks = chunks(IDs, trunk_size)
	for trunk in all_trunks:
		start_id = trunk[0]
		end_id = trunk[len(trunk) - 1]
		print 'start extract terms from ' + str(start_id) + ' to ' + str(end_id)
		docs = get_docs_in_set_query_search_engine(trunk)
		extract_term_freq_new(docs, stop_set, cur_dict, voc2stem, stem2voc)
		print 'finish extract terms from ' + str(start_id) + ' to ' + str(end_id)		
	end = time()
	print 'Finish tasks in ' + str(int(end - start)) + ' seconds'	

def pl_build_svm_features_new(IDs, trunk_size, schema, table, stop_set, word_dict):	
	from time import time
	from help_tools import chunks
	from db_util import get_docs_in_set_query_search_engine
	start = time()	
	all_trunks = chunks(IDs, trunk_size)
	for trunk in all_trunks:
		start_id = trunk[0]
		end_id = trunk[len(trunk) - 1]
		print 'start making SVM features from ' + str(start_id) + ' to ' + str(end_id)
		docs = get_docs_in_set_query_search_engine(trunk)
		vectors = extract_doc_features_new(docs, stop_set, word_dict)
		#insert_svm_features_into_db(schema, table, vectors)
		update_svm_features_into_db(schema, table, vectors)
		print 'finish making SVM features from ' + str(start_id) + ' to ' + str(end_id)		
	end = time()
	print 'Finish tasks in ' + str(int(end - start)) + ' seconds'

def pl_build_insert_svm_features_new(IDs, trunk_size, schema, table, stop_set, word_dict):	
	from time import time
	from help_tools import chunks
	from db_util import get_docs_in_set_query_search_engine
	start = time()	
	all_trunks = chunks(IDs, trunk_size)
	for trunk in all_trunks:
		start_id = trunk[0]
		end_id = trunk[len(trunk) - 1]
		print 'start making SVM features from ' + str(start_id) + ' to ' + str(end_id)
		docs = get_docs_in_set_query_search_engine(trunk)
		vectors = extract_doc_features_new(docs, stop_set, word_dict)
		insert_svm_features_into_db(schema, table, vectors)		
		print 'finish making SVM features from ' + str(start_id) + ' to ' + str(end_id)		
	end = time()
	print 'Finish tasks in ' + str(int(end - start)) + ' seconds'

def pl_build_insert_uwo_svm_features_new(IDs, trunk_size, schema, table, stop_set, word_dict):	
	from time import time
	from help_tools import chunks
	from db_util import get_docs_in_uwo_set_query_search_engine
	start = time()	
	all_trunks = chunks(IDs, trunk_size)
	for trunk in all_trunks:
		start_id = trunk[0]
		end_id = trunk[len(trunk) - 1]
		print 'start making SVM features from ' + str(start_id) + ' to ' + str(end_id)
		docs = get_docs_in_uwo_set_query_search_engine(trunk)
		vectors = extract_doc_features_new(docs, stop_set, word_dict)
		insert_svm_features_into_uwo_db(schema, table, vectors)		
		print 'finish making SVM features from ' + str(start_id) + ' to ' + str(end_id)		
	end = time()
	print 'Finish tasks in ' + str(int(end - start)) + ' seconds'
			
def write_down_dict(cur_dict, voc2stem, stem2voc, fname_dict, fname_voc_2_stem, fname_stem_2_voc):
	from help_tools import write_voc_2_stem, write_dict_with_occ
	write_voc_2_stem(voc2stem, stem2voc, fname_voc_2_stem, fname_stem_2_voc)
	write_dict_with_occ(cur_dict, fname_dict)	
		
def chunks(l, n):
    return [l[i:i+n] for i in range(0, len(l), n)]
    	
if __name__ == '__main__':				
	from IPython.parallel import Client
	from time import time

	#end global variables for model

	#db_id_list = 'sorted_unique_query_bing_actual_id_list.txt'
	db_id_list = 'new_query_bing_used_id_list.txt'
	base_dict_fname = 'query_bing_dictionary0703.txt'
	base_voc2stem_fname = 'query_bing_voc2stem.txt'
	base_stem2voc_fname = 'query_bing_stem2voc.txt'
	base_folder = '/home/mpi/shareddir/query_bing_dictionary'
	#base_folder = '.'
	stop_fname = 'new_english.stop'
	
	global_trunk_size = 60000
	local_trunk_size = 250
	start = time()

	rc = Client()

	#set up as blocking mode	
	mec = rc[:]
	mec.block = True

	mec.execute('import os')
	mec.execute('os.chdir("/home/mpi/query_search_project/")')	
	mec.execute('from build_dict_and_stem_map_query_search_engine_project import *')
	mec.execute('from help_tools import read_stop_list')	

	#init models
	#each machines load parts of the models	
	mec['base_dict_fname'] = base_dict_fname
	mec['stop_fname'] = stop_fname
	mec['local_trunk_size']	= local_trunk_size
	mec['base_voc2stem_fname']	= base_voc2stem_fname
	mec['base_stem2voc_fname']	= base_stem2voc_fname
	mec['base_folder'] = base_folder
	
	mec.scatter('my_id', rc.ids)
	
	#init dictionary
	mec.execute('cur_dict = {}')
	mec.execute('voc2stem = {}')
	mec.execute('stem2voc = {}')
		
	mec.execute('stop_words = read_stop_list(stop_fname)')
	print 'finish reading stopwords'
	
	#read all ids
	all_ids = read_id_list(db_id_list)	
	
	local_trunks = chunks(all_ids, global_trunk_size)
	
	n_trunk = len(local_trunks)
	m_trunk = 0
	for trunk in local_trunks:	
		start1 = time()			
		print 'start extract svm features into dictionary'
		mec.scatter('local_trunk', trunk)		
		mec.execute('pl_build_term_freq_list_new(local_trunk, local_trunk_size, stop_words, cur_dict, voc2stem, stem2voc)')
		print 'end extract svm features into dictionary'
		end1 = time()
		print 'Finish trunk ' +str(m_trunk) + '/' + str(n_trunk)+ ' in ' + str(int(end1 - start1)) + ' seconds'
		print '...'
		m_trunk += 1	
	mec.execute('write_down_dict(cur_dict, voc2stem, stem2voc, base_folder + "/" + str(my_id[0]) + "_" + base_dict_fname, base_folder + "/" + str(my_id[0]) + "_" + base_voc2stem_fname, base_folder + "/" + str(my_id[0]) + "_" + base_stem2voc_fname)')
	end = time()
	print 'Finish tasks in ' + str(int(end - start)) + ' seconds'
	
