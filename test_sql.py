from util import download_webpage, extract_content

query = ''
url = 'http://www.westernkendo.com/'
#download webpage
			
ct = download_webpage(url)
	
#extract content
error_state = 0	

title, body, keywords, description, charcode = extract_content(ct)												

error_state = 1

#encode html															
if charcode != '':
	if charcode == 'iso-utf-8':
		charcode = 'utf8'
	html = ct.decode(charcode)
	html = html.encode('utf8')								
"""	
title = page_results[url][0]
snippets = page_results[url][1]
rank = page_results[url][2]		
"""
title = ''
snippets = ''
rank = 10

title = title.encode('utf8')
snippets = snippets.encode('utf8')
url = url.encode('utf8')
														
error_state = 2

#write_data_to_database(query, url, snippets, title, description, keywords, body, html, rank)			
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
		values += ', "' + t + '"'
	if description != '':
		colums += ', description'
		values += ', "' + description + '"'
	if keywords != '':
		colums += ', keywords'
		values += ', "' + keywords + '"'
	colums += ', body, html, rank)'
	escape_html = con.escape_string(html)
	values += ', "' + body + '", "' + escape_html + '", ' + str(rank) + ')'	
	sql = 'insert into quey_search_engine.webs ' + colums + ' values ' + values
	
	error_state = 3
	
	cursor.execute(sql)
	cursor.close()
	con.commit()				
	con.close()		
	
except Exception:			
	if error_state == 1:
		logger.error('Connecting DBSERVER for URL ' + url)	
	elif error_state == 2:
		logger.error('Encoding SQL statement for URL ' + url)
	elif error_state == 3:
		logger.error('Executing SQL statement for URL ' + url)