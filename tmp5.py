a = ['z', 'a','a/b','a/x','a/y','z/x/q','a/b/c','a/x/t','a/y/w','z/x','b','b/d','b/d/e','a/b/q','a/b/z','a/b/w']


b =  sorted(a)
levels = ['' for i in range(20)]
last_i = -1
for bb in b:
	dx = bb.split('/')
	for i in range(len(dx)):
		if dx[i] != levels[i]:			
			os = ''
			for j in range(i):
				os += '\t'
			os += dx[i]
			levels[i] = dx[i]
			print os		
			last_i = i			
