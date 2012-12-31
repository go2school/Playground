def string_to_probs_query_bing(line, sep):
	probs = {}
	line = line.strip().split(sep)
	for l in line:
		l = l.split(':')
		probs[int(l[0])] = float(l[1])
	return probs
	
def probs_to_string_query_bing(probs):
	cats = probs.keys()
	cats.sort()
	str_p = [str(c)+':'+str(probs[c]) for c in cats]
	return ','.join(str_p)
	
def make_modified_probability_with_r_cut_probability_span_thresholded_specified_cat_query_bing(isShort, depth, max_depth, old_probs, span_threshold_distribution, predict_threshold, node, used_ids, largepos_probs, small_pos_probs):		
	import random
	#check if this example does not predict any category (check if it is other)	
	is_other = True
	pos_prediction = []
	
	if depth >= max_depth:
		return
		
	#filter used nodes
	child_nodes = [c for c in node.children if c.labelIndex in used_ids]
	
	#we do not need to care leaf nodes
	if len(child_nodes) == 0:
		return
	
	#get all positive prediction here
	for c in child_nodes:		
		if old_probs[c.labelIndex] >= predict_threshold:
			pos_prediction.append((c.labelIndex, old_probs[c.labelIndex]))
			is_other = False	
	
	if is_other == False:
		#check if it is prdicted more than span	
		#compute span first
		rv = random.random()			
		for p in span_threshold_distribution[root.labelIndex]:
			if rv <= p[1]:
				break
		#setup span
		span_threshold = p[0]
		
		#choose top k cats category
		pos_prediction = sorted(pos_prediction, key=lambda s:s[1], reverse=True)		
		needed = min(span_threshold, len(pos_prediction))		
		
		print 'needed ', needed
		#for not needed prediction, change its probability to small one
		for i in range(needed, len(pos_prediction)): #[needed, n]
			#if these small probs are still larger than prediction threhosld, we further reduce them by half
			if small_pos_probs[pos_prediction[i][0]] >= predict_threshold:	
				old_probs[pos_prediction[i][0]] = small_pos_probs[pos_prediction[i][0]]	 * 0.5
			else:
				old_probs[pos_prediction[i][0]] = small_pos_probs[pos_prediction[i][0]]	
			#print pos_prediction[i][0], old_probs[pos_prediction[i][0]], small_pos_probs[pos_prediction[i][0]]
		
		#goes down to deeper categories	
		for c in child_nodes:						
			#only change the subtree whose root's probability is larger than threshold
			if old_probs[c.labelIndex] >= predict_threshold:
				print 'drill down at' + str(c.labelIndex)
				make_modified_probability_with_r_cut_probability_span_thresholded_specified_cat_query_bing(isShort, depth + 1, max_depth, old_probs, span_threshold_distribution, predict_threshold, c, used_ids, largepos_probs, small_pos_probs)		
	else:
		#only if this doc is not short, we will check its chilren
		#otherwise, we discard its children
		if isShort == False:
			#if no prediction made at this level, then we enlarge them
			print 'other doc at' + str(node.labelIndex)
			#increase the positive score		
			all_prob_cats = [(c.labelIndex, largepos_probs[c.labelIndex]) for c in child_nodes]
			#choose top k categories
			all_prob_cats = sorted(all_prob_cats, key=lambda s:s[1], reverse=True)
			
			#compute span first
			rv = random.random()			
			for p in span_threshold_distribution[root.labelIndex]:
				if rv <= p[1]:
					break
			#setup span
			span_threshold = p[0]
			
			#increase only need probs
			needed = min(span_threshold, len(child_nodes))		
			for i in range(needed):	#only enlarge needed [0, needed]
				#just use the larger prediction, if it is still less than prediction, we do not care
				old_probs[all_prob_cats[i][0]] = all_prob_cats[i][1]		
			#go deeper
			for c in child_nodes:			
				if old_probs[c.labelIndex] >= predict_threshold:
					print 'drill down with modified at' + str(c.labelIndex)
					make_modified_probability_with_r_cut_probability_span_thresholded_specified_cat_query_bing(isShort, depth + 1, max_depth, old_probs, span_threshold_distribution, predict_threshold, c, used_ids, largepos_probs, small_pos_probs)		
				
				
