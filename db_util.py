def get_max_id(db):
	import   MySQLdb  	
	con   =   MySQLdb.connect(host="192.168.0.2",  port=3306, user="root",  passwd="see",  db="see")  
	cursor   =   con.cursor()  
	sql = 'select max(id) from ' + db
	cursor.execute(sql)
	id = cursor.fetchone()		
	maxid = int(id[0]) 
	cursor.close()
	con.close()
	return maxid
	
def get_min_id(db):
	import   MySQLdb  	
	con   =   MySQLdb.connect(host="192.168.0.2",  port=3306, user="root",  passwd="see",  db="see")  
	cursor   =   con.cursor()  
	sql = 'select min(id) from ' + db
	cursor.execute(sql)
	id = cursor.fetchone()		
	minid = int(id[0]) 
	cursor.close()
	con.close()
	return minid

def get_docs_between(start_id, to_id):
	import   MySQLdb  		
	docs = []
	con   =   MySQLdb.connect(host="192.168.0.2",  port=3306, user="root",  passwd="see",  db="see", use_unicode=True, charset='utf8')  
	cursor   =   con.cursor()  
	sql = 'select id, url, title, description, keywords, wholeText from uwo.webs where id >= ' + str(start_id) + ' and id <= ' + str(to_id)
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

def get_docs_between_new_uwo(start_id, to_id):
	import   MySQLdb  		
	docs = []
	con   =   MySQLdb.connect(host="192.168.0.2",  port=3306, user="root",  passwd="see",  db="see", use_unicode=True, charset='utf8')  
	cursor   =   con.cursor()  
	sql = 'select id, url, title, description, keywords, text from uwo.documents where id >= ' + str(start_id) + ' and id <= ' + str(to_id)
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

def get_docs_in_set(db, ids):
	import   MySQLdb  		
	docs = []
	con   =   MySQLdb.connect(host="192.168.0.2",  port=3306, user="root",  passwd="see",  db="see")  
	cursor   =   con.cursor()  
	sql = 'select id, url, title, description, keywords, body from '+db+' where id in (' + str(ids[0])	
	for id in ids[1:]:
		sql += ',' + str(id)
	sql += ')'
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
		
def get_docs_in_set_uwo(db, ids):
	import   MySQLdb  		
	docs = []
	con   =   MySQLdb.connect(host="192.168.0.2",  port=3306, user="root",  passwd="see",  db="see", use_unicode=True, charset='utf8')  
	cursor   =   con.cursor()  
	sql = 'select id, url, title, description, keywords, wholeText from '+db+' where id in (' + str(ids[0])	
	for id in ids[1:]:
		sql += ',' + str(id)
	sql += ')'
	cursor.execute(sql)
	while True:
		row = cursor.fetchone()		
		if row == None:
			break
		docs.append(row)
	cursor.close()
	con.close()
	return docs

def get_docs_between_query_search_engine(start_id, ids):
	import   MySQLdb  		
	docs = []
	con   =   MySQLdb.connect(host="192.168.0.2",  port=3306, user="root",  passwd="see",  db="query_search_engine", use_unicode=True, charset='utf8')  
	cursor   =   con.cursor()  
	sql = 'select id, title, text from query_search_engine.webdoc where id >= ' + str(start_id) + ' and id <= ' + str(to_id)
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
			
def get_docs_in_set_query_search_engine(ids):
	import   MySQLdb  		
	docs = []
	con   =   MySQLdb.connect(host="192.168.0.2",  port=3306, user="root",  passwd="see",  db="query_search_engine", use_unicode=True, charset='utf8')  
	cursor   =   con.cursor()  
	str_ids = [str(id) for id in ids]
	sql = 'select id, title, text from query_search_engine.webdoc where id in(' +','.join(str_ids) +')'
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

def get_docs_in_uwo_set_query_search_engine(ids):
	import   MySQLdb  		
	docs = []
	con   =   MySQLdb.connect(host="192.168.0.2",  port=3306, user="root",  passwd="see",  db="uwo", use_unicode=True, charset='utf8')  
	cursor   =   con.cursor()  
	str_ids = [str(id) for id in ids]
	sql = 'select id, title, content from uwo.uwo_new_nutch_docs where id in(' +','.join(str_ids) +')'
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
			
def get_all_urls(db):
	import   MySQLdb  	
	con   =   MySQLdb.connect(host="192.168.0.2",  port=3306, user="root",  passwd="see",  db="see")  
	cursor   =   con.cursor()  
	sql = 'select url from ' + db
	cursor.execute(sql)	
	urls = set()
	while True:
		row = cursor.fetchone()		
		if row == None:
			break
		urls.add(row[0])	
	cursor.close()
	con.close()
	return urls
	
def test_get_docs_in_set():
	ids = [1,2,3,4,5,6,7]
	docs=  get_docs_in_set(ids)
	for doc in docs:
		print doc[2]

def get_id_url_from_query(db, query):	
	import MySQLdb
	con   =   MySQLdb.connect(host="192.168.0.2",  port=3306, user="root",  passwd="see",  db="see", use_unicode=True, charset='utf8')  
	cursor   =   con.cursor()  
	sql = 'select id,url from '+db+' where query = "' + con.escape_string(query) + '"'
	print sql
	cursor.execute(sql)
	rows = cursor.fetchall()	
	cursor.close()
	con.close()
	return rows
	
if __name__ == '__main__':	
	#urls = get_all_urls('quey_search_engine.webs')
	test_get_docs_in_set()
