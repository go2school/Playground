from active_learning import *

def read_id_list(fname):
	id_list = []
	fd = open(fname)
	for line in fd:
		id_list.append(int(line.strip().split(' ')[0]))
	fd.close()
	return id_list
	
def string_to_probs(line, sep, ncats):
	probs = {}
	line = line.strip().split(sep)
	for c in range(ncats):
		probs[c] = float(line[c])
	return probs
			
def probs_to_string(probs):
	cats = probs.keys()
	cats.sort()
	str_p = [str(probs[c]) for c in cats]
	return ','.join(str_p)
				
def make_modified_probability(old_probs, threshold, repredict_other_threshold, node, largepos_probs):		
	#check if this example does not predict any category (check if it is other)
	is_other = True
	for c in node.children:		
		if old_probs[c.labelIndex] >= threshold:
			is_other = False
			break
	if is_other == False:		
		for c in node.children:						
			#only change the subtree whose root's probability is larger than threshold
			if old_probs[c.labelIndex] >= threshold:
				print 'drill down at' + str(c.labelIndex)
				make_modified_probability(old_probs, threshold, repredict_other_threshold, c, largepos_probs)
	else:
		print 'other doc at' + str(node.labelIndex)
		#increase the positive score		
		for c in node.children:
			#check if it is too small. if so, we do not take the risk to enlarge it
			if old_probs[c.labelIndex] >= repredict_other_threshold:				
				old_probs[c.labelIndex] = largepos_probs[c.labelIndex]
				if old_probs[c.labelIndex] >= threshold:
					print 'drill down with modified at' + str(c.labelIndex)
					make_modified_probability(old_probs, threshold, repredict_other_threshold, c, largepos_probs)

def make_modified_probability_bias_specified_cat(bias_cat, old_probs, threshold, node, largepos_probs):		
	#check if this example does not predict any category (check if it is other)
	is_other = True
	pos_prediction = []
	for c in node.children:		
		if old_probs[c.labelIndex] >= threshold:
			pos_prediction.append(c.labelIndex)
			is_other = False
			break
	if is_other == False:	
		#check if it is only predicted as bias cat, if so, then enlarge other by factor
		if len(pos_prediction) == 1 and pos_prediction[0] == bias_cat:
			for c in node.children:
				old_probs[c.labelIndex] = largepos_probs[c.labelIndex]
		for c in node.children:						
			#only change the subtree whose root's probability is larger than threshold
			if old_probs[c.labelIndex] >= threshold:
				print 'drill down at' + str(c.labelIndex)
				make_modified_probability_bias_specified_cat(bias_cat, old_probs, threshold, c, largepos_probs)
	else:
		print 'other doc at' + str(node.labelIndex)
		#increase the positive score		
		for c in node.children:						
			old_probs[c.labelIndex] = largepos_probs[c.labelIndex]
			if old_probs[c.labelIndex] >= threshold:
				print 'drill down with modified at' + str(c.labelIndex)
				make_modified_probability_bias_specified_cat(bias_cat, old_probs, threshold, c, largepos_probs)

