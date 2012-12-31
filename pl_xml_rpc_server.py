from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
from svm_server_util import extract_doc_id
from IPython.kernel import client
from time import time

#global variable for model
mec = None


dict_fname = '/home/mpi/dmoz_models/dictionary0102.txt'
stop_fname = 'new_english.stop'
idf_fname = 'food_idf.txt'

#base_model_file = '/home/xiao/liblinear-1.8/python/food_model'
#n_cats = 3
base_folder = '/home/mpi/see_all_models/'
base_model_file = 'model_SEE_0.2'
base_idf_file = 'idf_SEE_0.2'
base_local_dict_file = 'feature_indices_SEE_0.2'
base_model_para = 'model_SEE_0.2_addtional.txt'
n_cats = 662
cats = range(n_cats)

my_models = {}
my_cats = []
my_voc_maps = {}
my_idfs = {}
my_platts = {}

voc = {}
stop_words = {}
idf = {}
id2cat = {}
	
# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
	rpc_paths = ('/RPC2',)
	
# Register an instance; all the methods of the instance are
# published as XML-RPC methods
class SVMPrediction:
	#multi process classification		
	def get_category_name(self):		
		global id2cat		
		import simplejson as json		
		return json.dumps(id2cat)
		
	def get_categories(self):		
		return cats
	
	def predict_webpage_category_name_by_shrinked_features(self, id, cats, url):		
		global mec
		#download html
		from url_util import download_webpage
		html = download_webpage(url)
		
		mec['html'] = html		
		mec['predicted_cats'] = cats							
		mec.execute('from svm_server_util import from_html_to_svm_vector, multi_label_prediction_with_platts_calibration_feature_shrinkage')				
		mec.execute('svm_vector = from_html_to_svm_vector(html, voc, stop_words)')
		mec.execute('probs = multi_label_prediction_with_platts_calibration_feature_shrinkage(svm_vector, predicted_cats, my_voc_maps, my_idfs, my_models, my_platts, predict_param)')			
		all_probs = mec.gather('probs')		
									
		#merge request
		str_probs = ['"' + id2cat[str(prob[0])] + '":' + ('%.6f' % prob[1]) for prob in all_probs]	
		result = '{"id":' + str(id) + ', "probs":{'	+ ','.join(str_probs) + '}}'	
		print result		
		return result
			
	def predict_webpage_shrinked_features(self, id, cats, url):		
		global mec
		#download html
		from url_util import download_webpage
		html = download_webpage(url)
		
		mec['html'] = html		
		mec['predicted_cats'] = cats							
		mec.execute('from svm_server_util import from_html_to_svm_vector, multi_label_prediction_with_platts_calibration_feature_shrinkage')				
		mec.execute('svm_vector = from_html_to_svm_vector(html, voc, stop_words)')
		mec.execute('probs = multi_label_prediction_with_platts_calibration_feature_shrinkage(svm_vector, predicted_cats, my_voc_maps, my_idfs, my_models, my_platts, predict_param)')			
		all_probs = mec.gather('probs')		
									
		#merge request
		str_probs = ['"' + str(prob[0]) + '":' + ('%.6f' % prob[1]) for prob in all_probs]	
		result = '{"id":' + str(id) + ', "probs":{'	+ ','.join(str_probs) + '}}'	
		print result		
		return result
	
	def get_mode_A_B(self, cats):
		global mec
		mec['predicted_cats'] = cats
		mec.execute('from svm_server_util import get_multi_label_platts_model')
		mec.execute('modes, A, B = get_multi_label_platts_model(my_platts, predicted_cats)')		
		modes = mec.gather('modes')
		A = mec.gather('A')
		B = mec.gather('B')
		print modes, A, B
		return modes, A, B
			
	def predict_webpage_raw_shrinked_features(self, id, cats, str_svm_vector):		
		global mec
		#download html
		svm_vector = []
		terms = str_svm_vector.split(' ')
		for t in terms[1:]:
			wd, occ = t.split(':')
			svm_vector.append((int(wd), int(occ)))		
		mec['svm_vector'] = svm_vector		
		mec['predicted_cats'] = cats			
		mec.execute('from svm_server_util import  multi_label_prediction_with_feature_shrinkage')						
		mec.execute('probs = multi_label_prediction_with_feature_shrinkage(svm_vector, predicted_cats, my_voc_maps, my_idfs, my_models, my_platts, predict_param)')	
		all_probs = mec.gather('probs')
									
		#merge request
		str_probs = ['"' + str(prob[0]) + '":' + str(prob[1]) for prob in all_probs]	
		result = '{"id":' + str(id) + ', "probs":{'	+ ','.join(str_probs) + '}}'	
		print result		
		return result
	
	def predict_webpage_raw_shrinked_features_out_prob(self, id, cats, str_svm_vector):		
		global mec
		#download html
		svm_vector = []
		terms = str_svm_vector.split(' ')
		for t in terms[1:]:
			wd, occ = t.split(':')
			svm_vector.append((int(wd), int(occ)))		
		mec['svm_vector'] = svm_vector		
		mec['predicted_cats'] = cats			
		mec.execute('from svm_server_util import multi_label_prediction_with_platts_calibration_feature_shrinkage')				
		mec.execute('probs = multi_label_prediction_with_platts_calibration_feature_shrinkage(svm_vector, predicted_cats, my_voc_maps, my_idfs, my_models, my_platts, predict_param)')			
		all_probs = mec.gather('probs')
									
		#merge request
		str_probs = ['"' + str(prob[0]) + '":' + str(prob[1]) for prob in all_probs]	
		result = '{"id":' + str(id) + ', "probs":{'	+ ','.join(str_probs) + '}}'	
		print result		
		return result
			
	def predict_webpage_shrinked_features_debug(self, id, cats, url):		
		global voc, stop_words
		global my_voc_maps, my_idfs, my_models, my_platts
		#download html
		from url_util import download_webpage
		from svm_server_util import from_html_to_svm_vector, multi_label_prediction_with_platts_calibration_feature_shrinkage
		html = download_webpage(url)		
		svm_vector = from_html_to_svm_vector(html, voc, stop_words)		
		probs = multi_label_prediction_with_platts_calibration_feature_shrinkage(svm_vector, cats, my_voc_maps, my_idfs, my_models, my_platts, '')				
		#merge request
		str_probs = ['"' + str(prob[0]) + '":' + str(prob[1]) for prob in probs]	
		result = '{"id":' + str(id) + ', "probs":{'	+ ','.join(str_probs) + '}}'	
		print result		
		return result
			
	def predict_webpage_debug(self, id, cats, url):		
		#make svm features
		global voc, stop_words, idf
		from url_util import download_webpage, extract_content
		from svm_server_util import from_url_to_svm_feature
		svm_vector = from_url_to_svm_feature(url, voc, stop_words, idf)							
		#merge request
		request = str(id) + '_{' + ','.join(cats) + '}_' + svm_vector
		print request		
		return self.prediction_debug(request)		
		
	def prediction(self, doc):		
		from svm_server_util import extract_doc_id, extract_cats
		global n_cats, mec
		#extract id and cats
		id = extract_doc_id(doc)
		cats = extract_cats(doc, n_cats)		
		print 'classify ' + str(id)
		#do prediction
		mec['doc'] = doc
		mec['predicted_cats'] = cats		
		mec.execute('probs = multi_label_prediction(doc, predicted_cats, my_models)')		
		#gather results from slaves and merge them into a string
		probs = mec.gather('probs')				
		str_probs = ['"' + str(prob[0]) + '":' + str(prob[1]) for prob in probs]		
		result = '{"id":' + str(id) + ', "probs":{'		
		result += ','.join(str_probs)
		result += '}}'		
		return result
		
	def prediction_debug(self, doc):	
		global my_cats, my_models, n_cats
		from svm_server_util import multi_label_prediction, extract_cats
		print my_cats		
		id = extract_doc_id(doc)
		print 'classify ' + str(id)
		my_cats = extract_cats(doc, n_cats)		
		probs = multi_label_prediction(doc, my_cats, my_models)		
		#merge results as a string
		str_probs = ['"' + str(prob[0]) + '":' + str(prob[1]) for prob in probs]		
		result = '{"id":' + str(id) + ', "probs":{'		
		result += ','.join(str_probs)
		result += '}}'
		print result
		return result			
			


