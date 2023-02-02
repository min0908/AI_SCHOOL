# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# # 국토교통부 아파트 매매 및 전월세 실거래가 조회하기

import os
os.getcwd()
os.chdir('C:/Users/pmj03/likelion') #절대 경로 설정

#  ## 라이브러리 불러오기

# +
import pandas as pd
import requests
import datetime
from bs4 import BeautifulSoup as bs
import time
from time import strftime
import xml.etree.ElementTree as ET

# 시각화를 위한 라이브러리
import matplotlib as mpl
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
# -

# ## 쿼리 값 세팅
# - 지역코드 참고 : https://github.com/drtagkim/kor_gg_code/blob/master/region_code5.csv

#인증키
service_key = '%2BYVsKRNTx5iyEGoMkPbKjm0GNtP%2FoVkw1hPT256CxVJi0CBBIiNdWvCiqxdPMzHcSi2GW%2FQdYVy8F7Km43fEpQ%3D%3D'
#실거래자료의 년월
ymd = '202201'
#지역코드 - 경기도 성남시 분당구
geo_code='41135'
#페이지당 행의 개수
numrow = 1000


# ## url 세팅

url = f'http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev?'
url = f'{url}LAWD_CD={geo_code}&DEAL_YMD={ymd}&serviceKey={service_key}&numOfRows={numrow}'

# ## GET OK 200 확인

response = requests.get(url)
print(response)

# ## Columns 매핑

# +
result = bs(response.text, features='xml')
items = result.findAll('item')

# 컬럼명 찾기
columns = items[0].find_all()
columns[0].name

cols = []

for i in range(0, len(columns)):
    cols.append(columns[i].name)

print(cols)
# -

col_list = [
    '지역코드',
    '도로명',
    '법정동',
    '지번',
    '아파트',
    '건축년도',
    '층',
    '전용면적',
    '년',
    '월',
    '일',
    '거래금액',
    '도로명건물본번호코드',
    '도로명시군구코드',
    '도로명코드',
    '법정동본번코드',
    '법정동시군구코드',
    '거래유형',
    '중개사소재지'
]


# ## 한 페이지 내용을 가져오는 함수 (특정 달의 내용을 크롤링) - 혜원님 code를 사용하여 진행
#

def get_data(geo_code,ymd):
    url = f'http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev?'
    url = f'{url}LAWD_CD={geo_code}&DEAL_YMD={ymd}&serviceKey={service_key}&numOfRows={numrow}'
    
    response = requests.get(url)
    result = bs(response.text, features='xml')
    items = result.findAll('item')

    # 컬럼명 찾기
    columns = items[0].find_all()
    columns[0].name

    cols = []

    for i in range(0, len(columns)):
        cols.append(columns[i].name)
    
    
    # 문서내 모든 텍스트 가져오기
    all_txt = []

    for c in range(0,len(cols)):
        col = cols[c]
        for a in result.select(col):
            all_txt.append(a.text.strip())
            
    # 개별 거래내역별로 묶기
    sorted_txt = []

    for i in range(len(result.items)):
        temp = []
        a = list(range(i, len(all_txt), len(result.items)))
        for j in a:
            temp.append(all_txt[j])
        sorted_txt.append(temp)
    
    
    
    df = pd.DataFrame(sorted_txt, columns = cols)
    return df

get_data(geo_code,ymd)


# ## 모든 데이터 내용을 가져오는 함수
# - 경기도 성남시 분당구의 2022.01~ 2022.12 데이터수집
# - 년도를 입력받으면 해당년도의 아파트 실거래가 정보 출력하는 함수
# - 참고자료 
#     - https://ai-creator.tistory.com/24

# +
# 앞의 한달 데이터를 수집하는 함수인 get_data가 선행되어야 한다.

def get_all_data(geo_code,date_year):
    #년도를 입력받으면 년도+월 리스트 만들기
    year = [str("%02d" %(y)) for y in range(date_year, date_year + 1)]
    month = [str("%02d" %(m)) for m in range(1, 13)]
    base_date_list = ["%s%s" %(y, m) for y in year for m in month ]
    
    # 날짜 리스트에 있는 날짜값들을 순차적으로 get_data 함수에 대입하기
    items_list = []
    for base_date in base_date_list:
        df_one = get_data(geo_code, base_date)
        items_list += (df_one.values.tolist())
        time.sleep(0.01)
    
    # 얻어진 리스트를 데이터프레임으로 만들기
    df_result = pd.DataFrame(items_list,columns = df_one.columns)
    return df_result



# -

date_year = 2022
df = get_all_data(geo_code,date_year)
df

# ### (추가) PublicDataReader을 이용하여 불러온 데이터와 차이가 있는 지 확인해보기

# +
# PublicDataReader 설치하기
# !pip install PublicDataReader

# API 키를 발급받고 PublicDataReader 라이브러리에서 TransactionPrice라는 클래스를 가져온다.
from PublicDataReader import TransactionPrice
api = TransactionPrice(service_key)

