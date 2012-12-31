#from bingapi import bingapi
import bingapi
appid = '5288CAD808E07789BF0ECA3F55B704C3293D975B'
bing = bingapi.Bing(appid)
resp = bing.do_image_search('uwo', [('Image.Count', 10), ('Image.Offset', 0)])
print resp['SearchResponse']['Image']['Total']
results = resp['SearchResponse']['Image']['Results']
n = 0
for result in results:
	print 'Doc ' + str(n)
	title = ''
	desc = ''
	if 'Title' in result:
		title = result['Title']
	if 'Description' in result:
		desc = result['Description']
	print '	Title: ' + title
	print '	Description: ' + desc
	n += 1
