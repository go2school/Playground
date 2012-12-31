from IPython.parallel import Client
c = Client()
cats = range(662)
rc = c[:]
rc.scatter('my_cats', cats)

cat2ipengine = {}
for id in c.ids:
	cs = c[id]['my_cats']
	for cid in cs:
		cat2ipengine[cid] = id
