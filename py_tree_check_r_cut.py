def check_tree_r_cut_distrbution(root, used_cats, labels, cat_distribution):
	#filter nodes
	child_nodes = [c for c in root.children if c.labelIndex in used_cats]
	#count child prediction at this node
	n = 0
	for c in child_nodes:
		if c.labelIndex in labels:
			n += 1
	#accumulate statistics
	if n != 0:
		cat_distribution[root.labelIndex].append(n)
	for c in child_nodes:
		check_tree_r_cut_distrbution(c, used_cats, labels, cat_distribution)

def count_cat_distribution(used_cats, label_file, fname_cat_distrubiton):
	cat_distribution = {}
	for c in used_cats:
		cat_distribution[c] = []
	cat_distribution[-1] = []

	root = Node().read_tree(hier)

	fd = open(label_file)
	for line in fd:
		line = line.strip().split(' ')
		labels = set([int(l) for l in line[2:]])
		check_tree_r_cut_distrbution(root, used_cats, labels, cat_distribution)		
	fd.close()

	fd_w = open(fname_cat_distrubiton, 'w')
	ks = cat_distribution.keys()
	ks.sort()
	for k in ks:		
		ps = []
		for v in cat_distribution[k]:
			ps.append(str(v))
		if len(ps) == 0:
			fd_w.write(str(k) + '\n')
		else:
			fd_w.write(str(k) + ' ' + ' '.join(ps) + '\n')		
	fd_w.close()

def read_r_cut_distribution(fname):
	span_distribution = {}
	fd = open(fname)
	for line in fd:
		line = line.strip().split(' ')
		cid = int(line[0])
		probs = []
		for l in line[1:]:
			l = l.split(':')
			probs.append((int(l[0]), float(l[1])))
		span_distribution[cid] = probs
	fd.close()
	return span_distribution

def caculate_span_distribution(fname_cat_distrubiton, out_fname_cat_judge_probability):
	#get cat distribution
	infname = fname_cat_distrubiton
	cat_distribution = {}
	fd = open(infname)
	for line in fd:
		line = line.strip().split(' ')
		line = [int(l) for l in line]
		#we do not care leaves
		if line[0] not in leaves:
			if len(line) > 1:
				stats = {}
				for l in line[1:]:
					if l in stats:
						stats[l] += 1
					else:
						stats[l] = 1
				sm = sum(stats.values())
				for s in stats:
					stats[s] = float(stats[s])/sm
				cat_distribution[int(line[0])] = stats
	fd.close()

	fd = open(out_fname_cat_judge_probability, 'w')
	ks = cat_distribution.keys()
	ks.sort()
	for k in ks:
		stats = cat_distribution[k]
		ps = [[s, stats[s]] for s in stats]
		ps = sorted(ps, key=lambda s:s[0])
		for i in range(1, len(ps)):
			ps[i][1] += ps[i-1][1]
		out_str = []
		for p in ps:
			out_str.append(str(p[0]) + ':' + ('%.5f' % p[1]))
		fd.write(str(k) + ' ' + ' '.join(out_str) + '\n')
	fd.close()
	
if __name__ == '__main__':
	from active_learning import *
	hier = '/home/mpi/uwo_query_bing_workingspace/new_query_bing_hierarchy.txt'
	used_tree_nodes = '/home/mpi/uwo_query_bing_workingspace/used_tree_nodes.txt'
	label_file = '/home/mpi/uwo_query_bing_workingspace/new_new_query_bing_labels.txt'
	fname_cat_distrubiton = 'query_bing_training_dataset_cat_distribution.txt'
	out_fname_cat_judge_probability = 'new_query_bing_training_dataset_cat_probability.txt'

	used_cats = set()
	fd = open(used_tree_nodes)
	for line in fd:
		used_cats.add(int(line.strip()))
	fd.close()

	root = Node().read_tree(hier)

	leaves = []
	root.get_leaves(leaves)
	
	#count cat distribution from training dataset
	#count_cat_distribution(used_cats, label_file, fname_cat_distrubiton)
	#calculate cat frenquency (r-cut from Yiming Yang's paper)
	#caculate_span_distribution(fname_cat_distrubiton, out_fname_cat_judge_probability)
	z =read_r_cut_distribution(out_fname_cat_judge_probability)
	
