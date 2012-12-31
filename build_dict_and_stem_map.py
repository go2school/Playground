def extract_doc_features(docs, stop_words, cur_dict):
	from nltk.probability import FreqDist
	from nltk.tokenize import regexp_tokenize	
	from help_tools import remove_stop, stem_words
	vectors = []
	for doc in docs:
		
		id = doc[0]
		url = doc[1]
		title = doc[2]
		desc = doc[3]		
		keywords = doc[4]
		body = doc[5]
		
		if title == None:
			title = ''
		if url == None:
			url = ''
		if desc == None:
			desc = ''		
		if keywords == None:
			keywords = ''		
		if body == None:
			body = ''					
		
		#to lowercase
		title = title.lower()
		url = url.lower()
		desc = desc.lower()
		keywords = keywords.lower()
		body = body.lower()
			
		#feature vector
		vector = []
			
		#extract title
		if len(title)>0:
			title_wordlist = regexp_tokenize(title, '[a-zA-Z]+')
			title_removed = remove_stop(title_wordlist, stop_words)
			title_stemmed = stem_words(title_removed)			
			#add _t to the end of title
			title_removed = [t + '_t' for t in title_removed]
			title_stemmed = [t + '_t' for t in title_stemmed]									
			#compute freq
			cp = FreqDist(title_stemmed).items()
			for c in cp:
				arg_term = c[0]
				if arg_term in cur_dict:
					vector.append((cur_dict[c[0]], c[1]))
		
		if len(url)>0:
			url_wordlist = regexp_tokenize(url, '[a-zA-Z]+')
			url_removed = remove_stop(url_wordlist, stop_words)
			url_stemmed = stem_words(url_removed)
			#add _u to the end of title
			url_removed = [t + '_u' for t in url_removed]
			url_stemmed = [t + '_u' for t in url_stemmed]		
		
			cp = FreqDist(url_stemmed).items()
			for c in cp:
				arg_term = c[0]
				if arg_term in cur_dict:
					vector.append((cur_dict[c[0]], c[1]))
					
		#merge keywords and description
		desc = desc + ' ' + keywords
		#extract desc
		if len(desc)>0:
			desc_wordlist = regexp_tokenize(desc, '[a-zA-Z]+')
			desc_removed = remove_stop(desc_wordlist, stop_words)
			desc_stemmed = stem_words(desc_removed)
			
			#add _u to the end of title
			desc_removed = [t + '_kd' for t in desc_removed]
			desc_stemmed = [t + '_kd' for t in desc_stemmed]	
			
			cp = FreqDist(desc_stemmed).items()
			for c in cp:
				arg_term = c[0]
				if arg_term in cur_dict:
					vector.append((cur_dict[c[0]], c[1]))
					
		#extract body text		
		if len(body)>0:
			body_wordlist = regexp_tokenize(body, '[a-zA-Z]+')
			body_removed = remove_stop(body_wordlist, stop_words)
			body_stemmed = stem_words(body_removed)
			
			#add _u to the end of title
			body_removed = [t + '_b' for t in body_removed]
			body_stemmed = [t + '_b' for t in body_stemmed]	
			
			cp =FreqDist(body_stemmed).items()
			for c in cp:
				arg_term = c[0]
				if arg_term in cur_dict:
					vector.append((cur_dict[c[0]], c[1]))
					
		if len(vector) != 0:
				vector.sort()
				vectors.append((id, vector))
	return vectors
		
