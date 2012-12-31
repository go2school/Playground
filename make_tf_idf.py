def compute_idf(feature_fname, feature_idf_fname):
	import math
	idf = {}
	N = 0
	fd = open(feature_fname)
	for line in fd:
		line = line.strip().split(' ')	
		N += 1
		for l in line[1:]:
			wd, occ = l.split(':')
			if wd not in idf:
				idf[wd] = 1
			else:
				idf[wd] += 1
	fd.close()
	for w in idf.keys():
		idf[w] = math.log(float(N)/idf[w])
	fd = open(feature_idf_fname, 'w')
	for w in idf.keys():
		fd.write(str(w) + ' ' + ('%.6f' % idf[w]) + '\n')
	fd.close()
	return idf

def compute_tf_idf_by_vector(svm_vector, idf):
	import math
	words = []
	occs = []
	for v in svm_vector:
		if v[0] in idf:
			words.append(v[0])
			occs.append(v[1])
	sum_occ = sum(occs)
	tf_idfs = []
	for i in range(len(words)):
		v = float(occs[i]) / sum_occ * idf[words[i]]
		tf_idfs.append((words[i], v))
	tf_idfs.sort()	
	return tf_idfs
		
def compute_tf_by_vector(svm_vector, idf):
	import math
	words = []
	occs = []
	for v in svm_vector:
		if v[0] in idf:
			words.append(v[0])
			occs.append(v[1])
	sum_occ = sum(occs)
	tfs = []
	for i in range(len(words)):
		v = float(occs[i]) / sum_occ
		tfs.append((words[i], v))
	tfs.sort()	
	return tfs
		
def compute_tf_idf(feature_fname, idf, feature_idf_fname):
	fd = open(feature_fname)
	fd_w = open(feature_idf_fname, 'w')
	for line in fd:
		line = line.strip().split(' ')	
		id = line[0]
		words = []
		occs = []
		for l in line[1:]:
			wd, occ = l.split(':')
			if wd in idf:
				words.append(wd)
				occs.append(int(occ))
		wd_length = sum(occs)
		fd_w.write(id)
		for i in range(len(words)):
			v = float(occs[i])/wd_length*idf[words[i]]
			if v != 0:
				fd_w.write(' ' + words[i] + ':' + ('%.6f' % v))
		fd_w.write('\n')
	fd.close()
	fd_w.close()
	
def merge_feature_label(feature_fname, label_fname, merged_fname):
	#read in label
	labels = {}
	fd = open(label_fname)
	for line in fd:
		line = line.strip().split(' ')
		labels[line[0]] = line[1]
	fd.close()
	fd_w = open(merged_fname, 'w')
	fd = open(feature_fname)
	for line in fd:
		a = line.index(' ')
		id = line[:a]
		if id in labels:
			fd_w.write(labels[id] + ' ' + line[a+1:])
	fd.close()
	fd_w.close()


def read_idf_table(in_fname):
	idf = {}
	fd = open(in_fname)
	for line in fd:
		line = line.strip().split(' ')
		idf[line[0]] = float(line[1])
	fd.close()
	return idf
	
def covert_occ_to_tf_idf_data(idf_fname, global_fname, global_features):	
	idf = read_idf_table(idf_fname)
	compute_tf_idf(global_fname, idf, global_features)
		
if __name__ == '__main__':			
	compute_idf('food_features.txt', 'food_idf.txt')
	covert_occ_to_tf_idf_data('food_idf.txt', 'food_features.txt', 'food_tf_idf.txt')
	merge_feature_label('food_tf_idf.txt', 'food_labels.txt', 'food_training_data.txt')	
	covert_occ_to_tf_idf_data('food_idf.txt', 'uwo_features.txt', 'uwo_food_tf_idf.txt')
