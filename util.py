def search_bing(query, npages=5):
	import bingapi
	appid = '5288CAD808E07789BF0ECA3F55B704C3293D975B'
	bing = bingapi.Bing(appid)
	page_results = {}
	n = 0
	for index_page in range(npages):		
		resp = bing.do_web_search(query, [('Web.Count', 10), ('Web.Offset', index_page * 10)])		
		results = resp['SearchResponse']['Web']['Results']		
		for result in results:			
			title = ''
			desc = ''
			url = ''
			if 'Title' in result:
				title = result['Title']
			if 'Description' in result:
				desc = result['Description']
			if 'Url' in result:
				url = result['Url']	
			if url not in page_results:
				page_results[url] = (title, desc, n)
			n += 1
	return page_results
	
def download_webpage(link):
	import urllib2
	try:    
		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		lk = opener.open(link, timeout=10)	
		ct = lk.read()
		ct = ct.lower()	
	except Exception :		
		ct = ''
	return ct

def extract_content(ct):
	import nltk
	from nltk.tokenize import regexp_tokenize
	import re
	
	index1 = ct.find("<title>")
	index2 = ct.find('</title>', index1)
	
	title=""
	if index1!=-1 and index2!=-1:
		title= ct[(index1+len("<title>")):index2]
	
	body=re.sub("<title>(((?:(?! <title>).)*)|((.*)<title>(.*)))</title>","",ct)
	keywords=re.search("<meta\s+name=[\"|\']?keywords[\"|\']?\s+content=[\"|\']?([^\"]*)[\"|\']?", ct,2)
	if keywords==None:
		keywords=re.search("<meta\s+content=[\"|\']?([^\"]*)[\"|\']?\s+name=[\"|\']?keywords[\"|\']?", ct,2)
	desp=re.search("<meta\s+name=[\"|\']?description[\"|\']?\s+Content=[\"|\']?([^\"]*)[\"|\']?", ct,2)
	if desp==None:
		desp=re.search("<meta\s+content=[\"|\']?([^\"]*)[\"|\']?\s+name=[\"|\']?description[\"|\']?", ct,2)
	
	charcode = ''
	contenttype = re.search("<meta\s+http-equiv=[\"|\']?content-Type[\"|\']?\s+content=[\"|\']?([^\"]*)[\"|\']?", ct,2)
	if contenttype != None:
		contenttype = re.search('charset=(.+)', contenttype.group(1))
		if contenttype != None:
			charcode = contenttype.group(1)
	
	#clean html
	tmp_t=nltk.clean_html(title)
	
	if len(tmp_t)!=0:
		tmp_t=tmp_t.replace("\n", " ")
		tmp_t=re.sub("&\S*;"," ",tmp_t)
		tmp_t=re.sub("[^A-Za-z0-9,.;:'|\-\[\]/]"," ",tmp_t)
		tmp_t=re.sub("\""," ",tmp_t)
		tmp_t=re.sub("\s+"," ",tmp_t)
		tmp_t=re.sub("'","",tmp_t)
		t=tmp_t
	else:
		t=""

	body=nltk.clean_html(body)
	body=body.replace("\n", " ")
	body=re.sub("&\S*;"," ",body)
	body=re.sub("[^A-Za-z0-9,.;:'/]"," ",body)
	body=re.sub("\""," ",body)
	body=re.sub("\s+"," ",body)
	body=re.sub("\.+",".",body)
	body=re.sub("\.+",".",body)
	body=re.sub(",+",",",body)
	body=re.sub(";+",";",body)
	b=body
	
	if keywords!=None:
		tmp_k=keywords.group(1)
		tmp_k=nltk.clean_html(tmp_k)
		tmp_k=tmp_k.replace("\n", " ")
		tmp_k=re.sub("&\S*;"," ",tmp_k)
		tmp_k=re.sub("[^A-Za-z0-9,.;:'/]"," ",tmp_k)
		tmp_k=re.sub("\""," ",tmp_k)
		tmp_k=re.sub("\s+"," ",tmp_k)
		tmp_k=re.sub("\.+",".",tmp_k)
		tmp_k=re.sub("\.+",".",tmp_k)
		tmp_k=re.sub(",+",",",tmp_k)
		tmp_k=re.sub(";+",";",tmp_k)
		k=tmp_k
	else:
		k=""
	
	if desp!=None:
		 
		tmp_d=nltk.clean_html(desp.group(1))
		tmp_d=tmp_d.replace("\n", " ")
		tmp_d=re.sub("&\S*;"," ",tmp_d)
		tmp_d=re.sub("[^A-Za-z0-9,.;:'/]"," ",tmp_d)
		tmp_d=re.sub("\""," ",tmp_d)
		tmp_d=re.sub("\s+"," ",tmp_d)
		tmp_d=re.sub("\.+",".",tmp_d)
		tmp_d=re.sub("\.+",".",tmp_d)
		tmp_d=re.sub(",+",",",tmp_d)
		tmp_d=re.sub(";+",";",tmp_d)
		d=tmp_d
	else:
		d=""

	return t,b,k,d, charcode

