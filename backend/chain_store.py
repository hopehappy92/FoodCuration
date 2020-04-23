import os
import django
import json
import numpy as np
import pandas as pd
import requests
import pickle

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
 'backend.settings')
django.setup()

# # review가 1개 이상인 식당만 불러옴
request_all_stores = requests.get("http://i02d106.p.ssafy.io:8765/api/all_stores").json()
# request_all_stores = requests.get("http://127.0.0.1:8000/api/all_stores").json()
all_stores_df = pd.DataFrame(data=request_all_stores)

chain_stores = all_stores_df.groupby(["store_name"]).count() >= 40
chain_stores_list = list(chain_stores[chain_stores["id"]==True].index)
# print(chain_stores_list)

# # 모든 review 다 불러옴
request_all_reviews = requests.get("http://i02d106.p.ssafy.io:8765/api/reviews_info").json()
# request_all_reviews = requests.get("http://127.0.0.1:8000/api/reviews_info").json()
all_reviews_df = pd.DataFrame(data=request_all_reviews)

all_reviews_df["reg_time"] = pd.to_datetime(all_reviews_df["reg_time"])
all_reviews_df["years"] = all_reviews_df["reg_time"].dt.year
all_reviews_by_years = all_reviews_df[["store", "years", "score"]]
# print(all_reviews_by_years)

# merge
stores_reviews = pd.merge(
        all_stores_df, all_reviews_by_years, left_on="id", right_on="store"
    )
# print(stores_reviews)
stores_reviews_by_years = stores_reviews[["years", "store_name", "score"]]
# stores_reviews_2016 = stores_reviews_by_years[stores_reviews_by_years["years"]==2016]
# stores_reviews_2017 = stores_reviews_by_years[stores_reviews_by_years["years"]==2017]
# stores_reviews_2018 = stores_reviews_by_years[stores_reviews_by_years["years"]==2018]
# stores_reviews_2019 = stores_reviews_by_years[stores_reviews_by_years["years"]==2019]
stores_reviews_df = stores_reviews_by_years.groupby(["store_name"]).mean()
stores_reviews_df = stores_reviews_df.reset_index()
stores_reviews_df["chain"] = stores_reviews_df["store_name"].isin(chain_stores_list)
chain_top10 = stores_reviews_df[stores_reviews_df["chain"]==True].sort_values(by="score", ascending=False).head(n=10)[["store_name","score"]].reset_index(drop=True)
# print(chain_top10)
score_normal_or_chain = stores_reviews_df[["store_name", "score", "chain"]].groupby(["chain"]).mean()
# print(stores_reviews_df["score"].mean())
score_normal_or_chain.loc["all", "score"] = stores_reviews_df["score"].mean()
score_compare = score_normal_or_chain.reset_index()
print(chain_top10)
print(score_compare)
chain_result_list = [chain_top10, score_compare]

# with open('chain_result_list.p', 'wb') as file:
#     pickle.dump(chain_result_list, file)