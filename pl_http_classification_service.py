from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
from svm_server_util import extract_doc_id
from IPython.parallel import Client
from time import time
import BaseHTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from threading import Lock
import urllib
#global variable for model
mec = None
root = None
rc = None
#end global variables for model

#synchronized variable
lock = None

dict_fname = 'see_dmoz_dictionary0102.txt'
stop_fname = 'new_english.stop'
idf_fname = 'food_idf.txt'

#base_model_file = '/home/xiao/liblinear-1.8/python/food_model'
#n_cats = 3

base_folder = '/home/mpi/see_all_models/'
base_prob_estimation_folder = '/home/mpi/SEE_Probability_Estimation/pav_model'
base_prob_estimation_choice_file = '/home/mpi/SEE_Probability_Estimation/best_parameter.txt'
"""
base_folder = '/home/xiao/see_all_models/'
base_prob_estimation_folder = '/home/xiao/SEE_Probability_Estimation/pav_model'
base_prob_estimation_choice_file = '/home/xiao/SEE_Probability_Estimation/best_parameter.txt'
"""
base_model_file = 'model_SEE_0.2'
base_idf_file = 'idf_SEE_0.2'
base_local_dict_file = 'feature_indices_SEE_0.2'
base_model_para = 'model_SEE_0.2_addtional.txt'
base_pav_model_ext = 'SEE_0.2_pav_model'
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

#global variable to clear MultiEngineClient trash
N_mec = 0
N_mecClearSize = 5000

def print_HTML_tree_view(my_str_output, node, all_nodes, format_type, id2cat):
	#get how many nodes under current node
	m = 0
	for c in node.children:
		if c.labelIndex in all_nodes:
			m += 1
	if m != 0:
		my_str_output['str'] += '<ul>'
	for c in node.children:
		if c.labelIndex in all_nodes:			
			if format_type == 'name':
				my_str_output['str'] += '<li>' + id2cat[str(c.labelIndex)] + ' ' + all_nodes[c.labelIndex]
			else:
				my_str_output['str'] += '<li>' + str(c.labelIndex) + ' ' + all_nodes[c.labelIndex]
			print_HTML_tree_view(my_str_output, c, all_nodes, format_type, id2cat)
			my_str_output['str'] += '</li>'			
	if m != 0:
		my_str_output['str'] += '</ul>'
			
# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
	rpc_paths = ('/RPC2',)
	
