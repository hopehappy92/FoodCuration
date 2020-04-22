import os
import django
import json
import numpy as np
import pandas as pd
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
 'backend.settings')
django.setup()

# # review가 1개 이상인 식당만 불러옴
# request_all_reviews = requests.get("http://i02d106.p.ssafy.io:8765/api/all_stores").json()
request_all_stores = requests.get("http://127.0.0.1:8000/api/all_stores").json()
all_stores_df = pd.DataFrame(data=request_all_stores)

chain_stores = all_stores_df.groupby(["store_name"]).count() >= 50
chain_stores_list = list(chain_stores[chain_stores["id"]==True].index)
# print(all_stores_df)

# # 모든 review 다 불러옴
# request_all_reviews = requests.get("http://i02d106.p.ssafy.io:8765/api/reviews_info").json()
request_all_reviews = requests.get("http://127.0.0.1:8000/api/reviews_info").json()
all_reviews_df = pd.DataFrame(data=request_all_reviews)

all_reviews_df["reg_time"] = pd.to_datetime(all_reviews_df["reg_time"])
all_reviews_df["years"] = all_reviews_df["reg_time"].dt.year
all_reviews_by_years = all_reviews_df[["store", "years", "score"]]
# print(all_reviews_by_years)

stores_reviews = pd.merge(
        all_stores_df, all_reviews_by_years, left_on="id", right_on="store"
    )
print(stores_reviews)
# print(stores_reviews[["years", "store_name", "score"]].groupby(["store_name"]).mean())
