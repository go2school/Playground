def read_in_prediction(fname):	
	probs = []
	fd = open(fname)
	for line in fd:
		line = line.strip().split(' ')
		probs.append((int(line[0]), float(line[1])))
	fd.close()
	return probs
	
def write_down_add_solr_xml_files(fname, docs):		
	import codecs
	import random
	import re
	fd = codecs.open(fname, 'w', 'utf-8')			
	fd.write('<add>\n')
	n = 50
	for doc in docs:
		fd.write('\t<doc>\n')
		id = doc[0]
		url = doc[1]
		title = doc[2]
		text = doc[5]		
		text = re.sub('[\x00-\x08\x0B\x0C\x0E-\x1F]', '', text)
		prob = doc[6]				
		
		fd.write('\t\t<field name = "id">' + str(id) + '</field>\n')
		fd.write('\t\t<field name = "url"><![CDATA[' + url + ']]></field>\n')
		fd.write('\t\t<field name = "title"><![CDATA[' + title + ']]></field>\n')
		fd.write('\t\t<field name = "text"><![CDATA[' + text + ']]></field>\n')
		fd.write('\t\t<field name = "prob">' + str(prob) + '</field>\n')		
		for i in range(n):
			fd.write('\t\t<field name = "topic_'+str(i)+'">' + str(random.random()) + '</field>\n')		
		fd.write('\t</doc>\n')
		
	fd.write('</add>\n')
	fd.close()

def write_down_all_prediction(db, probs, folder, chunk_size):
	from help_tools import chunks
	from db_util import get_docs_in_set_uwo	
	chunk_probs_lst = chunks(probs, chunk_size)
	n = 0
	for chunk_probs in chunk_probs_lst:
		chunk_ids = [p[0] for p in chunk_probs]
		docs = get_docs_in_set_uwo(db, chunk_ids)
		new_docs = [[] for i in range(len(docs))]
		for i in range(len(docs)):
			for d in docs[i]:
				new_docs[i].append(d)
			new_docs[i].append(chunk_probs[i][1])			
		write_down_add_solr_xml_files(folder + '/' + str(n) + '.xml', new_docs)
		n += 1
		
if __name__ == '__main__':	
	probs = read_in_prediction('uwo_food_ranked_prob.txt')
	folder = 'solr_data_new'
	chunk_size = 10
	write_down_all_prediction('uwo.webs', probs, folder, chunk_size)
