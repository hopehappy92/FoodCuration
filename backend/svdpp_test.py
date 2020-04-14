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
from api.models import Review, CustomUser, Store
from django_pandas.io import read_frame

import pickle

with open('svdpp.p', 'rb') as file:    # james.p 파일을 바이너리 읽기 모드(rb)로 열기
    alg2 = pickle.load(file)
# user_id = 68632
user_id = 7
df = pd.DataFrame(columns=("user_id", "store_id", "score"))
# a = Review.objects.all()
# df = pd.DataFrame(list(a.values("user_id", "store_id", "score")))
# 내 리뷰 가져오기
for review in CustomUser.objects.get(id=user_id).review_set.all():
    # 이 리뷰의 매장 번호에 해당하는 매장의 리뷰들 가져오기
    # print(review.store_id)
    for review in Store.objects.get(id=review.store_id).review_set.all():
        # 이 리뷰 작성자들의 모든 리뷰 가져오기
        for review in CustomUser.objects.get(id=review.user_id).review_set.all():
            df.loc[review.id] = [review.user_id, review.store_id, review.score]
print(df)


print("---------------")
reader = surprise.Reader()
data = surprise.Dataset.load_from_df(df, reader)
alg = surprise.SVDpp()
output = alg.fit(data.build_full_trainset())
print("---------------")

print(df["store_id"])
cnt = 0
for store_id in df["store_id"].unique():
    print(store_id, alg.predict(uid=user_id, iid=store_id).est)
    print(user_id, store_id)
    a = Review.objects.filter(user=user_id).filter(store=store_id)
    if a:
        print(store_id, a[0].score)
        cnt += 1
        if cnt > 10:
            break
    print("---")

with open('svdpp.p', 'wb') as file:    # james.p 파일을 바이너리 쓰기 모드(wb)로 열기
    pickle.dump(alg, file)

print(dir(alg))
print(alg)

print(Review.objects.filter(user_id=user_id).values('store', 'score'))

print(alg2.predict(uid=7, iid=248259).est)
print(alg2.predict(uid=7, iid=248259).est)
print(alg2.predict(uid=7, iid=248259).est)
print(alg2.predict(uid=7, iid=248259).est)
print(alg2.estimate(u=7, i=248259))
print(alg2.estimate(u=7, i=248259))
print(alg2.estimate(u=7, i=248259))
# 50번 유저에 대해서 50번 유저가 보지 않은 모든 영화에 대한 점수 예측값을 구한다.
# 이미 시청한 영화는 추천 X
# iids = dataset['iid'].unique()
# # iids50 = dataset.loc[dataset['uid'] == 50, 'iid']

# store_ids = dataset2['store_id'].unique()
# store_ids50 = dataset2.loc[dataset2['user_id'] == 68632, 'store_id']

# 모든 영화 iids에서 50번 유저가 본 영화 iids50을 제외한 결과가 iids_to_pred이다
# iids_to_pred = np.setdiff1d(iids, iids50)


# 테스트셋을 해당 유저, 영화들 임의평점 4로 입력한 후 예측한 결과를 본다.
# testset = [[50, iid, 4.] for iid in iids_to_pred]
# predictions = alg.test(testset)
# print(predictions[0])

# print(predictions)
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
