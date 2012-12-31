from time import time
import urllib
v = '/?m=sfsdfs&th=0.5&tt=&bd=&url=http%3A%2F%2Fwww.google.ca%2Fsearch%3Fgcx%3Dw%26sourceid%3Dchrome%26'		
if v.find('?') > -1:						
	print v
	#parse parameters
	params= v[2:].split('&')
	print params
	dict_params = {}
	for p in params:
		a,b=p.split('=')
		dict_params[a] = b
	#parse uid, method, threshold and requested url
	uid = '-1'
	method = ''
	threshold = ''
	url = ''
	title = ''
	body = ''			
	if 'id' in dict_params:
		uid = dict_params['id']
	if 'm' in dict_params:
		method = dict_params['m']
	if 'th' in dict_params:
		threshold = dict_params['th']
	if 'tt' in dict_params:#title
		title = dict_params['tt']				
		title = urllib.unquote(title)
	if 'bd' in dict_params:
		body = dict_params['bd']			
		body = urllib.unquote(body)
	if 'url' in dict_params:
		url = dict_params['url']										
		url = urllib.unquote(url)
				
	print dict_params

	start_job = time()
			
	result = ''
	
	#start download
	bad_request = False
	html = ''
	#if this is a bad parameter
	start_download = time()
	if not (url != '' or body != ''):
		bad_request = True
	else:											
		#if user does not give body, we need to download it
		if body == '':								
			from url_util import download_webpage
			html = download_webpage(url)
			print 'HTML length is ' + str(len(html))			
			if len(html) >= 500:
				print html[:500]							
			if len(html) == 0:
				bad_request = True
	end_download = time()
	if bad_request == True:
		result = '{"id":' + uid + '}'
	
	print 'Finishing download ' + url + ' in ' + ('%.3f' % (end_download - start_download)) + 'seconds'
								
	#prepare parallel variables
	import uuid
	suffix_lst = [str(uuid.uuid4()).replace('-','') for i in range(10)]
	var_html = 'html_' + suffix_lst[0]
	var_title = 'title_' + suffix_lst[0]
	var_body = 'body_' + suffix_lst[0]
	var_predicted_cats = 'predicted_cats_' + suffix_lst[1]
	var_svm_vector = 'svm_vector_' + suffix_lst[2]
	var_probs = 'probs_' + suffix_lst[3]
	var_svm_len = 'len_svm_vectors_' + suffix_lst[4]
