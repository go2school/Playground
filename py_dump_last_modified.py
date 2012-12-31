def dump_last_modified(schema, table, outfname):
	import   MySQLdb  	
	con   =   MySQLdb.connect(host="192.168.0.2",  port=3306, user="root",  passwd="see",  db=schema)  
	cursor   =   con.cursor() 
	sql = 'select * from ' + schema + '.' + table + ' order by id asc'
	cursor.execute(sql)
	fd_w = open(outfname, 'w')
	while True:
		row = cursor.fetchone()
		if row != None:
			fd_w.write(str(row[0]) + ' ' + str(row[1]) + '\n')
		else:
			break
	cursor.close()
	con.close()	
	fd_w.close()

def read_empty_last_modified(fname):
	ids = []
	fd = open(fname)
	for line in fd:
		line = line.strip().split(' ')		
		if len(line) == 1:
			ids.append(line[0])
	fd.close()
	return ids

def update_date_to_db(fname, schema, table):
	import   MySQLdb  	
	con   =   MySQLdb.connect(host="192.168.0.2",  port=3306, user="root",  passwd="see",  db=schema)  
	cursor   =   con.cursor() 	
	fd = open(fname)
	for line in fd:
		line = line.strip().split(' ')
		sid = line[0]
		date = line[1]
		sql = 'update ' + schema + '.' + table + ' set last_modified="' + date + '" where id=' + sid
		cursor.execute(sql)
	cursor.close()
	con.close()	
	fd.close()

def change_last_mofidiefd(outfname, changed_empty_last_modified_fname):	
	ids = read_empty_last_modified(outfname)
	nids = [int(id) for id in ids]
	nids.sort()
	str_date = '2012-03-10T20:35:12Z'
	month = range(1,4)
	day = range(1, 20)
	hour = range(24)
	mins = range(60)
	seconds = range(60)
	#randomly sample date
	import random
	fd = open(changed_empty_last_modified_fname, 'w')
	for id in nids:
		smo = random.sample(month, 1)
		sd = random.sample(day, 1)
		sh = random.sample(hour, 1)
		sm = random.sample(mins, 1)
		ss = random.sample(seconds, 1)
		str_random_date = '2012-%02d-%02dT%02d:%02d:%02dZ' % (smo[0], sd[0], sh[0], sm[0], ss[0])
		fd.write(str(id) + ' ' + str_random_date + '\n')
	fd.close()
		
if __name__ == '__main__':
	schema = 'uwo'
	table = 'uwo_new_nutch_docs_last_modified'
	outfname = 'uwo_id_last_modified_list.txt'
	empty_last_modified_fname = 'uwo_id_empty_lastmodified_list.txt'
	changed_empty_last_modified_fname = 'uwo_changed_id_empty_lastmodified_list.txt'
	#dump_last_modified(schema, table, outfname)
	change_last_mofidiefd(outfname, changed_empty_last_modified_fname)
	update_date_to_db(changed_empty_last_modified_fname, schema, table)
	
