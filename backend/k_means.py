from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests

request_user = requests.get("http://i02d106.p.ssafy.io:8765/api/user").json()

user_df = pd.DataFrame(data=request_user, columns=['age', 'gender', 'review_count'])

def func(row):
    if row['gender'] == '남':
        return 1
    else:
        return 0

user_df['gender'] = user_df.apply(func, axis=1)
print(user_df.head())

kmeans = KMeans(n_clusters=3, init='k-means++', max_iter=300, random_state=0)
kmeans.fit(user_df)

print(kmeans.labels_[0:20])

user_df['clutser'] = kmeans.labels_
print(user_df.head(n=20))