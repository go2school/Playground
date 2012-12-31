def read_id_list(fname):
	id_list = []
	fd = open(fname)
	for line in fd:
		id_list.append(line.strip().split(' ')[0])
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


if __name__ == '__main__':
	svm_id_list_file = 'westernmustangs_svm_ids.txt'
	in_folder = '/home/xiao/mustangs_merged/'
	#in_file = 'uwo_new_results.txt'
	#table = 'uwo_new_prediction_2'
	in_file = 'mustangs_new_results_with_reference_and_other_pos_2_and_spanning.txt'
	table = 'uwo_new_prediction_3'

	svm_id_list_file = 'uwo_to_do_ids.txt'
	in_folder = '/home/xiao/uwo_to_do_merged/'
	#in_file = 'uwo_new_results.txt'
	#table = 'uwo_new_prediction_2'
	in_file = 'uwo_to_do_new_results.txt'
	table = 'uwo_new_prediction_3'
		
	svm_id_list_file = '/home/mpi/uwo_query_bing_workingspace/uwo_query_bing_test_ids.txt'
	in_folder = '/home/mpi/uwo_query_bing_merged_parameter_prediction'	
	in_file = 'query_bing_new_results_with_reference_and_other_pos_2_and_spanning_depth_2_limit.txt'
	table = 'uwo_new_prediction_5'
	
	#make id list
	infname = '/home/mpi/uwo_query_bing_workingspace/uwo_query_bing_id_svm.txt'
	fd = open(infname)
	fd_w = open(svm_id_list_file, 'w')
	for line in fd:
		a = line.index(' ')
		fd_w.write(line[:a] + '\n')
	fd_w.close()
	fd.close()

	svm_id_list = read_id_list(svm_id_list_file)
	
	fd = open(in_folder + '/' + in_file)
	import MySQLdb
	con   =   MySQLdb.connect(host="192.168.0.2",  port=3306, user="root",  passwd="see",  db="uwo")  
	cursor   =   con.cursor() 
	for id in svm_id_list:
		line = fd.readline().strip()
		sql = 'insert into ' + table + ' values (' + str(id) + ', "' + line + '")'	
		#sql = 'update ' + table + ' set prediction="'+line + '" where id=' + str(id)	
		cursor.execute(sql)
	#cursor.execute('delete from uwo_new_prediction_3 where id >= 0')
	con.commit()
	cursor.close()
	con.close()
	fd.close()
