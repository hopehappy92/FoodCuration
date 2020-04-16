import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()
import requests

import pandas as pd
import matplotlib.pyplot as plt
from math import log

from api.models import Review

from wordcloud import WordCloud
# import matplotlib.pyplot as plt
from konlpy.tag import Okt  

from pprint import pprint

b = open('text/stopword.txt', 'r', encoding='utf-8')
stopwordtext = b.read()
stop_words = stopwordtext.split('\n')

####################################### 데이터 전처리중 ###########################33
# a = Review.objects.all() 
# df = pd.DataFrame(list(a.values("user_id", "store_id", "score", "content")))
# print(df)

# # okt=Okt()

# # df_classify = dict()
# # for i in range(10):
# #   # print(i)
# #   # print(df.iloc[i]["content"])
# #   if not df.iloc[i]["content"]:
# #     # print(df.iloc[i]["content"])
# #     continue
# #   df_classify[df.iloc[i]["store_id"]] = []
# #   nouns = okt.nouns(df.iloc[i]["content"])
# #   # print(tmp)
# #   # text = ' '.join(tmp)
# #   # print(text)
# #   df_classify[df.iloc[i]["store_id"]].append([df.iloc[i]["score"], nouns])
# #   # if df.iloc[i]["store_id"] not in df_classify:
# #   #   df_classify[df.iloc[i]["store_id"]].push([df.iloc[i]["score"], nouns])
# #   # else:
# #   #   df_classify[df.iloc[i]["store_id"]] = df_classify.get(df.iloc[i]["store_id"]) + nouns
# # pprint(df_classify)

# request_all_review = requests.get("http://i02d106.p.ssafy.io:8765/api/store_reviews?page_size=1000000").json()
# # print(request_all_review)
# df = pd.DataFrame(request_all_review.get("results"))
# print(df)

# request_store = requests.get("http://i02d106.p.ssafy.io:8765/api/store/10").json()
# # print(request_store)

###########################################################################################



def tf(t, d):
  return d.count(t)

def idf(t, docs):
  df = 0
  for doc in docs:
      df += t in doc
  return log(N/(df + 1))

def tfidf(t, d, docs):
  return tf(t,d)* idf(t, docs)

tmpset = {
  15: [
    [5, [
      '전포 윗길에 새로 생긴! 호주에서 온 쉐프가 직접 요리하는 호주식 레스토랑!'
    ]],
    [4, [
      '샌드위치 내용물도 알차게 들어있고 맛있었어요 가성비 추천'
    ]],
    [2, [
      '홈플러스 1층 매장 푸드코트 내 있는 매장인데 계란찜정식은 처음보고 시켜봣는데 사진 그대로 치즈가 넘쳐 흐르는 계란찜이 메인이였네요 \n 치즈는 위에만 있어 금방 굳어 아쉬웠지만 맛은 평범하지만 보는재미가 있고 가성비 갠차는곳이였어요'
    ]],
    [1, [
      '전 여기 5년전에 가봤었는데 그때 기억은 별로였어요 \n 단체손님이 많았고, 차려지는건 많은데, 손가는게 별로없는...지금은 어떤지 몰겠네요'
    ]]
  ]
}
okt = Okt()

for store_id in tmpset.keys():
  store_reviews = tmpset.get(store_id)
  N = len(store_reviews)
  # print(store_reviews)

  good_review = []
  bad_review = []

  docs = []
  for i in range(N):
    if store_reviews[i][0] >= 3:
      good_review.append(i)
    else:
      bad_review.append(i)
    for j in store_reviews[i][1]:
      docs.append(j)
  # print(docs)

  voca = []
  for doc in docs:
    nouns = okt.nouns(doc)
    tmp = []
    for w in nouns:
      if w not in stop_words:
        tmp.append(w)
    voca += tmp
  voca = list(set(voca))
  # print(voca)

  # result = []
  # for i in range(N): 
  #   result.append([])
  #   d = docs[i]
  #   # print(d)
  #   for j in range(len(voca)):
  #     t = voca[j]        
  #     # print(t)
  #     result[-1].append(tf(t, d))
  # # print(result)
  # tf_ = pd.DataFrame(result, columns = voca)
  # print(tf_)

  # result = []
  # for j in range(len(voca)):
  #   t = voca[j]
  #   # print(t)
  #   result.append(idf(t, docs))
  # idf_ = pd.DataFrame(result, index = voca, columns = ["IDF"])
  # print(idf_)

  result = []
  for i in range(N):
    result.append([])
    d = docs[i]
    for j in range(len(voca)):
      t = voca[j]
      result[-1].append(tfidf(t,d,docs))
  tfidf_ = pd.DataFrame(result, columns = voca)
  print(tfidf_)

  # print(good_review, bad_review)
  good_words = []
  bad_words = []
  for i in range(len(tfidf_)):
    if i in good_review:
      for idx, value in enumerate(tfidf_.iloc[i]):
        if value > 0:
          if 0 <= value < 0.3:
            value = 1
          elif 0.3 <= value < 0.6:
            value = 3
          elif 0.6 <= value < 0.9:
            value = 5
          elif 0.9 <= value < 1.1:
            value = 7
          elif 1.1 <= value < 1.3:
            value = 9
          elif 1.3 <= value < 1.5:
            value = 11
          elif 1.5 <= value < 1.7:
            value = 13
          else:
            value = 15
          good_words.append((voca[idx], value))
          # good_words += (str(voca[idx]) + " ")
        # print(voca[idx], value)
    else:
      for idx, value in enumerate(tfidf_.iloc[i]):
        if value > 0:
          if 0 <= value < 0.3:
            value = 1
          elif 0.3 <= value < 0.6:
            value = 3
          elif 0.6 <= value < 0.9:
            value = 5
          elif 0.9 <= value < 1.1:
            value = 7
          elif 1.1 <= value < 1.3:
            value = 9
          elif 1.3 <= value < 1.5:
            value = 11
          elif 1.5 <= value < 1.7:
            value = 13
          else:
            value = 15
          bad_words.append((voca[idx], value))
          # bad_words += (str(voca[idx]) + " ")
  print("good_words : ", good_words) 
  print("bad_words : ", bad_words)

  wordcloud = WordCloud(
    font_path="C:\\Windows\\Fonts\\HMKMMAG.TTF",
    background_color = 'white', #배경색
    width = 800, 
    height = 600
  ).generate_from_frequencies(dict(good_words))

  plt.figure(figsize = (15, 10)) # (가로인치, 세로인치) 
  plt.axis("off") # 축눈금 제거
  plt.imshow(wordcloud) # 이미지가 표시되도록 
  plt.show() # 최종 출력문

  wordcloud = WordCloud(
    font_path="C:\\Windows\\Fonts\\HMKMMAG.TTF",
    background_color = 'white', #배경색
    width = 800, 
    height = 600
  ).generate_from_frequencies(dict(bad_words))

  plt.figure(figsize = (15, 10)) # (가로인치, 세로인치) 
  plt.axis("off") # 축눈금 제거
  plt.imshow(wordcloud) # 이미지가 표시되도록 
  plt.show() # 최종 출력문
        