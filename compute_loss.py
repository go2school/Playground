def compute_pr_re_f1(predictions, trues):
	pr = 0
	re = 0
	f1 = 0
	tp = 0
	fp = 0
	fn = 0
	for i in range(len(predictions)):
		if predictions[i] == 1 and trues[i] == 1:
			tp += 1
		elif predictions[i] == 1 and trues[i] == -1:
			fp += 1
		elif predictions[i] == -1 and trues[i] == 1:
			fn += 1
	if tp + fp == 0:
		pr = 0
	else:
		pr = float(tp)/(tp+fp)
	if tp + fn == 0:
		re = 0
	else:
		re = float(tp)/(tp+fn)
	if pr + re == 0:
		f1 = 0
	else:
		f1 = 2*pr*re/(pr+re)
	return pr, re, f1, tp, fp , fn
	
def read_in_liblinear_probability_prediction(fname):
	predicted_probs = []
	fd = open(fname)
	for line in fd:
		line = line.strip().split(' ')
		predicted_probs.append(float(line[1]))
	fd.close()
	return predicted_probs[1:]

def check_probability_prediction(fname, ids_fname, threshold, out_fname):
	probs = read_in_liblinear_probability_prediction(fname)
	fd = open(ids_fname)
	ids = fd.read()	
	fd.close()	
	ids = ids.split('\n')
	
	id_prob = []
	for i in range(len(ids)-1):
		id_prob.append((int(ids[i]), probs[i]))		
	id_prob = sorted(id_prob, key=lambda s:s[1], reverse=True)
	
	cut_off_probs = []
	for i in range(len(id_prob)):
		if id_prob[i][1] >= threshold:
			cut_off_probs.append(id_prob[i])
		else:
			break
			
	fd_w = open(out_fname, 'w')
	for i in range(len(cut_off_probs)):
		fd_w.write(str(cut_off_probs[i][0]) + ' ' + ('%.5f' % cut_off_probs[i][1]) + '\n')
	fd_w.close()
	return cut_off_probs
	
def check_prediction(fname, ids_fname):
	fd = open(fname)
	ct = fd.read()	
	fd.close()
	fd = open(ids_fname)
	ids = fd.read()	
	fd.close()
	ct = ct.split('\n')
	ids = ids.split('\n')
	n_pos = ct.count('1')
	n_neg = ct.count('-1')
	pos_ids = [int(ids[i]) for i in range(len(ct)) if ct[i]=='1']
	print pos_ids
	return n_pos, n_neg, pos_ids
	
def show_prediction(predict_labels_fname, dataset):	
	#read prediction
	predicted_labels = []
	fd = open(predict_labels_fname)
	for line in fd:
		predicted_labels.append(int(line.strip()))
	fd.close()

	#read true label
	true_labels = []
	fd = open(dataset)
	for line in fd:
		a = line.index(' ')
		true_labels.append(int(line[:a]))	
	fd.close()

	pr, re, f1, tp , fp ,fn = compute_pr_re_f1(predicted_labels, true_labels)
	print pr, re, f1, tp , fp , fn

def show_prediction_prob(predict_labels_fname, dataset,  threshold):	
	#read probability prediction
	predicted_probs = read_in_liblinear_probability_prediction(predict_labels_fname)	
	
	#set label by threshold
	predicted_labels = []
	for p in predicted_probs:
		if p >= threshold:
			predicted_labels.append(1)
		else:
			predicted_labels.append(-1)
	
	#read true label
	true_labels = []
	fd = open(dataset)
	for line in fd:
		a = line.index(' ')
		true_labels.append(int(line[:a]))	
	fd.close()
	
	pr, re, f1, tp , fp ,fn = compute_pr_re_f1(predicted_labels, true_labels)
	print pr, re, f1, tp , fp , fn

def compute_loss_multilabel(predictions, trues):		
	ids = predictions.keys()
	prs = []
	res = []
	f1s = []
	for id in ids:
		p_set = set(predictions[id])
		t_set = set(trues[id])
		in_set = p_set & t_set
		if len(p_set) == 0:
			pr = 0
		else:
			pr = float(len(in_set))/len(p_set)		
		if len(t_set) == 0:
			re = 0
		else:
			re = float(len(in_set))/len(t_set)
		if pr + re == 0:
			f1 = 0
		else:
			f1 = 2* pr * re / (pr + re)
		print pr, re, f1
		prs.append(pr)
		res.append(re)
		f1s.append(f1)
	return sum(prs)/len(prs), sum(res)/len(res), sum(f1s)/len(f1s)
	

if __name__ == '__main__':	
	#show_prediction('food_prediction.txt', 'food_training_data.txt')
	#z=check_prediction('uwo_food_prediction.txt', 'uwo_ids.txt')
	show_prediction_prob('food_prediction.txt', 'food_training_data.txt', 0.5)
	#check_probability_prediction('food_prediction.txt', 'food_ids.txt', 0.5, 'food_ranked_prob.txt')
	check_probability_prediction('uwo_food_prediction.txt', 'uwo_ids.txt', 0.5, 'uwo_food_ranked_prob.txt')
 
