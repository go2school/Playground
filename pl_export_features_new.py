from IPython.kernel import client
from db_util import get_max_id
from help_tools import chunks
from time import time

fname_stop = 'new_english.stop'
fname_dict = 'new_uwo_dict'
feature_fname = 'new_uwo_features'
local_trunk_size = 10000

mec = client.MultiEngineClient()

#prepaer lib
mec.execute('import os')
mec.execute('os.chdir("/media/01CC16F5ED7072F0/seeuwo/query_bing")')
mec.execute('from help_tools import read_stop_list, read_dict')
mec.execute('from pl_routin import do_job_adv_new')

#prepare para
mec['fname_stop'] = fname_stop
mec['fname_dict'] = fname_dict
mec['feature_fname'] = feature_fname
mec['local_trunk_size'] = local_trunk_size

#read dictionary and stop words
mec.execute('vocabulary = read_dict(fname_dict)')
mec.execute('stop_sets = read_stop_list(fname_stop)')

#make ids
ids = mec.get_ids()
mec.scatter('my_id', ids)

#make trunks
max_id = get_max_id('uwo.webs')
global_ids = range(max_id)
mec.scatter('my_trunk', global_ids)

#do jobs
start = time()
print 'start extracting features '
mec.execute('do_job_adv_new(feature_fname + "_" + str(my_id[0]), my_trunk, local_trunk_size, stop_sets, vocabulary)')
print 'finish extracting features '
end = time()
print 'Finish tasks in ' + str(int(end - start)) + ' seconds'

#merge files
fd_w = open(feature_fname, 'w')
for id in mec.get_ids():
	fd = open(feature_fname + '_' + str(id))
	for line in fd:
		line = line.strip()
		fd_w.write(line + '\n')
	fd.close()
fd_w.close()
