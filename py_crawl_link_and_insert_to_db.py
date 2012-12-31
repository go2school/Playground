if __name__ == '__main__': 
	from url_util import *
	import MySQLdb
	#link = 'https://iwc.uwo.ca/iwc_static/layout/login-uwo.html?lang=en-us&02.01_184110&svcs=abs,mail,calendar,c11n'
	#ct = download_webpage(link)
	#t,b,k,d, charcode = extract_content(ct)
	#b = remove_nontext(b)
	
	boost = 3
	site = 'mail.uwo.ca'
	url = 'http://mail.uwo.ca'	
	title = 'UWO Mail'
	content = "welcome to convergence , western's webmail client. for assistance, please contact the its helpdesk . reminder: its will never ask for your password by email. do not share your password with anyone. sign in with your western account javascript is required. username: password: forgot your password"
	contentType = 'text/html'
	userID = 'UWO'
	tstamp = '2012-03-07T00:11:01.978Z'
	
	
	boost = 3.71234
	site = 'student.uwo.ca'
	url = 'http://student.uwo.ca'	
	title = 'Student Center University of Western Ontario'
	content = 'Student Center allows future and current students, and alumni to access their admission and/or student information at Western. Student Center is your connection to managing a wide range of activities-from managing courses and fees, grades, maintaining contact information, viewing academic records and more. You may access the Student Center using your Western identity. '
	contentType = 'text/html'
	userID = 'UWO'
	tstamp = '2012-03-08T09:38:01.978Z'
	
	
	con   =   MySQLdb.connect(host="192.168.0.2",  port=3306, user="root",  passwd="see",  db="uwo")  
	cursor   =   con.cursor() 
	cursor.execute("insert into uwo.uwo_new_nutch_docs (boost, site, url, title, content, contentType, userID, tstamp) values (%s, %s, %s, %s, %s, %s, %s, %s)", (str(boost), site, url, title, content, contentType, userID, tstamp))
	cursor.close()
	con.close()
	