# Register an instance; all the methods of the instance are
# published as XML-RPC methods
class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):	
	def do_OPTIONS(self):			
		self.send_response(200, "ok")		
		self.send_header('Access-Control-Allow-Origin', '*')				
		self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
		self.send_header("Access-Control-Allow-Headers", "X-Requested-With")		
		
	def do_GET(self):				
		global mec
		global root
		global id2cat
		global N_mec
		global lock
		global rc
		
		#faf flat classificaiton, all result, flat view
		#fff flat classificaiton, filtered result, flat view
		#fat flat classificaiton, all result, tree view
		#hft hierarchical classification, filtered result, tree view
		#hff hierarchical classification, filtered result, flat view		
		
		#output all probability
		#v = '/?id=0&m=sfsdfs&th=0.5&tt=department&bd=text&url=http%3A%2F%2Fwww.google.ca%2Fsearch%3Fgcx%3Dw%26sourceid%3Dchrome%26'		
		if self.path.find('?') > -1:						
			print self.path
			#parse parameters
			params= self.path[2:].split('&')
						
			dict_params = {}
			for p in params:
				a,b=p.split('=')
				dict_params[a] = b
			#parse uid, method, threshold and requested url
			uid = '0'
			method = ''
			threshold = ''
			url = ''
			title = ''
			body = ''
			format_type = 'name'
			body_text_fname = ''			
			if 'id' in dict_params:
				uid = dict_params['id']
			if 'm' in dict_params:
				method = dict_params['m']
			if 'th' in dict_params:
				threshold = dict_params['th']
			if 'tt' in dict_params:#if title is served
				title = dict_params['tt']				
				title = urllib.unquote(title)
			if 'bd' in dict_params:
				body = dict_params['bd']			
				body = urllib.unquote(body)
			if 'url' in dict_params:
				url = dict_params['url']										
				url = urllib.unquote(url)
			if 'ft'	in dict_params:#if file format is served
				format_type = dict_params['ft']	
			if 'fn'	in dict_params:#if local file name is served
				body_text_fname = dict_params['fn']	
				body_text_fname = urllib.unquote(body_text_fname)	
				
			print dict_params
			
			start_job = time()
			
			result = ''
			
			#start download
			bad_request = False
			html = ''
			#if this is a bad parameter
			start_download = time()
			if not (url != '' or body != '' or body_text_fname != ''):
				bad_request = True
			else:											
				#if user does not give body 
				if body == '':
					if body_text_fname == '':#and he/she does not give me body file name, we need to download it
						from url_util import download_webpage
						html = download_webpage(url)
						print 'HTML length is ' + str(len(html))			
						if len(html) >= 500:
							print html[:500]							
						if len(html) == 0:
							bad_request = True
					else:
						#read body from file
						try:
							fd = open(body_text_fname)
							body = fd.read()
							fd.close()											
						except Exception:
							bad_request = True
			end_download = time()
			if bad_request == True:
				result = '{"id":' + str(-1) + '}'								
			else:						
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
			
				#parse text
				start_classification = time()
				
				try:	
					#synchronization			
					#synchronization			
					#synchronization			
					lock.acquire()
					
					#fif use does not give body, we need to parse raw html
					if body == '':					
						mec[var_html] = html									
						mec.execute('from svm_server_util import from_html_to_svm_vector, multi_label_prediction_with_platts_calibration_feature_shrinkage, multi_label_prediction_with_platts_pav_calibration_feature_shrinkage')																			
						mec.execute(var_svm_vector + ' = from_html_to_svm_vector(' + var_html + ', voc, stop_words)')
					else:#other wise, we just extract text
						mec[var_title] = title
						mec[var_body] = body				
						mec.execute('from svm_server_util import from_title_body_to_svm_vector, multi_label_prediction_with_platts_calibration_feature_shrinkage, multi_label_prediction_with_platts_pav_calibration_feature_shrinkage')																			
						mec.execute(var_svm_vector + ' = from_title_body_to_svm_vector(' + var_title + ', ' +var_body+ ', voc, stop_words)')
					
					#do classification
					mec[var_predicted_cats] = cats		
					#mec.execute(var_probs + ', ' + var_svm_len + ' = multi_label_prediction_with_platts_calibration_feature_shrinkage('+var_svm_vector+', '+var_predicted_cats+', my_voc_maps, my_idfs, my_models, my_platts, predict_param)')			
					mec.execute(var_probs + ', ' + var_svm_len + ' = multi_label_prediction_with_platts_pav_calibration_feature_shrinkage('+var_svm_vector+', '+var_predicted_cats+', my_voc_maps, my_idfs, my_models, my_prob_model_choice, my_platts, my_pav_models, predict_param)')											
					all_probs = mec.gather(var_probs)			
					#check svm vector length	
					svm_length = mec.gather(var_svm_len)	
					ls = [l[1] for l in svm_length]		
					print 'svm vector length ', min(ls), max(ls), float(sum(ls))/len(ls)
					
					#clear working variables
					mec[var_html] = None
					mec[var_predicted_cats] = None
					mec[var_title] = None
					mec[var_body] = None
					mec[var_probs] = None
					mec[var_svm_len] = None
					
					end_classification = time()
					
					#synchronization			
					#synchronization			
					#synchronization							
				
					N_mec += 1
					if N_mec > N_mecClearSize:								
						N_mec = 0
						#clear IPyton ipcontroller objects
						rc.purge_results('all')					
						mec.results.clear()
						rc.results.clear()
						rc.metadata.clear()
				
				except:
					bad_request= True
					result = '{"id":' + str(-1) + '}'
				finally:
					lock.release()
				
				if bad_request == False:						
					print 'Finishing classification in ' + ('%.3f' % (end_classification - start_classification)) + 'seconds'	
									
					optional_field = '"time_download":' + ('%.6f' % (end_download - start_download)) + ', "time_classification":' + ('%.6f' % (end_classification - start_classification))
						
					start_merge_result = time()
						
					#merge result
					if method == 'faf':
						if format_type == 'name':
							str_probs = ['"' + id2cat[str(prob[0])] + '":' + ('%.6f' % prob[1]) for prob in all_probs]	
						else:
							str_probs = ['"' + str(prob[0]) + '":' + ('%.6f' % prob[1]) for prob in all_probs]	
						result = '{"id":' + uid + ', "probs":{'	+ ','.join(str_probs) + '}, ' + optional_field +'}'	
					elif method == 'fff':
						#filtering results by threshold
						threshold = float(threshold)
						predict_labels = set()
						for p in all_probs:
							if p[1] >= threshold:
								predict_labels.add(p[0])											
						#merge request
						if format_type == 'name':
							str_probs = ['"' + id2cat[str(prob[0])] + '":' + ('%.6f' % prob[1]) for prob in all_probs if prob[0] in predict_labels]	
						else:
							str_probs = ['"' + str(prob[0]) + '":' + ('%.6f' % prob[1]) for prob in all_probs if prob[0] in predict_labels]	
						result = '{"id":' + uid + ', "probs":{'	+ ','.join(str_probs) + '}, ' + optional_field +'}'	
					elif method == 'fat':
						#merge request
						dict_all_probs = {}
						for prob in all_probs:				
							dict_all_probs[prob[0]] = '%.6f' % prob[1]
								
						#make tree view
						my_str_output = {'str':''}
						print_HTML_tree_view(my_str_output, root, dict_all_probs, format_type, id2cat)
									
						result = '{"id":' + uid + ', "content": "'  + my_str_output['str'] + '", ' + optional_field +'}'
					elif method == 'hff':
						#filtering results by threshold
						threshold = float(threshold)
						predict_labels = set()
						for p in all_probs:
							if p[1] >= threshold:
								predict_labels.add(p[0])
						out_set = set()
						root.filter_result_labels(predict_labels, out_set)							
						predict_labels = out_set
													
						#merge request
						if format_type == 'name':
							str_probs = ['"' + id2cat[str(prob[0])] + '":' + ('%.6f' % prob[1]) for prob in all_probs if prob[0] in predict_labels]	
						else:
							str_probs = ['"' + str(prob[0]) + '":' + ('%.6f' % prob[1]) for prob in all_probs if prob[0] in predict_labels]	
						result = '{"id":' + uid + ', "probs":{'	+ ','.join(str_probs) + '}, ' + optional_field +'}'
					elif method == 'hft':
						#filtering results by threshold
						threshold = float(threshold)
						predict_labels = set()
						for p in all_probs:
							if p[1] >= threshold:
								predict_labels.add(p[0])
						out_set = set()
						root.filter_result_labels(predict_labels, out_set)							
						predict_labels = out_set
													
						#merge request
						dict_all_probs = {}
						for prob in all_probs:
							if prob[0] in predict_labels:
								dict_all_probs[prob[0]] = '%.6f' % prob[1]
								
						#make tree view
						my_str_output = {'str':''}
						print_HTML_tree_view(my_str_output, root, dict_all_probs, format_type, id2cat)
						
						result = '{"id":' + uid + ', "content": "'  + my_str_output['str'] + '", ' + optional_field +'}'
					end_merge_result = time()
					print 'Finishing mergering in ' + ('%.3f' % (end_merge_result - start_merge_result)) + 'seconds'											
							
			self.send_response(200)
			self.send_header('Content-Type', 'text/javascript')
			self.send_header('Access-Control-Allow-Origin', '*')
			self.send_header('Content-Length', len(result))
			self.send_header('Expires', '-1')
			self.send_header('Cache-Control', 'no-cache')
			self.send_header('Pragma', 'no-cache')
			self.end_headers()

			self.wfile.write(result)		
			self.wfile.flush()
			#self.connection.shutdown(1)							
			
			end_job = time()
			
			#print result
			print 'Finishing job in ' + ('%.3f' % (end_job - start_job)) + 'seconds'
							
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
		mec.execute('from svm_server_util import from_html_to_svm_vector, multi_label_prediction_with_platts_calibration_feature_shrinkage, multi_label_prediction_with_platts_pav_calibration_feature_shrinkage')				
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
			

