import os
def get_num_lines(fname):
	n = 0
	fd = open(fname)
	for line in fd:
		n += 1
	fd.close()
	return n

#split a list into several trunks
def chunks(l, n):
    return [l[i:i+n] for i in range(0, len(l), n)]
 
def read_probs(file, id_trunk, size_line, block_size, n_read):
	#get start position
	start_pos = id_trunk * block_size * size_line
	res = []
	fd = open(file)
	#skip lines before
	fd.seek(start_pos, 0)
	for i in range(n_read):
		line = fd.readline()
		prob = float(line)
		res.append(prob)
	fd.close()
	return res
	   	
def check_correctness(merged_fname, n, fname2):
	probs2 = []
	fd = open(fname2)
	for line in fd:
		probs2.append(float(line.strip()))
	fd.close()
	probs1 = []
	fd = open(merged_fname)
	for line in fd:
		line = line.strip().split(',')
		probs1.append(float(line[n]))
	fd.close()
	return probs1, probs2
		
def merge_parametered():
	n_cats = 662
	trunk_size = 500
	line_length = 8
	in_file_ext = 'uwo_parameter_probability.txt'
	in_folder = '/home/mpi/uwo_parameter_prediction/'
	out_folder = '/home/xiao/uwo_parameter_merged_prediction'
	out_file_ext = 'uwo_parameter_merged_probability.txt'

	#parameters = [0.25, 0.5, 4]
	parameters = [0.5]
	num_lines = get_num_lines(in_folder + '0_pos_0.25_' + in_file_ext)

	all_trunks = chunks(range(num_lines), trunk_size)
	for parameter in parameters:
		id_trunk = 0
		all_probs = {}	
		fd = open(out_folder + '/' + str(parameter) + '_' + out_file_ext, 'w')
		fd.close()
		for trunk in all_trunks:
			for c in range(n_cats):
				all_probs[c] = None
			for c in range(n_cats):
				fname = in_folder + str(c) + '_pos_' + str(parameter) + '_' + in_file_ext
				probs = read_probs(fname, id_trunk, line_length, trunk_size, len(trunk))			
				all_probs[c] = probs
			id_trunk += 1
			fd = open(out_folder + '/' + str(parameter) + '_' + out_file_ext, 'a')
			for i in range(len(trunk)):
				str_prediction = []
				for c in range(n_cats):
					str_prediction.append(str(all_probs[c][i]))
				fd.write(','.join(str_prediction) + '\n')
			fd.close()
			
