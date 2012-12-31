fd = open(fname, 'w')
for k in ks:
	fd.write(k)
	for v in stem_dict[k]:
		fd.write(' ' + v)
	fd.write('\n')
fd.close()
