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
for store in Store.objects.filter(review_count__gte=10).values("id"):
  storeset.add(store['id'])
# print(storeset)
df = pd.DataFrame(Review.objects.all().values("user", "store", "score", "content"))
df = df[df["store"].isin(storeset)]
# print(df)
# print(len(df))

df_classify = dict()
# for i in range(len(df)):
for i in range(9):
  if df.iloc[i]["store"] not in df_classify.keys():
    df_classify[df.iloc[i]["store"]] = []
  df_classify[df.iloc[i]["store"]].append([df.iloc[i]["score"], [df.iloc[i]["content"]]])
# pprint(df_classify)
###########################################################################################


######################        분석시작       ########################################
# for store in df_classify.keys():
#   store_reviews = df_classify.get(store)
#   N = len(store_reviews)
#   # print(store_reviews)

#   good_review = []
#   bad_review = []


#   ######################        문장 분류       ##################################
#   docs = []
#   for i in range(N):
#     if store_reviews[i][0] >= 3:
#       good_review.append(i)
#     else:
#       bad_review.append(i)
#     for j in store_reviews[i][1]:
#       docs.append(j)
#   # print(docs)
#   ##############################################################################


#   ######################        문장 형태소분석 stop_words 적용          ##########################
#   voca = []
#   for doc in docs:
#     nouns = okt.nouns(doc)
#     tmp = []
#     for w in nouns:
#       if w not in stop_words:
#         tmp.append(w)
#     voca += tmp
#   voca = list(set(voca))
#   # print(voca)
#   ####################################################################

#   ######################        TF           #############################
#   # result = []
#   # for i in range(N): 
#   #   result.append([])
#   #   d = docs[i]
#   #   # print(d)
#   #   for j in range(len(voca)):
#   #     t = voca[j]        
#   #     # print(t)
#   #     result[-1].append(tf(t, d))
#   # # print(result)
#   # tf_ = pd.DataFrame(result, columns = voca)
#   # print(tf_)
#   ##############################################################################

#   ######################        IDF           ##################################
#   # result = []
#   # for j in range(len(voca)):
#   #   t = voca[j]
#   #   # print(t)
#   #   result.append(idf(t, docs))
#   # idf_ = pd.DataFrame(result, index = voca, columns = ["IDF"])
#   # print(idf_)
#   ##############################################################################

#   ######################        TF-IDF         ####################################
#   result = []
#   for i in range(N):
#     result.append([])
#     d = docs[i]
#     for j in range(len(voca)):
#       t = voca[j]
#       result[-1].append(tfidf(t,d,docs))
#   tfidf_ = pd.DataFrame(result, columns = voca)
#   # print(tfidf_)
#   ##############################################################################

#   ######################        워드클라우딩       #############################
#   # print(good_review, bad_review)
#   good_words = []
#   bad_words = []
#   for i in range(len(tfidf_)):
#     if i in good_review:
#       for idx, value in enumerate(tfidf_.iloc[i]):
#         if value > 0:
#           if 0 <= value < 0.3:
#             value = 1
#           elif 0.3 <= value < 0.6:
#             value = 3
#           elif 0.6 <= value < 0.9:
#             value = 5
#           elif 0.9 <= value < 1.1:
#             value = 7
#           elif 1.1 <= value < 1.3:
#             value = 9
#           elif 1.3 <= value < 1.5:
#             value = 11
#           elif 1.5 <= value < 1.7:
#             value = 13
#           else:
#             value = 15
#           good_words.append((voca[idx], value))
#           # good_words += (str(voca[idx]) + " ")
#         # print(voca[idx], value)
#     else:
#       for idx, value in enumerate(tfidf_.iloc[i]):
#         if value > 0:
#           if 0 <= value < 0.3:
#             value = 1
#           elif 0.3 <= value < 0.6:
#             value = 3
#           elif 0.6 <= value < 0.9:
#             value = 5
#           elif 0.9 <= value < 1.1:
#             value = 7
#           elif 1.1 <= value < 1.3:
#             value = 9
#           elif 1.3 <= value < 1.5:
#             value = 11
#           elif 1.5 <= value < 1.7:
#             value = 13
#           else:
#             value = 15
#           bad_words.append((voca[idx], value))
#           # bad_words += (str(voca[idx]) + " ")
#   # print("good_words : ", good_words) 
#   # print("bad_words : ", bad_words)

