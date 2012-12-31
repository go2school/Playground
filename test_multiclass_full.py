import xmlrpclib
from liblinearutil import *
import simplejson as json
import time
from help_tools import read_id_cat
from dataset_util import read_multi_label



id2cat = read_id_cat('uwo_id_cat_name')

n = 10
s = xmlrpclib.ServerProxy('http://localhost:8000')

labels = read_multi_label('/media/01CC16F5ED7072F0/see_workingdirectory/svm_probs/dmoz_train_labels_12072011.txt')

modes, A, B = s.get_mode_A_B(range(n))
modes_dc = {}
A_dc = {}
B_dc = {}
for m in modes:
	modes_dc[m[0]] = m[1]
for a in A:
	A_dc[a[0]] = a[1]
for b in B:
	B_dc[b[0]] = b[1]
predictions = {}
predictions_probs = {}

fd = open('/media/01CC16F5ED7072F0/see_workingdirectory/svm_probs/dmoz_train_features_12072011.txt')
m = 0
for line in fd:
	line = line.strip()
	a = line.index(' ')
	id = int(line[:a])	
	"""
	probs = s.predict_webpage_raw_shrinked_features(0, range(n), line)
	data = json.loads(probs)
	real_probs = data['probs']
	#compute prob
	import math
	for c in real_probs:
		print c, 1.0/(1.0+math.exp(real_probs[c]*A_dc[int(c)] + B_dc[int(c)]))
	"""
	probs= s.predict_webpage_raw_shrinked_features_out_prob(0, range(n), line)
	data = json.loads(probs)
	real_probs = data['probs']
	print real_probs
	threshold = 0.5
	#for c in real_probs.keys():
	predict_labels = []
	predict_probs = []
	for c in [str(i) for i in range(n)]:
		if int(c) in id2cat and c in real_probs and real_probs[c] >= threshold:
			predict_labels.append(int(c))
			predict_probs.append((int(c), real_probs[c]))
	predictions[id]= predict_labels
	predictions_probs[id] = predict_probs
	m += 1
	if m > 5:
		break
fd.close()

fd = open('predicted_labels', 'w')
for id in predictions.keys():
	fd.write(str(id) + ' ' + str(len(predictions[id])))
	for l in predictions[id]:
		fd.write(' ' + str(l))
	fd.write('\n')
fd.close()
"""



data = json.loads(probs)
real_probs = data['probs']
print real_probs
threshold = 0.8
prediction = []
#for c in real_probs.keys():
for c in [str(i) for i in range(1,21)]:
	if int(c) in id2cat and real_probs[c] >= threshold:
		prediction.append((id2cat[int(c)], real_probs[c]))
print prediction		

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
"""
