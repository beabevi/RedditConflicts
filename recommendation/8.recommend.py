from scipy.sparse import load_npz
import numpy as np
import pyprind
from sklearn.metrics.pairwise import cosine_similarity


tfidf = load_npz('tfidf.npz')

similarities = np.load('similarities.npy')

flatten = lambda l: [item for sublist in l for item in sublist]

alternate = lambda lists: [x for t in zip(*lists) for x in t]

def user_to_preferences(user_prefs):
  tmp = user_prefs.strip().split(' ')
  prefs = []
  for e in tmp:
    sub_comms = e.split(':')
    prefs.append((int(sub_comms[0]), int(sub_comms[1])))
  return sorted(prefs, key=lambda x: x[1], reverse=True)

def recommend(interest):
  recommendations = []
  for sub, _ in interest:
    top_indexes = np.argpartition(similarities[sub], -7)[-7:]
    similar_subs = top_indexes[np.argsort(similarities[sub][top_indexes])][::-1]
    recommendations.append(similar_subs.tolist())

  recommendations = alternate(recommendations)
  for sub, _ in interest:
    if sub in recommendations: recommendations.remove(sub)
  return recommendations

def recommend2(u_interest):
  interest = []
  for e in u_interest:
    interest.append(e[0])
  user = (tfidf[interest[0]] + tfidf[interest[1]])/2

  sim = cosine_similarity(tfidf, user)[:,0]
  top_indexes = np.argpartition(sim, -7)[-7:]
  recommendations = top_indexes[np.argsort(sim[top_indexes])][::-1].tolist()

  for sub in interest:
    if sub in recommendations: recommendations.remove(sub)

  return recommendations


at_least_one = 0

n_users = 32256

bar = pyprind.ProgBar(n_users)

tot_precision = [0] * 5
tot_recall = [0] * 5


with open('user_prefs/sub_user.sample') as f:
  for line in f:
    prefs = user_to_preferences(line)
    recommendations = recommend2(prefs[:2])
    if len(set(recommendations) & set([e for e, _ in prefs[2:]])) > 0:
      at_least_one += 1
    
    for k in range(1, 6):
      top_k = recommendations[:k]
      tot_precision[k - 1] += len(set(top_k) & set([e for e, _ in prefs[2:]])) / k
      tot_recall[k - 1] += len(set(top_k) & set([e for e, _ in prefs[2:]])) / len(prefs[2:])

    bar.update()

print(at_least_one / n_users)

tot_precision = [i/n_users for i in tot_precision]
tot_recall = [i/n_users for i in tot_recall]

print("P@k: ", tot_precision)
print("R@k: ", tot_recall)
