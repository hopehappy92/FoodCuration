from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests

request_store = requests.get("http://i02d106.p.ssafy.io:8765/api/store/10").json()
request_all_review = requests.get("http://i02d106.p.ssafy.io:8765/api/reviews").json()


store_df = pd.DataFrame(data=request_store)
all_review_df = pd.DataFrame(data=request_all_review)

store_df['sum'] = 0
store_df = store_df.set_index('id')
print(store_df.head())

# 조건으로 설정해서 찾으니까 어려워서 index로 변경해버림
for dic in request_all_review:
    if('score' in dic.keys() and 'user' in dic.keys() and 'store' in dic.keys()):
        store_df.loc[dic['store'], 'sum'] += store_df.loc[dic['store'], 'sum'] + dic['score']

print(123)
print(store_df.head(n=15))




