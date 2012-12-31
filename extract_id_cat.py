import   MySQLdb  	
con   =   MySQLdb.connect(host="192.168.0.2",  port=3306, user="root",  passwd="see",  db="see")  
cursor   =   con.cursor()  
sql = 'select id, cat_name from uwo.categories'
cursor.execute(sql)
rows = cursor.fetchall()
fd = open('uwo_id_cat_name', 'w')
for r in rows:
	fd.write(str(r[0]) + ' ' + r[1] + '\n')
fd.close()
cursor.close()
con.close()
