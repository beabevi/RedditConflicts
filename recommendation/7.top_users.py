from collections import Counter

FILE_IN = 'sample/test.csv'


subreddits = []

users_subs = {}


def get_sub_idx(sub):
    i = -1
    try:
        i = subreddits.index(sub)
    except ValueError:
        pass
    return i

with open(FILE_IN) as f:
    for line in f:
        tmp = line.split(',')
        sub = tmp[0]
        author = tmp[1]

        if author == '[deleted]' or author.lower().endswith('bot'):
            continue

        sub_idx = get_sub_idx(sub)
        if  sub_idx == -1:
            subreddits.append(sub)
            sub_idx = len(subreddits) - 1
        
        user_subs = users_subs.get(author, [])

        if user_subs == []:
            users_subs[author] = []
        
        users_subs[author].append(sub_idx)

out_head = open('user_prefs/subs_users.head', 'w')
out_head.write('\n'.join(subreddits))
out_head.close()

out_body = open('user_prefs/subs_users.body', 'w')

for user in users_subs:
    c = Counter(users_subs[user])

    if len(c.keys()) < 5: continue

    out_body.write(user)
    out_body.write(',')

    for k in c:
        out_body.write(subreddits[k] + ":" + str(c.get(k)) + " ")
    out_body.write('\n')

out_body.close()