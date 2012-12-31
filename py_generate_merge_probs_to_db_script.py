import os
work_folder = '/media/DataVolume1/seeuwo/url_reorganization'
universities = ['utoronto', 'uqueens', 'umcmaster', 'uyork', 'uottawa', 'ucarleton', 'uguelph', 'uryerson', 'uwilfridlaurier', 'ubrock']
fd_w = open('all_merge_probs_to_db.sh', 'w')
for u in universities:	
	cmd1 = 'python py_merge_probs_to_single_file.py --schema ' + u
	fd_w.write('echo "' + cmd1 + '"\n')
	fd_w.write(cmd1 + '\n')
	cmd2 = 'python py_store_single_probs_to_db.py --schema ' + u
	fd_w.write('echo "' + cmd2 + '"\n')
	fd_w.write(cmd2 + '\n')
fd_w.close()
os.system('chmod 777 *.sh')