def extract_term_freq(docs, stop_words, cur_dict, voc2stem, stem2voc):
	from nltk.probability import FreqDist
	from nltk.tokenize import regexp_tokenize	
	from help_tools import remove_stop, stem_words, make_voc2stem
	for doc in docs:
		
		id = doc[0]
		url = doc[1]
		title = doc[2]
		desc = doc[3]		
		keywords = doc[4]
		body = doc[5]
		
		if title == None:
			title = ''
		if url == None:
			url = ''
		if desc == None:
			desc = ''		
		if keywords == None:
			keywords = ''		
		if body == None:
			body = ''					
		
		#to lowercase
		title = title.lower()
		url = url.lower()
		desc = desc.lower()
		keywords = keywords.lower()
		body = body.lower()
				
		#extract title
		if len(title)>0:
			title_wordlist = regexp_tokenize(title, '[a-zA-Z]+')
			title_removed = remove_stop(title_wordlist, stop_words)
			title_stemmed = stem_words(title_removed)			
			#add _t to the end of title
			title_removed = [t + '_t' for t in title_removed]
			title_stemmed = [t + '_t' for t in title_stemmed]						
			#make voc to stem mapping
			make_voc2stem(title_removed, title_stemmed, voc2stem, stem2voc)			
			
			#compute freq
			cp = FreqDist(title_stemmed).items()
			for c in cp:
				arg_term = c[0]
				if arg_term not in cur_dict:
					cur_dict[arg_term] = 1
				else:
					cur_dict[arg_term] += 1
		
		if len(url)>0:
			url_wordlist = regexp_tokenize(url, '[a-zA-Z]+')
			url_removed = remove_stop(url_wordlist, stop_words)
			url_stemmed = stem_words(url_removed)
			#add _u to the end of title
			url_removed = [t + '_u' for t in url_removed]
			url_stemmed = [t + '_u' for t in url_stemmed]		
			#make voc to stem mapping
			make_voc2stem(url_removed, url_stemmed, voc2stem, stem2voc)			
			
			cp = FreqDist(url_stemmed).items()
			for c in cp:
				arg_term = c[0]
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
			
			#add _u to the end of title
			desc_removed = [t + '_kd' for t in desc_removed]
			desc_stemmed = [t + '_kd' for t in desc_stemmed]	
			make_voc2stem(desc_removed, desc_stemmed, voc2stem, stem2voc)			
			
			cp = FreqDist(desc_stemmed).items()
			for c in cp:
				arg_term = c[0]
				if arg_term not in cur_dict:
					cur_dict[arg_term] = 1
				else:
					cur_dict[arg_term] += 1
					
		#extract body text		
		if len(body)>0:
			body_wordlist = regexp_tokenize(body, '[a-zA-Z]+')
			body_removed = remove_stop(body_wordlist, stop_words)
			body_stemmed = stem_words(body_removed)
			
			#add _u to the end of title
			body_removed = [t + '_b' for t in body_removed]
			body_stemmed = [t + '_b' for t in body_stemmed]	
			
			make_voc2stem(body_removed, body_stemmed, voc2stem, stem2voc)			
			
			cp =FreqDist(body_stemmed).items()
			for c in cp:
				arg_term = c[0]
				if arg_term not in cur_dict:
					cur_dict[arg_term] = 1
				else:
					cur_dict[arg_term] += 1
		
	
def build_term_freq_list(max_id, trunks, stop_set):	
	from time import time
	from help_tools import chunks
	from db_util import get_docs_between
	start = time()
	cur_dict = {}
	voc2stem = {}
	stem2voc = {}
	#make trunks
	all_ids = range(max_id)
	all_trunks = chunks(all_ids, trunks)
	tot_trunks = len(all_trunks)
	for trunk in all_trunks:
		start_id = trunk[0]
		end_id = trunk[len(trunk) - 1]
		print 'start extract terms from ' + str(start_id) + ' to ' + str(end_id)
		docs = get_docs_between(start_id, end_id)
		extract_term_freq(docs, stop_set, cur_dict, voc2stem, stem2voc)
		print 'finish extract terms from ' + str(start_id) + ' to ' + str(end_id)
		tot_trunks -= 1
		print str(tot_trunks) + ' remained'		
	end = time()
	print 'Finish tasks in ' + str(int(end - start)) + ' seconds'
	return cur_dict, voc2stem, stem2voc

def pl_build_term_freq_list(IDs, trunk_size, stop_set):	
	from time import time
	from help_tools import chunks
	from db_util import get_docs_between
	start = time()
	cur_dict = {}
	voc2stem = {}
	stem2voc = {}	
	all_trunks = chunks(IDs, trunk_size)
	for trunk in all_trunks:
		start_id = trunk[0]
		end_id = trunk[len(trunk) - 1]
		print 'start extract terms from ' + str(start_id) + ' to ' + str(end_id)
		docs = get_docs_between(start_id, end_id)
		extract_term_freq(docs, stop_set, cur_dict, voc2stem, stem2voc)
		print 'finish extract terms from ' + str(start_id) + ' to ' + str(end_id)		
	end = time()
	print 'Finish tasks in ' + str(int(end - start)) + ' seconds'
	return cur_dict, voc2stem, stem2voc
			
if __name__ == '__main__':			
	from db_util import get_max_id
	from help_tools import read_stop_list, write_dict, write_term_freq, write_voc_2_stem
	trunks = 10000
	
	fname_dict = 'adv_uwo_full_dict'
	fname_stop = 'new_english.stop'
	fname_freq = 'adv_uwo_f'
	fname_voc_2_stem = 'adv_uwo_voc_to_stem.txt'
	fname_stem_2_voc = 'adv_uwo_stem_to_voc.txt'
	
	maxid = get_max_id('uwo.webs')	
	stop_set = read_stop_list(fname_stop)
	term_freqs, voc2stem, stem2voc = build_term_freq_list(maxid, trunks, stop_set)
	write_dict(term_freqs, fname_dict)
	write_term_freq(term_freqs, fname_freq)
	write_voc_2_stem(voc2stem, stem2voc, fname_voc_2_stem, fname_stem_2_voc)

