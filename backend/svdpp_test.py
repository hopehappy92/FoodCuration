import surprise
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

import numpy as np
import pandas as pd
import urllib
import io
import zipfile
from api.models import Review
from django_pandas.io import read_frame

# tmpFile = urllib.request.urlopen('https://www.librec.net/datasets/filmtrust.zip')
# tmpFile = zipfile.ZipFile(io.BytesIO(tmpFile.read()))
# dataset = pd.read_table(io.BytesIO(tmpFile.read('ratings.txt')), sep = ' ', names = ['uid', 'iid', 'rating'])
# tmpFile.close()
# dataset.head()
# print(dataset.head())
# 희소행렬 형태로 데이터가 저장되어 있음. sparse
#    uid  iid  rating
# 0    1    1     2.0
# 1    1    2     4.0
# 2    1    3     3.5
# 3    1    4     3.0
# 4    1    5     4.0

# 모든 데이터가 아니라 관계 있는 데이터만 가져온다.
# 어떤 유저가 작성한 리뷰에 해당하는 매장
# user_id = 68632
user_id = 115682
df = pd.DataFrame(list(Review.objects.filter(user_id=user_id).values("store")))
print(df)
stores = df['store'].unique()
# 그 매장에 리뷰들 전부 다
df2 = pd.DataFrame(columns=("user_id", "store_id", "score"))
reviews = []
idx = 0
for store in stores:
    for review in Review.objects.filter(store_id=store).values("user", "store", "score"):
        df2.loc[idx] = list(review.values())
        idx += 1
# df2 = pd.DataFrame(list(reviews))
print(df2)
reader = surprise.Reader()
data = surprise.Dataset.load_from_df(df2, reader)
alg = surprise.SVDpp()
output = alg.fit(data.build_full_trainset())

print(df2["store_id"])
for store_id in df2["store_id"].unique():
    print(store_id, alg.predict(uid=user_id, iid=store_id).est)
pred = alg2.predict(uid='68632', iid='15')
score = pred2.est
print(score2)

# 50번 유저에 대해서 50번 유저가 보지 않은 모든 영화에 대한 점수 예측값을 구한다.
# 이미 시청한 영화는 추천 X
# iids = dataset['iid'].unique()
# iids50 = dataset.loc[dataset['uid'] == 50, 'iid']

store_ids = dataset2['store_id'].unique()
store_ids50 = dataset2.loc[dataset2['user_id'] == 68632, 'store_id']

# 모든 영화 iids에서 50번 유저가 본 영화 iids50을 제외한 결과가 iids_to_pred이다
# iids_to_pred = np.setdiff1d(iids, iids50)

store_ids_to_pred = np.setdiff1d(store_ids, store_ids50)

# 테스트셋을 해당 유저, 영화들 임의평점 4로 입력한 후 예측한 결과를 본다.
# testset = [[50, iid, 4.] for iid in iids_to_pred]
# predictions = alg.test(testset)
# print(predictions[0])

# print(predictions)

testset2 = [[68632, store_id, 0.] for store_id in store_ids_to_pred]
predictions2 = alg2.test(testset2)
predictions2.sort(key = lambda x: x[3], reverse=True)
print(predictions2)
print(predictions2[0])
print(predictions2[-1])

# pred_ratings = np.array([pred.est for pred in predictions])
# i_max = pred_ratings.argmax()
# iid = iids_to_pred[i_max]
# print('Top item for user 50 has iid {0} with predicted rating {1}'.format(iid, pred_ratings[i_max]))

pred_ratings2 = np.array([pred.est for pred in predictions2])
# print(pred_ratings2)
i_max2 = pred_ratings2.argmax()
iid2 = store_ids_to_pred[i_max2]
print('Top item for user 68632 has iid {0} with predicted rating {1}'.format(iid2, pred_ratings2[i_max2]))



# param_grid = {'lr_all': [.001, .01], 'reg_all': [.1, .5]}
# gs = surprise.model_selection.GridSearchCV(surprise.SVDpp, param_grid, measures=['rmse', 'mae'], cv=3)
# gs.fit(data)
# print(gs.best_params['rmse'])

# alg = surprise.SVDpp(lr_all = .001)
# output = surprise.model_selection.cross_validate(alg, data, verbose = True)
# print(output)

param_grid = {'lr_all': [.001, .01], 'reg_all': [.1, .5]}
# 추천성능 평가기준 rmse: root mean squared error (오차 제곱의 합 평균)
# mae: mean absolute error (오차 절대값의 합 평균)
# fcp: fraction of concordant pairs (number of concordant pairs/number of discordant pairs)
gs = surprise.model_selection.GridSearchCV(surprise.SVDpp, param_grid, measures=['rmse', 'mae'], cv=3)
gs.fit(data2)
print(gs.best_params['rmse'])

alg2 = surprise.SVDpp(lr_all = .001)
output2 = surprise.model_selection.cross_validate(alg2, data2, verbose = True)
print(output2)