def make_modified_probability_bias_thresholded_specified_cat(bias_cat, old_probs, span_threshold, threshold, node, largepos_probs):		
	#check if this example does not predict any category (check if it is other)
	is_other = True
	pos_prediction = []
	for c in node.children:		
		if old_probs[c.labelIndex] >= threshold:
			pos_prediction.append(c.labelIndex)
			is_other = False
			break
	if is_other == False:	
		#check if it is only predicted as bias cat, if so, then enlarge other by factor
		if len(pos_prediction) == 1 and pos_prediction[0] == bias_cat:
			#choose top k cats except the bias category
			all_prob_cats = [(c.labelIndex, largepos_probs[c.labelIndex]) for c in node.children if c.labelIndex != bias_cat]
			all_prob_cats = sorted(all_prob_cats, key=lambda s:s[1], reverse=True)
			needed = min(span_threshold-1, len(node.children)-1)#minus 1 means we do not want predict as bias cat
			if needed >= 1:
				for i in range(needed):				
					old_probs[all_prob_cats[i][0]] = all_prob_cats[i][1]
		#we do not go deeper
		"""
		for c in node.children:						
			#only change the subtree whose root's probability is larger than threshold
			if old_probs[c.labelIndex] >= threshold:
				print 'drill down at' + str(c.labelIndex)
				make_modified_probability_bias_thresholded_specified_cat(bias_cat, old_probs, span_threshold, threshold, c, largepos_probs)
		"""
	else:
		print 'other doc at' + str(node.labelIndex)
		#increase the positive score		
		#choose top k cats except the bias category
		all_prob_cats = [(c.labelIndex, largepos_probs[c.labelIndex]) for c in node.children]
		all_prob_cats = sorted(all_prob_cats, key=lambda s:s[1], reverse=True)
		needed = min(span_threshold, len(node.children)-1)#minus 1 means we do not want predict as bias cat
		if needed >= 1:
			for i in range(needed):				
				old_probs[all_prob_cats[i][0]] = all_prob_cats[i][1]
		#we do not go deeper
		"""
		for c in node.children:			
			if old_probs[c.labelIndex] >= threshold:
				print 'drill down with modified at' + str(c.labelIndex)
				make_modified_probability_bias_thresholded_specified_cat(bias_cat, old_probs, span_threshold, threshold, c, largepos_probs)
		"""

def make_modified_probability_with_r_cut_span_thresholded_specified_cat_query_bing(old_probs, span_threshold, predict_threshold, node, used_ids, largepos_probs, small_pos_probs):		
	#check if this example does not predict any category (check if it is other)
	is_other = True
	pos_prediction = []
	#filter used nodes
	child_nodes = [c for c in node.children if c.labelIndex in used_ids]
	#get all positive prediction here
	for c in child_nodes:		
		if old_probs[c.labelIndex] >= predict_threshold:
			pos_prediction.append((c.labelIndex, old_probs[c.labelIndex]))
			is_other = False			
	if is_other == False:
		#check if it is prdicted more than span				
		#choose top k cats category
		pos_prediction = sorted(pos_prediction, key=lambda s:s[1], reverse=True)		
		needed = min(span_threshold, len(pos_prediction))		
		#for not needed prediction, change its probability to small one
		for i in range(needed, len(pos_prediction)): #[needed, n]
			#if these small probs are still larger than prediction threhosld, we further reduce them by half
			if small_pos_probs[pos_prediction[i][0]] >= predict_threshold:	
				old_probs[pos_prediction[i][0]] = small_pos_probs[pos_prediction[i][0]]	 * 0.5
			else:
				old_probs[pos_prediction[i][0]] = small_pos_probs[pos_prediction[i][0]]	
		#goes down to deeper categories	
		for c in child_nodes:						
			#only change the subtree whose root's probability is larger than threshold
			if old_probs[c.labelIndex] >= predict_threshold:
				print 'drill down at' + str(c.labelIndex)
				make_modified_probability_with_r_cut_span_thresholded_specified_cat_query_bing(old_probs, span_threshold, predict_threshold, c, used_ids, largepos_probs, small_pos_probs)		
	else:
		#if no prediction made at this level, then we enlarge them
		print 'other doc at' + str(node.labelIndex)
		#increase the positive score		
		all_prob_cats = [(c.labelIndex, largepos_probs[c.labelIndex]) for c in child_nodes]
		#choose top k categories
		all_prob_cats = sorted(all_prob_cats, key=lambda s:s[1], reverse=True)
		needed = min(span_threshold, len(child_nodes))		
		for i in range(needed):	#only enlarge needed [0, needed]
			#just use the larger prediction, if it is still less than prediction, we do not care
			old_probs[all_prob_cats[i][0]] = all_prob_cats[i][1]		
		#go deeper
		for c in child_nodes:			
			if old_probs[c.labelIndex] >= predict_threshold:
				print 'drill down with modified at' + str(c.labelIndex)
				make_modified_probability_with_r_cut_span_thresholded_specified_cat_query_bing(old_probs, span_threshold, predict_threshold, c, used_ids, largepos_probs, small_pos_probs)		
		