# 분석할 지역인 '경기도 성남시 분당구'의 시군코드를 알아본다.
import PublicDataReader as pdr
sigungu_name = "분당구"
code = pdr.code_bdong()
code.loc[(code['시군구명'].str.contains(sigungu_name, na=False)) &
         (code['읍면동명'].isna())]

# 2022년 1년동안 경기도 성남시 분당구의 아파트 매매 데이터를 불러오기
df_sale = api.get_data(
    property_type="아파트",
    trade_type="매매",
    sigungu_code="41135",
    start_year_month = "202201",
    end_year_month="202212"
    )

df_sale.shape #(1091,28) -> 행과 열의 개수가 위와 동일함
# -

df_sale.head() #컬럼의 순서만 다를뿐 같게 나오는 걸 확인해볼 수 있다.


# ### (추가) xml.etree을 이용하여 불러온 데이터와 차이가 있는 지 확인해보기

# +
# 한달 데이터만 불러오기

def get_data2(geo_code,ymd):
    url = f'http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev?'
    url = f'{url}LAWD_CD={geo_code}&DEAL_YMD={ymd}&serviceKey={service_key}&numOfRows={numrow}'
    
    response = requests.get(url)
    tree = ET.fromstring(response.content)
    items=tree[1][0]
    itemsList =[[i.text for i in item] for item in items]
    columns = [i.tag for i in items[0]]
    
    df= pd.DataFrame(itemsList,columns = columns)
    return df

# +
# 2022년도 분당구 데이터 불러오기


def get_all_data2(geo_code,date_year):
    #년도를 입력받으면 년도+월 리스트 만들기
    year = [str("%02d" %(y)) for y in range(date_year, date_year + 1)]
    month = [str("%02d" %(m)) for m in range(1, 13)]
    base_date_list = ["%s%s" %(y, m) for y in year for m in month ]
    
    # 날짜 리스트에 있는 날짜값들을 순차적으로 get_data 함수에 대입하기
    items_list = []
    for base_date in base_date_list:
        df_one = get_data2(geo_code, base_date)
        items_list += (df_one.values.tolist())
        time.sleep(0.01)
    
    # 얻어진 리스트를 데이터프레임으로 만들기
    df_result = pd.DataFrame(items_list,columns = df_one.columns)
    return df_result


# -

date_year = 2022
df_check = get_all_data2(geo_code,date_year)
df_check

# ## csv파일로 저장하고 확인하기

file_name1 ="2022년도 분당구 아파트 매매2.csv"
df.to_csv(file_name1, encoding="utf-8-sig",index = False)

#읽어오기
pd.read_csv(file_name1)

# # 데이터 전처리

# ## 필요한 컬럼만 추출

# 28개의 columns 중에 19개 columns만 분석에 사용할 예정
df= df[col_list]

# ## 데이터 타입 변경
# - 건축년도, 층, 전용면적, 년, 월, 일, 거래금액 은 int / float형태로 변경해주기
# - 일부 행이 한칸씩 당겨져있어 타입 변경시 오류 발생 → 헤결방법을 아직 못찾았습니다..
# - 타입 변경을 안하면 뒤에 했던 분석을 못하게 되니 데이터 분석부분은 PublicDataReader로 불러온 자료를 이용하여 실행했습니다.
# ![image.png](attachment:image.png)

df.거래금액.str.strip().str.replace(",","").astype(int)

df.층.str.strip().str.replace(",","").astype(int)

# ## 데이터 요약

df_sale.info()

# 범주형 변수 기초통계
df_sale.describe(include="O")

# 수치형 변수 기초통계
df_sale.describe()

# +
# 법정동 기준 아파트 매매가의 중위값 비교 
# %matplotlib inline 

plt.figure(figsize=(20,8))
sns.set_style('darkgrid')
plt.rc('font', family='Nanumgothic')

sns.barplot(data=df_sale, x="법정동" , y ='거래금액', palette='Set2')
plt.show
# -

# ## 결측값 확인

# 코드 결과 : 도로명지상지하코드, 중개사소재지,해제사유발생일, 해제여부에 결측값 존재
# 아직 분석방향을 확실히 정하지 못했으므로 함부로 제거하거나 치환하지 않는다.
pd.DataFrame(df_sale.isnull().sum())

# ## 중복값 확인

# +
# 각 컬럼별 중복값의 개수
# 분당구의 데이터이므로 지역과 관련된 변수는 다 중복된다.
duple_col = list(df_sale.columns)

for i in range(len(df_sale.columns)):
    print({duple_col[i]: df_sale[list(df_sale.columns)[i]].duplicated().sum()})
# -

# ## 매매 거래금액 이상치 확인
# - 여러 수치형 변수 중에 평균과의 차이가 가장 궁금한 변수는 거래금액이므로 IQR을 이용하여 이상치를 확인한다.

# +
# boxplot으로 시각화해보기

plt.boxplot(df_sale["거래금액"])
plt.xlabel('Price')
plt.title('Boxplot of the sale price of apartments')
plt.show()

