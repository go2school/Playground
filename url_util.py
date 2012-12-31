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

def remove_nontext(body):
	import re
	body=body.replace("\n", " ")
	body=re.sub("&\S*;"," ",body)
	body=re.sub("[^A-Za-z0-9,.;:'/]"," ",body)
	body=re.sub("\""," ",body)
	body=re.sub("\s+"," ",body)
	body=re.sub("\.+",".",body)
	body=re.sub("\.+",".",body)
	body=re.sub(",+",",",body)
	body=re.sub(";+",";",body)	
	return body
	
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
