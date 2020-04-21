import os
import django
import json
import numpy as np
import pandas as pd
import surprise 
import requests
from math import sqrt
from surprise.model_selection import cross_validate

from surprise import KNNBaseline
from surprise import SVD, Dataset, accuracy, Reader
from surprise.model_selection import train_test_split
from surprise.dataset import DatasetAutoFolds
from surprise.model_selection import GridSearchCV

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
 'backend.settings')
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

print(1234)
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
print(ratings_df.shape)
print(1234)

# reader => 범위 설정  & 학습 부분
reader = Reader(rating_scale=(1, 5))
review_data = surprise.Dataset.load_from_df(df=ratings_df, reader=reader)
trainset = review_data.build_full_trainset()

knn_gs = cross_validate(KNNBaseline(), review_data, cv=5, n_jobs=5, verbose=False)
param_grid = {'k': [10, 20, 30, 40, 50, 60]}
knn_gs = GridSearchCV(KNNBaseline, param_grid, measures=['rmse', 'mae'], cv=5, n_jobs=5)
knn_gs.fit(review_data)
print(knn_gs.cv_results)
print(knn_gs.cv_results['mean_test_rmse'])
print(knn_gs.cv_results['mean_test_mae'])
print('학습 시작')
# 피어슨 유사도로 학습
sim_options = {'name': 'pearson', 'user_based': True}
algo = surprise.KNNBaseline(k=30, sim_options=sim_options)
algo.fit(trainset)
print('학습 완료')

# 안가본 식당
def get_uneaten(ratings, store_list, user_id):
    eaten_store = ratings[ratings['user'] == user_id]['store'].tolist()
    uneaten_store = [store for store in store_list if store not in eaten_store]
    print('평점 매긴 식당 수 : ', len(eaten_store), '추천 대상 식당 수 : ', len(uneaten_store), '전체 식당 수 : ', len(store_list)  )

    return uneaten_store



# 추천 식당 정렬해서 리턴
def recomm_store(algo, user_id, unvisited_store, top_n=10):
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

top_store_preds = recomm_store(algo, 243883, unvisited_store)
print('#### Top 10 음식점####')
for top_store in top_store_preds:
    print(top_store)

print('결과 툭')