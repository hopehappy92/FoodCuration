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
# df_09 = csv_data_09[csv_data_09["가맹점_시도명"] == "서울"][[
#     "가맹점_시도명", 
#     "가맹점_시군구명",
#     "성별", 
#     "연령", 
#     "승인시간대1", 
#     "결제금액", 
#     "회원수"]]

# df_10 = csv_data_10[csv_data_10["가맹점_시도명"] == "서울"][[
#     "가맹점_시도명", 
#     "가맹점_시군구명",
#     "성별", 
#     "연령", 
#     "승인시간대1", 
#     "결제금액", 
#     "회원수"]]

# # 합치기
# df_all = pd.concat([df_09, df_10])

# # row 수 확인
# # print("9월 데이터 row 수: ", len(df_09)) # 7476758
# # print("10월 데이터 row 수: ", len(df_10)) # 7875424
# # print("전체 데이터 row 수: ", len(df_all)) # 15352182

# # # 컬럼명 변경
# df_all = df_all.rename(
#     columns= {
#         '가맹점_시도명': 'city', 
#         '가맹점_시군구명': 'district', 
#         '성별': 'gender', 
#         '연령': 'age', 
#         '승인시간대1': 'time',
#         '결제금액': 'all_payment',
#         '회원수': 'customers',
#         })

# =======================pickle 사용================================

# 쓰기
# with open('df_district_all.p', 'wb') as file:
#     pickle.dump(df_all, file)

# # 읽기
with open('df_district_all.p', 'rb') as file:
    df_all = pickle.load(file)

# print(df_all)

# 지역별 소비량(결제량) 순위
# df_by_district = df_all.groupby(["district"])[["all_payment", "customers"]].sum()
# df_by_district["payment"] = df_by_district["all_payment"]/df_by_district["customers"]
# df_all_payment_by_district = df_by_district.sort_values(by="all_payment", ascending=False)
# print(df_all_payment_by_district)


# 지역별 성별에 따른 소비량(결제량) 순위
# df_by_district_gender = df_all.groupby(["district", "gender"])[["all_payment", "customers"]].sum()
# df_all_payment_by_gender = df_by_district_gender[df_by_district_gender.index.get_level_values(1)=="2.여성"].sort_values(by="customers", ascending=False)
# print(df_all_payment_by_gender)
# gender_list = ["1.남성", "2.여성"]
# for i in gender_list:
#     print(df_by_district_gender[df_by_district_gender.index.get_level_values(1)==i].sort_values(by="customers", ascending=False).head(n=3))


# 지역별 연령대에 따른 소비량(결제량) 순위
# df_by_age = df_all.groupby(["district", "age"])[["all_payment", "customers"]].sum()
# df_all_payment_by_age= df_by_age[df_by_age.index.get_level_values(1)=="7.70대이상"].sort_values(by="all_payment", ascending=False)
# print(df_all_payment_by_age)

# 지역별 연령대에 따른 소비량(결제량) 순위 --- 2
district_top5 = df_all.groupby(["district"])[["all_payment", "customers"]].sum().sort_values(by="all_payment", ascending=False).head(n=5).index
district_top5_list = list(district_top5)
df_district_top5 = df_all[df_all["district"].isin(district_top5_list)]
df_district_top5_by_age = df_district_top5.groupby(["age", "district"])[["all_payment", "customers"]].sum()
df_district_top5_by_age_10 = df_district_top5_by_age[df_district_top5_by_age.index.get_level_values(0)=="1.10대"]
df_district_top5_by_age_20 = df_district_top5_by_age[df_district_top5_by_age.index.get_level_values(0)=="2.20대"]
print(df_district_top5_by_age_10.rank(method='min', ascending=False).reset_index().set_index(["district"]))
print(df_district_top5_by_age_20.rank(method='min', ascending=False).reset_index().set_index(["district"]))




# 지역별 시간대에 따른 소비량(결제량) 순위
# df_by_time = df_all.groupby(["district", "time"])[["all_payment", "customers"]].sum()
# df_all_payment_by_time= df_by_time[df_by_time.index.get_level_values(1)==6].sort_values(by="all_payment", ascending=False)
# for i in range(24):
#     print(df_by_time[df_by_time.index.get_level_values(1)==i].sort_values(by="all_payment", ascending=False).head(n=3))
# print(df_all_payment_by_time)


