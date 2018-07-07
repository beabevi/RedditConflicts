from random import randint
import lzma
import json

def hit():
  """
    Returns true 1/8 times on average
  """

  if randint(1, 8) == 8:
    return True
  else:
    return False


data = lzma.open('data/RC_2017-12.xz')
out = open('sample/RC_2017-12.1over8.sample', 'w')
out_head = open('sample/RC_2017-12.1over8.head', 'w')

attrs = ['subreddit', 'author', 'id',
'author_flair_css_class',
'author_flair_text',
'controversiality',
'created_utc',
'distinguished',
'edited',
'gilded',
'is_submitter',
'link_id',
'parent_id',
'permalink',
'retrieved_on',
'score',
'stickied',
'subreddit_id',
'subreddit_type',
'body']

others = []

for line in data:
  if hit():
    curr = json.loads(line)
    for i in range(0, len(attrs)):
      if i != 0:
        out.write(',')
      
      to_write = str(curr.get(attrs[i], ''))
      to_write = to_write.replace('\n', ' ').replace('\r', '').replace(',', ' ')
      out.write( to_write )

    for k in curr.keys():
      if not k in attrs and not k in others:
        others.append(k)
        print(others)
    
    out.write('\n')

out.close()

for attr in attrs:
  out_head.write(attr + '\n')

out_head.close()