#algorithm
#recusively do
#if we reach the maximal depth, then just return
#if it is short, we reduce all its positive svm weight by half
#for each node
#	if the node has children prediction based on threshold
#		shrinks the prediction by spanning distribution
#	else
#		if it is not short
#			then we enlarge some categories' prediction based on spanning distribution				
if __name__ == '__main__': 										
	from py_modified_svm_probs import *
	from py_tree_check_r_cut import read_r_cut_distribution
	
	folder = '/home/mpi/uwo_query_bing_merged_parameter_prediction'
	file_ext = 'query_bing_parameter_merged_probability.txt'
	#file_ext = 'short_query_bing_parameter_merged_probability.txt'
	#file_ext = 'tmp.txt'
	dmoz_tree = '/home/mpi/uwo_query_bing_workingspace/new_query_bing_hierarchy.txt'
	short_file = 'uwo_query_bing_short_doc_10.txt'
	
	svm_id_list_file = '/home/mpi/uwo_query_bing_workingspace/uwo_query_bing_id_list.txt'
	output_folder = '/home/mpi/uwo_query_bing_merged_parameter_prediction/'
	output_file = 'query_bing_new_results_with_reference_and_other_pos_2_and_spanning_depth_2_limit.txt'
	used_tree_nodes = '/home/mpi/uwo_query_bing_workingspace/used_tree_nodes.txt'
	span_distrubiton_fname = '/home/mpi/uwo_query_bing_workingspace/new_query_bing_training_dataset_cat_probability.txt'
	#actual_ids_fname = 'actual_ids.txt'
	actual_ids_fname = 'st.txt'
	max_depth = 2#maximal depth shall we go
	
	span_threshold_distribution = read_r_cut_distribution(span_distrubiton_fname)
	print span_threshold_distribution
	
	cats = set()
	fd = open(used_tree_nodes)
	for line in fd:
		cats.add(int(line.strip()))
	fd.close()
	
	parameters = [1, 0.5, 2]
	threshold = 0.5	
	#span_threshold = 2
	
	#open all files
	fd_list = []
	for p in parameters:
		fd = open(folder + '/' + str(p) + '_' + file_ext)
		fd_list.append(fd)
		
	#get doc ID	
	svm_id_list = read_id_list(svm_id_list_file)
	short_id_list = set(read_id_list(short_file))
	#short_id_list = set(read_id_list(actual_ids_fname))

	#read tree
	root = Node().read_tree(dmoz_tree)

	#only considering normal case (1), reduce positive by half case (0.5) and double positive case (2)
	normal = 0
	short = 1
	largepos = 2

	fd_w = open(output_folder + output_file, 'w')
	for id in svm_id_list:
	#for id in short_id_list:
		print id
		#read line at each result	
		lines = ['' for i in range(len(parameters))]
		for i in range(len(parameters)):
			lines[i] = fd_list[i].readline()		
				
		#read normal prediction			
		old_probs = string_to_probs_query_bing(lines[normal], ',')
		#read large prediction			
		large_pos_probs = string_to_probs_query_bing(lines[largepos], ',')		
		#read small prediction			
		small_pos_probs = string_to_probs_query_bing(lines[short], ',')	
		
		isShort = False
		if id in short_id_list:
			#reset normal probs by using short results
			old_probs = {}
			for p in small_pos_probs:
				old_probs[p] = small_pos_probs[p]
			print 'see short at ' + str(id)		
			isShort = True			
				
		make_modified_probability_with_r_cut_probability_span_thresholded_specified_cat_query_bing(isShort, 0, max_depth, old_probs, span_threshold_distribution, threshold, root, cats, large_pos_probs, small_pos_probs)
		#write probs		
		str_probs = probs_to_string_query_bing(old_probs)
		fd_w.write(str_probs + '\n')			
	fd_w.close()