def find_query_from_database():
	all_queries = []
	try:				
		import MySQLdb
		con   =   MySQLdb.connect(host="192.168.0.2",  port=3306, user="root",  passwd="see",  db="see", use_unicode=True, charset='utf8')  
		cursor   =   con.cursor()  
		sql  = 'select distinct query from query_search_engine.webs'
		cursor.execute(sql)
		rows = cursor.fetchall()
		for r in rows:
			all_queries.append(r[0])
		cursor.close()
		con.close()
	except Exception:
		print 'err'
	return all_queries

def find_urls_from_database():
	all_urls = []
	try:				
		import MySQLdb
		con   =   MySQLdb.connect(host="192.168.0.2",  port=3306, user="root",  passwd="see",  db="see", use_unicode=True, charset='utf8')  
		cursor   =   con.cursor()  
		sql  = 'select url from query_search_engine.webs'
		cursor.execute(sql)
		rows = cursor.fetchall()
		for r in rows:
			all_urls.append(r[0])
		cursor.close()
		con.close()
	except Exception:
		print 'err'
	return all_urls

def write_data_to_database(query, url, snippets, title, description, keywords, body, html, rank):
	try:
		error_state = 1
		
		import MySQLdb
		con   =   MySQLdb.connect(host="192.168.0.2",  port=3306, user="root",  passwd="see",  db="see", use_unicode=True, charset='utf8')  
		cursor   =   con.cursor()  
		
		error_state = 2
		
		#make SQL statement				
		colums = '(query, url'
		values = '("' + query + '", "' + url + '"'
		if snippets != '':
			colums += ', snippets'
			escap_snippets = con.escape_string(snippets)
			values += ', "' + escap_snippets + '"'
		if title != '':
			colums += ', title'
			values += ', "' + title + '"'
		if description != '':
			colums += ', description'
			values += ', "' + description + '"'
		if keywords != '':
			colums += ', keywords'
			values += ', "' + keywords + '"'
		colums += ', body, html, rank)'
		escape_html = con.escape_string(html)
		values += ', "' + body + '", "' + escape_html + '", ' + str(rank) + ')'	
		sql = 'insert into query_search_engine.webs ' + colums + ' values ' + values
		
		error_state = 3
		
		cursor.execute(sql)
		cursor.close()
		con.commit()				
		con.close()		
		
	except Exception:			
		if error_state == 1:
			logger.error('Connecting DBSERVER for URL ' + url)	
			print 'Connecting DBSERVER for URL ' + url
		elif error_state == 2:
			logger.error('Encoding SQL statement for URL ' + url)
			print 'Encoding SQL statement for URL ' + url	

def init_logging(name, log_fpath):
	import logging
	logger = logging.getLogger(name)
	hdlr = logging.FileHandler(log_fpath)
	formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
	hdlr.setFormatter(formatter)
	logger.addHandler(hdlr) 
	logger.setLevel(logging.WARNING)
	return logger

