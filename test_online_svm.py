from liblinearutil import *
import urllib2
import zlib
import simplejson as json
"""
url_2 = 'http://localhost:8000/?q=1_234:0.12_235:0.12'
fd = urllib2.urlopen(url_2)
ct=fd.read()
fd.close()
"""


base_url = 'http://localhost:8000/?q='
#parameter = <id>_<wd:data>+
#y, x = svm_read_problem('../heart_scale')
y, x = svm_read_problem('food_training_data.txt')
n = 0
predictions = []
for xx in x[:10]:
	#id
	q = str(n)
	#cats
	q += '_{-1}'
	#features
	wds = xx.keys()
	wds.sort()
	for wd in wds:
		q += '_' + str(wd) + ':' + str(xx[wd])
	request_url = base_url + q
	#print request_url
	x1=zlib.compress(request_url)
	print len(request_url), len(x1)
	
	fd = urllib2.urlopen(request_url)
	ct=fd.read()
	fd.close()
	data = json.loads(ct)
	predictions.append(data[0]['probs'])	
	n += 1

