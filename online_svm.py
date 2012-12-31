import BaseHTTPServer
import SimpleHTTPServer
import CGIHTTPServer
import urllib
import random
import string, cgi, time
from os import curdir, sep
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from svm_server_util import load_model#, extract_content

#global variable for model
svm_models = {}
base_model_file = '/home/xiao/liblinear-1.8/python/heart_scale.model'
base_model_file = '/home/xiao/liblinear-1.8/python/food_model'
#n_cats = 3
n_cats = 1

	
class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):#(SimpleHTTPServer.SimpleHTTPRequestHandler):		
	def do_GET(self):				
		if self.path.endswith(".html"):
			f = open(curdir + sep + self.path) #self.path has /test.html
#note that this potentially makes every file on your computer readable by the internet

			self.send_response(200)
			self.send_header('Content-type',	'text/html')
			self.end_headers()
			self.wfile.write(f.read())
			self.connection.shutdown(1)
			f.close()
			return				
			
			
		elif self.path.find('?') > -1:# and self.path[:4] == '/?q=':
			import urllib 
			url = self.path[4:]
			#print self.path
			url = urllib.unquote_plus(url)
			print url
			body = ''
			result = ''
			quotes = []
			quotes.append((result))										
			body += ','.join(quotes)
			body += ']'

			#if 'callback' in form:
			#	body = ('%s(%s);' % (form['callback'], body))
		   
			self.send_response(200)
			self.send_header('Content-Type', 'text/javascript')
			self.send_header('Content-Length', len(body))
			self.send_header('Expires', '-1')
			self.send_header('Cache-Control', 'no-cache')
			self.send_header('Pragma', 'no-cache')
			self.end_headers()

			self.wfile.write(body)		
			self.wfile.flush()
			self.connection.shutdown(1)
	
	def do_POST(self):
		import cgi
		global rootnode
		try:			
			ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
			
			if ctype == 'multipart/form-data':
				query=cgi.parse_multipart(self.rfile, pdict)
			#print 'a ' + query
			#print 'b ' + ctype
			#print 'c ' + pdict
			self.send_response(301)			
			self.end_headers()
			
			upfilecontent = query.get('upfile')
			#print "filecontent", upfilecontent[0]
			self.wfile.write("<HTML>POST OK.<BR><BR>");
			self.wfile.write(upfilecontent[0]);
            
		except :
			pass	

if __name__ == '__main__': 
	for i in range(n_cats):
		model = load_model(base_model_file + '_' + str(i))	
		svm_models[i] = model
	
	bhs = BaseHTTPServer.HTTPServer(('', 8000), MyHandler)
	bhs.serve_forever()
