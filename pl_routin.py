def do_jobs(fd, my_trunk, local_trunk_size, stop_sets, vocabulary):	
	from help_tools import chunks
	from db_util import get_docs_between
	from build_dict_and_stem_map import extract_doc_features	
		
	local_trunks = chunks(my_trunk, local_trunk_size)	
	for trunk in local_trunks:
		start_id = trunk[0]
		end_id = trunk[len(trunk) - 1]
		docs = get_docs_between(start_id, end_id)
		vectors = extract_doc_features(docs, stop_sets, vocabulary)
		for vector in vectors:			
			fd.write(str(vector[0]))
			for wd in vector[1]:
				fd.write(' ' + str(wd[0]) + ':' + str(wd[1]))
			fd.write('\n')

def do_job_adv(fname, my_trunk, local_trunk_size, stop_sets, vocabulary):	
	from help_tools import chunks
	from db_util import get_docs_between
	from build_dict_and_stem_map import extract_doc_features	
		
	fd = open(fname, 'w')
	local_trunks = chunks(my_trunk, local_trunk_size)	
	for trunk in local_trunks:
		start_id = trunk[0]
		end_id = trunk[len(trunk) - 1]
		docs = get_docs_between(start_id, end_id)
		vectors = extract_doc_features(docs, stop_sets, vocabulary)
		for vector in vectors:			
			fd.write(str(vector[0]))
			for wd in vector[1]:
				fd.write(' ' + str(wd[0]) + ':' + str(wd[1]))
			fd.write('\n')
	fd.close()

def do_job_adv_new(fname, my_trunk, local_trunk_size, stop_sets, vocabulary):	
	from help_tools import chunks
	from db_util import get_docs_between_new_uwo
	from build_dict_and_stem_map_new import extract_doc_features_new	
		
	fd = open(fname, 'w')
	local_trunks = chunks(my_trunk, local_trunk_size)	
	for trunk in local_trunks:
		start_id = trunk[0]
		end_id = trunk[len(trunk) - 1]
		docs = get_docs_between_new_uwo(start_id, end_id)
		vectors = extract_doc_features_new(docs, stop_sets, vocabulary)
		for vector in vectors:			
			fd.write(str(vector[0]))
			for wd in vector[1]:
				fd.write(' ' + str(wd[0]) + ':' + str(wd[1]))
			fd.write('\n')
	fd.close()
