if __name__ == '__main__':
	import os
	ips = ['192.168.0.1', '192.168.0.11', '192.168.0.12']	
	for i in range(len(ips)):		
		cmd = 'scp -r /home/mpi/.ipython/profile_default/security/ ' + ips[i] + ':/home/mpi/.ipython/profile_default/security/'
		os.system(cmd)
