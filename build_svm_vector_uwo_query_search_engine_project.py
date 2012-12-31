if __name__ == '__main__': 
	from IPython.parallel import Client
	from time import time
	from build_dict_and_stem_map_query_search_engine_project import *
	#end global variables for model

	#db_id_list = 'sorted_unique_query_bing_actual_id_list.txt'
	db_id_list = 'new_3_uwo_all_solr_doc_ids.txt'
	#use dict where rare words occuring less than 3 are removed
	base_dict_fname = '/home/mpi/query_bing_project/query_bing_rare_removed_3.txt'		
	#base_folder = '.'
	stop_fname = 'new_english.stop'
	schema_name = 'uwo'
	table_name = 'uwo_query_bing_nutch_svm_vector'
	global_trunk_size = 50000
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
	mec.execute('pl_build_insert_uwo_svm_features_new(my_trunk, local_trunk_size, schema, table, stop_words, word_dict)')	
	
	end = time()

	print 'using time as ' + str(end - start) + ' seconds'

		
		
	
