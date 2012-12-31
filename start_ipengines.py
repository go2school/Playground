if __name__ == '__main__':
	import os
	ips = ['192.168.0.1', '192.168.0.10', '192.168.0.11', '192.168.0.12']
	process = [6, 4, 4, 4]
	for i in range(len(ips)):	
		for j in range(process[i]):
				cmd = 'ssh ' + ips[i] + ' ipengine > /dev/null 2>&1 &'
				os.system(cmd)
