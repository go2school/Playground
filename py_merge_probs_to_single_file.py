def usage():
	print 'cmd --schema <schema> '
	
if __name__ == '__main__':
	import sys, getopt
	import subprocess
	opts, args = getopt.getopt(sys.argv[1:], 'x', ['schema='])	
	global_trunk_size = 50000
	work_folder = '/home/mpi/url_reorganization'	
	schema = ''	
	doc_table = 'new_nutch_docs'		
	for o, a in opts:
		if o == "--schema":
			schema = a				
	if schema == '':
		print usage()
		sys.exit(1)
		
						
	from py_merge_probs_to_file import *
	#merge mustang prediction		
	trunk_size = 500
	line_length = 8
	
	in_file_ext = 'query_bing_test_predicted_probs'
	in_folder = '/home/mpi/shareddir/seeuwo/'+schema+'_query_bing_prediction'
	out_folder = '/home/mpi/shareddir/seeuwo/merged_prediction'
	out_file_ext = schema + '_query_bing_merged_probability.txt'
	doc_id_files = 'doc_ids'
	used_id_file = '/home/mpi/uwo_query_bing_workingspace/used_tree_nodes.txt'
	
	#read the category we use
	used_ids = []
	fd = open(used_id_file)
	for line in fd:
		used_ids.append(int(line.strip()))
	fd.close()
	
	#read how many example for the testing data
	num_lines = get_num_lines(in_folder + '/' + doc_id_files)

	#split the testing data into trunks
	all_trunks = chunks(range(num_lines), trunk_size)
	
	id_trunk = 0
	all_probs = {}	
	#create merged file
	fd = open(out_folder + '/' +out_file_ext, 'w')
	fd.close()
	for trunk in all_trunks:
		for c in used_ids:
			all_probs[c] = None
		for c in used_ids:
			fname = in_folder + '/' + str(c) + '_' + in_file_ext
			probs = read_probs(fname, id_trunk, line_length, trunk_size, len(trunk))
			all_probs[c] = probs
		id_trunk += 1
		fd = open(out_folder + '/' + out_file_ext, 'a')
		for i in range(len(trunk)):
			str_prediction = []
			for c in used_ids:
				str_prediction.append(str(c)+':'+str(all_probs[c][i]))
			fd.write(','.join(str_prediction) + '\n')
		fd.close()
	
	p1,p2=check_correctness(out_folder +  '/' + out_file_ext, used_ids[0], in_folder + '/' + str(used_ids[0]) + '_' + in_file_ext)
	for i in range(len(p1)):
		if p1[i] != p2[i]:
			print p1[i], p2[i], 'err'
