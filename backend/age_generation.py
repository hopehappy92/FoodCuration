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
# df_09 = csv_data_09[(csv_data_09["가맹점_시도명"] == "서울") & ((csv_data_09["성별"] == "1.남성") | (csv_data_09["성별"] == "2.여성"))][["가맹점_시군구명", "성별", "연령", "승인시간대1", "가맹점업종코드", "결제금액"]]
# df_10 = csv_data_10[(csv_data_10["가맹점_시도명"] == "서울") & ((csv_data_10["성별"] == "1.남성") | (csv_data_10["성별"] == "2.여성"))][["가맹점_시군구명", "성별", "연령", "승인시간대1", "가맹점업종코드", "결제금액"]]
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

# # 읽기
# with open('df_age_generation.p', 'rb') as file:
#     df_all = pickle.load(file)
# print('읽어왔다')


# def get_people(df_all, age, divider):
    
#     gen_df = df_all[df_all['generation']==age]
#     sum = 0

#     food_df = gen_df[((gen_df['type_code']>2001) & (gen_df['type_code']<2200)) | ((gen_df['type_code']>2400) & (gen_df['type_code']<2500))]
#     sum +=int(food_df["all_payment"].sum())
#     print('--------food 정보 출력 완료')

#     living_df = gen_df[((gen_df['type_code']>3000) & (gen_df['type_code']<3500)) | ((gen_df['type_code']>6100) & (gen_df['type_code']<6111)) | ((gen_df['type_code']>1100) & (gen_df['type_code']<1200))]
#     sum +=int(living_df["all_payment"].sum())
#     print('--------living 정보 출력 완료')

#     fashion_df = gen_df[((gen_df['type_code']>1000) & (gen_df['type_code']<1100)) | ((gen_df['type_code']>1200) & (gen_df['type_code']<1300))]
#     sum +=int(fashion_df["all_payment"].sum())
#     print('--------fashion 정보 출력 완료')

#     car_df = gen_df[((gen_df['type_code']>5500) & (gen_df['type_code']<5700))]
#     sum +=int(car_df["all_payment"].sum())
#     print('-----------자동차 주유 정보 출력 완료')

#     edu_df = gen_df[((gen_df['type_code']>8106) & (gen_df['type_code']<8200)) | ((gen_df['type_code']>6113) & (gen_df['type_code']<6200))]
#     sum +=int(edu_df["all_payment"].sum())
#     print('-------------교육비 정보 출력 완료')

#     taxi_df = gen_df[(gen_df['type_code']==5306)]
#     sum +=int(taxi_df["all_payment"].sum())
#     print('------------택시비 출력 완료')

#     travel_df = gen_df[((gen_df['type_code']>5000) & (gen_df['type_code']<5306)) | ((gen_df['type_code']>5306) & (gen_df['type_code']<5405))]
#     sum +=int(travel_df["all_payment"].sum())
#     print('------------여행 및 숙박 정보 출력 완료')

#     call_df = gen_df[(gen_df['type_code']==8212)]
#     sum +=int(call_df["all_payment"].sum())
#     print('-----------통신비 정보 출력 완료')

#     charge_df = gen_df[((gen_df['type_code']>8000) & (gen_df['type_code']<8100)) | ((gen_df['type_code']>8205) & (gen_df['type_code']<8222))]
#     sum +=int(charge_df["all_payment"].sum())
#     print('---------- 세금 및 기타 요금 출력 완료')

#     medical_df = gen_df[((gen_df['type_code']>7000) & (gen_df['type_code']<7100))]
#     sum +=int(medical_df["all_payment"].sum())
#     print('-------------- 의료 정보 출력 완료')

#     beauty_df = gen_df[((gen_df['type_code']>7100) & (gen_df['type_code']<7200))]
#     sum +=int(beauty_df["all_payment"].sum())
#     print('-------------- 미용 정보 출력 완료')

#     hobby_df = gen_df[((gen_df['type_code']>6000) & (gen_df['type_code']<6300))]
#     sum +=int(hobby_df["all_payment"].sum())
#     print('-------------- 취미 정보 출력 완료')

#     nightlife_df = gen_df[(gen_df['type_code']==2299) | (gen_df['type_code']==2312) | (gen_df['type_code']==2317) | (gen_df['type_code']==4113) | (gen_df['type_code']==7104) | (gen_df['type_code']==7299)]
#     sum +=int(nightlife_df["all_payment"].sum())
#     print('---------------  유흥 정보 출력 완료')

#     sum /= divider
#     return int(sum)

# print(get_people(df_all, '2.20대', 1222000))
# print(get_people(df_all, '3.30대', 2023000))
# print(get_people(df_all, '4.40대', 2379000))
# print(get_people(df_all, '5.50대', 2135000))

# get_people로 추측한 추정 이용 고객 수입니다.
# list = [280224, 246964, 290639, 310272]


# def get_portion(df_all, age, people):
#     list = []
#     gen_df = df_all[df_all['generation']==age]

#     food_df = gen_df[((gen_df['type_code']>2001) & (gen_df['type_code']<2200)) | ((gen_df['type_code']>2400) & (gen_df['type_code']<2500))]
#     list.append(int(food_df["all_payment"].sum()/people))

