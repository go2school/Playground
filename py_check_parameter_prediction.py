folder = '/home/mpi/uwo_query_bing_merged_parameter_prediction'
file_ext = 'query_bing_parameter_merged_probability.txt'
dmoz_tree = '/home/mpi/uwo_query_bing_workingspace/new_query_bing_hierarchy.txt'
short_file = 'uwo_short_doc_10.txt'
svm_id_list_file = '/home/mpi/uwo_query_bing_workingspace/uwo_query_bing_id_list.txt'
output_folder = '/home/mpi/uwo_query_bing_merged_parameter_prediction/'
output_file = 'query_bing_new_results_with_reference_and_other_pos_2_and_spanning.txt'
used_tree_nodes = '/home/mpi/uwo_query_bing_workingspace/used_tree_nodes.txt'
span_distrubiton_fname = '/home/mpi/uwo_query_bing_workingspace/new_query_bing_training_dataset_cat_probability.txt'
actual_ids = 'actual_ids.txt'

parameters = [1, 0.5, 2]

ids = set()
fd = open(short_file)
for line in fd:
	line = line.strip().split(' ')
	ids.add(line[0])
fd.close()


flist = []
oflist = []
for p in parameters:
	tfd = open(folder + '/' + str(p) + '_' + file_ext)
	wfd = open(folder + '/' + str(p) + '_short_' + file_ext, 'w')
	flist.append(tfd)
	oflist.append(wfd)

fd = open(svm_id_list_file)	
fd_id = open(actual_ids, 'w')
for line in fd:	
	lines = []
	for i in range(3):
		lines.append(flist[i].readline().strip())
	if line.strip() in ids:
		for i in range(3):
			oflist[i].write(lines[i] + '\n')	
		fd_id.write(line.strip() + '\n')	
for i in range(3):			
	flist[i].close()
	oflist[i].close()
fd.close()	
fd_id.close()
