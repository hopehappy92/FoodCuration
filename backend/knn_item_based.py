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
from math import acos, cos, sin, radians

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

all_store = Store.objects.all().values("id", "latitude", "longitude", "category")
all_review = Review.objects.all().values("store_id", "score")

new_df = pd.DataFrame(columns=['category', 'store_id'])

near_store = set()
category_set = set()
clat =37.5
clon = 126.9
count = 0
all_store

temp_store_name = 213012
temp_category_set = set()
for store in all_store:
    if(store['id']==temp_store_name):
        categories = store["category"].split("|")
        for category in categories:
            temp_category_set.add(category)

print(len(temp_category_set))
for store in all_store:
    lat = store['latitude']
    lon = store['longitude']
    if 6371*acos(cos(radians(lat))*cos(radians(clat))*cos(radians(clon)-radians(lon))+sin(radians(lat))*sin(radians(clat))) < 1:
        near_store.add(store['id'])
        categories = store["category"].split("|")
        for category in categories:
            category_set.add(category)
            new_df.loc[len(new_df)] = [category, store['id']]

# store에서 category값만 분류
print(len(near_store))
print(near_store)
print(len(category_set))
print(len(new_df))
print(category_set)
near_store_review = list()

for review in all_review:
    if review['store_id'] in near_store:
        near_store_review.append(review)

# 근처에 있는 식당들의 review만 가져옴
print(len(near_store_review))




request_all_review = pd.DataFrame(near_store_review)
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















