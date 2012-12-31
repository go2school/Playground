class Node:	
	def __init__(self):
		self.labelIndex = -1
		self.name = 'Top'
		self.children = []
		self.parent = -1		
		self.subsize = 0
		self.depth = 0
	
	def get_all_node_ids(self, name_2_id, cache):
		cache.append(self.name)
		if self.labelIndex != -1:			
			name_2_id['\\'.join(cache[1:])] = self.labelIndex			
		for c in self.children:			
			c.get_all_node_ids(name_2_id, cache)
		cache.pop()
			
	def get_all_node_ids_label_id(self, name_2_id, cache):
		cache.append(str(self.labelIndex))
		if self.labelIndex != -1:			
			name_2_id['\\'.join(cache[1:])] = self.labelIndex			
		for c in self.children:			
			c.get_all_node_ids_label_id(name_2_id, cache)
		cache.pop()
		
	def get_all_node_ids_2(self, id_paths, cache):
		cache.append(str(self.labelIndex))
		if self.labelIndex != -1:			
			id_paths.append('/'.join(cache[1:]))
		for c in self.children:			
			c.get_all_node_ids_2(id_paths, cache)
		cache.pop()
	
	def filter_result_labels(self, in_set, out_set):
		for c in self.children:
			if c.labelIndex in in_set:
				out_set.add(c.labelIndex)
				c.filter_result_labels(in_set, out_set)
		
	def sort_label_ids(self, old_2_new_mapper, new_2_old_mapper):
		q = []
		for ch in self.children:
			q.append(ch)
		id = 0
		while q != []:
			nd = q.pop(0)
			#record mapping
			old_2_new_mapper[nd.labelIndex] = id
			new_2_old_mapper[id] = nd.labelIndex
			#change label 
			nd.labelIndex = id
			id += 1
			for ch in nd.children:
				q.append(ch)			
		
	def add(self, child):
		self.children.append(child)
		child.parent = self
		child.depth = self.depth + 1
	
	def find_child(self, nm):
		for c in self.children:
			if c.name == nm:
				return c
		return -1
						
	def get_tree_size(self):
		sum = 1
		for i in self.children:
			sum += i.get_tree_size()
		self.subsize = sum
		return sum	
	
	def get_subtree_size(self, subsize):
		for c in self.children:
			subsize[c.labelIndex] = c.subsize
			c.get_subtree_size(subsize)			
			
	def get_subtree_weight(self, weight):
		for c in self.children:
			ratio = float(c.subsize) / c.parent.subsize
			weight[c.labelIndex] = ratio
			c.get_subtree_weight(weight)
	
	def read_dmoz_tree(self, file):
		root = Node()
		fd = open(file)
		for line in fd:
			line = line.replace('\n', '')
			line = line.split('\t')
			path = line[0]
			id = line[1]
			path = path.split('/')
			nd = root
			for p in path:
				ret = nd.find_child(p)
				if ret == -1:
					t_nd = Node()
					t_nd.labelIndex = int(id)
					t_nd.name = p
					nd.add(t_nd)
					nd = t_nd
				else:
					nd = ret
		fd.close()
		return root
	
	def read_dmoz_ontology_tree(self, file):
		#create nodes
		nodes = []
		for i in range(100000):
			nd = Node()
			nd.labelIndex = i-1
			nodes.append(nd)				
		fd = open(file)		
		for line in fd:
			labels = line.strip().split('\t')	
			parent = int(labels[0])
			child = int(labels[1])			
			nodes[parent].add(nodes[child])
		fd.close()
		return nodes[0]
		
	def read_ohsumed_tree(self, file):
		fd= open(file)
		id = 0
		top = Node()		
		for line in fd:
			line = line.strip().split('\\')
			nd = top
			cat = 'Top'
			for l in line:
				cat += '\\' + l
				c = nd.find_child(l)
				if c == -1:
					new_nd = Node()
					new_nd.labelIndex = id
					new_nd.name = l
					nd.add(new_nd)
					nd = new_nd
				else:
					nd = c					
			id += 1
 		fd.close()
		return top
		
	def read_wipo_tree(self, file, max_depth):
		root = Node()
		fd = open(file)
		id = 0
		for line in fd:
			line = line.strip()								
			path = line.split('\\')
			nd = root
			for p in path[:max_depth]:				
				ret = nd.find_child(p)
				if ret == -1:
					t_nd = Node()
					t_nd.labelIndex = int(id)
					id += 1
					t_nd.name = p
					nd.add(t_nd)
					nd = t_nd
				else:
					nd = ret
		fd.close()
		return root
		
	def read_tree(self,file):
		#read all string
		fd=open(file)
		ct=fd.read()
		fd.close()
		#create nodes
		nodes = []
		for i in range(50000):
			nd = Node()
			nd.labelIndex = i-1
			nodes.append(nd)
		#begin parse		
		ct = ct.replace('#','').strip()
		ct_nodes = ct.split('|')
		for n in ct_nodes:
			if n is not '':
				ct_ns = n.split(',')	
				labelIndex = int(ct_ns[0])
				for id in ct_ns[1:(len(ct_ns)-1)]:
					nodes[labelIndex].add(nodes[int(id)])
		return nodes[0]	
	
	def read_parent_child_pair_tree(self, file):		
		#create nodes
		nodes = {}
		fd = open(file)
		for line in fd:
			line = line.replace('\n','')
			line = line.split(' ')
			parent = int(line[0])
			child = int(line[1])
			if parent not in nodes:
				nd = Node()
				nd.labelIndex = parent
				nodes[parent] = nd
			if child not in nodes:
				nd = Node()
				nd.labelIndex = child
				nodes[child] = nd
			nodes[parent].add(nodes[child])
		fd.close()
		root = Node()
		roots = []
		for label in nodes.keys():
			if nodes[label].parent == -1:				
				roots.append(label)
		if len(roots) == 1:
			root = nodes[roots[label]]
		else:
			for label in roots:
				root.add(nodes[label])
		return root, nodes
		
	def write_tree(self, file):
		q = [self]
		out_str = ''
		while q != []:
			top = q.pop(0)
			if top.children != []:
				out_str += str(top.labelIndex+1) + ','
				for nd in top.children:
					out_str += str(nd.labelIndex +1) + ','
					q.append(nd)
				out_str += '|'
		out_str += '#'
		fd = open(file,'w')
		fd.write(out_str)
		fd.close()

	def write_hier_path(self, fname):
		name2id = {}
		cache = []
		self.get_all_node_ids(name2id, cache)
		fd = open(fname, 'w')
		names = name2id.keys()
		names.sort()
		for name in names:
			fd.write(str(name2id[name]) + ' ' + name + '\n')
		fd.close()
		
	def get_ancestor_nodes(self, ancestors):
		for c in self.children:
			n = c.parent
			while n.labelIndex is not -1:
				if c.labelIndex not in ancestors:
					ancestors[c.labelIndex] = [n.labelIndex]
				else:
					ancestors[c.labelIndex].append(n.labelIndex)
			c.get_ancestor_nodes(ancestors)
			
	def get_parents(self, parents):
		for c in self.children:
			parents[c.labelIndex] = c.parent.labelIndex
			c.get_parents(parents)
			
	def get_nodes_per_level(self, nodes):
		for c in self.children:
			nodes[c.depth].append(c.labelIndex)
			c.get_nodes_per_level(nodes)
	
	def get_nodes_per_level(self, depth, nodes):
		for c in self.children:
			nodes[depth].append(c.labelIndex)
			c.get_nodes_per_level(depth + 1, nodes)
	
	def get_id_to_node_map(self, nodes):		
		for c in self.children:
			nodes[c.labelIndex] = c
			c.get_id_to_node_map(nodes)
		
	def get_max_level(self):
		level = 0
		for c in self.children:		
			if c.get_max_level() + 1 > level:
				level = c.get_max_level() + 1
		return level	
		
	def get_leaves(self, leaves):
		for c in self.children:
			if c.children == []:
				leaves.append(c)
			else:
				c.get_leaves(leaves)
	
	def get_node_depth(self, depth_seq):
		for c in self.children:
			depth_seq[c.labelIndex] = c.depth
			c.get_node_depth(depth_seq)
		
	def find_leaves_in_list(self, st, leaves):	
		if self.labelIndex != -1:
			if self.labelIndex in st:				
				is_leaf = 1
				for c in self.children:
					if c.labelIndex in st:
						is_leaf = 0
						break
				if is_leaf == 1:
					leaves.add(self.labelIndex)				
				for c in self.children:
					c.find_leaves_in_list(st, leaves)
		else:
			for c in self.children:
				c.find_leaves_in_list(st, leaves)
	
