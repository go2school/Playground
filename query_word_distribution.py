def query_db(query):
	docs = []
	import   MySQLdb  			
	con   =   MySQLdb.connect(host="192.168.0.2",  port=3306, user="root",  passwd="see",  db="see")  
	cursor   =   con.cursor()  
	sql = 'select id, url, snippets, title, description, keywords, body from quey_search_engine.webs where query="' + query + '"'
	cursor.execute(sql)
	print sql
	while True:
		row = cursor.fetchone()		
		if row == None:
			break		
		id = row[0]
		url = row[1]
		snippets = row[2]
		title = row[3]
		description = row[4]
		keywords = row[5]
		body = row[6]		
		docs.append((id, url, title, description, keywords, body))
	cursor.close()
	con.close()	
	return docs
	
def compute_word_distribution(docs, stop_sets, vocabulary):
	from build_dict_and_stem_map import extract_term_freq
	cur_dict = {}
	voc2stm = {}
	stm2voc = {}
	extract_term_freq(docs, stop_sets, cur_dict, voc2stm, stm2voc)
	actual_dict = {}
	#filtering words
	for word in cur_dict:
		if word in vocabulary:
			actual_dict[word] = cur_dict[word]			
	#compute total words
	tot_words = sum(actual_dict.values())
	for word in actual_dict:
		actual_dict[word] = float(actual_dict[word])/tot_words
	return actual_dict
	
if __name__ == '__main__':
	from help_tools import read_stop_list, read_dict, read_stem_to_words
	fname_stop = 'new_english.stop'
	fname_dict = 'uwo_full_dict'
	query = 'meal site:uwo.ca'
	docs = query_db(query)
	vocabulary = read_dict(fname_dict)
	stop_sets = read_stop_list(fname_stop)
	actual_dict = compute_word_distribution(docs, stop_sets, vocabulary)
	word_pairs = [(k, actual_dict[k]) for k in actual_dict.keys()]
	word_pairs = sorted(word_pairs, key=lambda s:s[1], reverse=True)	
