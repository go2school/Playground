if __name__ == '__main__':
	import os
	ips = ['192.168.0.1', '192.168.0.10', '192.168.0.11', '192.168.0.12']	
	for i in range(len(ips)):		
		cmd = 'ssh ' + ips[i] + ' killall -v ipengine > /dev/null 2>&1 &'
		os.system(cmd)
