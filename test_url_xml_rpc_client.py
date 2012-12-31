import xmlrpclib
from url_util import download_webpage
from liblinearutil import *
import simplejson as json
import time
from active_learning import *
from help_tools import read_id_cat

def extractlinks(url, html):
	links = []	
	from BeautifulSoup import BeautifulSoup
	import urlparse 	
	soup = BeautifulSoup(html)
	anchors = soup.findAll('a')	
	for a in anchors:
		try:
			links.append(urlparse.urljoin(url, a['href']))		
		except Exception:
			pass
	return links	

from active_learning import *
	
hier = 'dmoz_hierarchy.txt'
root = Node().read_tree(hier)

id2cat = read_id_cat('uwo_id_cat_name')
s = xmlrpclib.ServerProxy('http://localhost:8000')
print s.system.listMethods()

url = 'http://www.math.uwo.ca'
html = download_webpage(url)
links = extractlinks(url, html)

all_links =  links
"""
all_links = []
for url in links:
	html = download_webpage(url)
	links = extractlinks(url, html)
	all_links += links
"""	
	
id = 0
#cats = [0, 85, 157, 224, 275, 304, 349, 369, 466, 564, 627]
cats = range(662)
predictions = {}
predictions_probs = {}
start = time.time()
for link in all_links:
	ct = s.predict_webpage_shrinked_features(id, cats, link)
	data = json.loads(ct)
	real_probs = data['probs']	
	threshold = 0.5
	#for c in real_probs.keys():
	predict_labels = []
	predict_probs = []
	for c in cats:
		if str(c) in real_probs and real_probs[str(c)] >= threshold:
			predict_labels.append(int(c))
			predict_probs.append((int(c), real_probs[str(c)]))	
	out_set = set()	
	root.filter_result_labels(predict_labels, out_set)
	out_cat_name = [id2cat[o] for o in out_set]
	predictions[id] = out_cat_name
	predictions_probs[id] = predict_probs
		
	print 'receiving doc ' + str(data['id']) + ' ' + (','.join(predictions[id])) + ' ' + link
	id += 1

end = time.time()
print 'using ' + str(end - start) + ' seconds'
print 'average speed ' + str(float(len(all_links))/(end - start)) + ' docs/second'
