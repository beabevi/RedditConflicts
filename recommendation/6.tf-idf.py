from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import scipy as scp
import numpy as np
import pandas as pd
import pyprind

FILE_IN = "sub_tokens.csv"

tfidf = TfidfVectorizer(max_features=20000, sublinear_tf=True)


def top_subreddits():
  data = pd.read_csv('top_5000_subreddits.index', header=None)
  return data.values[:,0].tolist()

top_subs = top_subreddits()

tokens = []

with open(FILE_IN) as f:
  for line in f:
    sub, token = line.split(',')
    tokens.append(token)



vecs = tfidf.fit_transform(tokens)

scp.sparse.save_npz('tfidf.npz', vecs)

similarities = cosine_similarity(vecs)

np.save('similarities.npy', similarities)

"""
sims = []


for i, sub in enumerate(top_subs):
  m = 0
  m_i = 0
  for j in range(0, len(top_subs)):
    if j != i and similarities[i][j] > m:
      m = similarities[i][j]
      m_i = j

  sims.append((sub, top_subs[m_i]))

print(sims)
"""