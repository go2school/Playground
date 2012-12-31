def checker(feature_file, label_file):
	f_id = []
	fd_f = open(feature_file)
	for line in fd_f:
		a = line.index(' ')
		f_id.append(int(line[:a]))
	fd_f.close()
	
	l_id = []
	fd_l = open(label_file)
	for line in fd_l:
		a = line.index(' ')
		l_id.append(int(line[:a]))
	fd_l.close()
	if len(f_id) != len(l_id):
		print 'wrong length ' + str(len(f_id)) + ' ' + str(len(l_id))
	for i in range(len(f_id)):
		if f_id[i] != l_id[i]:
			print 'wrong ' + str(i)  + ' in ' + feature_file + ' and ' + label_file			

def check_labels(file, label_size):
	fd = open(file)
	labels = [0 for i in range(label_size)]
	for line in fd:		
		line = line.replace('\n','')
		line = line.split(' ')		
		if int(line[1]) != len(line[2:]):
			print 'Wrong label format at ' + line
		for l in line[2:]:
			labels[int(l)] += 1
	fd.close()
	for i in range(len(labels)):
		if labels[i] == 0:
			print "Positive empty at " + str(i)
	return labels

def check_labels_hier(file, hier_file):
	from active_learning import *
	root = Node()
	root = root.read_tree(hier_file)
	label_size = root.get_tree_size() - 1
	fd = open(file)
	labels = [0 for i in range(label_size)]
	for line in fd:		
		line = line.replace('\n','')
		line = line.split(' ')		
		if int(line[1]) != len(line[2:]):
			print 'Wrong label format at ' + line
		for l in line[2:]:
			labels[int(l)] += 1
	fd.close()
	for i in range(len(labels)):
		if labels[i] == 0:
			print "Positive empty at " + str(i)
	return labels
	
def check_features(fname):
	fs = set()
	fd = open(fname)
	for line in fd:
		line = line.strip().split(' ')
		for l in line[1:]:
			l = l.split(':')
			fs.add(int(l[0]))
	fd.close()
	print len(fs)
	return fs
	
def read_positive_count(file, label_size):
	fd = open(file)
	labels = [0 for i in range(label_size)]
	n = 0
	for line in fd:
		line = line.replace('\n','')
		line = line.split(' ')		
		n += 1
		for l in line[2:]:
			labels[int(l)] += 1
	fd.close()	
	return labels, n
	
def count(file1, label_size):
	tot_l=open(file1)
	l=[]
	for i in range(0,label_size):
		l.append(0)
	len1=0
	for line in tot_l:
		labels=line.strip().split(" ")					
		for label in labels[2:]:
			l[int(label)]+=1
	tot_l.close()
	return l

def check_ex_labels(hier_file, file):
	from active_learning import * 
	root = Node()
	root = root.read_tree(hier_file)
	max_depth = root.get_max_level()
	ns = []
	fd = open(file)
	ndoc = 0
	for line in fd:
		line = line.strip().split(' ')
		ns.append(int(line[1]))
		ndoc += 1
	fd.close()
	print ndoc, float(len([n for n in ns if n > max_depth]))/ndoc
	return ndoc, ns, float(len([n for n in ns if n > max_depth]))/ndoc
	
def check_feature_freq(fname):	
	occs = {}
	length = []
	num_wds  = []
	fd = open(fname)
	for line in fd:
		line = line.strip().split(' ')
		sum_occ = 0
		for l in line[1:]:
			l = l.split(':')
			word = l[0]
			occ = int(l[1])
			if occ not in occs:
				occs[occ] = 1
			else:
				occs[occ] += 1
			sum_occ += occ
		num_wds.append(len(line[1:]))
		length.append(sum_occ)
	fd.close()	
	return occs, num_wds, length
	
def sample_mean_variance(vs):
	import math
	min_v = min(vs)
	max_v = max(vs)
	mean_v = sum(vs)/len(vs)	
	if len(vs) == 1:
		stdev_v = 0
	else:
		tmp = [(q - mean_v)*(q - mean_v) for q in vs]
		stdev_v = math.sqrt(sum(tmp)/(len(tmp)-1))
	return min_v, max_v, mean_v, stdev_v

def extract_ids(fname, id_fname):
	fd = open(fname)
	fd_w = open(id_fname, 'w')
	for line in fd:
		a = line.index(' ')
		fd_w.write(line[:a] + '\n')
	fd.close()
	fd_w.close()

def check_doc_length(fname):	
	lens = [] 
	fd = open(fname)
	for line in fd:
		line = line.strip().split(' ')		
		lens.append(len(line[1:]))
	fd.close()
	return lens
	
def read_multi_label(fname):
	labels = {}
	fd = open(fname)
	for line in fd:
		line = line.strip().split(' ')
		id = int(line[0])
		n_label = int(line[1])
		ls = []
		if n_label != 0:
			ls = [int(l) for l in line[2:]]
		labels[id] = ls
	fd.close()
	return labels
	
if __name__ == '__main__':	
	checker('food_tf_idf.txt', 'food_labels.txt')
	extract_ids('uwo_features.txt', 'uwo_ids.txt')
	extract_ids('food_labels.txt', 'food_ids.txt')
	#lens = check_doc_length('uwo_food_tf_idf.txt')
	#from nltk.probability import FreqDist
	#cp = FreqDist(lens).items()
