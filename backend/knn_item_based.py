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


def recoNearStroe(temp_id):
    # 초기 데이터 받아와
    all_store =pd.DataFrame(Store.objects.all().values("id", "latitude", "longitude", "category"))
    min_review = 5

    # 원하는 id에 해당하는 삭당 정보 받아와
    near_store = pd.DataFrame(columns=["id", 'category', 'category_count', 'calc'])
    temp_store = all_store.loc[all_store['id'] == temp_id]
    temp_store_name = temp_store['id']
    clat = temp_store['latitude'].values[0]
    clon = temp_store['longitude'].values[0]

    # 해당 식당의 카테고리 먼저 가져와
    category_set = set(temp_store['category'].values[0].split('|'))
    
    # 이게 잘 안 먹히네요
    # all_store = all_store.loc[6371*acos(cos(radians(all_store['latitude']))*cos(radians(clat))*cos(radians(clon)-radians(all_store['longitude']))+sin(radians(all_store['latitude']))*sin(radians(clat))) < 1]


    # for문이 속도가 느려 전처리를 좀 했습니다. 정사각형 약 1km반경으로 가져왔습니다
    con1 = (all_store['longitude']<(0.01+clon))
    con2 = ((clon -0.01) <all_store['longitude'])
    con3 = (all_store['latitude']<(0.01+clat))
    con4 = ((clat -0.01) <all_store['latitude'])
    all_store = all_store[con1 & con2 & con3 & con4]

    # 반경 1km 내에 있으면 category 겹치는게 몇개인지 계산
    for i in range(len(all_store)):
        store = all_store.iloc[i]
        lat = store['latitude']
        lon = store['longitude']
        if 6371*acos(cos(radians(lat))*cos(radians(clat))*cos(radians(clon)-radians(lon))+sin(radians(lat))*sin(radians(clat))) < 1:
            if(store['id']==temp_id):
                continue
            categories = store["category"].split('|')
            count = 0
            for c in categories:
                if c in category_set:
                    count += 1
            near_store.loc[len(near_store)] = [store['id'], store['category'], count, 0]

    # 필요한 review들만 가져옴
    review_df = pd.DataFrame(Review.objects.all().values("score", "store_id"))
    review_df = review_df[review_df['store_id'].isin(set(near_store['id']))]

    review_df = review_df.groupby('store_id').agg(['sum', 'count', 'mean'])['score']
    a = sum(review_df['sum'])/sum(review_df['count'])

    # 인기도 고려한 평점 계산
    review_df['calc'] = review_df.apply(lambda x: ((x['count']/(x['count']+min_review))*x['mean'] + (min_review/(x['count']+min_review))*a), axis=1)

    for i in review_df.index:
        val = review_df.loc[i]
        store_calc = val['calc']
        near_store.loc[near_store['id']==i, 'calc'] = store_calc

    # 카테고리 일치 개수, 인기도 고려한 평점 순 정렬
    near_store.sort_values(by=['category_count', 'calc'], inplace=True, ascending=False)

    return near_store

print(recoNearStroe(124164))













