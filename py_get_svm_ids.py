infname = '/home/mpi/uwo_query_bing_workingspace/uwo_query_bing_id_svm.txt'
outfname = '/home/mpi/uwo_query_bing_workingspace/uwo_query_bing_test_ids.txt'
fd = open(infname)
fd_w = open(outfname, 'w')
for line in fd:
	a = line.index(' ')
	fd_w.write(line[:a] + '\n')
fd_w.close()
fd.close()
