import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()
import requests

import pandas as pd
import matplotlib.pyplot as plt
from math import log

from api.models import Review, Store

from wordcloud import WordCloud
# import matplotlib.pyplot as plt
from konlpy.tag import Okt  

from pprint import pprint

######################        stop_words 불러오기        #################
b = open('text/stopword.txt', 'r', encoding='utf-8')
stopwordtext = b.read()
stop_words = stopwordtext.split('\n')
##############################################################################
wordlist = set()

######################         함수        ########################################
def tf(t, d):
  return d.count(t)

def idf(t, docs):  
  df = 0
  for doc in docs:
      df += t in doc
  return log(N/(df + 1))

def tfidf(t, d, docs):
  return tf(t,d)* idf(t, docs)

okt = Okt()
##############################################################################


######################        데이터 전처리중           ###########################33
storeset = set()
for store in Store.objects.filter(review_count__gte=5).values("id"):
  storeset.add(store['id'])
# print(storeset)
df = pd.DataFrame(Review.objects.all().values("user", "store", "score", "content"))
df = df[df["store"].isin(storeset)]
# print(df)
# print(len(df))

df_classify = dict()
for i in range(len(df)):
# for i in range(9):
  if df.iloc[i]["store"] not in df_classify.keys():
    df_classify[df.iloc[i]["store"]] = []
  df_classify[df.iloc[i]["store"]].append([df.iloc[i]["score"], [df.iloc[i]["content"]]])
# pprint(df_classify)
###########################################################################################


######################        분석시작       ########################################
for store_id in df_classify.keys():
  store_reviews = df_classify.get(store_id)
  N = len(store_reviews)
  # print(store_reviews)

  good_review = []
  bad_review = []


  ######################        문장 분류       ##################################
  docs = []
  for i in range(N):
    if store_reviews[i][0] >= 3:
      good_review.append(i)
    else:
      bad_review.append(i)
    for j in store_reviews[i][1]:
      docs.append(j)
  # print(docs)
  ##############################################################################


  ######################        문장 형태소분석 stop_words 적용          ##########################
  voca = []
  for doc in docs:
    nouns = okt.nouns(doc)
    tmp = []
    for w in nouns:
      if w not in stop_words:
        tmp.append(w)
    voca += tmp
  voca = list(set(voca))
  print(voca)
  ######################        TF-IDF         ####################################
  result = []
  for i in range(N):
    result.append([])
    d = docs[i]
    for word in voca:
      result[-1].append(tfidf(word,d,docs))
  tfidf_ = pd.DataFrame(result, columns = voca)
  # print(tfidf_)
  ##############################################################################

  ######################        워드클라우딩       #############################
  # print(good_review, bad_review)
  good_words = []
  bad_words = []
  for i in range(len(tfidf_)):
    if i in good_review:
      for idx, value in enumerate(tfidf_.iloc[i]):
        if value > 0:
          good_words.append((voca[idx], value))
          # good_words += (str(voca[idx]) + " ")
        # print(voca[idx], value)
    # else:
    #   for idx, value in enumerate(tfidf_.iloc[i]):
    #     if value > 0:

    #       bad_words.append((voca[idx], value))
          # bad_words += (str(voca[idx]) + " ")
  # print("good_words : ", good_words) 
  # print("bad_words : ", bad_words)


  store_tag_sort = sorted(good_words, key=lambda x: x[1], reverse=True)
  tags = set()
  for tag in store_tag_sort:
    tags.add(tag[0])
    wordlist.add(tag[0])
    if len(tags) > 9:
        break
  print(store_tag_sort)
  print(tags)
  store = Store.objects.get(id=store_id)
  a = '|'.join(tags)
  print(a)
  
  store.tag = a
  store.save()
#   print(a)#   store.tag = 
##########################################################################
print(wordlist)