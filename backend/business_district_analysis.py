import pandas as pd
import pickle


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
# df_09 = csv_data_09[(csv_data_09["가맹점_시도명"] == "서울")&(csv_data_09["개인기업구분"]=="개인")][[
#     "가맹점_시도명", 
#     "가맹점_시군구명",
#     "승인시간대1",
#     "가맹점업종코드",
#     "결제금액", 
#     "결제건수",
#     "회원수"]]

# df_10 = csv_data_10[(csv_data_10["가맹점_시도명"] == "서울")&(csv_data_10["개인기업구분"]=="개인")][[
#     "가맹점_시도명", 
#     "가맹점_시군구명",
#     "승인시간대1", 
#     "가맹점업종코드",
#     "결제금액", 
#     "결제건수",
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
#         '승인시간대1': 'time',
#         '가맹점업종코드': 'code',
#         '결제금액': 'all_payment',
#         '결제건수': 'pay_counts',
#         '회원수': 'customers',
#         })

# =======================pickle 사용================================

# 쓰기
# with open('df_district_all.p', 'wb') as file:
#     pickle.dump(df_all, file)

# # 읽기
with open('df_district_all.p', 'rb') as file:
    df_all = pickle.load(file)

# esential_code_list = [2003, 2004, 2099, 2104, 2107, 2109, 2110, 2112]


# code_to_tob = {
#   "2003": "제과점/아이스크림점",
#   "2004": "커피/음료전문점",
#   "2099": "패스트푸드점",
#   "2104": "한식",
#   "2107": "일식/생선회집",
#   "2109": "중식",
#   "2110": "양식",
#   "2112": "일반주점",
# }


# df_all = df_all[df_all["code"].isin(esential_code_list)]

# df_all['code'] = df_all['code'].astype(str)

# df_all['tob'] = df_all['code'].apply(lambda x: code_to_tob[x])
# df_all = df_all[["district", "tob", "all_payment"]]
business_district = pd.read_csv('../../data/business_district.csv', encoding = 'CP949')
business_district = business_district.rename(
    columns={
        'Unnamed: 0': 'district'
    }
)
business_district = business_district.set_index('district')
columns_list=["양식", "일반주점", "일식/생선회집", "제과점/아이스크림점", "중식", "커피/음료전문점", "패스트푸드점", "한식"]
business_district_count = business_district[columns_list].stack()
business_district_count = pd.DataFrame(business_district_count)
business_district_count = business_district_count.rename(columns={0:"count"})
business_district_payments = df_all.groupby(["district", "tob"]).sum().reset_index()
business_district_count = business_district_count.reset_index().rename(
    columns = {
        'level_1': 'tob'
    }
)
# print(business_district_count)
# print(business_district_payments)

business_district = pd.concat([business_district_payments, business_district_count["count"]], axis=1)
business_district["avg_payment"] = business_district["all_payment"]/business_district["count"]
business_district["rank"] = business_district.groupby("tob")["avg_payment"].rank(method="min", ascending=False)
business_district = business_district[["tob", "district", "rank"]]
for tob in columns_list:
    c1 = business_district["tob"] == tob
    c2 = business_district["rank"] <= 3
    print(business_district[c1 & c2].sort_values(by='rank'))


