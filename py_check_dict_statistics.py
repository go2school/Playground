from help_tools import *

if __name__ == '__main__': 	
	dict_fname = '/home/mpi/query_bing_project/query_bing_rare_removed_3.txt'
	whole_dict = read_dict_query_bing_freq(dict_fname, ' ')
	#sort by occ
	words = [(w, whole_dict[w][0], whole_dict[w][1]) for w in whole_dict]
	words = sorted(words, key = lambda s:s[2], reverse=True)
