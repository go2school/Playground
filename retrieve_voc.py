def chunks(l, n):
    return [l[i:i+n] for i in range(0, len(l), n)]
	
def get_max_id():
	import   MySQLdb  	
	con   =   MySQLdb.connect(host="192.168.0.2",  port=3306, user="root",  passwd="see",  db="see")  
	cursor   =   con.cursor()  
	sql = 'select max(id) from uwo.webs'
	cursor.execute(sql)
	id = cursor.fetchone()		
	maxid = int(id[0]) 
	cursor.close()
	con.close()
	return maxid
	
def get_min_id():
	import   MySQLdb  	
	con   =   MySQLdb.connect(host="192.168.0.2",  port=3306, user="root",  passwd="see",  db="see")  
	cursor   =   con.cursor()  
	sql = 'select min(id) from uwo.webs'
	cursor.execute(sql)
	id = cursor.fetchone()		
	minid = int(id[0]) 
	cursor.close()
	con.close()
	return minid

def get_docs_between(start_id, to_id):
	import   MySQLdb  		
	docs = []
	con   =   MySQLdb.connect(host="192.168.0.2",  port=3306, user="root",  passwd="see",  db="see")  
	cursor   =   con.cursor()  
	sql = 'select id, title, description, keywords, wholeText from uwo.webs where id >= ' + str(start_id) + ' and id <= ' + str(to_id)
	cursor.execute(sql)
	print sql
	while True:
		row = cursor.fetchone()		
		if row == None:
			break
		docs.append(row)
	cursor.close()
	con.close()
	return docs
	
def read_stop_list(fname):
	stops = set()
	fd = open(fname)
	for line in fd:
		line = line.strip()
		stops.add(line)
	fd.close()
	return stops
	
def remove_stop(word_list, stop_set):		
	word_list = [w for w in word_list if w not in stop_set]	
	return 	word_list

def stem_words(word_list):
	from nltk.stem import PorterStemmer
	#we use a simple stemer
	stm = PorterStemmer()
	word_list = [stm.stem(w) for w in word_list]
	return word_list	
			
def extract_term_freq(docs, stop_words, cur_dict):
	from nltk.probability import FreqDist
	from nltk.tokenize import regexp_tokenize	
	for doc in docs:
		id = doc[0]
		title = doc[1]
		desc = doc[2]		
		keywords = doc[3]
		body = doc[4]
		
		if title == None:
			title = ''
		if desc == None:
			desc = ''		
		if keywords == None:
			keywords = ''		
		if body == None:
			body = ''					
		
		#to lowercase
		title = title.lower()
		desc = desc.lower()
		keywords = keywords.lower()
		body = body.lower()
				
		#extract title
		if len(title)>0:
			title_wordlist = regexp_tokenize(title, '[a-zA-Z]+')
			title_removed = remove_stop(title_wordlist, stop_words)
			title_stemmed = stem_words(title_removed)
			cp = FreqDist(title_stemmed).items()
			for c in cp:
				arg_term = c[0] + '_t'
				if arg_term not in cur_dict:
					cur_dict[arg_term] = 1
				else:
					cur_dict[arg_term] += 1
		
		#merge keywords and description
		desc = desc + ' ' + keywords
		#extract desc
		if len(desc)>0:
			desc_wordlist = regexp_tokenize(desc, '[a-zA-Z]+')
			desc_removed = remove_stop(desc_wordlist, stop_words)
			desc_stemmed = stem_words(desc_removed)
			cp = FreqDist(desc_stemmed).items()
			for c in cp:
				arg_term = c[0] + '_kd'
				if arg_term not in cur_dict:
					cur_dict[arg_term] = 1
				else:
					cur_dict[arg_term] += 1
					
		#extract body text		
		if len(body)>0:
			body_wordlist = regexp_tokenize(body, '[a-zA-Z]+')
			body_removed = remove_stop(body_wordlist, stop_words)
			body_stemmed = stem_words(body_removed)
			cp =FreqDist(body_stemmed).items()
			for c in cp:
				arg_term = c[0] + '_b'
				if arg_term not in cur_dict:
					cur_dict[arg_term] = 1
				else:
					cur_dict[arg_term] += 1
		
	
def build_term_freq_list(max_id, trunks, stop_set):	
	from time import time
	start = time()
	cur_dict = {}
	#make trunks
	all_ids = range(max_id)
	all_trunks = chunks(all_ids, trunks)
	tot_trunks = len(all_trunks)
	for trunk in all_trunks:
		start_id = trunk[0]
		end_id = trunk[len(trunk) - 1]
		print 'start extract terms from ' + str(start_id) + ' to ' + str(end_id)
		docs = get_docs_between(start_id, end_id)
		extract_term_freq(docs, stop_set, cur_dict)
		print 'finish extract terms from ' + str(start_id) + ' to ' + str(end_id)
		tot_trunks -= 1
		print str(tot_trunks) + ' remained'		
	end = time()
	print 'Finish tasks in ' + str(int(end - start)) + ' seconds'
	return cur_dict
	
def read_dict(fname):
	cur_dict = {}
	fd = open(fname)
	for line in fd:
		line = line.strip()
		line = line.split(' ')
		word = line[0]
		id = int(line[1])
		cur_dict[word] = id
	fd.close()
	return cur_dict

def write_term_freq(term_freq, fname):
	terms = term_freq.keys()
	terms.sort()
	fd = open(fname, 'w')
	for term in terms:
		fd.write(term + ' ' + str(term_freq[term]) + '\n')
	fd.close()
	
def write_dict(term_freq, fname):
	terms = term_freq.keys()
	terms.sort()
	id = 1
	fd = open(fname, 'w')
	words = term_freq.keys()
	for term in terms:
		fd.write(term + ' ' + str(id) + '\n')
		id += 1
	fd.close()

if __name__ == '__main__':		
	trunks = 5000
	fname_dict = 'uwo_full_dict'
	fname_stop = 'new_english.stop'
	fname_freq = 'uwo_full_freq'

	maxid = get_max_id()		
	stop_set = read_stop_list(fname_stop)
	term_freqs = build_term_freq_list(maxid, trunks, stop_set)
	write_dict(term_freqs, fname_dict)
	write_term_freq(term_freqs, fname_freq)
