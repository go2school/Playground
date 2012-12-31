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
	
t,b,k,d, charcode = extract_content(ct)

error_state = 0
#encode html
if charcode != '':
	if charcode == 'iso-utf-8':
		charcode = 'utf8'
	html = ct.decode(charcode)
	html = html.encode('utf8')
body = b
error_state = 1
