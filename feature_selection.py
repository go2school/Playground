def get_tp_fp(dataset_fname):
	tp = {}
	fp = {}	
	pos = 0
	neg = 0
	fd = open(dataset_fname)
	for line in fd:
		line = line.strip().split(' ')
		label = line[0]
		words = []
		for l in line[1:]:
			word, occ = l.split(':')
			words.append(int(word))
		if label == '1':
			pos += 1
			for wd in words:
				if wd not in tp:
					tp[wd] = 1
				else:
					tp[wd] += 1				
		else:
			neg += 1
			for wd in words:
				if wd not in fp:
					fp[wd] = 1
				else:
					fp[wd] += 1
	fd.close()
	return tp, fp, pos, neg, pos + neg			

def merge_tp_fp(tp, fp):
	tp_words = set(tp.keys())
	fp_words = set(fp.keys())
	return tp_words.union(fp_words)

def entropy(x, y):
	import math
	x = float(x)
	y = float(y)
	xy = x + y	
	if xy == 0:
		return 1.0
	p1 = x / xy
	p2 = y / xy
	if p1 == 0 or p2 == 0:
		return 0.0		
	return -p1*math.log(p1, 2)-p2*math.log(p2, 2)
	
def information_gain(pos, neg, tp, fp):
	fn = pos - tp
	tn = neg - fp    
	freq = float(tp + fp)/(pos + neg)
	e1 = entropy(pos, neg)
	e2 = entropy(tp, fp)
	e3 = entropy(tn ,fn) 
	
	return e1-(freq*e2+(1-freq)*e3)

def doc_frenquency(tp, fp):
	return float(tp + fp)

def chi_t(count, expect):
	if expect == 0:
		return 0
	else:
		return (count - expect) * (count - expect) / expect
	
def chi_squared(pos, neg, tp, fp):
	fn = pos - tp
	tn = neg - fp
	tot = pos + neg
	pos_ratio = float(pos)/tot
	neg_ratio = float(neg)/tot
	
	v1 = chi_t(tp, (tp + fp) * pos_ratio)
	v2 = chi_t(fn, (tn + fn) * pos_ratio)
	v3 = chi_t(fp, (tp + fp) * neg_ratio)
	v4 = chi_t(tn, (tn + fn) * neg_ratio)	
	return v1 + v2 + v3 + v4
	
def RationalApproximation(t):
	# Abramowitz and Stegun formula 26.2.23.    
	# The absolute value of the error should be less than 4.5 e-4.    
	c = [2.515517, 0.802853, 0.010328];    
	d = [1.432788, 0.189269, 0.001308];    
	return t - ((c[2]*t + c[1])*t + c[0]) /   (((d[2]*t + d[1])*t + d[0])*t + 1.0);


def NormalCDFInverse(p):
	import math
	if p == 0:
		p = 0.0005
	if p == 1:
		p = 0.9995	
	if p < 0.0 or p > 1.0:
		s = "Invalid input argument (" + str(p) + "); must be larger than 0 but less than 1.";        		
		raise Exception(s) 		
	if p < 0.5:		
		return -RationalApproximation(math.sqrt(-2.0*math.log(p)))    	
	else:
		return RationalApproximation(math.sqrt(-2.0*math.log(1-p)))
	
def BNS(pos, neg, tp, fp):
	import math
	if pos == 0:
		tpr = 0
	else:
		tpr = float(tp)/pos
	if neg == 0:
		fpr = 0
	else:
		fpr = float(fp)/neg	
	
	a = NormalCDFInverse(tpr);
	b = NormalCDFInverse(fpr);
	return math.fabs(a-b);
	
def odds_ratio(pos, neg, tp, fp):
	if pos == 0:
		tpr = 0
	else:
		tpr = float(tp)/pos
		if tpr >= 1:
			tpr = 0.99999#to avoid divide by zero
	if neg == 0:
		fpr = 0.00001#to avoid divide by zero
	else:
		fpr = float(fp)/neg
	return tpr*(1-fpr)/((1-tpr)*fpr)

def F1(pos, neg, tp, fp):
	v = pos + tp + fp
	if v == 0:
		return 0
	else:
		return 2 * float(tp) / v
		
