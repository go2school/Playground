def multi_label_load_model(my_cats, base_model_fname):
	svm_models = {}
	from liblinearutil import load_model
	for c in my_cats:		
		model = load_model(base_model_fname + '_' + str(c))	  
		svm_models[c] = model
	return svm_models
	
def multi_label_prediction(doc, n_cats, my_cats, svm_models):
	from liblinearutil import predict	
	from svm_server_util import extract_content
	#extract id, categories and features
	id, cats, features = extract_content(doc, n_cats)	
	probs = []
	print id, cats, features
	for c in my_cats:
		p_label, p_acc, p_val = predict([1], [features], svm_models[c], '-b 1')
		probs.append((c, p_val[0][0]))							
	return probs
