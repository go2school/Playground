from util import download_webpage, extract_content

title = 'a'
snippets = 'b'
rank = 1
url = 'http://www.westernkendo.com/'
query = 'x'

title = title.encode('utf8')
snippets = snippets.encode('utf8')
url = url.encode('utf8')


ct = download_webpage(url)
if ct == '':
	logger.error('Download URL ' + url)
error_state = 0
#encode html
if charcode != '':
	if charcode == 'iso-utf-8':
		charcode = 'utf8'
	html = ct.decode(charcode)
	html = html.encode('utf8')
body = b
error_state = 1


t,b,k,d, charcode = extract_content(ct)
#write_data_to_database(query, url, snippets, t, d, k, b, ct, rank)					
title = t
description = d
keywords = k



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