def readUnlabeledDocIDs(file):
	fd=open('al_dmoz_unlabeled_doc_ids','r')
	undocids=set()
	for line in fd:
		line.replace('\n','')
		undocids.add(int(line))
	fd.close()
	return undocids
	
def writeUnlabeledDocIDs(in_doc_ids, selected_doc_ids, out_file):
	remain = in_doc_ids - selected_doc_ids
	fd = open(out_file, 'w')
	for x in remain:
		fd.write(x + '\n')
	fd.close()
	
def sampleUnlabeledDocs(usedDocIDs, num, feature_file_in, feature_file_out, label_file_in, label_file_out):	
	#sample num of docs from doc id set
	sampleDocIDs = set()
	if num > len(usedDocIDs):
		sampleDocIDs = usedDocIDs
	else:
		import random
		sampleDocIDs = random.sample(usedDocIDs, num)	
	
	#open file for sample
	feature_fd = open(feature_file_in)
	label_fd = open(label_file_in)		

	sampled_doc_ids = []
	feature_buf = []
	label_buf = []
	n = 0
	for line_label in label_fd:	
		line_feature = feature_fd.readline()
		#check doc id
		a = line_label.index(' ')
		id = line_label[:a]
		id = int(id)
		if id in sampleDocIDs:
			feature_buf.append(line_feature)
			label_buf.append(line_label)			
			sampled_doc_ids.append(id)
			n+=1
			#if get all docs, then break
			if n == num:
				break
	feature_fd.close()
	label_fd.close()
	
	feature_fd_w = open(feature_file_out,'w')
	label_fd_w = open(label_file_out,'w')
	for i in range(len(feature_buf)):
		feature_fd_w.write(feature_buf[i])
		label_fd_w.write(label_buf[i])
	feature_fd_w.close()
	label_fd_w.close()
	
	return sampled_doc_ids

