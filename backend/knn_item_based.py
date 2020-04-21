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

# # review가 10개 이상인 식당만 불러옴
# request_store = requests.get("http://i02d106.p.ssafy.io:8765/api/store/10").json()
# # review가 10개 이상인 유저만 불러옴
# request_user = requests.get("http://i02d106.p.ssafy.io:8765/api/user").json()
# 모든 review 다 불러옴


request_all_review = requests.get("http://i02d106.p.ssafy.io:8765/api/reviews").json()
print(type(request_all_review))
# ten_review_store_df = pd.DataFrame(data=request_store)
# ten_review_user_df = pd.DataFrame(data=request_user)
# all_user_df = pd.DataFrame(data=request_all_review)
# print('데이터 불러오기 완료')
# ten_review_store_list = set()
# ten_review_user_list = set()

# print(1234)
# for store in request_store:
#     ten_review_store_list.add(store['id'])
# for user in request_user:
#     ten_review_user_list.add(user['id'])

# selected_review_list = list()
# for dic in request_all_review:
#     if('score' in dic.keys() and 'user' in dic.keys() and 'store' in dic.keys()):
#         if(dic['user'] in ten_review_user_list and dic['store'] in ten_review_store_list):
#             selected_review_list.append(dic)

# ratings_df = pd.DataFrame(selected_review_list)
# ratings_df = ratings_df[['store', 'user', 'score']]
# print(ratings_df.shape)
# print(1234)
request_all_review = pd.DataFrame(request_all_review)
reader = Reader(rating_scale=(1, 5))
request_all_review = surprise.Dataset.load_from_df(df=request_all_review, reader=reader)
trainset = request_all_review.build_full_trainset()
sim_options = {'name': 'pearson_baseline', 'user_based': False}
algo = KNNBaseline(sim_options=sim_options)
algo.fit(trainset)

print('완료')



# Read the mappings raw id <-> movie name
rid_to_name, name_to_rid = read_item_names()

# Retrieve inner id of the movie Toy Story
toy_story_raw_id = name_to_rid['Toy Story (1995)']
toy_story_inner_id = algo.trainset.to_inner_iid(toy_story_raw_id)

# Retrieve inner ids of the nearest neighbors of Toy Story.
toy_story_neighbors = algo.get_neighbors(toy_story_inner_id, k=10)

# Convert inner ids of the neighbors into names.
toy_story_neighbors = (algo.trainset.to_raw_iid(inner_id)
                       for inner_id in toy_story_neighbors)
toy_story_neighbors = (rid_to_name[rid]
                       for rid in toy_story_neighbors)

print()
print('The 10 nearest neighbors of Toy Story are:')
for movie in toy_story_neighbors:
    print(movie)















