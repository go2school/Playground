def write_down_stat(infname ,outfname):
	fd = open(infname)
	fd_w = open(outfname, 'w')
	for line in fd:
		line = line.strip().split(' ')
		id = int(line[0])
		dlen = len(line[1:])	
		fd_w.write(str(id) + ' ' +str(dlen) + '\n')
	fd.close()
	fd_w.close()

def read_stats(fname):
	doc_len = []
	fd = open(fname)
	fd.close()

if __name__ == '__main__': 
	infname = '/home/mpi/uwo_query_bing_workingspace/uwo_query_bing_id_svm.txt'
	outfname = 'uwo_query_bing_id_doc_length.txt'
	write_down_stat(infname, outfname)