#     living_df = gen_df[((gen_df['type_code']>3000) & (gen_df['type_code']<3500)) | ((gen_df['type_code']>6100) & (gen_df['type_code']<6111)) | ((gen_df['type_code']>1100) & (gen_df['type_code']<1200))]
#     list.append(int(living_df["all_payment"].sum()/people))

#     fashion_df = gen_df[((gen_df['type_code']>1000) & (gen_df['type_code']<1100)) | ((gen_df['type_code']>1200) & (gen_df['type_code']<1300))]
#     list.append(int(fashion_df["all_payment"].sum()/people))

#     car_df = gen_df[((gen_df['type_code']>5500) & (gen_df['type_code']<5700))]
#     list.append(int(car_df["all_payment"].sum()/people))

#     edu_df = gen_df[(((gen_df['type_code']>8106) & (gen_df['type_code']<8200)) | ((gen_df['type_code']>6113) & (gen_df['type_code']<6200)))]
#     list.append(int(edu_df["all_payment"].sum()/people))
    
#     taxi_df = gen_df[(gen_df['type_code']==5306)]
#     list.append(int(taxi_df["all_payment"].sum()/people))

#     travel_df = gen_df[((gen_df['type_code']>5000) & (gen_df['type_code']<5306)) | ((gen_df['type_code']>5306) & (gen_df['type_code']<5405))]
#     list.append(int(travel_df["all_payment"].sum()/people))

#     call_df = gen_df[(gen_df['type_code']==8212)]
#     list.append(int(call_df["all_payment"].sum()/people))

#     insurance_df = gen_df[(gen_df['type_code']>8000) & (gen_df['type_code']<8100)]
#     list.append(int(insurance_df["all_payment"].sum()/people))

#     charge_df = gen_df[((gen_df['type_code']>8205) & (gen_df['type_code']<8216)) | ((gen_df['type_code']>8216) & (gen_df['type_code']<8222))]
#     list.append(int(charge_df["all_payment"].sum()/people))

#     medical_df = gen_df[((gen_df['type_code']>7000) & (gen_df['type_code']<7100))]
#     list.append(int(medical_df["all_payment"].sum()/people))

#     beauty_df = gen_df[((gen_df['type_code']>7100) & (gen_df['type_code']<7200))]
#     list.append(int(beauty_df["all_payment"].sum()/people))

#     hobby_df = gen_df[((gen_df['type_code']>6000) & (gen_df['type_code']<6300))]
#     list.append(int(hobby_df["all_payment"].sum()/people))

#     nightlife_df = gen_df[(gen_df['type_code']==2299) | (gen_df['type_code']==2312) | (gen_df['type_code']==2317) | (gen_df['type_code']==4113) | (gen_df['type_code']==7104) | (gen_df['type_code']==7299)]
#     list.append(int(nightlife_df["all_payment"].sum()/people))


#     return list

# columns = ['식생활', '생활용품', '패션잡화' , '자동차/주유', '교육비', '택시비', '여행 및 숙박', '통신비', '보힘료', '세금 및 기타 요금', '의료', '미용', '취미', '유흥']

# row1 = get_portion(df_all, '2.20대', 280224)
# row2 = get_portion(df_all, '3.30대', 246964)
# row3 = get_portion(df_all, '4.40대', 290639)
# row4 = get_portion(df_all, '5.50대', 310272)

# print(row1)

# c_row1 = [i/12220 for i in row1]
# c_row2 = [i/20230 for i in row2]
# c_row3 = [i/23790 for i in row3]
# c_row4 = [i/21350 for i in row4]

# dataframe = pd.DataFrame([row1, row2, row3, row4], columns=columns)
# portion_dataframe = pd.DataFrame([c_row1, c_row2, c_row3, c_row4], columns=columns)

# print(list(dataframe.loc[0]))
# print(portion_dataframe)

# generations = [0 for i in range(4)]
# count1 = 0
# count2 = 0
# count3 = 0
# count4 = 0
# # for i in range(4):
# for i in range(4):
#     generations[i] = {}
# print(type(generations[0]))
# for j in range(14):
#     t = (j+10)%14
#     if j==13:
#         generations[0][columns[t]] = [row1[t], round(100-count1,1)]
#         generations[1][columns[t]] = [row2[t], round(100-count2,1)]
#         generations[2][columns[t]] = [row3[t], round(100-count3,1)]
#         generations[3][columns[t]] = [row4[t], round(100-count4,1)]
#     else:
#         count1 += round(c_row1[t],1)
#         count2 += round(c_row2[t],1)
#         count3 += round(c_row3[t],1)
#         count4 += round(c_row4[t],1)
#         generations[0][columns[t]] = [row1[t], round(c_row1[t],1)]
#         generations[1][columns[t]] = [row2[t], round(c_row2[t],1)]
#         generations[2][columns[t]] = [row3[t], round(c_row3[t],1)]
#         generations[3][columns[t]] = [row4[t], round(c_row4[t],1)]

# dic = {}
# dic['20대'] = generations[0]
# dic['30대'] = generations[1]
# dic['40대'] = generations[2]
# dic['50대'] = generations[3]

# # 쓰기
# with open('df_age_generation.p', 'wb') as file:
#     pickle.dump(dic, file)


# 읽기
with open('df_age_generation.p', 'rb') as file:
    dic = pickle.load(file)
print('읽어왔다')
print(dic)
