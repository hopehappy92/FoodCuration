import pandas as pd
import pickle
import plotly.graph_objs as go
from plotly import tools

# # 2019-09.csv 불러오기 
# csv_data_09 = pd.read_csv('../../data/2019-09.csv', encoding = 'CP949', 
# dtype={
#     "회원_시도명": str, 
#     "회원_시군구명": str,
#     "개인기업구분": str,
#     "성별": str,
#     "연령": str,
#     "매출년월일": str,
#     "가맹점_시도명": str,
#     "가맹점_시군구명": str,
#     "가맹점_읍면동명": str,
#     })
# # 2019-10.csv 불러오기
# csv_data_10 = pd.read_csv('../../data/2019-10.csv', encoding = 'CP949', 
# dtype={
#     "회원_시도명": str, 
#     "회원_시군구명": str,
#     "개인기업구분": str,
#     "성별": str,
#     "연령": str,
#     "매출년월일": str,
#     "가맹점_시도명": str,
#     "가맹점_시군구명": str,
#     "가맹점_읍면동명": str,
#     })

# # 컬럼값 처리, 서울로 필터링
# df_09 = csv_data_09[(csv_data_09["가맹점_시도명"] == "서울")][["가맹점_시군구명", "성별", "연령", "승인시간대1", "가맹점업종코드", "결제금액"]]
# df_10 = csv_data_10[(csv_data_10["가맹점_시도명"] == "서울")][["가맹점_시군구명", "성별", "연령", "승인시간대1", "가맹점업종코드", "결제금액"]]
# df_all = pd.concat([df_09, df_10])


# # row 수 확인
# print("9월 데이터 row 수: ", len(df_09)) # 4887435
# print("10월 데이터 row 수: ", len(df_10)) # 5191326
# print("전체 데이터 row 수: ", len(df_all)) # 10078761


# # 컬럼명 변경
# df_all = df_all.rename(
#     columns= {
#         '가맹점_시군구명': 'city',
#         '성별': 'gender',
#         '연령': 'generation',
#         '승인시간대1': 'time',
#         '가맹점업종코드': 'type_code',
#         '결제금액': 'all_payment' })

# # 쓰기
# with open('df_age_generation.p', 'wb') as file:
#     pickle.dump(df_all, file)


# 통계청 정보에 따르면 2017년 소비자 평균 소비액은 아래와 같음
# 20대 : 122.2만원
# 30대 : 202.3만원
# 40대 : 237.9만원
# 50대 : 213.5만원

# 기업하고 기타 뺴야됨

# 읽기
with open('df_age_generation.p', 'rb') as file:
    df_all = pickle.load(file)
print('읽어왔다')

twenties_df = df_all
# twenties_df = df_all[df_all['generation']=='2.20대']
# print(twenties_df)
print('--------20대 정보 출력 완료')




# food_df = twenties_df[((twenties_df['type_code']>2001) & (twenties_df['type_code']<2200)) | ((twenties_df['type_code']>2400) & (twenties_df['type_code']<2500))]
# print(food_df)
# print('--------food 정보 출력 완료')


# living_df = twenties_df[((twenties_df['type_code']>3000) & (twenties_df['type_code']<3500)) | ((twenties_df['type_code']>6100) & (twenties_df['type_code']<6111)) | ((twenties_df['type_code']>1100) & (twenties_df['type_code']<1200))]
# print(living_df)
# print('--------living 정보 출력 완료')

# fashion_df = twenties_df[((twenties_df['type_code']>1000) & (twenties_df['type_code']<1100)) | ((twenties_df['type_code']>1200) & (twenties_df['type_code']<1300))]
# print(fashion_df)
# print('--------fashion 정보 출력 완료')

# car_df = twenties_df[((twenties_df['type_code']>5500) & (twenties_df['type_code']<5700))]
# print(car_df)
# print('-----------자동차 주유 정보 출력 완료')

# edu_df = twenties_df[((twenties_df['type_code']>8106) & (twenties_df['type_code']<8200)) | ((twenties_df['type_code']>6113) & (twenties_df['type_code']<6200))]
# print(edu_df)
# print('-------------교육비 정보 출력 완료')

# travel_df = twenties_df[((twenties_df['type_code']>5000) & (twenties_df['type_code']<5405))]
# print(travel_df)
# print('------------여행 및 숙박 정보 출력 완료')

# call_df = twenties_df[(twenties_df['type_code']==8212)]
# print(call_df)
# print('-----------통신비 정보 출력 완료')

# charge_df = twenties_df[((twenties_df['type_code']>8000) & (twenties_df['type_code']<8100)) | ((twenties_df['type_code']>8205) & (twenties_df['type_code']<8222))]
# print(charge_df)
# print('---------- 세금 및 기타 요금 출력 완료')

# medical_df = twenties_df[((twenties_df['type_code']>7000) & (twenties_df['type_code']<7100))]
# print(medical_df)
# print('-------------- 의료 정보 출력 완료')

# beauty_df = twenties_df[((twenties_df['type_code']>7100) & (twenties_df['type_code']<7200))]
# print(beauty_df)
# print('-------------- 의료 정보 출력 완료')

# hobby_df = twenties_df[((twenties_df['type_code']>6000) & (twenties_df['type_code']<6300))]
# print(hobby_df)
# print('-------------- 의료 정보 출력 완료')

nightlife_df = twenties_df[(twenties_df['type_code']==2299) | (twenties_df['type_code']==2312) | (twenties_df['type_code']==2317) | (twenties_df['type_code']==4113) | (twenties_df['type_code']==7104) | (twenties_df['type_code']==7299)]
print(nightlife_df)
print('---------------  유흥 정보 출력 완료')













# young_meal_df = df_all[(df_all['type_code'] != 2004) & ((df_all['generation'] == '2.20대') | (df_all['generation'] == '3.30대'))][['time', 'all_payment']]
# old_meal_df = df_all[(df_all['type_code'] != 2004) & ((df_all['generation'] == '4.40대') | (df_all['generation'] == '5.50대'))][['time', 'all_payment']]

# print('----------평균 밥값---------')
# young_breakfast_df = young_meal_df[(young_meal_df['time']>5) & (young_meal_df['time']<11)]['all_payment']
# young_breakfast_df = young_breakfast_df.sum()
# print(int(young_breakfast_df[0] / young_breakfast_df[1]))
# young_lunch_df = young_meal_df[(young_meal_df['time']>10) & (young_meal_df['time']<15)]['all_payment']
# young_lunch_df = young_lunch_df.sum()
# print(int(young_lunch_df[0] / young_lunch_df[1]))
# young_dinner_df = young_meal_df[(young_meal_df['time']>16) & (young_meal_df['time']<21)]['all_payment', 'customers']
# young_dinner_df = young_dinner_df.sum()
# print(int(young_dinner_df[0] / young_dinner_df[1]))
# print('--------------------------')


# young_desert_df = df_all[(df_all['type_code'] == 2004) & ((df_all['generation'] == '2.20대') | (df_all['generation'] == '3.30대'))][['all_payment', 'customers']]
# old_desert_df = df_all[(df_all['type_code'] == 2004) & ((df_all['generation'] == '4.40대') | (df_all['generation'] == '5.50대'))][['all_payment', 'customers']]
# young_desert_df = young_desert_df.sum()
# old_desert_df = old_desert_df.sum()
# print('----------------')
# print(int(young_desert_df[0] / young_desert_df[1]))
# print(int(old_desert_df[0] / old_desert_df[1]))

