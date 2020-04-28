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

# from api.models import Store #상점 46만개
# from api.models import Review # 리뷰 9만개
# from api.models import CustomUser # 유저 1.8만개

b = open('text/stopword.txt', 'r', encoding='utf-8')
stopwordtext = b.read()
stop_words = stopwordtext.split('\n')
okt = Okt()
def tf(t, d):
  return d.count(t)

def idf(t, docs):  
    df = 0
    for doc in docs:
        df += t in doc
    return log(N/(df + 1))

def tfidf(t, d, docs):
  return tf(t,d)* idf(t, docs)

a = Review.objects.filter(reg_time__gte="2019-03-01 00:00:00")
d = Review.objects.all()
b = ''
c = []
vocas = set()
for review in a:
    b += review.content + '\n'
    nouns = okt.nouns(review.content)
    for noun in nouns:
        vocas.add(noun)
for review in d:
    c.append(review.content)

N = len(vocas)
r = []
for voca in vocas:
    r.append([tfidf(voca, b, c), voca])
print([w[1] for w in sorted(r, reverse=True)[:300]])