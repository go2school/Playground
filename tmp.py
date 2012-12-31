len_lst = {}
for l in labels:
	if l[1] not in len_lst:
		len_lst[l[1]] = [l[0]]
	else:
		len_lst[l[1]].append(l[0])
