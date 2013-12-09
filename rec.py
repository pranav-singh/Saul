from math import sqrt
from pymongo import MongoClient
import re

# Returns the Pearson correlation coefficient for p1 and p2
def sim_pearson(p1,p2,person,other):
  client = MongoClient()
  db = client['saul']
  col = db['dict']

  # Get the list of mutually rated items
  si = {}
  for item in p1[person]:
    if item in p2[other]:
      si[item] = 1
  
  # Find the number of elements
  n = len(si)
  
  # if they are no ratings in common, return 0
  if n == 0:
    return 0
  
  # Add up all the preferences
  sum1 = sum([p1[person][it] for it in si])
  sum2 = sum([p2[other][it] for it in si])
  
  # Sum up the squares
  sum1Sq = sum([pow(p1[person][it],2) for it in si])
  sum2Sq = sum([pow(p2[other][it],2) for it in si])
  
  # Sum up the products
  pSum = sum([p1[person][it]*p2[other][it] for it in si])
  
  # Calculate Pearson score
  num = pSum-(sum1*sum2/n)
  den = sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
  if den == 0:
    return 0
  r = num/den
  return r

# Gets recommendations for a person by using a weighted average
# of every other user's rankings
def getRecommendations(person):
  totals = {}
  simSums = {}
  
  client = MongoClient()
  db = client['saul']
  col = db['dict']
  
  for obj in col.find():
    if obj.keys()[0] == '_id':
      check = obj.keys()[1]
    else:
      check = obj.keys()[0]
    if person == check:
      user = obj
      break

  for obj in col.find():
    if obj.keys()[0] == '_id':
      other = obj.keys()[1]
    else:
      other = obj.keys()[0]
    if person == other:
      continue

    sim = sim_pearson(user,obj,person,other)
    if sim <= 0:
      continue
    for item in obj[other]:
      if user[person][item] == 0:
        totals.setdefault(item,0)
        totals[item] += obj[other][item]*sim

        simSums.setdefault(item,0)
        simSums[item] += sim

  rankings = [(total/simSums[item],item) for item,total in totals.items()]
  rankings.sort()
  rankings.reverse()
  return rankings

# Returns the best matches for person from the prefs dictionary.
# Number of results and similarity function are optional params.
def topMatches(prefs,movie):
  scores = [(sim_pearson(prefs,movie,other),other)
    for other in prefs if other != movie]
  # Sort the list so the highest scores appear at the top
  scores.sort( )
  scores.reverse( )
  return scores

#Swapping movies and critics
def transformPrefs(prefs):
  result = {}
  for person in prefs:
    for item in prefs[person]:
      result.setdefault(item,{})

      # Flip item and person
      result[item][person]=prefs[person][item]
  return result

if __name__ == '__main__':
  user = raw_input("Enter the user name: ")
  print getRecommendations(user)
