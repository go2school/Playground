url = 'http://www.google.ca/search?gcx=w&sourceid=chrome&'
from url_util import download_webpage, extract_content
html = download_webpage(url)

t,b,k,d, charcode = extract_content(html)
import urllib2
import urllib
req = 'http://localhost:8000/?m=hft&th=0.5&tt=&bd=&url=http%3A%2F%2Fwww.google.ca%2Fsearch%3Fgcx%3Dw%26sourceid%3Dchrome%26'
q = 'http://localhost:8000/?m=hft&th=0.5'
#q += '&tt=' + urllib.quote(t, safe='~()*!.\'')
#q += '&bd=' + urllib.quote(b, safe='~()*!.\'')
q += '&url=' + urllib.quote(url, safe='~()*!.\'')
print q.split('&')

#test jvscript and python encode
old_u = "http://www.google.ca/search?sourceid=chrome&ie=UTF-8&q=python+quote+slash#hl=en&sa=X&ei=QRD0TrCTBYXCgAf4q_GLAg&ved=0CBcQvwUoAQ&q=python+equivalent+to+encodeuricomponent&spell=1&bav=on.2,or.r_gc.r_pw.r_cp.,cf.osb&fp=9ffc1b2e83a09913&biw=893&bih=538(=!21231313113)~`@#$%^&*_-{}[]:;\"'|\?/>.<,|\\"
jv_u = "http%3A%2F%2Fwww.google.ca%2Fsearch%3Fsourceid%3Dchrome%26ie%3DUTF-8%26q%3Dpython%2Bquote%2Bslash%23hl%3Den%26sa%3DX%26ei%3DQRD0TrCTBYXCgAf4q_GLAg%26ved%3D0CBcQvwUoAQ%26q%3Dpython%2Bequivalent%2Bto%2Bencodeuricomponent%26spell%3D1%26bav%3Don.2%2Cor.r_gc.r_pw.r_cp.%2Ccf.osb%26fp%3D9ffc1b2e83a09913%26biw%3D893%26bih%3D538(%3D!21231313113)~%60%40%23%24%25%5E%26*_-%7B%7D%5B%5D%3A%3B%22'%7C%5C%3F%2F%3E.%3C%2C%7C%5C"

print urllib.quote(old_u) == jv_u

print urllib.quote(old_u, safe='~()*!.\'') == jv_u

u1 = urllib.quote(old_u, safe='~()*!.\'')
u2 = urllib.unquote(u1)
print u2 == old_u

fd = urllib2.urlopen(q)
ct = fd.read()
fd.close()
print ct
