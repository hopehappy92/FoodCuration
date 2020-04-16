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

from pprint import pprint
import math

# review가 10개 이상인 식당만 불러옴
request_store = requests.get("http://i02d106.p.ssafy.io:8765/api/store/10").json()
# review가 10개 이상인 유저만 불러옴
request = requests.get("http://i02d106.p.ssafy.io:8765/api/user").json()
request_all_review = requests.get("http://i02d106.p.ssafy.io:8765/api/reviews").json()
qs1= pd.DataFrame(data=request_store)
qs3= Review.objects.all()

ten_review_store_list= []
human_list = []
for user in request:
    human_list.append(user['id'])
# print(len(request))
for store in request_store:
    ten_review_store_list.append(store['id'])

review_list = list(qs3.values())
store_list = []
for dic in review_list:
    if('score' in dic.keys() and 'user_id' in dic.keys() and 'store_id' in dic.keys()):
        if(dic['user_id'] in human_list and dic['store_id'] in ten_review_store_list):
            store_list.append(dic['store_id'])
store_list = list(dict.fromkeys(store_list))
# print(len(store_list))
# print(store_list[0])
# print(store_list[1])

#리스트로 바꾼 다음 데이터프레임으로 변환
stores = qs1
review = pd.DataFrame(list(qs3.values()))
ratings = review[['user_id', 'store_id', 'score']]
# print(ratings.iloc[0])
# print(ratings.iloc[1])

# reader => 범위 설정  & 학습 부분
reader = Reader(rating_scale=(1, 5))
review_data = DatasetAutoFolds(df=ratings, reader=reader)
trainset = review_data.build_full_trainset()

# 피어슨 유사도로 학습
# sim_options = {'name': 'pearson', 'user_based': True}
# algo = surprise.KNNBasic(k=15, sim_options=sim_options)
# predictions = algo.fit(trainset)

# # rmse = accuracy.rmse(predictions, verbose=True)
# # print(rmse)
# # param_grid = {'n_epochs' : [20, 40, 60], 'n_factors': [50, 100, 200]}

# # gs = GridSearchCV(SVD, param_grid, measures=['rmse', 'mae'], cv=3)
# # gs.fit(data)

# # print(gs.best_score['rmse'])
# # print(gs.best_params['rmse'])

# # 안가본 식당
# def get_uneaten(ratings, store_list, user_id):
#     eaten_store = ratings[ratings['user_id'] == user_id]['store_id'].tolist()
#     uneaten_store = [store for store in store_list if store not in eaten_store]
#     print('평점 매긴 식당 수 : ', len(eaten_store), '추천 대상 식당 수 : ', len(uneaten_store), '전체 식당 수 : ', len(store_list)  )

#     return uneaten_store

# # 추천 식당 정렬해서 리턴
# def recomm_store(algo, user_id, unvisited_store, top_n=10):
#     predicitons = []
    
    
#     predicitons = [algo.predict(str(user_id), str(kk), r_ui=4, verbose=True) for kk in unvisited_store]
#     pre1 = algo.predict(str(user_id), str(86))
#     pre2 = algo.predict(str(user_id), str(149))
#     # print(123)
#     # print(pre1)
#     # print(pre2)
#     # print(predicitons[0])
#     # print(predicitons[1])
#     def sortkey_est(pred):
#         return pred.est
    
#     predicitons.sort(key=sortkey_est, reverse=False)

#     top_predictions = predicitons[:top_n]

#     top_store_ids = [ int(pred.iid) for pred in top_predictions]
#     top_store_rating = [pred.est for pred in top_predictions]

#     top_sotre_preds = [ (id, rating) for id, rating in zip(top_store_ids, top_store_rating) ]


#     return top_sotre_preds

# unvisited_store = get_uneaten(ratings, store_list, 235)

# top_store_preds = recomm_store(algo, 235, unvisited_store, top_n=10)
# print('#### Top 10 음식점####')
# for top_store in top_store_preds:
#     print(top_store)



# algo = SVD(n_factors=50, random_state=0)
# algo.fit(trainset)

# predicitons = algo.test(testset)
# print('type : ', type(predicitons), ' size : ', len(predicitons))
# print('prediction 결과의 최초 5개 추출')
# print(predicitons[:5])


# print([(pred.uid, pred.iid, pred.est) for pred in predicitons[:3]])

# print(accuracy.rmse(predicitons))

# from surprise.model_selection import cross_validate

# algo1 = SVD(random_state=0)
# cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)

# GridSearchCV 이용
# from surprise.model_selection import GridSearchCV
# param_grid = {'n_epochs' : [20, 40, 60], 'n_factors': [50, 100, 200]}

# gs = GridSearchCV(SVD, param_grid, measures=['rmse', 'mae'], cv=3)
# gs.fit(data)

# print(gs.best_score['rmse'])
# print(gs.best_params['rmse'])

# from surprise.model_selection import cross_validate
# cross_validate(algo, data)


# data_folds = DatasetAutoFolds(df=review ,reader=reader)
# full_trainset = data_folds.build_full_trainset()







# user_id = 390564
# uid = str(390564)
# iid = str(1)

# def get_uneaten(review, stores, user_id):
#     eaten_stores = review[review['user_id'] == user_id]['store_id'].tolist()

