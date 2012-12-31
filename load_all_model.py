def load_models(folder, filepostfix):
	import os
	from liblinearutil import load_model
	files = os.listdir(folder)
	files.sort()
	models = {}
	for f in files:		
		if f.endswith(filepostfix):			
			print 'loading ' + f
			a = f.index('_')
			id = int(f[:a])			
			m = load_model(folder + '/' + f)
			models[id] = m
	return models

def load_idfs(folder, filepostfix):
	import os	
	files = os.listdir(folder)
	files.sort()
	idfs = {}
	for f in files:
		if f.endswith(filepostfix):
			print 'loading ' + f
			a = f.index('_')
			id = int(f[:a])	
			idf = {}
			fd = open(folder + '/' + f)
			for line in fd:
				line = line.strip().split(':')
				idf[int(line[0])] = float(line[1])
			fd.close()
			idfs[id] = idf
	return idfs
	
def load_feature_indices(folder, filepostfix):
	import os	
	files = os.listdir(folder)
	files.sort()
	features = {}
	for f in files:
		if f.endswith(filepostfix):
			print 'loading ' + f
			a = f.index('_')
			id = int(f[:a])	
			feature = {}
			fd = open(folder + '/' + f)
			for line in fd:
				line = line.strip().split(':')
				feature[int(line[0])] = int(line[1])
			fd.close()
			features[id] = feature
	return features

def load_idfs_as_list(folder, filepostfix):
	import os	
	files = os.listdir(folder)
	files.sort()
	idfs = {}
	for f in files:
		if f.endswith(filepostfix):
			print 'loading ' + f
			a = f.index('_')
			id = int(f[:a])	
			idf = []
			fd = open(folder + '/' + f)
			for line in fd:
				line = line.strip().split(':')
				idf.append((int(line[0]), float(line[1])))
			fd.close()
			idf.sort()
			idfs[id] = idf
	return idfs
	
def load_feature_indices_as_list(folder, filepostfix):
	import os	
	files = os.listdir(folder)
	files.sort()
	features = {}
	for f in files:
		if f.endswith(filepostfix):
			print 'loading ' + f
			a = f.index('_')
			id = int(f[:a])	
			feature = []
			fd = open(folder + '/' + f)
			for line in fd:
				line = line.strip().split(':')
				feature.append((int(line[0]), int(line[1])))
			fd.close()
			feature.sort()
			features[id] = feature
	return features
	
folder = '/home/xiao/dmoz_models/dmoz_multiclass_full_models'	
models = load_models(folder, 'model_dmoz_multiclass_full')
idfs = load_idfs_as_list(folder, 'idf_dmoz_multiclass_full')
features = load_feature_indices_as_list(folder, 'feature_indices_dmoz_multiclass_full')
