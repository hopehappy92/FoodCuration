import pandas as pd
import pickle

# 읽기
with open('pickles_tob/df_all.p', 'rb') as file:
    df_all = pickle.load(file)

# 업종별 코드로 데이터 필터링
# 1.의류: 1001, 1003, 1004, 1007, 1008, 1010, 1099
# 2.악세사리류: 1201, 1202, 1203, 1204, 1205, 1206, 1207, 1208, 1299
# 3.제과점/아이스크림점: 2003
# 4.커피/음료전문점: 2004
# 5.패스트푸드점: 2099
# 6.한식: 2104
# 7.일식/생선회집: 2107
# 8.중식: 2109
# 9.양식: 2110
# 10.주점: 2112
# 11.편의점: 4112
# 12.숙박: 5001, 5101, 5102, 5103, 5104
# 13.헬스장: 6010
# 14.미용원/피부미용원: 7102, 7103
# 15.화장품점: 7106
# df_type = df_all[df_all["type_code"].isin([7102, 7103])]
df_type = df_all[df_all["type_code"] == 7106]

# 일별 그룹화, all_payment와 customers의 합
df_type = df_type[["date", "all_payment", "customers"]]
df_sum_by_date = df_type.groupby(["date"]).sum()
df_sum_by_date["avg_payment"] = df_sum_by_date["all_payment"]/df_sum_by_date["customers"]

# 날짜 타입 변경
df_sum_by_date["date"] = df_sum_by_date.index
df_sum_by_date_copy = df_sum_by_date.copy()
df_sum_by_date_copy["new_date"] = df_sum_by_date_copy["date"].map(lambda x: "20" + x[:2] + "-" + x[2:4] + "-" + x[4:])
df_sum_by_date_copy["new_date"] = pd.to_datetime(df_sum_by_date_copy["new_date"])

changed_df = df_sum_by_date_copy[["all_payment", "customers", "avg_payment", "new_date"]]
# print(changed_df)

# 일자(n,m,t)에 따른 Stochastic(KDJ)의 값을 구하기 위해 함수형태로 만듬
def get_stochastic(df, n=15, m=5, t=3):
    
    # 입력받은 값이 dataframe이라는 것을 정의해줌
    df = pd.DataFrame(df)
    
    # n일중 최고가
    ndays_high = df.all_payment.rolling(window=n, min_periods=1).max()
    # n일중 최저가
    ndays_low = df.all_payment.rolling(window=n, min_periods=1).min()
 
    # Fast%K 계산
    kdj_k = ((df.all_payment - ndays_low) / (ndays_high - ndays_low))*100
    # Fast%D (=Slow%K) 계산
    kdj_d = kdj_k.ewm(span=m).mean()
    # Slow%D 계산
    kdj_j = kdj_d.ewm(span=t).mean()
 
    # dataframe에 컬럼 추가
    df = df.assign(kdj_k=kdj_k, kdj_d=kdj_d, kdj_j=kdj_j).dropna()
    
    return df

result_df = get_stochastic(changed_df)
# 최종결과
print(result_df)

# 쓰기
with open('pickles_tob/df_cosmetics.p', 'wb') as file:
    pickle.dump(result_df, file)




