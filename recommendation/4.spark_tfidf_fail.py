
# coding: utf-8

# In[1]:


from pyspark.ml.feature import StringIndexer
import pandas as pd

from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .appName("WIR") \
    .getOrCreate()

def top_n_subreddits(n):
  data = pd.read_csv('data_stats/RC_2017-12.subs.csv')
  data.subreddit = data.subreddit.astype(str)
  data.comments = data.comments.astype(int)

  data_filtered = data[data.comments > 1000].sort_values(by=['comments'], ascending=False)
  return set(data_filtered.values[:n][:,0].tolist())

subs = top_n_subreddits(10000)


# In[2]:


df = spark.read.load("sample/RC_2017-12.1over8.sample",
                     format="csv", sep=",", inferSchema="true", header="false")
df = df.toDF('subreddit', 'author', 'id',
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
'body')
df = df.select(df['subreddit'], df['body'])


# In[3]:


res = df.rdd.filter(lambda r: r[0] in subs).map(lambda r: (r[0], r[1] if not r[1] is None else "" )).groupByKey().map(lambda e: (e[0], " ".join(e[1])))


# In[4]:


res_df = res.toDF().toDF('sub', 'words')
res_df.write.csv('sub_words.1over4.csv')


# In[ ]:

"""
from pyspark.ml.feature import RegexTokenizer
from pyspark.ml.feature import StopWordsRemover
from pyspark.ml.feature import HashingTF, IDF

tkn = RegexTokenizer().setInputCol("words").setOutputCol("subwords").setPattern("\\W").setToLowercase(True)
tokenized = tkn.transform(res_df)

englishStopWords = StopWordsRemover.loadDefaultStopWords("english")
stops = StopWordsRemover().setStopWords(englishStopWords).setInputCol("subwords").setOutputCol('without_stops')

stoprem = stops.transform(tokenized)
stoprem.select('sub', 'without_stops').rdd.map(lambda r: (r[0], " ".join(r[1]))).toDF().write.csv('stopsrem.csv')

tmp = stoprem.select('without_stops')

tf = HashingTF().setInputCol("without_stops").setOutputCol("TFOut").setNumFeatures(1000)
idf = IDF().setInputCol("TFOut").setOutputCol("IDFOut").setMinDocFreq(2)

idf.fit(tf.transform(tmp)).transform(tf.transform(tmp)).show(2, False)



# In[14]:


sub_indexer = StringIndexer(inputCol='subreddit', outputCol='subindex') 
indexed = sub_indexer.fit(df).transform(df)


# In[18]:


indexed.rdd.map(lambda x: x).collect()

"""