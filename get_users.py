import urllib2
import re

url = "http://www.spoj.com/ranks/users/"
html  = urllib2.urlopen(url).read()
content = []
content = html.split('\n')
for line in content:
  res = re.match('<a.*start=(\d+)',line)
  if res:
    total = int(res.group(1))

f = open('users','a')
num = 0

while num <= total:
  for line in content:
    res = re.match('<td><a href="/users/(\w+).*</a></td>$',line)
    if res:
      f.write(res.group(1))
      f.write("\n")
  num = num + 100
  url = "http://www.spoj.com/ranks/users/start=" + str(num)
  html  = urllib2.urlopen(url).read()
  content = html.split('\n')
f.close()
