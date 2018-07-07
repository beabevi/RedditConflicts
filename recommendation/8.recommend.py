from scipy.sparse import load_npz
import numpy as np
import pyprind



tfidf = load_npz('tfidf.npz')

similarities = np.load('similarities.npy')

flatten = lambda l: [item for sublist in l for item in sublist]

def recommend(interest):
  recommendations = []
  for sub, _ in interest:
    similar_subs = np.argpartition(similarities[sub], -5)[-5:]
    recommendations.append(similar_subs.tolist())
  
  recommendations = set(flatten(recommendations))
  for sub, _ in interest:
    if sub in recommendations: recommendations.remove(sub)
  return recommendations


def user_to_preferences(user_prefs):
  tmp = user_prefs.strip().split(' ')
  prefs = []
  for e in tmp:
    sub_comms = e.split(':')
    prefs.append((int(sub_comms[0]), int(sub_comms[1])))
  return sorted(prefs, key=lambda x: x[1], reverse=True)

at_least_one = 0

n_users = 258035

bar = pyprind.ProgBar(n_users)

with open('user_prefs/subs_users.1over4.body') as f:
  for line in f:
    prefs = user_to_preferences(line)
    if len(recommend(prefs[:2]) & set([e for e, _ in prefs[2:]])) > 0:
      at_least_one += 1
    bar.update()

print(at_least_one / n_users)