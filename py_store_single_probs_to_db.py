def read_id_list(fname):
	id_list = []
	fd = open(fname)
	for line in fd:
		id_list.append(line.strip())
	fd.close()
	return id_list
	
def uwo_to_db():
	svm_id_list_file = 'uwo_new_svm_ids.txt'
	in_folder = '/home/xiao/uwo_parameterized_prediction/'
	#in_file = 'uwo_new_results.txt'
	#table = 'uwo_new_prediction_2'
	in_file = 'uwo_new_results_with_reference_and_other_pos_2_and_spanning.txt'
	table = 'uwo_new_prediction_3'

	svm_id_list = read_id_list(svm_id_list_file)
	fd = open(in_folder + in_file)
	import MySQLdb
	con   =   MySQLdb.connect(host="192.168.0.2",  port=3306, user="root",  passwd="see",  db="uwo")  
	cursor   =   con.cursor() 
	for id in svm_id_list:
		line = fd.readline().strip()
		sql = 'insert into ' + table + ' values (' + str(id) + ', "' + line + '")'	
		cursor.execute(sql)
	#cursor.execute('delete from uwo_new_prediction_3 where id >= 0')
	con.commit()
	cursor.close()
	con.close()
	fd.close()

def clue_to_db():
	svm_id_list_file = '/home/mpi/clueweb09_id.csv'
	in_folder = '/home/xiao/clueweb09_merged_prediction/'
	in_file = 'clueweb09_merged_probability.txt'
	table = 'predictions'
	
	
	svm_id_list = read_id_list(svm_id_list_file)
	fd = open(in_folder + in_file)
	import MySQLdb
	con   =   MySQLdb.connect(host="192.168.0.2",  port=3306, user="root",  passwd="see",  db="clueweb09")  
	cursor   =   con.cursor() 
	for id in svm_id_list:
		line = fd.readline().strip()
		sql = 'insert into ' + table + ' values ("' + str(id) + '", "' + line + '")'	
		cursor.execute(sql)
	con.commit()
	cursor.close()
	con.close()
	fd.close()


def usage():
	print 'cmd --schema <schema> '
	
if __name__ == '__main__':
	import sys, getopt
	import subprocess
	opts, args = getopt.getopt(sys.argv[1:], 'x', ['schema='])	
	global_trunk_size = 50000
	work_folder = '/home/mpi/url_reorganization'	
	schema = ''	
	doc_table = 'new_nutch_docs'		
	for o, a in opts:
		if o == "--schema":
			schema = a				
	if schema == '':
		print usage()
		sys.exit(1)		
		
	svm_id_list_file = '/home/mpi/shareddir/seeuwo/' + schema + '_query_bing_prediction/doc_ids'
	in_folder = '/home/mpi/shareddir/seeuwo/merged_prediction'
	in_file_ext = schema + '_query_bing_merged_probability.txt'	
	table = 'new_prediction'
	
	svm_id_list = read_id_list(svm_id_list_file)	
	fd = open(in_folder + '/' + in_file_ext)
	import MySQLdb
	con   =   MySQLdb.connect(host="192.168.0.2",  port=3306, user="root",  passwd="see",  db="uwo")  
	cursor   =   con.cursor() 
	for id in svm_id_list:
		line = fd.readline().strip()
		sql = 'insert into ' + schema + '.' + table + ' values (' + str(id) + ', "' + line + '")'	
		#sql = 'update ' + schema + '.' + table + ' set prediction="'+line + '" where id=' + str(id)	
		cursor.execute(sql)	
	con.commit()
	cursor.close()
	con.close()
	fd.close()
