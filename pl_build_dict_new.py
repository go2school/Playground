from IPython.kernel import client
from db_util import get_max_id
from time import time

fname_stop = 'new_english.stop'
fname_dict = 'new_uwo_dict'
fname_freq = 'new_uwo_freq'
local_trunk_size = 10000
fname_voc_2_stem = 'new_uwo_voc_to_stem'
fname_stem_2_voc = 'new_uwo_stem_to_voc'
	
mec = client.MultiEngineClient()
mec.execute('import os')
mec.execute('os.chdir("/media/01CC16F5ED7072F0/seeuwo/query_bing")')

#prepaer lib
mec.execute('from build_dict_and_stem_map_new import pl_build_term_freq_list_new')
mec.execute('from help_tools import read_stop_list, write_dict, write_term_freq, write_voc_2_stem')

#prepare para
mec['local_trunk_size'] = local_trunk_size
mec['fname_stop'] = fname_stop
mec['fname_dict'] = fname_dict
mec['fname_freq'] = fname_freq
mec['fname_voc_2_stem'] = fname_voc_2_stem
mec['fname_stem_2_voc'] = fname_stem_2_voc

#make data list
max_id = get_max_id('uwo.webs')
#max_id = 5000
global_ids = range(max_id)
mec.scatter('my_trunk', global_ids)

#prepare engine IDs
ids = mec.get_ids()
mec.scatter('my_id', ids)

#prepare output data
mec.execute('fname_dict = fname_dict + "_" + str(my_id[0])')
mec.execute('fname_freq = fname_freq + "_" + str(my_id[0])')
mec.execute('fname_voc_2_stem = fname_voc_2_stem + "_" + str(my_id[0])')
mec.execute('fname_stem_2_voc = fname_stem_2_voc + "_" + str(my_id[0])')

start = time()
print 'start extracting dict in total ' + str(len(global_ids))
#read stop words
mec.execute('stop_sets = read_stop_list(fname_stop)')
#begin making dictionary
mec.execute('term_freqs, voc2stem, stem2voc = pl_build_term_freq_list_new(my_trunk, local_trunk_size, stop_sets)')
mec.execute('write_dict(term_freqs, fname_dict)')
mec.execute('write_term_freq(term_freqs, fname_freq)')
mec.execute('write_voc_2_stem(voc2stem, stem2voc, fname_voc_2_stem, fname_stem_2_voc)')
end = time()
print 'Finish extracting dict in ' + str(int(end - start)) + ' seconds'