def init_multilabel_models(cats):		
	#init library	
	#with global variables
	global mec, base_model_file, base_folder, base_local_dict_file, base_idf_file, base_model_para, base_prob_estimation_choice_file, base_prob_estimation_folder
	global stop_fname, dict_fname
	global id2cat
	global root
	global lock
	global rc
	
	from help_tools import read_id_cat			
	from active_learning import Node		
	
	#read hierarchy
	hier = 'dmoz_hierarchy.txt'
	root = Node().read_tree(hier)

	
	id2cat = read_id_cat('uwo_id_cat_name')
	
	rc = Client()	
	mec = rc[:]
	mec.block = True
	mec.execute('import os')
	mec.execute('os.chdir("/home/mpi/query_search_project/")')	
	#mec.execute('os.chdir("/media/01CC16F5ED7072F0/seeuwo/query_bing")')	
	mec.execute('from svm_server_util import multi_label_load_model, multi_label_load_idf, multi_label_load_feature_map, multi_label_load_platts_model, multi_label_prediction')
	mec.execute('from help_tools import read_stop_list, read_dict')
	mec.execute('from see_probability_estimation import read_model_choice, read_pav_parameters_by_ids')
	
	#create lock variable
	lock = Lock()
	
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
	mec['base_prob_estimation_folder'] = base_prob_estimation_folder
	mec['base_prob_estimation_choice_file'] = base_prob_estimation_choice_file
	mec['base_pav_model_ext'] = base_pav_model_ext
	mec.scatter('my_cats', cats)
	mec.execute('my_models = multi_label_load_model(my_cats, base_folder, base_model_file)')
	mec.execute('my_idfs = multi_label_load_idf(my_cats, base_folder, base_idf_file, ":")')
	mec.execute('my_voc_maps = multi_label_load_feature_map(my_cats, base_folder, base_local_dict_file, ":")')
	mec.execute('my_platts = multi_label_load_platts_model(my_cats, base_folder, base_model_para)')
	mec.execute('stop_words = read_stop_list(stop_fname)')
	mec.execute('voc = read_dict(dict_fname, ",")')	
	#read probability choice
	#added by xiao 01242012
	mec.execute('my_prob_model_choice = read_model_choice(base_prob_estimation_choice_file)')
	mec.execute('my_pav_models = read_pav_parameters_by_ids(my_cats, base_prob_estimation_folder, base_pav_model_ext)')
	
if __name__ == '__main__': 		
	#init_multilabel_model_debug(range(21))	
	#cats = range(n_cats)
	#cats =  [0, 85, 157, 224, 275, 304, 349, 369, 466, 564, 627]
	init_multilabel_models(cats)	
	
	# Create server
	bhs = BaseHTTPServer.HTTPServer(('', 8000), MyHandler)
	bhs.serve_forever()
	
	"""
	server = SimpleXMLRPCServer(("localhost", 8000), requestHandler=RequestHandler)
	server.register_introspection_functions()
	
	#register functions
	server.register_instance(SVMPrediction())

	# Run the server's main loop
	server.serve_forever()
	"""