def init_models_debug(cats, base_model_file):
	#preload SVM model
	global my_cats, my_models
	from svm_server_util import multi_label_load_model	
	my_models = multi_label_load_model(cats, base_model_file)	
	print 'init slaves done'	

def init_helper(dict_fname, stop_fname, idf_fname):
	#load vocabulary, stop word list and idf table
	#These variables will be used to extract features
	global voc, stop_words, idf
	from help_tools import read_dict, read_stop_list, read_idf	
	voc = read_dict(dict_fname)
	stop_words = read_stop_list(stop_fname)
	idf = read_idf(idf_fname)
	
def init_multilabel_model_debug(cats):
	global voc, stop_words, my_models, my_voc_maps, my_idfs, my_cats, my_platts
	global base_model_file, base_idf_file, base_local_dict_file, base_model_para, stop_fname, dict_fname, base_folder
	from svm_server_util import multi_label_load_model, multi_label_load_idf, multi_label_load_feature_map, multi_label_load_platts_model
	from help_tools import read_stop_list, read_dict
	
	my_cats = cats	
	my_models = multi_label_load_model(my_cats, base_folder, base_model_file)	
	my_idfs = multi_label_load_idf(my_cats, base_folder, base_idf_file, ':')
	my_voc_maps = multi_label_load_feature_map(my_cats, base_folder, base_local_dict_file, ':')
	my_platts = multi_label_load_platts_model(my_cats, base_folder, base_model_para)
	
	stop_words = read_stop_list(stop_fname)
	voc = read_dict(dict_fname, ',')

