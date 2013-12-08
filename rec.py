import urllib2
import re

url = "http://www.spoj.com/problems/classical/"
html  = urllib2.urlopen(url).read()
content = []
content = html.split('\n')
for line in content:
  res = re.match('<a.*start=(\d+)',line)
  if res:
    total = int(res.group(1))

f = open('problems','a')
num = 0

while num <= total:
  for line in content:
    res = re.match('<a href="/problems/(\w+).*</a></td>$',line)
    if res:
      f.write(res.group(1))
      f.write("\n")
  num = num + 50
  url = "http://www.spoj.com/problems/classical/start=" + str(num)
  html  = urllib2.urlopen(url).read()
  content = html.split('\n')



