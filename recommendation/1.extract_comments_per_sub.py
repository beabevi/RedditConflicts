import lzma
import json

data = lzma.open('data/RC_2017-12.xz')

subs = {}

for line in data:
  curr = json.loads(line)
  
  if not curr['subreddit'] in subs.keys():
    subs[curr['subreddit']] = 0
  
  subs[curr['subreddit']] += 1

data.close()

out = open('data_stats/RC_2017-12.subs.csv', mode='w')

out.write('subreddit,comments\n')

for key in subs.keys():
  out.write(str(key) + ',' + str(subs[key]) + "\n")

out.close()