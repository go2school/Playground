from IPython.kernel import client
from db_util import get_max_id
from help_tools import chunks
from time import time

fname_stop = 'new_english.stop'
fname_dict = 'uwo_dict'
feature_fname = 'uwo_features.txt'
global_trunks = 50000
local_trunk_size = 10000

mec = client.MultiEngineClient()
mec.execute('import os')
mec.execute('os.chdir("/media/01CC16F5ED7072F0/seeuwo/query_bing")')
#prepaer lib
mec.execute('from help_tools import read_stop_list, read_dict, read_stem_to_words')
mec.execute('from time import time')
mec.execute('from help_tools import chunks')
mec.execute('from db_util import get_docs_between')
mec.execute('from build_dict_and_stem_map import extract_doc_features')
mec.execute('from pl_routin import do_jobs')

#prepare para
mec['fname_stop'] = fname_stop
mec['fname_dict'] = fname_dict
mec['feature_fname'] = feature_fname
mec['local_trunk_size'] = local_trunk_size
#read dictionary and stop words
mec.execute('vocabulary = read_dict(fname_dict)')
mec.execute('stop_sets = read_stop_list(fname_stop)')
ids = mec.get_ids()
mec.scatter('my_id', ids)
#make result files
mec.execute('fd = open("features_" + str(my_id[0]) + ".txt", "w")')
start = time()
#make trunks
max_id = get_max_id('uwo.webs')
global_ids = range(max_id)
global_trunks = chunks(global_ids, global_trunks)
tot_trunks = len(global_trunks)
#do jobs
for global_trunk in global_trunks:
	start_id = global_trunk[0]
	end_id = global_trunk[len(global_trunk) - 1]
	print 'start extracting features from ' + str(start_id) + ' to ' + str(end_id)
	mec.scatter('my_trunk', global_trunk)
	mec.execute('do_jobs(fd, my_trunk, local_trunk_size, stop_sets, vocabulary)')
	"""
	#for debug
	from pl_routin import do_jobs
	from help_tools import read_stop_list, read_dict
	vocabulary = read_dict(fname_dict)
	stop_sets = read_stop_list(fname_stop)
	do_jobs(0, global_trunk, local_trunk_size, stop_sets, vocabulary)
	"""
	print 'finish extracting features from ' + str(start_id) + ' to ' + str(end_id)
	tot_trunks -= 1
	print str(tot_trunks) + ' remained'		
end = time()
mec.execute('fd.close()')
print 'Finish tasks in ' + str(int(end - start)) + ' seconds'
