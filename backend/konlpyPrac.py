import os
import django
import json
import numpy as np
import pandas as pd
import requests
from konlpy.tag import Komoran
import pandas as pd # 데이터프레임 사용을 위해
from math import log # IDF 계산을 위해

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import Review

Komoran = Komoran()


all_reviews = Review.objects.all()
review_list = list(all_reviews.values())
classification = 0

good_reviews = []
bad_reviews = []

for review_info in review_list[:10]:
    for key, value in review_info.items():
        if key == 'score' and int(value) > 3:
            classification = 'good'
        elif key == 'score' and int(value) < 3:
            classification = 'bad'
        elif key == 'score' and int(value) == 3:
            classificationm = 0
        
        if key == 'content' and classification == 'good':
            good_reviews.append(value)
        elif key == 'content' and classification == 'bad':
            bad_reviews.append(value)
        else:
            pass

# print('--------긍정적인 리뷰-----------')
# print(good_reviews)

# print('========부정적인 리뷰============')
# print(bad_reviews)

print(len(good_reviews))

docs = [
  '먹고 싶은 사과',
  '먹고 싶은 바나나',
  '길고 노란 바나나 바나나',
  '저는 과일이 좋아요'
] 
vocab = list(set(w for doc in docs for w in doc.split()))
vocab.sort()
N = len(docs) # 총 문서의 수

def tf(t, d):
    return d.count(t)

def idf(t):
    df = 0
    for doc in docs:
        df += t in doc
    return log(N/(df + 1))

def tfidf(t, d):
    return tf(t,d)* idf(t)



result = []
for i in range(N): # 각 문서에 대해서 아래 명령을 수행
    result.append([])
    d = docs[i]
    for j in range(len(vocab)):
        t = vocab[j]        
        result[-1].append(tf(t, d))

tf_ = pd.DataFrame(result, columns = vocab)
print(tf_)

result = []
for j in range(len(vocab)):
    t = vocab[j]
    result.append(idf(t))

idf_ = pd.DataFrame(result, index = vocab, columns = ["IDF"])

result = []
for i in range(N):
    result.append([])
    d = docs[i]
    for j in range(len(vocab)):
        t = vocab[j]

        result[-1].append(tfidf(t,d))

tfidf_ = pd.DataFrame(result, columns = vocab)