#   ############ 보여줄 경우에 사용 ##########
#   # if good_words:
#   #   good_wordcloud = WordCloud(
#   #     font_path="C:\\Windows\\Fonts\\HMKMMAG.TTF",  #한글 폰트 적용, 안하면 깨짐
#   #     background_color = 'white', #배경색
#   #     width = 800, 
#   #     height = 600
#   #   ).generate_from_frequencies(dict(good_words))

#   #   plt.figure(figsize = (15, 10)) # (가로인치, 세로인치) 
#   #   plt.axis("off") # 축눈금 제거
#   #   plt.imshow(good_wordcloud) # 이미지가 표시되도록 
#   #   plt.show() # 최종 출력문

#   # if bad_words:
#   #   bad_wordcloud = WordCloud(
#   #     font_path="C:\\Windows\\Fonts\\HMKMMAG.TTF",
#   #     background_color = 'white',
#   #     width = 800, 
#   #     height = 600
#   #   ).generate_from_frequencies(dict(bad_words))

#   #   plt.figure(figsize = (15, 10))
#   #   plt.axis("off") 
#   #   plt.imshow(bad_wordcloud)  
#   #   plt.show() 

#   ############# 저장할 경우에 사용 ###############
#   # if good_words:
#   #   good_wordcloud = WordCloud(
#   #     font_path="C:\\Windows\\Fonts\\HMKMMAG.TTF",  #한글 폰트 적용, 안하면 깨짐
#   #     background_color = 'white', #배경색
#   #     width = 800, 
#   #     height = 600
#   #   ).generate_from_frequencies(dict(good_words))
#   #   good_wordcloud.to_file('wordcloudimg/{}_good.png'.format(store))
    
#   # if bad_words:
#   #   bad_wordcloud = WordCloud(
#   #     font_path="C:\\Windows\\Fonts\\HMKMMAG.TTF",
#   #     background_color = 'white',
#   #     width = 800, 
#   #     height = 600
#   #   ).generate_from_frequencies(dict(bad_words))
#   #   bad_wordcloud.to_file('wordcloudimg/{}_bad.png'.format(store))
#   ################################################################

#   store_tag_sort = sorted(good_words, key=lambda x: x[1], reverse=True)[:10]
#   print(store_tag_sort)
###########################################################################


############################### 유사도 해보는중 ###############################
# from sklearn.feature_extraction.text import TfidfVectorizer
# tfidf = TfidfVectorizer()
# tfidf_matrix = tfidf.fit_transform(df['content'])
# # overview에 대해서 tf-idf 수행
# print(tfidf_matrix.shape)

print(len(df))
print(len(df_classify))

from sklearn.metrics.pairwise import linear_kernel
cosine_sim = linear_kernel(tfidf_, tfidf_)
# print(cosine_sim)

test = list()
for i, v in enumerate(storeset):
  tmp = {
    "index": int(i),
    "value": int(v)
  }
  test.append(tmp)
# print(test[0].get("value"))
indices_before = pd.DataFrame(test)
# print(indices_before)
indices = pd.DataFrame(indices_before.index, index=indices_before["value"]).drop_duplicates()
# print(indices)

idx = indices.at[317443, 0]
# print(idx)

def get_recommendations(title, cosine_sim=cosine_sim):
    # 선택한 영화의 타이틀로부터 해당되는 인덱스를 받아옵니다. 이제 선택한 영화를 가지고 연산할 수 있습니다.
    idx =  indices.at[title, 0]
    # print(idx)
    # 모든 영화에 대해서 해당 영화와의 유사도를 구합니다.
    sim_scores = list(enumerate(cosine_sim[idx]))
    # print("111111111111 : ", sim_scores)
    # 유사도에 따라 영화들을 정렬합니다.
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # print("22222222222 : ", sim_scores)
    # 가장 유사한 10개의 영화를 받아옵니다.
    sim_scores = sim_scores[1:11]
    # print("333333333 : ", sim_scores)
    # 가장 유사한 10개의 영화의 인덱스를 받아옵니다.
    movie_indices = []
    for i in sim_scores:
      movie_indices.append([i[0], i[1]])
    # print(movie_indices)
    # 가장 유사한 10개의 영화의 제목을 리턴합니다.
    return movie_indices

for idx, value in get_recommendations(317443):
  print("유사한 store id : ", indices_before.iloc[idx]["value"], "cosine 유사도 값 : ", value)