# +
#IQR = Q3- Q1 을 이용하여 이상치의 개수를 구해보기
q3 = df_sale["거래금액"].quantile(0.75) 
q1 = df_sale["거래금액"].quantile(0.25)

iqr = q3 - q1
out_cut = iqr * 1.5

# lower , upper bound
lower , upper = q1 - out_cut , q3 + out_cut

out_money1 = df_sale["거래금액"] > upper
out_money2 = df_sale["거래금액"] < lower
count_true = sum(out_money1) + sum(out_money2)

print(f"총 이상치의 개수는 {count_true}개 입니다.")
# -

# # 데이터 분석

# ## 이상치로 분류될 정도로 분당에서 매매거래금액이 높은 아파트는 어디일까?

# +
# 이상치에 해당되는 행 인덱스 구하기
out_index = df_sale.index[out_money1 == True].tolist()

# 전체 데이터프레임에서 행인덱스를 이용하여 필요한 데이터 추출하기
df_top = df_sale.loc[out_index]
# -

display(pd.DataFrame(df_top["법정동"].value_counts()).T)

df_top.groupby(['법정동','아파트']).size().reset_index(name='count')

# +
plt.figure(figsize=(15,8))
sns.set_style('whitegrid')
plt.rc('font', family='NanumGothic') 

sns.countplot(data=df_top, x="법정동" , hue='아파트', palette='Set2')
# -

# ## 상관분석
# - 가격에 영향을 미치는 요인들이 무엇이 있을까?

# 매매가격이 높은 아파트 데이터로 상관분석
# 저는 날짜를 뺀 나머지로 실시했습니다.
# 모두 양의 상관관계 : 층수가 높아지거나, 전용면적이 넓어지거나 , 건축년도가 최신일수록 거래금액도 올라가는 경향이 보인다.
df_sale[['건축년도','층','전용면적','거래금액']].corr()

#heatmap으로 상관관계를 표시
plt.rcParams["figure.figsize"] = (8,8)
plt.rc('font', family='NanumGothic') 
sns.heatmap(df_sale[['건축년도','층','전용면적','거래금액']].corr(),
           annot = True, #실제 값 화면에 나타내기
           cmap = 'Purples', #색상
           vmin = -1, vmax=1 , #컬러차트 영역 -1 ~ +1
          )

# # (추가) 전월세 실거래가

# 2022년 1년동안 경기도 성남시 분당구의 아파트 전월세 데이터를 불러오기
df_rent = api.get_data(
    property_type="아파트",
    trade_type="전월세",
    sigungu_code="41135",
    start_year_month = "202201",
    end_year_month="202212"
    )

# ## 법정동 기준 아파트 보증금의 중위값 비교

# +
# 법정동 기준 아파트 보증금의 중위값 비교\
plt.figure(figsize=(20,8))
sns.set_style('darkgrid')
plt.rc('font', family='Nanumgothic')

sns.barplot(data=df_rent, x="법정동" , y ='보증금액', palette='Set1')
# -

# ## 법정동 기준 아파트 월세값의 중위값 비교

# +
# 법정동 기준 아파트 월세의 중위값 비교 
plt.figure(figsize=(20,8))
sns.set_style('darkgrid')
plt.rc('font', family='Nanumgothic')

sns.barplot(data=df_rent, x="법정동" , y ='월세금액', palette='Set2')
# -

# ## 이상치로 분류될 정도로 분당에서 보증금이 높은 아파트

# +
#IQR = Q3- Q1 을 이용
q3 = df_rent["보증금액"].quantile(0.75) 
q1 = df_rent["보증금액"].quantile(0.25)

iqr = q3 - q1
out_cut = iqr * 1.5

# lower , upper bound
lower , upper = q1 - out_cut , q3 + out_cut

out_money1 = df_rent["보증금액"] > upper
out_money2 = df_rent["보증금액"] < lower
# -

# 이상치에 해당되는 행 인덱스 구하기
out_index = df_rent.index[out_money1 == True].tolist()
# 전체 데이터프레임에서 행인덱스를 이용하여 필요한 데이터 추출하기
df_deposit = df_rent.loc[out_index]
# 이상치에는 어떤 아파트가 많고 또 어느 동에 많이 위치해 있을까?
display(pd.DataFrame(df_deposit["법정동"].value_counts()).T)

# +
plt.rc('font', family='NanumGothic') 
    
df_deposit['법정동'].value_counts().plot.pie(autopct='%1.1f%%', figsize=(5,5))
plt.title('2022년 분당구 아파트 보증금 이상치')
plt.ylabel('')
# -

# ## 상관분석
# - 월세, 전세금 모두 종전 금액과 높은 상관관계를 보인다.

df_rent[df_deposit.columns.difference(['년','월','일'])].corr()

#heatmap으로 상관관계를 표시
plt.rcParams["figure.figsize"] = (8,8)
sns.heatmap(df_rent[df_deposit.columns.difference(['년','월','일'])].corr(),
           annot = True, #실제 값 화면에 나타내기
           cmap = 'Greys', #색상
           vmin = -1, vmax=1 , #컬러차트 영역 -1 ~ +1
          )
     
