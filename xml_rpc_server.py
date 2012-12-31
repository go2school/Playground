from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
from svm_server_util import load_model, extract_content

#global variable for model
svm_models = {}
base_model_file = '/home/xiao/liblinear-1.8/python/heart_scale.model'
base_model_file = '/home/xiao/liblinear-1.8/python/food_model'
#n_cats = 3
n_cats = 1

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
	rpc_paths = ('/RPC2',)
	
# Register an instance; all the methods of the instance are
# published as XML-RPC methods
class SVMPrediction:
	def prediction(self, doc):
		from liblinearutil import predict
		id, cats, features = extract_content(doc, n_cats)
		print 'classify ' + str(id)
		probs = []
		for c in cats:
			p_label, p_acc, p_val = predict([1], [features], svm_models[c], '-b 1')
			probs.append((c, p_val[0][0]))						
		str_probs = ['"' + str(prob[0]) + '":' + str(prob[1]) for prob in probs]
		result = '{"id":' + str(id) + ', "probs":{'		
		result += ','.join(str_probs)
		result += '}}'
		return result				
		
			
if __name__ == '__main__': 
	for i in range(n_cats):
		model = load_model(base_model_file + '_' + str(i))	
		svm_models[i] = model
	
	# Create server
	server = SimpleXMLRPCServer(("localhost", 8000), requestHandler=RequestHandler)
	server.register_introspection_functions()
	
	#register functions
	server.register_instance(SVMPrediction())

	# Run the server's main loop
	server.serve_forever()
