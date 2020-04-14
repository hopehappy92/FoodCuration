import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from pprint import pprint
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt

from api.models import Review, CustomUser, Store

from wordcloud import WordCloud, STOPWORDS
# import matplotlib.pyplot as plt
from konlpy.tag import Okt  


############### 워드 클라우드 저장 #######################
# a = Review.objects.all() 
# df = pd.DataFrame(list(a.values("user_id", "store_id", "score", "content")))
# print(df)

# okt=Okt()

# df_classify = dict()
# for i in range(100):
#   # print(i)
#   # print(df.iloc[i]["content"])
#   if not df.iloc[i]["content"]:
#     # print(df.iloc[i]["content"])
#     continue
#   tmp = okt.nouns(df.iloc[i]["content"])
#   text = ' '.join(tmp)
#   # print(text)
#   if df.iloc[i]["store_id"] not in df_classify:
#     df_classify[df.iloc[i]["store_id"]] = text
#   else:
#     df_classify[df.iloc[i]["store_id"]] = df_classify.get(df.iloc[i]["store_id"]) + text
# # pprint(df_classify)

# for i in df_classify.keys():
#   wordcloud = WordCloud(
#     font_path="C:\\Windows\\Fonts\\HMKMMAG.TTF",
#     stopwords = STOPWORDS,
#     background_color = 'white', #배경색
#     width = 800, 
#     height = 600
#   ).generate(df_classify.get(i))
#   wordcloud.to_file('wordcloudimg/{}.png'.format(i))
#############################################################

# plt.figure(figsize = (15, 10)) # (가로인치, 세로인치) 
# plt.axis("off") # 축눈금 제거
# plt.imshow(wordcloud) # 이미지가 표시되도록 
# plt.show() # 최종 출력문

#morphs pos nouns



### pandas
# from math import log

# docs = [
#   '먹고 싶은 사과',
#   '먹고 싶은 바나나',
#   '길고 노란 바나나 바나나',
#   '저는 과일이 좋아요'
# ] 
# vocab = list(set(w for doc in docs for w in doc.split()))
# vocab.sort()
# print(vocab)

# N = len(docs) # 총 문서의 수

# def tf(t, d):
#   return d.count(t)

# def idf(t):
#   df = 0
#   for doc in docs:
#       df += t in doc
#   return log(N/(df + 1))

# def tfidf(t, d):
#   return tf(t,d)* idf(t)

# result = []
# for i in range(N): # 각 문서에 대해서 아래 명령을 수행
#   result.append([])
#   d = docs[i]
#   for j in range(len(vocab)):
#     t = vocab[j]        
#     result[-1].append(tf(t, d))

# tf_ = pd.DataFrame(result, columns = vocab)
# print(tf_)

# result = []
# for j in range(len(vocab)):
#   t = vocab[j]
#   result.append(idf(t))

# idf_ = pd.DataFrame(result, index = vocab, columns = ["IDF"])
# print(idf_)

# result = []
# for i in range(N):
#   result.append([])
#   d = docs[i]
#   for j in range(len(vocab)):
#     t = vocab[j]
#     result[-1].append(tfidf(t,d))

# tfidf_ = pd.DataFrame(result, columns = vocab)
# print(tfidf_)


### scikit-learn
# from sklearn.feature_extraction.text import CountVectorizer
# corpus = [
#     'you know I want your love',
#     'I like you',
#     'what should I do ',    
# ]
# vector = CountVectorizer()
# print(vector.fit_transform(corpus).toarray()) # 코퍼스로부터 각 단어의 빈도 수를 기록한다.
# print(vector.vocabulary_) # 각 단어의 인덱스가 어떻게 부여되었는지를 보여준다.

# from sklearn.feature_extraction.text import TfidfVectorizer
# corpus = [
#     'you know I want your love',
#     'I like you',
#     'what should I do ',    
# ]
# tfidfv = TfidfVectorizer().fit(corpus)
# print(tfidfv.transform(corpus).toarray())
# print(tfidfv.vocabulary_)
# print(sorted(tfidfv.vocabulary_.items())) # 단어사전 정렬


### konlpy // Okt
# from konlpy.tag import Okt  
# okt=Okt()  
# print(okt.morphs("열심히 코딩한 당신, 연휴에는 여행을 가봐요"))
# print(okt.pos("열심히 코딩한 당신, 연휴에는 여행을 가봐요"))  
# print(okt.nouns("열심히 코딩한 당신, 연휴에는 여행을 가봐요"))  

### konlpy // Kkma
# from konlpy.tag import Kkma  
# kkma=Kkma()  
# print(kkma.morphs("열심히 코딩한 당신, 연휴에는 여행을 가봐요"))
# print(kkma.pos("열심히 코딩한 당신, 연휴에는 여행을 가봐요"))  
# print(kkma.nouns("열심히 코딩한 당신, 연휴에는 여행을 가봐요"))  


# from nltk.corpus import stopwords 
# from nltk.tokenize import word_tokenize 

# example = "고기를 아무렇게나 구우려고 하면 안 돼. 고기라고 다 같은 게 아니거든. 예컨대 삼겹살을 구울 때는 중요한 게 있지."
# stop_words = ""
# # 위의 불용어는 명사가 아닌 단어 중에서 저자가 임의로 선정한 것으로 실제 의미있는 선정 기준이 아님
# stop_words=stop_words.split(' ')
# word_tokens = word_tokenize(example)

# result = [] 
# for w in word_tokens: 
#     if w not in stop_words: 
#         result.append(w) 
# # 위의 4줄은 아래의 한 줄로 대체 가능
# # result=[word for word in word_tokens if not word in stop_words]

# print(word_tokens) 
# print(result)

########################## stop_word 적용 ################################
a = open('text/text.txt', 'r', encoding='utf-8')
b = open('text/stopword.txt', 'r', encoding='utf-8')
text = a.read()
stopwordtext = b.read()
stop_words = stopwordtext.split('\n')

def get_noun(text):
  okt = Okt()
  noun = okt.nouns(text)
  result = [] 
  for w in noun: 
      if w not in stop_words: 
          result.append(w)
  for i,v in enumerate(result):
    if len(v) < 2:
      result.pop(i)
  count = Counter(result)
  noun_list = count.most_common(1000)
  return noun_list

text_sort = get_noun(text)
print(text_sort) 

wordcloud = WordCloud(
    font_path="C:\\Windows\\Fonts\\HMKMMAG.TTF",
    background_color = 'white', #배경색
    width = 800, 
    height = 600
  ).generate_from_frequencies(dict(text_sort))

plt.figure(figsize = (15, 10)) # (가로인치, 세로인치) 
plt.axis("off") # 축눈금 제거
plt.imshow(wordcloud) # 이미지가 표시되도록 
plt.show() # 최종 출력문
################################################################