
def print_HTML_tree(fd, node):
	if len(node.children) != 0:
		fd.write('<ul>')
	for c in node.children:
		fd.write('<li>' + str(c.labelIndex))
		print_HTML_tree(fd, c)
		fd.write('</li>\n')
	if len(node.children) != 0:
		fd.write('</ul>\n')



def print_HTML_tree_select_2(my_str_output, node, all_nodes):
	#get how many nodes under me
	m = 0
	for c in node.children:
		if c.labelIndex in all_nodes:
			m += 1
	if m != 0:
		my_str_output['str'] += '<ul>'
	for c in node.children:
		if c.labelIndex in all_nodes:
			my_str_output['str'] += '<li>' + str(c.labelIndex) + ' AAAAAAA' + str(all_nodes[c.labelIndex])
			print_HTML_tree_select_2(my_str_output, c, all_nodes)
			my_str_output['str'] += '</li>\n'			
	if m != 0:
		my_str_output['str'] += '</ul>\n'		
		
		
def print_HTML_tree_select(fd, node, all_nodes):
	#get how many nodes under me
	m = 0
	for c in node.children:
		if c.labelIndex in all_nodes:
			m += 1
	if m != 0:
		fd.write('<ul>')
	for c in node.children:
		if c.labelIndex in all_nodes:
			fd.write('<li>' + str(c.labelIndex) + ' AAAAAAA' + str(all_nodes[c.labelIndex]))
			print_HTML_tree_select(fd, c, all_nodes)
			fd.write('</li>\n')
	if m != 0:
		fd.write('</ul>\n')


from active_learning import Node
root = Node().read_tree('dmoz_hierarchy.txt')
fd  = open('/home/xiao/apache-solr-3.4.0/example/webapps/ajax_solr/examples/tnp.html', 'w')
fd.write('<html><body>')
my_str = {'str':''}
print_HTML_tree_select_2(my_str, root, {0:0.23, 85:0.12121, 1:0.2323, 2:0.999, 57:0.876778, 3:0.989238})
fd.write(my_str['str'])
fd.write('</body></html>')
fd.close()