if __name__ == '__main__': 				
	"""
	n_cats = 662
	trunk_size = 500
	line_length = 8
	in_file_ext = 'clueweb09_probability.txt'
	in_folder = '/home/mpi/clueweb09_prediction//'
	out_folder = '/home/xiao/clueweb09_merged_prediction/'
	out_file_ext = 'clueweb09_merged_probability.txt'
	
	num_lines = get_num_lines(in_folder + '0_' + in_file_ext)
	"""
	
	"""		
	all_trunks = chunks(range(num_lines), trunk_size)
	id_trunk = 0
	all_probs = {}	
	fd = open(out_folder + '/' + out_file_ext, 'w')
	fd.close()
	for trunk in all_trunks:
		for c in range(n_cats):
			all_probs[c] = None
		for c in range(n_cats):
			fname = in_folder + str(c) + '_' + in_file_ext
			probs = read_probs(fname, id_trunk, line_length, trunk_size, len(trunk))			
			all_probs[c] = probs
		id_trunk += 1
		fd = open(out_folder + '/' + out_file_ext, 'a')
		for i in range(len(trunk)):
			str_prediction = []
			for c in range(n_cats):
				str_prediction.append(str(all_probs[c][i]))
			fd.write(','.join(str_prediction) + '\n')
		fd.close()
	p1,p2=check_correctness(out_folder + '/' + out_file_ext, 5, in_folder + '5_' + in_file_ext)
	for i in range(len(p1)):
		if p1[i] != p2[i]:
			print p1[i], p2[i], 'err'
			
	"""	
	"""
	merge_parametered()
	
	

	in_file_ext = 'uwo_parameter_probability.txt'
	in_folder = '/home/mpi/uwo_parameter_prediction/'
	out_folder = '/home/xiao/uwo_parameter_merged_prediction'
	out_file_ext = 'uwo_parameter_merged_probability.txt'
	p1,p2=check_correctness(out_folder + '/0.5_' + out_file_ext, 5, in_folder + '5_pos_0.5_' + in_file_ext)
	for i in range(len(p1)):
		if p1[i] != p2[i]:
			print p1[i], p2[i], 'err'
	

	n_cats = 662
	trunk_size = 500
	line_length = 8
	in_file_ext = 'uwo_probability.txt'
	in_folder = '/home/mpi/uwo_prediction/'
	#in_file_ext = 'uwo_big_pos_probability.txt'
	#in_folder = '/home/mpi/uwo_big_pos_prediction/'
	out_folder = '/home/xiao/uwo_parameter_merged_prediction'
	out_file_ext = 'uwo_parameter_merged_probability.txt'

	parameters = [1]
	num_lines = get_num_lines(in_folder + '0_' + in_file_ext)

	all_trunks = chunks(range(num_lines), trunk_size)
	for parameter in parameters:
		id_trunk = 0
		all_probs = {}	
		fd = open(out_folder + '/' + str(parameter) + '_' + out_file_ext, 'w')
		fd.close()
		for trunk in all_trunks:
			for c in range(n_cats):
				all_probs[c] = None
			for c in range(n_cats):
				fname = in_folder + str(c) + '_' + in_file_ext
				probs = read_probs(fname, id_trunk, line_length, trunk_size, len(trunk))
				all_probs[c] = probs
			id_trunk += 1
			fd = open(out_folder + '/' + str(parameter) + '_' + out_file_ext, 'a')
			for i in range(len(trunk)):
				str_prediction = []
				for c in range(n_cats):
					str_prediction.append(str(all_probs[c][i]))
				fd.write(','.join(str_prediction) + '\n')
			fd.close()
			
	p1,p2=check_correctness(out_folder + '/1_' + out_file_ext, 5, in_folder + '5_' + in_file_ext)
	for i in range(len(p1)):
		if p1[i] != p2[i]:
			print p1[i], p2[i], 'err'
	"""
	
	#merge mustang prediction
	
	n_cats = 662
	trunk_size = 500
	line_length = 8
	
	in_file_ext = 'mustangs_parameter_probability.txt'
	in_folder = '/home/mpi/mustangs_parameter_prediction/'
	out_folder = '/home/xiao/mustangs_merged/'
	out_file_ext = 'mustangs_parameter_merged_probability.txt'
	
	
	in_file_ext = 'uwo_query_bing_parameter_probability.txt'
	in_folder = '/home/mpi/uwo_query_bing_parameter_prediction/'
	out_folder = '/home/mpi/uwo_query_bing_merged_parameter_prediction/'
	out_file_ext = 'query_bing_parameter_merged_probability.txt'
	
	#in_file_ext = 'uwo_big_pos_probability.txt'
	#in_folder = '/home/mpi/uwo_big_pos_prediction/'
	
	used_id_file = '/home/mpi/uwo_query_bing_workingspace/used_tree_nodes.txt'
	
	used_ids = []
	fd = open(used_id_file)
	for line in fd:
		used_ids.append(int(line.strip()))
	fd.close()

	parameters = [0.5, 1, 2]
	num_lines = get_num_lines(in_folder + '0_pos_1_' + in_file_ext)

	all_trunks = chunks(range(num_lines), trunk_size)
	for parameter in parameters:
		id_trunk = 0
		all_probs = {}	
		fd = open(out_folder + '/' + str(parameter) + '_' + out_file_ext, 'w')
		fd.close()
		for trunk in all_trunks:
			for c in used_ids:
				all_probs[c] = None
			for c in used_ids:
				fname = in_folder + str(c) + '_pos_' + str(parameter) + '_' + in_file_ext
				probs = read_probs(fname, id_trunk, line_length, trunk_size, len(trunk))
				all_probs[c] = probs
			id_trunk += 1
			fd = open(out_folder + '/' + str(parameter) + '_' + out_file_ext, 'a')
			for i in range(len(trunk)):
				str_prediction = []
				for c in used_ids:
					str_prediction.append(str(c)+':'+str(all_probs[c][i]))
				fd.write(','.join(str_prediction) + '\n')
			fd.close()
			
	p1,p2=check_correctness(out_folder + '/1_' + out_file_ext, 0, in_folder + '0_pos_1_' + in_file_ext)
	for i in range(len(p1)):
		if p1[i] != p2[i]:
			print p1[i], p2[i], 'err'
