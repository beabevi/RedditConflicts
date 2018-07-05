from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import bottleneck as bn
import pandas as pd

FILE_IN = "sub_tokens.csv"

tfidf = TfidfVectorizer(max_features=20000, sublinear_tf=True)


def top_n_subreddits(n):
  data = pd.read_csv('data_stats/RC_2017-12.subs.csv')
  data.subreddit = data.subreddit.astype(str)
  data.comments = data.comments.astype(int)

  data_filtered = data[data.comments > 1000].sort_values(by=['comments'], ascending=False)
  return data_filtered.values[:n][:,0].tolist()

def top_n_indexes(arr, n):
    idx = bn.argpartition(arr, arr.size-n, axis=None)[-n:]
    width = arr.shape[1]
    return [divmod(i, width) for i in idx]

top_subs = top_n_subreddits(300)

subs = []

tokens = []

with open(FILE_IN) as f:
  for line in f:
    sub, token = line.split(',')
    if sub not in top_subs: continue
    subs.append(sub)
    tokens.append(token)



vecs = tfidf.fit_transform(tokens)

similarities = cosine_similarity(vecs)

sims = []

for i, sub in enumerate(subs):
  m = 0
  m_i = 0
  for j in range(0, len(subs)):
    if j != i and similarities[i][j] > m:
      m = similarities[i][j]
      m_i = j

  sims.append((sub, subs[m_i]))

print(sims)