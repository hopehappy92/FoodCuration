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
    store = Store.objects.get(id=temp_id)
    all_store = Store.objects.all()
    store_df = pd.DataFrame(all_store.values("id", "longitude", "latitude", "category"))
    min_review = 5
    print('start')
    lon = store.longitude
    lat = store.latitude
    store_df = store_df[store_df["longitude"] - lon < 0.015]
    store_df = store_df[store_df["longitude"] - lon > -0.015]
    store_df = store_df[store_df["latitude"] - lat < 0.015]
    store_df = store_df[store_df["latitude"] - lat > -0.015]
    store_df = store_df[store_df.apply(lambda x: 6371*acos(cos(radians(lat))*cos(radians(x["latitude"]))*cos(radians(x["longitude"])-radians(lon))+sin(radians(lat))*sin(radians(x["latitude"]))), axis=1) < 1][["id", "category"]]
    print('===')
    a = []
    store_category_set = set(store.category.split('|'))
    for categories in store_df["category"]:
        cnt = 0
        for category in categories.split('|'):
            if category in store_category_set:
                cnt += 1
        a.append(cnt)
    store_df['count'] = a
    print('카테고리 for문 완료')
    # 필요한 review들만 가져옴
    review_df = pd.DataFrame(Review.objects.all().values("user_id", "score", "store_id"))
    review_df = review_df[review_df['store_id'].isin(set(store_df['id']))]

    review_df = review_df.groupby('store_id').agg(['sum', 'count', 'mean'])['score']
    a = sum(review_df['sum'])/sum(review_df['count'])

    # 인기도 고려한 평점 계산
    review_df['calc'] = review_df.apply(lambda x: ((x['count']/(x['count']+min_review))*x['mean'] + (min_review/(x['count']+min_review))*a), axis=1)
    
    # store_df = pd.merge(user_df["cluster"], review_df, left_index=True, right_on="user_id")
    print(store_df)
    print(store_df[["id", "count"]])
    print(review_df["calc"])
    store_df = pd.merge(store_df[["id", "count"]], review_df["calc"], right_index=True, left_on="id", how='outer').set_index('id')

    store_df['calc'] = store_df['calc'].fillna(0.0)
    # 카테고리 일치 개수, 인기도 고려한 평점 순 정렬
    store_df.sort_values(by=['count', 'calc'], inplace=True, ascending=False)

    return store_df.index[:20]

print(recoNearStroe(124164))













