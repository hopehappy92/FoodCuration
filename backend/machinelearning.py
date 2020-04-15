import os
import django
import json
import numpy as np
import pandas as pd
import surprise
import requests
from math import sqrt
from surprise.model_selection import cross_validate

from surprise import SVD, Dataset, accuracy, Reader
from surprise.model_selection import train_test_split
from surprise.dataset import DatasetAutoFolds

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import Store #상점 46만개
from api.models import Review # 리뷰 9만개
from api.models import CustomUser # 유저 1.8만개

# review가 10개 이상인 식당만 불러옴
request_store = requests.get("http://i02d106.p.ssafy.io:8765/api/store/10").json()
# review가 10개 이상인 유저만 불러옴
request_user = requests.get("http://i02d106.p.ssafy.io:8765/api/user").json()
# 모든 review 다 불러옴
request_all_review = requests.get("http://i02d106.p.ssafy.io:8765/api/reviews").json()

ten_review_store_df = pd.DataFrame(data=request_store)
ten_review_user_df = pd.DataFrame(data=request_user)
all_user_df = pd.DataFrame(data=request_all_review)
print('데이터 불러오기 완료')
ten_review_store_list = set()
ten_review_user_list = set()
for store in request_store:
    ten_review_store_list.add(store['id'])
for user in request_user:
    ten_review_user_list.add(user['id'])

selected_review_list = list()
for dic in request_all_review:
    if('score' in dic.keys() and 'user' in dic.keys() and 'store' in dic.keys()):
        if(dic['user'] in ten_review_user_list and dic['store'] in ten_review_store_list):
            selected_review_list.append(dic)

ratings_df = pd.DataFrame(selected_review_list)
ratings_df = ratings_df[['user', 'store', 'score']]
print(ratings_df)

# reader => 범위 설정  & 학습 부분
reader = Reader(rating_scale=(1, 5))
review_data = surprise.Dataset.load_from_df(df=ratings_df, reader=reader)
trainset = review_data.build_full_trainset()

print('학습 시작')
# 피어슨 유사도로 학습
sim_options = {'name': 'pearson', 'user_based': True}
algo = surprise.KNNBaseline(k=15, sim_options=sim_options)
predictions = algo.fit(trainset)
print('학습 완료')
# 1위: 469245번 유저 461번 리뷰
# 2위: 243883번 유저 389번 리뷰
# 3위: 328775번 유저 380번 리뷰
# 4위: 391794번 유저 362번 리뷰
# 5위: 74999번 유저 352번 리뷰
# 6위: 179719번 유저 317번 리뷰
# 7위: 724982번 유저 285번 리뷰
# 8위: 103304번 유저 282번 리뷰
# 9위: 728009번 유저 271번 리뷰
# 10위: 390564번 유저 268번 리뷰
# 11위: 180519번 유저 257번 리뷰
# 12위: 485567번 유저 249번 리뷰
# 13위: 218901번 유저 243번 리뷰
# 14위: 32143번 유저 240번 리뷰
# 15위: 884890번 유저 233번 리뷰
# 16위: 151946번 유저 227번 리뷰
# 17위: 745537번 유저 220번 리뷰
# 18위: 213301번 유저 217번 리뷰
# 19위: 9852번 유저 214번 리뷰
# 20위: 350771번 유저 213번 리뷰

# 안가본 식당
def get_uneaten(ratings, store_list, user_id):
    eaten_store = ratings[ratings['user'] == user_id]['store'].tolist()
    uneaten_store = [store for store in store_list if store not in eaten_store]
    print('평점 매긴 식당 수 : ', len(eaten_store), '추천 대상 식당 수 : ', len(uneaten_store), '전체 식당 수 : ', len(store_list)  )

    return uneaten_store



# 추천 식당 정렬해서 리턴
def recomm_store(algo, user_id, unvisited_store, top_n=35):
    predicitons = []
    predicitons = [algo.predict(user_id, kk) for kk in unvisited_store]
    def sortkey_est(pred):
        return pred.est
    
    predicitons.sort(key=sortkey_est, reverse=True)

    top_predictions = predicitons[:top_n]
    # print(top_predictions)
    top_store_ids = [ int(pred.iid) for pred in top_predictions]
    top_store_rating = [pred.est for pred in top_predictions]

    top_sotre_preds = [ (id, rating) for id, rating in zip(top_store_ids, top_store_rating) ]


    return top_sotre_preds

unvisited_store = get_uneaten(ratings_df, ten_review_store_list, 243883)

top_store_preds = recomm_store(algo, 243883, unvisited_store, top_n=35)
print('#### Top 10 음식점####')
for top_store in top_store_preds:
    print(top_store)

print('결과 툭')