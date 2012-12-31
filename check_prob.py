def f1():
	import os
	fs=os.listdir('solr_data_new/small')
	probs = []
	for f in fs:
		fd = open('solr_data_new/small' + '/' + f)
		for line in fd:
			if line.startswith('		<field name = "topic_0">'):
				a = line.index('>')
				b = line.rindex('<')
				v = line[a+1:b]
				probs.append(float(v))			
		fd.close()
	v = [p for p in probs if p >= 0.5 and p <= 0.9]
	print len(probs), len(v)

def f3():
	import os
	fs=os.listdir('solr_data_new/small')
	probs = []
	probs2 = []
	for f in fs:
		fd = open('solr_data_new/small' + '/' + f)
		for line in fd:
			if line.startswith('		<field name = "topic_0">'):
				a = line.index('>')
				b = line.rindex('<')
				v = line[a+1:b]
				probs.append(float(v))			
			if line.startswith('		<field name = "topic_1">'):
				a = line.index('>')
				b = line.rindex('<')
				v = line[a+1:b]
				probs2.append(float(v))			
		fd.close()
	v = []
	for i in range(len(probs)):
		if probs[i] >= 0.5 and probs[i] <= 0.9 and probs2[i] >= 0.5 and probs2[i] <= 0.9:
			v.append(1)
	print len(probs), len(v)
	
def f2():
	probs =  []
	fd = open('as.txt')
	for line in fd:
		if line.startswith('<float name="topic_0">'):
			a = line.index('>')
			b = line.rindex('<')
			v = line[a+1:b]
			probs.append(float(v))			
	fd.close()
	v = [p for p in probs if p >= 0.5 and p <= 0.9]
	print len(probs), len(v)

f1()
f2()
f3()