def HU_score(root, weight, probs):
	hu = 0
	for c in root.children:
		labelIndex = root.children.labelIndex
		#compute uncertainty
		p = probs[labelIndex]
		u = abs(p - 0.5)
		#accumulate uncertainty
		hu += u * weight[labelIndex]
		hu += HU_score(c, weight, probs)
	return hu

def active_learning(root, weight, unlabeled_doc_ids, select_num, file_base):	
	#read all probs
	num = root.get_tree_size()
	probs = []
	for i in range(num):
		fd = open(str(i) + '_' + file_base)		
		ps = []
		for line in fd:
			line = line.replace('\n','')			
			ps.append(float(line))
		fd.close()
		probs.append(ps)
	
	#begin active learning
	vs = []
	for i in range(len(probs[0])):
		p = []
		for j in range(num):
			p.append(probs[j][i])
		v = HU_score(root, weight, p)
		vs.append((unlabeled_doc_ids[i], v))
	vs = sorted(vs, key=lambda s:s[1],reverse=True)
	
	#return selected doc ids
	return [vs[i][0] for i in range(select_num)]
	
def localize_selected_docs(parents, selected_doc_ids, sampled_features_file, sampled_labels_file, feature_file_base, label_file_base):
	#init 
	newdocs = []
	newlabels = []
	label_size = root.get_tree_size()
	for i in label_size:
		newdocs.append([])
		newlabels.append([])
		
	#localize data
	fd = open(sampled_labels_file)	
	for line in fd:
		line = line.replace('\n','')
		id = int(line[0])
		#get labels
		labels = line[2:]
		labels.append(-1)
		labels = set(labels)		
		for labelIndex in range(label_size):
			#is positive
			if labelIndex in labels:
				newdocs[labelIndex].append(id)
				newlabels[labelIndex].append(1)
			#is negative
			elif parents[labelIndex] in labels:
				newdocs[labelIndex].append(id)
				newlabels[labelIndex].append(-1)
	fd.close()
	
	#read in whole dataset
	docs = {}
	fd = open(sampled_features_file)
	for line in fd:
		a = line.index(' ')
		id = line[:a]
		docs[int(id)] = line
	fd.close()
	#append data at the end of each node's dataset
	for labelIndex in range(label_size):
		if newdocs[labelIndex] is not []:
			#append features
			fd = open(str(labelIndex) + '_' + feature_file_base,'a')
			for nd in newdocs[labelIndex]:
				fd.write(docs[nd])
			fd.close()
			#append labels
			fd = open(str(labelIndex) + '_' + label_file_base,'a')
			for nl in newlabels[labelIndex]:
				fd.write(nl + '\n')
			fd.close()
	return newdocs
	