#     total_stores = stores['id'].tolist()

#     uneaten_store = [store for store in total_stores if store not in eaten_stores]
#     print('평점 매긴 음식점 수: ', len(eaten_stores))

#     return uneaten_store



# def recomm_store(algo, user_id, unvisited_store, top_n=1000):
#     predicitons = [algo.predict(str(user_id), str(store_id)) for store_id in unvisited_store]
#     def sortkey_est(pred):
#         return pred.est
    
#     predicitons.sort(key=sortkey_est, reverse=True)
#     print(len(predicitons))
#     top_predictions = predicitons[449000:450000]

#     top_store_ids = [ int(pred.iid) for pred in top_predictions]
#     top_store_rating = [pred.est for pred in top_predictions]
#     # top_store_titles = stores[stores.store_id.isin(top_store_ids)]['title']

#     top_sotre_preds = [ (id, rating) for id, rating in zip(top_store_ids, top_store_rating) ]

#     return top_sotre_preds

# unvisited_store = get_uneaten(review, stores, 390564)
# print(len(stores))
# print(len(unvisited_store))

# top_store_preds = recomm_store(algo, 390564, unvisited_store, top_n=1000)
# print('#### Top 10 음식점####')
# for top_store in top_store_preds:
#     print(top_store)


# a = trainset.ur
# # print(a)
# tmp = dict()
# for i in range(len(a)):
#     # print(a[i])
#     ttmp = dict()
#     for j in range(len(a[i])):
#         ttmp[a[i][j][0]] = a[i][j][1]
#     # print(ttmp)
#     tmp[i] = ttmp
# pprint(tmp[23])

a = ratings.groupby(["user_id", "store_id"]).mean()
tmp = dict()
ttmp = dict()
check = -1
for i in range(len(a)):
    # check = a.iloc[i].name[0]
    if (check != a.iloc[i].name[0]):
        check = a.iloc[i].name[0]
        tmp[int(a.iloc[i].name[0])-1] = ttmp
        ttmp = dict()
        ttmp[int(a.iloc[i].name[1])] = float(a.iloc[i].score)
    else:
        ttmp[int(a.iloc[i].name[1])] = float(a.iloc[i].score)
# pprint(tmp)


def sim_pearson(data, name1, name2):
    avg_name1 = 0
    avg_name2 = 0
    count = 0
    for movies in data[name1]:
        if movies in data[name2]: #같은 영화를 봤다면
            avg_name1 = data[name1][movies]
            avg_name2 = data[name2][movies]
            count += 1
    if (count != 0):
        avg_name1 = avg_name1 / count
        avg_name2 = avg_name2 / count
        
        sum_name1 = 0
        sum_name2 = 0
        sum_name1_name2 = 0
        count = 0
        for movies in data[name1]:
            if movies in data[name2]: #같은 영화를 봤다면
                sum_name1 += pow(data[name1][movies] - avg_name1, 2)
                sum_name2 += pow(data[name2][movies] - avg_name2, 2)
                sum_name1_name2 += (data[name1][movies] - avg_name1) * (data[name2][movies] - avg_name2)
        if (sum_name1 != 0 and sum_name2 != 0):
            return sum_name1_name2 / (math.sqrt(sum_name1)*math.sqrt(sum_name2))
    return 0

def top_match(data, name, index=3, sim_function=sim_pearson):
    li=[]
    for i in data: #딕셔너리를 돌고
        if name!=i: #자기 자신이 아닐때만
            li.append((sim_function(data,name,i),i)) #sim_function()을 통해 상관계수를 구하고 li[]에 추가
    li.sort() #오름차순
    li.reverse() #내림차순
    return li[:index]

# print(sim_pearson(ratings, 'Dave','Alex'))
# print(top_match(ratings, 'Dave', 3))

def getRecommendation (data, person, k=15, sim_function=sim_pearson):
    
    result = top_match(data, person, k)
    
    score = 0 # 평점 합을 위한 변수
    li = list() # 리턴을 위한 리스트
    score_dic = dict() # 유사도 총합을 위한 dic
    sim_dic = dict() # 평점 총합을 위한 dic

    for sim, name in result: # 튜플이므로 한번에
        print("유사도: ", sim, ", 유저: ", name)
        # print(sim, name)
        if sim < 0 : continue #유사도가 양수인 사람만
        for movie in data[name]: 
            if movie not in data[person]: #name이 평가를 내리지 않은 영화
                score += sim * data[name][movie] # 그사람의 영화평점 * 유사도
                score_dic.setdefault(movie, 0) # 기본값 설정
                score_dic[movie] += score # 합계 구함

                # 조건에 맞는 사람의 유사도의 누적합을 구한다
                sim_dic.setdefault(movie, 0) 
                sim_dic[movie] += sim

            score = 0  #영화가 바뀌었으니 초기화한다
    
    for key in score_dic:
        if sim_dic[key] != 0:
            score_dic[key] = score_dic[key] / sim_dic[key] # 평점 총합/ 유사도 총합
            li.append((score_dic[key],key)) # list((tuple))의 리턴을 위해서.
    li.sort() #오름차순
    li.reverse() #내림차순
    print("############가게별 예상 평점#################")
    print(li)
    return li


print("############################")
getRecommendation(tmp, 950224)
# print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
print(len(tmp[950224]))