def init_multilabel_models(cats):		
	#init library	
	global mec, base_model_file, base_folder, base_local_dict_file, base_idf_file, base_model_para
	global stop_fname, dict_fname
	global id2cat
	
	from help_tools import read_id_cat	
	id2cat = read_id_cat('uwo_id_cat_name')
		
	mec = client.MultiEngineClient()	
	mec.execute('import os')
	mec.execute('os.chdir("/home/mpi/query_search_project/")')	
	mec.execute('from svm_server_util import multi_label_load_model, multi_label_load_idf, multi_label_load_feature_map, multi_label_load_platts_model, multi_label_prediction')
	mec.execute('from help_tools import read_stop_list, read_dict')
	
	#init models
	#each machines load parts of the models	
	mec['base_model_file'] = base_model_file	
	mec['base_folder'] = base_folder
	mec['base_local_dict_file'] = base_local_dict_file
	mec['base_idf_file'] = base_idf_file
	mec['base_model_para'] = base_model_para
	mec['stop_fname'] = stop_fname
	mec['dict_fname'] = dict_fname
	mec['predict_param'] = ''
	mec.scatter('my_cats', cats)
	mec.execute('my_models = multi_label_load_model(my_cats, base_folder, base_model_file)')
	mec.execute('my_idfs = multi_label_load_idf(my_cats, base_folder, base_idf_file, ":")')
	mec.execute('my_voc_maps = multi_label_load_feature_map(my_cats, base_folder, base_local_dict_file, ":")')
	mec.execute('my_platts = multi_label_load_platts_model(my_cats, base_folder, base_model_para)')
	mec.execute('stop_words = read_stop_list(stop_fname)')
	mec.execute('voc = read_dict(dict_fname, ",")')	
	
