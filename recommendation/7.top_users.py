from collections import Counter
import pandas as pd

FILE_IN = 'sample/RC_2017-12.1over4.sample'
FILE_OUT = 'user_prefs/subs_users.1over4.body'

def top_subreddits():
  data = pd.read_csv('top_5000_subreddits.index', header=None)
  return data.values[:,0].tolist()

subreddits = top_subreddits()

sub_index = {}
for i, sub in enumerate(subreddits):
  sub_index[sub] = i

users_subs = {}


with open(FILE_IN) as f:
    for line in f:
        tmp = line.split(',')
        sub = tmp[0]
        author = tmp[1]

        if author == '[deleted]' or author.lower().endswith('bot'):
            continue

        sub_idx = sub_index.get(sub, -1)
        if sub_idx == -1:
            continue

        user_subs = users_subs.get(author, [])

        if user_subs == []:
            users_subs[author] = []
        
        users_subs[author].append(sub_idx)


out_body = open(FILE_OUT, 'w')

for user in users_subs:
    c = Counter(users_subs[user])

    if len(c.keys()) < 6: continue

    for k in c:
        out_body.write(str(k) + ":" + str(c.get(k)) + " ")
    out_body.write('\n')

out_body.close()