def flag_selection(label_size, localized_docs, file_base):
	for i in range(label_size):
		fd = open(str(i) + '_' + file_base)
		if localized_docs[i] is not []:
			fd.write('CHANGED')
		else:
			fd.write('NO_CHANGED')
		fd.close()
		
if __name__ == '__main__':	
	root = Node()
	root = root.read_tree('/home/mpi/uwo_query_bing_workingspace/new_query_bing_hierarchy.txt')
	depth = root.get_max_level()
	nodes_per_level= [[] for i in range(depth)]	
	used_nodes = []
	fd = open('/home/mpi/uwo_query_bing_workingspace/used_tree_nodes.txt')
	for line in fd:
		used_nodes.append(int(line.strip()))
	fd.close()
	used_nodes = set(used_nodes)
	root.get_nodes_per_level(0, nodes_per_level)
	nodes_per_level_used = [[],[],[],[]]
	for d in [0, 1, 2, 3]:
		nodes_per_level_used[d] = set([l for l in nodes_per_level[d] if l in used_nodes])
		print d, len(nodes_per_level_used[d])
	#count number of examples per level
	num_ex_per_level = [0 for d in [0,1,2,3]]
	num_ex_labels = {}
	for d in used_nodes:
		num_ex_labels[d] = 0
	"""
	fd = open('/home/mpi/uwo_query_bing_workingspace/new_new_query_bing_labels.txt')
	for line in fd:
		line = line.strip().split(' ')
		line = [int(l) for l in line]
		for l in line[2:]:
			if l in used_nodes:
				num_ex_labels[l] += 1
	fd.close()	
	for d in [0,1,2,3]:
		sm = sum([num_ex_labels[l] for l in nodes_per_level_used[d]])
		print d, sm
	"""
	fd = open('/home/mpi/uwo_query_bing_workingspace/new_new_query_bing_labels.txt')
	ex_per_level = [set() for d in [0,1,2,3]]
	for line in fd:
		line = line.strip().split(' ')
		line = [int(l) for l in line]
		#check where does this example fall
		levels = 0
		for l in line[2:]:
			for d in [0,1,2,3]:
				if l in nodes_per_level_used[d]:
					levels = d
		for l in range(levels+1):
			num_ex_per_level[l] += 1
			ex_per_level[l].add(line[0])
	fd.close()		
	for d in [0, 1, 2, 3]:
		print d, num_ex_per_level[d]
	for d in [0, 1, 2, 3]:
		fw = open('/media/DataVolume1/seeuwo/training_set_stats/'+str(d)+'.txt', 'w')
		for ex in ex_per_level[d]:
			fw.write(str(ex) + '\n')
		fw.close()
