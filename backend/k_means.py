from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests

request_user = requests.get("http://i02d106.p.ssafy.io:8765/api/user").json()
request_all_review = requests.get("http://i02d106.p.ssafy.io:8765/api/reviews").json()

user_id = pd.DataFrame(data=request_user, columns=['id'])
user_df = pd.DataFrame(data=request_user, columns=['age', 'gender'])
# print(user_df.head(n=100))
def func(row):
    if row['gender'] == '남':
        return 5
    else:
        return 0

user_df['gender'] = user_df.apply(func, axis=1)
print(user_df.head())

# kmeans 학습
kmeans = KMeans(n_clusters=5, init='k-means++', max_iter=300, random_state=0)
kmeans.fit(user_df)


print('cluster 완료')
# kmeans.labels_ : 클러스터를 할당시킴
user_df['clutser'] = kmeans.labels_
user_df['id'] = user_id
print(kmeans.cluster_centers_)

# set들의 list 어떻게 만들지
set_list = [set(), set(), set(), set(), set()]
score_list = [0 for i in range(5)]
count_list = [0 for i in range(5)]

# 데이터프레임에 .loc로 넣어주기 휘암
idx0 = 0
idx1 = 0
idx2 = 0
idx3 = 0
idx4 = 0

group0_df = pd.DataFrame(columns=['id', 'score'])
group0_df['score'] = group0_df['score'].astype(float)
group1_df = pd.DataFrame(columns=['id', 'score'])
group1_df['score'] = group1_df['score'].astype(float)
group2_df = pd.DataFrame(columns=['id', 'score'])
group2_df['score'] = group2_df['score'].astype(float)
group3_df = pd.DataFrame(columns=['id', 'score'])
group3_df['score'] = group3_df['score'].astype(float)
group4_df = pd.DataFrame(columns=['id', 'score'])
group4_df['score'] = group4_df['score'].astype(float)


print('id에 따라 그룹 분류중...')

for df in user_df.iterrows():
    set_list[df[1]['clutser']].add(df[1]['id'])

print('개별이 속한 그룹으로 리뷰 분산 진행 중....')
for dic in request_all_review:
    user_id = dic['user']
    store_id = dic['store']
    score = dic['score']
    
    if(score!=1 and score!=2 and score!=3 and score!=4 and score!=5):
        continue
    if user_id in set_list[0]:
        score_list[0] += dic['score']
        count_list[0] += 1
        group0_df.loc[idx1] = [store_id, score]
        idx0 += 1
    elif user_id in set_list[1]:
        score_list[1] += dic['score']
        count_list[1] += 1
        group1_df.loc[idx2] = [store_id, score]
        idx1 += 1
    elif user_id in set_list[2]:
        score_list[2] += dic['score']
        count_list[2] += 1
        group2_df.loc[idx2] = [store_id, score]
        idx2 += 1
    elif user_id in set_list[3]:
        score_list[3] += dic['score']
        count_list[3] += 1
        group3_df.loc[idx2] = [store_id, score]
        idx3 += 1
    elif user_id in set_list[4]:
        score_list[4] += dic['score']
        count_list[4] += 1
        group4_df.loc[idx2] = [store_id, score]
        idx4 += 1
print('분산완료')
group0_df = group0_df.sort_values(by=['score'], axis=0, ascending=True)
group1_df = group1_df.sort_values(by=['score'], axis=0, ascending=True)
group2_df = group2_df.sort_values(by=['score'], axis=0, ascending=True)
group3_df = group3_df.sort_values(by=['score'], axis=0, ascending=True)
group4_df = group4_df.sort_values(by=['score'], axis=0, ascending=True)
print('정렬완료')

for i in range(5):
    score_list[i] /= count_list[i]

for i in range(5):
    print(len(set_list[i]),end=' ')

def knn_grouping(df, nbr):
    grouped = df.groupby('id')
    grouped = grouped.agg(['sum', 'count', 'mean'])
    grouped = grouped['score']

    grouped['calc'] = (grouped['count']/(grouped['count']+3))*grouped['mean'] + (3/(grouped['count']+3))*nbr
    grouped.sort_values(['calc'], ascending=False, inplace=True)
    print(grouped)

    return grouped


# 5가지 그룹별 맛집 순위
knn_grouping(group0_df, score_list[0])
knn_grouping(group1_df, score_list[0])
knn_grouping(group2_df, score_list[0])
knn_grouping(group3_df, score_list[0])
knn_grouping(group4_df, score_list[0])


# 성별과 나이를 받아서 k_means
centroid = kmeans.cluster_centers_
temp_gender = '남'
temp_age = 47
# 나이와 gender를 받아서 뿌려줌

def get_cluster(centroid, age, gender):

    def gender_to_integer(gender):
        if gender=='남':
            return 5
        else:
            return 0

    gtoi = gender_to_integer(gender);

    index = -1
    init_distance = 9999999

    for i in range(5):
        distance = 0
        distance_y = centroid[i][0]
        distance_x = centroid[i][1]

        distance += (distance_y-age)*(distance_y-age) + (distance_x-gtoi)*(distance_x-gtoi)
        if(init_distance<distance):
            init_distance = distance
            index = i


    return index

get_cluster(centroid, temp_age, temp_gender)


