def get_label_counts():
	labels = []
	vs= {}
	sn = 0
	dn = 0
	fd = open('query_bing_id_merged_categories.txt')
	for line in fd:
		line = line.strip().split(' ')
		id = line[0]
		p =len(line[1:])
		labels.append((id, p))
		sn += p
		dn += 1
		if p in vs:
			vs[p] += 1
		else:
			vs[p] = 1
	fd.close()
	print float(sn)/dn
	return labels, vs, sn, dn

def get_ex_per_label(fname):
	labels = {}
	fd = open(fname)
	for line in fd:
		line = line.strip().split(' ')
		eid = int(line[0])
		for l in line[1:]:
			l = int(l)
			if l not in labels:
				labels[l] = 1
			else:
				labels[l] += 1
	fd.close()
	return labels
	
def make_empty_cats(in_svm_tree, in_label_fname, out_empty_cat_fname):	
	#def check_empty(fname, tree):
	from active_learning import *
	#root = Node().read_tree('new_wiki_subject_svm_hierarchy.txt')
	root = Node().read_tree(in_svm_tree)
	id2node = {}
	root.get_id_to_node_map(id2node)
	#labels = get_ex_per_label('query_bing_id_merged_categories.txt')
	labels = get_ex_per_label(in_label_fname)
	#fd_w = open('query_bing_empty_cat_id_list.txt', 'w')
	fd_w = open(out_empty_cat_fname, 'w')
	for id in id2node:
		if id not in labels:
			fd_w.write(str(id) + '\n')
	fd_w.close()

def stat():
	labels, vs, sn, dn = get_label_counts()
	ex_per_labels = get_ex_per_label('query_bing_id_merged_categories.txt')
	n_labels = [(e, ex_per_labels[e]) for e in ex_per_labels]
	n_labels = sorted(n_labels, key = lambda s:s[1])
	len_stat = [(v, vs[v]) for v in vs]
	len_stat = sorted(len_stat, key=lambda s:s[0], reverse=True)
	len_ele = [l[0] for l in len_stat]
	n_ele = [l[1] for l in len_stat] 
	for i in range(len(n_ele)):
		print i, len_ele[i], n_ele[i], 1 - float(sum(n_ele[:i+1]))/dn

def remove_examples_more_than_n_categories(in_fname, out_fname, threshold):	
	fd = open(in_fname)
	fd_w = open(out_fname, 'w')
	for line in fd:
		tmp_l = line
		line = line.strip().split(' ')
		id = line[0]
		p =len(line[1:])
		if p <= threshold:
			fd_w.write(tmp_l)
	fd_w.close()
	fd.close()

def check_empty(label_fname, cat_fname, threshold):
	ex_per_label = get_ex_per_label(label_fname)
	labels = set()
	fd = open(cat_fname)
	for line in fd:
		labels.add(int(line.strip()))
	fd.close()
	for l in labels:
		if ex_per_label[l] < threshold:
			print 'get small cat at ' + str(l)

def dump_used_ids(infname, outfname):	
	fd = open(infname)
	fd_w = open(outfname, 'w')	
	for line in fd:
		a = line.index(' ')
		fd_w.write(line[:a] + '\n')
	fd_w.close()
	fd.close()
	
if __name__ == "__main__":
	in_label_file = 'query_bing_id_merged_categories.txt'
	out_label_file = 'query_bing_id_filtered_categories.txt'
	svm_tree = 'new_wiki_subject_svm_hierarchy.txt'
	out_empty_file = 'query_bing_id_empty_categories.txt'
	small_categories_fname = 'query_bing_small_categories.txt'
	filtered_ids = 'filtered_tree_nodes.txt'
	used_tree_nodes = 'used_tree_nodes.txt'
	used_ex_fname = 'new_query_bing_used_id_list.txt'
	threshold = 20
	small_cat_threshold = 10
	
	
	#check_empty(out_label_file, used_tree_nodes, small_cat_threshold)
	
	#filter examples with more than 20 categories
	remove_examples_more_than_n_categories(in_label_file, out_label_file, threshold)
			
	#filter categories with less than 10 examples
	#write down small cateories
	labels = get_ex_per_label(out_label_file)
	ls = [(l, labels[l])for l in labels]
	ls = sorted(ls, key=lambda s:s[1])
	fd = open(small_categories_fname, 'w')	
	small_cats = set()
	for l in ls:
		if l[1] < small_cat_threshold:
			fd.write(str(l[0]) + ' ' + str(l[1]) + '\n')
			small_cats.add(l[0])
	fd.close()
	
	#write down actually used
	from active_learning import *
	root = Node().read_tree(svm_tree)
	id2node = {}
	root.get_id_to_node_map(id2node)	
	fd_w = open(filtered_ids, 'w')
	for id in id2node:
		if id not in small_cats:
			fd_w.write(str(id) + '\n')
	fd_w.close()
	
	#remake the XML tree
	#check empty categories again
	make_empty_cats(svm_tree, out_label_file, out_empty_file)	
	
	dump_used_ids(out_label_file, used_ex_fname)