#
#old_probs: original probability
#span_cats: the braching spacning factor at each node
#
def check_prediction_span(old_probs, span_cats, threshold, node):		
	#increase the positive score	
	span_cats[node.labelIndex] = 0		
	for c in node.children:								
		if old_probs[c.labelIndex] >= threshold:								
			span_cats[node.labelIndex] += 1	#parent node count one spanning			
			check_prediction_span(old_probs, span_cats, threshold, c)
	
def compare_prediction(f1, f2, ncats):
	fd1 = open(f1)								
	fd2 = open(f2)
	for line in fd1:
		p1 = string_to_probs(line.strip(), ',', ncats)
		line = fd2.readline().strip()
		p2 = string_to_probs(line.strip(), ',', ncats)
		for c in range(ncats):
			if p1[c] != p2[c]:
				print p1[c], p2[c], 'diff'
	fd1.close()
	fd2.close()
									
if __name__ == '__main__': 										
	
	folder = '/home/xiao/mustangs_merged'
	file_ext = 'mustangs_parameter_merged_probability.txt'
	dmoz_tree = 'dmoz_hierarchy.txt'
	short_file = 'mustangs_short_doc_10.txt'
	svm_id_list_file = 'westernmustangs_svm_ids.txt'
	output_folder = '/home/xiao/mustangs_merged/'
	output_file = 'mustangs_new_results.txt'
	
	folder = '/home/xiao/uwo_to_do_merged'
	file_ext = 'to_do_parameter_merged_probability.txt'
	dmoz_tree = 'dmoz_hierarchy.txt'
	short_file = 'uwo_to_do_short_doc_10.txt'
	svm_id_list_file = 'uwo_to_do_ids.txt'
	output_folder = '/home/xiao/uwo_to_do_merged/'
	output_file = 'uwo_to_do_new_results.txt'
	
	
	"""
	folder = '/home/xiao/uwo_parameter_merged_prediction'
	file_ext = 'uwo_parameter_merged_probability.txt'
	dmoz_tree = 'dmoz_hierarchy.txt'
	short_file = 'uwo_short_doc_10.txt'
	svm_id_list_file = 'uwo_new_svm_ids.txt'
	output_folder = '/home/xiao/uwo_parameterized_prediction/'
	output_file = 'uwo_new_results.txt'
	"""
	
	parameters = [1, 0.5, 2]
	threshold = 0.5
	ncats = 662
	repredict_other_threshold = 0.1

	#compare_prediction(output_folder + 'uwo_new_results_with_reference_and_other_pos_2_and.txt', output_folder + 'uwo_new_results_with_reference_and_other_pos_2_and_spanning.txt', ncats)
	
	#open all files
	fd_list = []
	for p in parameters:
		fd = open(folder + '/' + str(p) + '_' + file_ext)
		fd_list.append(fd)
		
	#get doc ID	
	svm_id_list = read_id_list(svm_id_list_file)
	short_id_list = set(read_id_list(short_file))

	#read tree
	root = Node().read_tree(dmoz_tree)

	#only considering normal case (1), reduce positive by half case (0.5) and double positive case (2)
	normal = 0
	short = 1
	largepos = 2

	fd_w = open(output_folder + output_file, 'w')
	for id in svm_id_list:
		print id
		#read line at each result	
		lines = ['' for i in range(len(parameters))]
		for i in range(len(parameters)):
			lines[i] = fd_list[i].readline()		
		if id in short_id_list:
			#use short results
			str_probs = lines[short].strip()
			print 'see short at ' + str(id)
		else:
			#string to prob dict		
			old_probs = string_to_probs(lines[normal], ',', ncats)
			tmp = {}
			for a in old_probs:
				tmp[a] = old_probs[a]
			large_pos_probs = string_to_probs(lines[largepos], ',', ncats)		
			make_modified_probability(old_probs, threshold, repredict_other_threshold, root, large_pos_probs)
			str_probs = probs_to_string(old_probs)
		fd_w.write(str_probs + '\n')	
	fd_w.close()
