import urllib2
import re
from pymongo import MongoClient

f = open('users','r')
client = MongoClient()
db = client['saul']
col = db['dict']

for user in f:
  user = user.strip("\n")
  url = "http://www.spoj.com/users/" + user
  html  = urllib2.urlopen(url).read()
  content = []
  content = html.split('\n')
  data = {}
  for line in content:
    res = re.match('.*<a href="/status/(\w+).*</a></td>',line)
    if res:
      data[res.group(1)] = 1
  fd = open('problems','r')
  for prob in fd:
    prob = prob.strip("\n")
    if prob not in data.keys():
      data[prob] = 0
  post = {user: data}
  col.insert(post)

