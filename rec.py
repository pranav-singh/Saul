import urllib2
import re

url = "http://www.spoj.com/problems/classical/"
html  = urllib2.urlopen(url).read()
content = []
content = html.split('\n')
for line in content:
  res = re.match('<a href="/problems/(\w+).*</a></td>$',line)
  if res:
    print res.group(1)

