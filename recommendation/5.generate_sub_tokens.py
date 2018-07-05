import re
import pyprind

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

ps = PorterStemmer()
sw = set(stopwords.words('english'))

remove_stops = lambda l:  [w for w in l if w not in sw]
string_to_tokens = lambda s: re.findall(r'\w+', s.strip(',. ?1').lower())
stem_list = lambda l: [ps.stem(e) for e in l]

remove_dups = lambda l: list(set(l))

num_lines = 27158
bar = pyprind.ProgBar(num_lines)

FILE_IN = 'each_sub_comm.csv'
FILE_OUT = 'sub_tokens.csv'

out = open(FILE_OUT, 'w')

with open(FILE_IN) as f:
  for line in f:
    sub, tokens = line.split(',')

    tokens = string_to_tokens(tokens)
    tokens = remove_stops(tokens)
    tokens = stem_list(tokens)

    out.write(sub)
    out.write(',')
    out.write(" ".join(tokens))

    out.write('\n')

    bar.update()

out.close()