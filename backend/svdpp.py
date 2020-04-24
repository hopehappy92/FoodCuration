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


obj = Review.objects.all().values("user_id", "store_id", "score")
dataset2 = pd.DataFrame(list(obj))
print(dataset2)




# lower_rating = dataset['rating'].min()
# upper_rating = dataset['rating'].max()
# print('Review range: {0} to {1}'.format(lower_rating, upper_rating))
# 점수의 최소 최대값 확인하는부분

# 점수의 범위를 0.5~4로 지정하고 불러온다
# reader = surprise.Reader(rating_scale = {0.5, 4.})
# data = surprise.Dataset.load_from_df(dataset, reader)

reader2 = surprise.Reader()
data2 = surprise.Dataset.load_from_df(dataset2, reader2)


# SVD++ 알고리즘을 적용하겠다.
# alg = surprise.SVDpp()
# output = alg.fit(data.build_full_trainset())
alg2 = surprise.SVDpp()
output2 = alg2.fit(data2.build_full_trainset())

# 유저 50번 영화 52번에 대해서 예측값을 구한다.
# pred = alg.predict(uid='50', iid='52')
# score = pred.est
# print(score)

pred2 = alg2.predict(uid='68632', iid='15')
score2 = pred2.est
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