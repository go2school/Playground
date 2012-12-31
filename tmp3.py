
n = 50
fd = open('tmp_2.txt', 'w')
for i in range(n):
	fd.write('<field name = "topic_'+str(i)+'" type="float" indexed="true" stored="true" />\n')
fd.close()