def test_feature_selection():
	pos = 1000
	neg = 5000
	tp = 4
	fp = 100	
	print 'IG', information_gain(pos, neg, tp, fp)	
	print 'BNS', BNS(pos, neg, tp, fp)	
	print 'F1', f1(pos, neg, tp, fp)	
	print 'ODDS', odds_ratio(pos, neg, tp, fp)	
	print 'CHI', chi_squared(pos, neg, tp, fp)	
	print 'DF', doc_frenquency(tp, fp)
	
def write_down_ranked_words(data, fname):
	fd = open(fname, 'w')
	for d in data:
		fd.write(str(d[0]) + ' ' + str(d[1]) + '\n')
	fd.close()

def convert_ranked_words_to_term(fname, out_fname, reverse_dict):
	fd = open(fname)
	fd_w = open(out_fname, 'w')
	for line in fd:
		line = line.strip().split(' ')
		fd_w.write(reverse_dict[int(line[0])] + ' ' + line[1] + '\n')
	fd_w.close()
	fd.close()
	
if __name__ == '__main__':	
	#test_feature_selection()	
	dict_fname = 'adv_uwo_full_dict'
	
	dataset_fname = 'food_training_data.txt'
	tp, fp, pos, neg, tot_doc = get_tp_fp(dataset_fname)
	voc = merge_tp_fp(tp, fp)
	methods = ['IG, BNS', 'F1', 'ODDS', 'CHI', 'DF']
	bns = []
	f1 = []
	ig = []
	odds = []
	chi = []
	df = []
	for word in voc:
		tp_v = 0
		fp_v = 0
		if word in tp:
			tp_v = tp[word]
		if word in fp:
			fp_v = fp[word]
		if tp_v !=0 and fp_v != 0:
			ig.append((word, information_gain(pos, neg, tp_v, fp_v)))						
			bns.append((word, BNS(pos, neg, tp_v, fp_v)))
			f1.append((word, F1(pos, neg, tp_v, fp_v)))
			odds.append((word, odds_ratio(pos, neg, tp_v, fp_v)))
			chi.append((word, chi_squared(pos, neg, tp_v, fp_v)))
			df.append((word, doc_frenquency(tp_v, fp_v)))				
			
	ig = sorted(ig, key=lambda s:s[1], reverse=True)		
	bns = sorted(bns, key=lambda s:s[1], reverse=True)
	f1 = sorted(f1, key=lambda s:s[1], reverse=True)
	odds = sorted(odds, key=lambda s:s[1], reverse=True)
	chi = sorted(chi, key=lambda s:s[1], reverse=True)
	df = sorted(df, key=lambda s:s[1], reverse=True)
	
	write_down_ranked_words(ig, 'food_ig_ranked_words.txt')
	write_down_ranked_words(bns, 'food_bns_ranked_words.txt')
	write_down_ranked_words(f1, 'food_f1_ranked_words.txt')
	write_down_ranked_words(odds, 'food_odds_ranked_words.txt')
	write_down_ranked_words(chi, 'food_chi_ranked_words.txt')
	write_down_ranked_words(df, 'food_df_ranked_words.txt')
		
	from help_tools import read_dict, build_reverse_dict
	my_dict = read_dict(dict_fname)
	reverse_dict = build_reverse_dict(my_dict)
	convert_ranked_words_to_term('food_ig_ranked_words.txt', 'food_ig_ranked_terms.txt', reverse_dict)
	convert_ranked_words_to_term('food_bns_ranked_words.txt', 'food_bns_ranked_terms.txt', reverse_dict)
	convert_ranked_words_to_term('food_f1_ranked_words.txt', 'food_f1_ranked_terms.txt', reverse_dict)
	convert_ranked_words_to_term('food_odds_ranked_words.txt', 'food_odds_ranked_terms.txt', reverse_dict)
	convert_ranked_words_to_term('food_chi_ranked_words.txt', 'food_chi_ranked_terms.txt', reverse_dict)
	convert_ranked_words_to_term('food_df_ranked_words.txt', 'food_df_ranked_terms.txt', reverse_dict)