def deubg():
	from url_util import download_webpage
	from svm_server_util import from_html_to_svm_vector, multi_label_prediction_with_feature_shrinkage
	from svm_server_util import multi_label_load_model, multi_label_load_idf, multi_label_load_feature_map, multi_label_load_platts_model, platts_calibration
	from help_tools import read_stop_list, read_dict
	
	url = 'http://dir.yahoo.com/Arts/'
	dict_fname = '/home/mpi/dmoz_models/dictionary0102.txt'
	stop_fname = 'new_english.stop'
	idf_fname = 'food_idf.txt'
	base_folder = '/home/xiao/dmoz_models/dmoz_multiclass_full_models/'
	base_model_file = 'model_dmoz_multiclass_full'
	base_idf_file = 'idf_dmoz_multiclass_full'
	base_local_dict_file = 'feature_indices_dmoz_multiclass_full'
	base_model_para = 'model_dmoz_multiclass_full_addtional.txt'
	n_cats = 5


	my_models = {}
	my_cats = []
	my_voc_maps = {}
	my_idfs = {}

	voc = {}

	stop_words = {}
	idf = {}
	
	cats = [0,1]
	my_cats = [0,1]	
	my_models = multi_label_load_model(my_cats, base_folder, base_model_file)	
	my_idfs = multi_label_load_idf(my_cats, base_folder, base_idf_file, ':')
	my_voc_maps = multi_label_load_feature_map(my_cats, base_folder, base_local_dict_file, ':')
	my_platts = multi_label_load_platts_model(my_cats, base_folder, base_model_para)
	
	stop_words = read_stop_list(stop_fname)
	voc = read_dict(dict_fname, ',')
	
	html = download_webpage(url)		
	svm_vector = from_html_to_svm_vector(html, voc, stop_words)
	print svm_vector
	#probs = multi_label_prediction_with_feature_shrinkage(svm_vector, cats, my_voc_maps, my_idfs, my_models, '')
	predict_param = ''
	from liblinearutil import predict
	from make_tf_idf import compute_tf_idf_by_vector
	probs = []
	for c in cats:
		if c in my_models:	
			print 'classify ' + str(c)
			#make tf idf
			tf_idf = compute_tf_idf_by_vector(svm_vector, my_idfs[c])
			print 'get', tf_idf
			#make SVM feature
			features = {}
			for wd in tf_idf:
				features[wd[0]] = wd[0]
			p_label, p_acc, p_val = predict([1], [features], my_models[c], predict_param)		
			calibrated_prob = platts_calibration(p_val[0][0], my_platts[c][0], my_platts[c][1], my_platts[c][2])
			probs.append((c, calibrated_prob))		
			
	print probs					
	#merge request
	str_probs = ['"' + str(prob[0]) + '":' + str(prob[1]) for prob in probs]	
	result = '{"id":' + str(id) + ', "probs":{'	+ ','.join(str_probs) + '}}'
	print sum([features[i+1] * my_models[0].w[i] for i in range(my_models[0].nr_feature) if (i+1) in features])	
	
if __name__ == '__main__': 	
	#init helper	
	#init_helper(dict_fname, stop_fname, idf_fname)	
		
	#init models		
	#init_models_debug(range(n_cats), base_model_file)
	#deubg()
	
	#init_multilabel_model_debug(range(21))	
	#cats = range(n_cats)
	#cats =  [0, 85, 157, 224, 275, 304, 349, 369, 466, 564, 627]
	init_multilabel_models(cats)
	#init_multilabel_models(range(500,540))
	
	# Create server
	server = SimpleXMLRPCServer(("localhost", 8000), requestHandler=RequestHandler)
	server.register_introspection_functions()
	
	#register functions
	server.register_instance(SVMPrediction())

	# Run the server's main loop
	server.serve_forever()
