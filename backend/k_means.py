from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests

request_user = requests.get("http://i02d106.p.ssafy.io:8765/api/user").json()
request_all_review = requests.get("http://i02d106.p.ssafy.io:8765/api/reviews").json()

# id / age, gender 기준으로 dataframe 분리
user_id = pd.DataFrame(data=request_user, columns=['id'])
user_df = pd.DataFrame(data=request_user, columns=['age', 'gender'])

def func(row):
    if row['gender'] == '남':
        return 5
    else:
        return 0

# gender 값을 정수로 변환
user_df['gender'] = user_df.apply(func, axis=1)
print(user_df.head())

# kmeans 학습
kmeans = KMeans(n_clusters=5, init='k-means++', max_iter=300, random_state=0)
kmeans.fit(user_df)
print('cluster 완료')

# kmeans.labels_ : 몇번 클르서티인지 라벨링 붙이고 분리했었던 id col을 붙임
user_df['clutser'] = kmeans.labels_
user_df['id'] = user_id
print(kmeans.cluster_centers_)

# cluster를 관리하기 위해 set_list를 만듬
set_list = [set(), set(), set(), set(), set()]

# cluster들의 평균을 구하기 위한 list
score_list = [0 for i in range(5)]
count_list = [0 for i in range(5)]

# 빠른 연산을 위해 데이터프레임에 .loc로 넣어주기 휘암
idx0 = 0
idx1 = 0
idx2 = 0
idx3 = 0
idx4 = 0

# cluster로 나누어 review들을 관리할 데이터프레임 생성
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

# cluster에 해당하는 곳에 id값을 넣음
print('id에 따라 그룹 분류중...')
for df in user_df.iterrows():
    set_list[df[1]['clutser']].add(df[1]['id'])

# review들을 모두 확인하면서 48번 라인에 만들었던 dataframe에 넣음
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

# cluster의 평균 구하기
for i in range(5):
    score_list[i] /= count_list[i]

# 데이터프레임에서 인기도와 평점을 고려한 평점 계산기
def knn_grouping(df, nbr):
    grouped = df.groupby('id')
    grouped = grouped.agg(['sum', 'count', 'mean'])
    grouped = grouped['score']

    grouped['calc'] = (grouped['count']/(grouped['count']+3))*grouped['mean'] + (3/(grouped['count']+3))*nbr
    grouped.sort_values(['calc'], ascending=False, inplace=True)
    print(grouped)

    return grouped


# 5가지 그룹별 맛집 순위 -> 저장해야하는 값
group0 = knn_grouping(group0_df, score_list[0])
group1 = knn_grouping(group1_df, score_list[0])
group2 = knn_grouping(group2_df, score_list[0])
group3 = knn_grouping(group3_df, score_list[0])
group4 = knn_grouping(group4_df, score_list[0])

# centroid -> 저쟁해야하는 값
centroid = kmeans.cluster_centers_
print("centroid")
print(centroid)
# 어느  cluster에 속하는지 알려줌
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

# 성별과 나이를 받아서 k_means하기 위한 임시값
temp_gender = '남'
temp_age = 47

# 
cluster = get_cluster(centroid, temp_age, temp_gender)

def get_Top_stores(cluster, n=10):
    if(cluster==0):
        return group0.head()
    elif(cluster==1):
        return group1.head()
    elif(cluster==2):
        return group2.head()
    elif(cluster==3):
        return group3.head()
    elif(cluster==4):
        return group4.head()

result = get_Top_stores(cluster)
print(result)
