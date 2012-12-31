import xmlrpclib
from liblinearutil import *
import urllib2
import zlib
import simplejson as json
import time

s = xmlrpclib.ServerProxy('http://localhost:8000')
#print s.prediction_debug('1_{-1}_13333:0.12_2:0.112112')
#print s.predict_webpage_debug('http://www.usc.uwo.ca/page.asp?id=50')
# Print list of available methods
print s.system.listMethods()


#parameter = <id>_<wd:data>+
#y, x = svm_read_problem('../heart_scale')
y, x = svm_read_problem('food_training_data.txt')
start = time.time()
n = 0
predictions = []
for xx in x:
	#id
	doc = str(n)
	#cats
	doc += '_{-1}'
	#features
	wds = xx.keys()
	wds.sort()
	for wd in wds:
		doc += '_' + str(wd) + ':' + str(xx[wd])	
	ct = s.prediction_debug(doc)	
	data = json.loads(ct)
	predictions.append((data['id'], data['probs']))	
	n += 1
end = time.time()
print 'using ' + str(end - start) + ' seconds'
print 'average speed ' + str(float(len(y))/(end - start)) + ' docs/second'