def make_filters():
	filters = "zzz|z3|9|o|obj|exe|class|jar|bmp|gif|jpeg|tar|7z|rar|iso|png|tiff|mid|mp2|mp3|mp4|ps|wav|avi|mov|mpeg|ram|m4v|rm|smil|wmv|swf|wma|zip|rar|gz|pdf|doc|docx|ppt|pptx"
	filters = filters.split('|')	
	return filters

def filter_urls(url, ent_filters):		            
	for ent in ent_filters:	
		ent = '.' + ent
		if url.lower().endswith(ent):
			return True	
	return False	
	
def read_id_urls(fname):
	rows = []
	fd = open(fname)
	for line in fd:
		line= line.strip().split(' ')
		rows.append(line)
	fd.close()
	return rows
	
def sample_id_by_check_exist(ids, existed_ids, n):
	import random
	set_ids = set(ids)
	set_existed_ids = set(existed_ids)
	set_remained_ids = set_ids - set_existed_ids
	sampled_ids = random.sample(set_remained_ids, n)
	sampled_ids = [int(r) for r in sampled_ids]
	sampled_ids.sort()
	return sampled_ids
	
def test_sampled():
	from db_util import get_id_url_from_query
	all_ids = read_id_urls('uwo_id_urls.txt')
	existed_ids =  get_id_url_from_query('food site:uwo.ca')
	print sample_id_by_check_exist([r[0] for r in all_ids], [r[0] for r in existed_ids], 100)
	
if __name__ == "__main__":	
	#rows=  get_id_url_from_query('food site:uwo.ca')
	#rows =read_id_urls('uwo_id_urls.txt')
	#test_sampled()
	
	logger = init_logging('bing_query', 'rountine_bing.log')	

	site = 'site:queensu.ca'	
	word_list = set(['dairy', 'veggie', 'juice', 'spicy', 'sandwich', 'food', 'diet', 'vitamins', 'meal', 'grill', 'cheese', 'dessert', 'fries', 'chicken', 'salad', 'lunch', 'dinner', 'dining', 'cuisine', 'eating', 'nutrition', 'beer', 'drink'])
	
	#make url extension filters
	ent_filters = make_filters()
	#filtering exist queries
	all_queries = find_query_from_database()	
	word_list = [w for w in word_list if w + ' ' + site not in all_queries]
	#make url existing filters
	all_urls = set(find_urls_from_database())
	
	for words in word_list:
		query = words + ' ' + site
		
		page_results = search_bing(query)
		
		for url in page_results.keys():			
			error_state = -1
			try:
				#download webpage
				if filter_urls(url, ent_filters) or url in all_urls:
				#if filter_urls(url, ent_filters):
					continue
				
				all_urls.add(url)
					
				ct = download_webpage(url)
				if ct == '':
					logger.error('Download URL ' + url)
					continue
					
				#extract content
				error_state = 0	
				
				title = page_results[url][0]
				snippets = page_results[url][1]
				rank = page_results[url][2]				
				title = title.encode('utf8')
				snippets = snippets.encode('utf8')
				url = url.encode('utf8')
				
				title, body, keywords, description, charcode = extract_content(ct)																
				error_state = 1

				#encode html															
				if charcode != '':
					if charcode == 'iso-utf-8':
						charcode = 'utf8'
					html = ct.decode(charcode)
					html = html.encode('utf8')												

				error_state = 2
				
				write_data_to_database(query, url, snippets, title, description, keywords, body, html, rank)
			
				error_state = 3			
			except Exception:
				if error_state == 0:
					logger.error('Extracting HTML content for URL ' + url)
					print 'Extracting HTML content for URL ' + url
				elif error_state == 1:
					logger.error('Encoding HTML content for URL ' + url)					
					print 'Encoding HTML content for URL ' + url
				elif error_state == 2:
					logger.error('Writing DB for URL ' + url)							
					print 'Writing DB for URL ' + url

			if error_state == 3:
				logger.info('Successfully storing content for URL ' + url)

	
