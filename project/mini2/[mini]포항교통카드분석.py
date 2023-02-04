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

# # **포항시 BIS 교통카드 사용내역 분석**

# ## 2020/03/01~ 2020/03/07 데이터 합치기

"""
import pandas as pd
df_1 =pd.read_csv('03_01.csv')
df_2 =pd.read_csv('03_02.csv')
df_3 =pd.read_csv('03_03.csv')
df_4 =pd.read_csv('03_04.csv')
df_5 =pd.read_csv('03_05.csv')
df_6 =pd.read_csv('03_06.csv')
df_7 =pd.read_csv('03_07.csv')


df_list = [df_1,df_2,df_3,df_4,df_5,df_6,df_7]
trfcard = pd.concat(df_list, ignore_index = True)

trfcard.to_csv('trfcard.csv', encoding="utf-8-sig", index = False)
"""

# ## 라이브러리 불러오기

# +
import pandas as pd
import numpy as np
from datetime import datetime

import matplotlib.pyplot as plt
import koreanize_matplotlib #한글폰트
import seaborn as sns
import folium

# 그래프에 retina display 적용
# %config InlineBackend.figure_format = 'retina'
# %matplotlib inline
# -

# ## 데이터 탐색 및 전처리

# trfcard.csv 파일 불러오기
df = pd.read_csv("trfcard.csv")

df.head()

# 13개의 컬럼, 36718개의 데이터로 이루어져있다.
df.shape

# 보기 편하게끔 컬럼명을 한글로 바꿔주기
col_list= ['승차시각' , '하차시각', '노선명','노선설명','승객연령','환승여부',
            '추가운임여부','승차정류장','승차정류장_GPS_X','승차정류장_GPS_Y',
            '하차정류장', '하차정류장_GPS_X', '하차정류장_GPS_Y']
df.columns = col_list

# 승하차시간의 Dtype이 잘돗 되어있음
# 데이터형태 변환 필요
df.info()

# datetime으로 바꿔주기 위해 먼저 int에서 str 형태로 변환하기
# strptime을 이용해 str에서 datetime으로 변환하기
# 이렇게 하는 이유는 날짜가 데이터 문자 그대로 나와야하지만,
# int로 되어있어 바로 pd.to_datetime으로 하면 1970년으로 나옴
# 하차시각도 동일하게 적용
df['승차시각'] = df['승차시각'].astype('str')
df['승차시각'] = df['승차시각'].apply(lambda x :datetime.strptime(x, '%Y%m%d%H%M%S'))

df['하차시각'] = df['하차시각'].astype('str')
df['하차시각'] = df['하차시각'].apply(lambda x :datetime.strptime(x, '%Y%m%d%H%M%S'))

# +
#2020-03-01~2020-03-07의 데이터이므로 일 + 시간에 집중하기
# 승차/하차 별 day, dayname, time(시:분:초) , hour(시) 파생변수 생성
df['승차일'] = df['승차시각'].dt.day
df['하차일'] = df['하차시각'].dt.day 

df['승차요일'] = df['승차시각'].dt.dayofweek
df['하차요일'] = df['하차시각'].dt.dayofweek

#find_dayofweek 함수로 요일 숫자를 넘겨주면 요일명을 반환하는 함수

def find_dayofweek(day_no):
    dayofweek = "월화수목금토일"
    return dayofweek[day_no]

df["승차요일명"] = df["승차요일"].map(find_dayofweek)
df['하차요일명'] = df["하차요일"].map(find_dayofweek)

df['승차time'] = df['승차시각'].dt.time
df['하차time'] = df['하차시각'].dt.time 

df['승차hour'] = df['승차시각'].dt.hour    
df['하차hour'] = df['하차시각'].dt.hour
# -

# 탑승시간 파생변수 생성
df['탑승시간'] = df['하차시각'] - df['승차시각']

df.info()

# 데이터 결측값의 개수 확인 → 0개 
# 하지만 승객연령에 none 값이 25개 있음 -> 이걸 어떻게 처리하면 좋을까?
# 연령부분만 제외하고 다른 열 데이터는 잘 보존되어 있음 -> 연령분석시에만 제외
df.isnull().sum() 

# 연령부분만 제외하고 다른 열 데이터는 잘 보존되어 있음 -> 연령분석시에만 제외
df['승객연령'].value_counts()

# 데이터 중복값의 개수 확인 → 0개 
df.duplicated().sum()

# ## 버스 탑승시간 기초통계

# 탑승시간의 기초통계 
df['탑승시간'].describe()

# <탑승시간> -> 이것도 그래프로 표현한다면 어떻게 할 수 있을까?
# - 최소탑승시간: 5초 (타시긴 한걸까)
# - 최대탑승시간: 1시간 29분 51초
# - 탑승시간 중위수 :12분 11초
# - 평균: 14분 59초

# ## 시간대별 버스 승차/하차자 수

# +
#그래프 객체 생성(figure에 2개의 서브플롯 생성) - pandas 사용
fig = plt.figure(figsize=(15,5))
ax1 = fig.add_subplot(1,2,1) #한줄에 2개의 서브플랏 중 첫번째
ax2 = fig.add_subplot(1,2,2)

a = df['승차hour'].value_counts().sort_index()
a.plot.bar(rot= 0 ,edgecolor = 'black', linewidth = 1.5, ax=ax1)
ax1.set_title('시간대별 버스승차자 수' , size = 15 , fontweight = 'bold')

b = df['하차hour'].value_counts().sort_index()
b.plot.bar(rot= 0 , color = 'Purple',edgecolor = 'black', linewidth = 1.5, ax=ax2);
ax2.set_title('시간대별 버스하차자 수' , size = 15 , fontweight = 'bold');
# -

# - <시간대별 그래프>
# - 2020/03/01 ~ 2020/03/06은  일요일 ~ 토요일
# - 예상 : 버스를 가장 많이 타고 내리는 시간대는 출퇴근하는 오전 7시 ~ 9시와 오후 6시 ~ 8시 사이쯤 될 것이다.
# - 결과 : 오전 7시부터 오후 6시 사이에 탑승객이 많은 편이다.
#
# - 왜그럴까?
# 1. 오전에는 출퇴근 하시는 분들이, 오후에는 시장에 가서 장보거나 학원등의 일상생활에 버스가 많이 쓰일 것이다.
#
# 2. 예상과의 다르게 저녁 시간대에 버스 이용객이 비교적 적은데 그 이유는 무엇일까?
#     - 퇴근 시간들이 6시 이전인 곳이 많을까
#     - 설마 출근만 하시고 퇴근은 못하신걸까

# ## 요일별 승객분포

df['승차요일명'].value_counts()

# +
#그래프 객체 생성(figure에 2개의 서브플롯 생성) - pandas 사용
fig = plt.figure(figsize=(15,5))
ax1 = fig.add_subplot(1,2,1) #한줄에 2개의 서브플랏 중 첫번째
ax2 = fig.add_subplot(1,2,2)

a = df['승차요일명'].value_counts()
a.plot.bar(rot= 0 ,color = 'green', edgecolor = 'black', linewidth = 1.5, ax=ax1)
ax1.set_title('요일별 버스승차자 수' , size = 15 , fontweight = 'bold')

b = df['하차요일명'].value_counts()
b.plot.bar(rot= 0 , color = 'gold', edgecolor = 'black', linewidth = 1.5, ax=ax2);
ax2.set_title('요일별 버스하차자 수' , size = 15 , fontweight = 'bold');
# -

# - 월요일에 버스 이용객이 제일 많고 일요일에 버스 이용객이 제일 적다
# - 주말이라고 많이 이용하는게 아닌거 보면 평일에 포항시민들이 일상생활에서 버스를 많이 이용하는 편이라고 유추해볼 수 있다.

# ## 승객연령별 승차 시간 분포

# 승객연령이 None인 행을 제외한 데이터프레임 df1 생성
df1 = df[~(df['승객연령'] == 'None')]

pd.crosstab(df1['승객연령'],df1['승차hour'])

# 각 연령별 데이터 프레임 생성
df_2 = df1[df1['승객연령']=='일반']
df_3 = df1[df1['승객연령']=='청소년']
df_4 = df1[df1['승객연령']=='어린이']

# +
fig, axes = plt.subplots(2, 2, figsize=(20, 15))

a = sns.countplot(ax=axes[0,0], x = '승차hour', palette = 'Set2',data = df_2)
a.set_title('승객연령 = 일반 승차시간', size = 10 , fontweight = 'bold')

b = sns.countplot(ax=axes[0,1], x = '승차hour', palette = 'Set2',data = df_3)
b.set_title('승객연령 = 청소년 승차시간', size = 10 , fontweight = 'bold')

c = sns.countplot(ax=axes[1,0], x = '승차hour', palette = 'Set2',data = df_4)
c.set_title('승객연령 = 어린이 승차시간', size = 10, fontweight = 'bold')

d = sns.countplot(ax=axes[1,1], x = '승차hour', hue = '승객연령', palette='Set3',dodge = False, data=df1)
d.set_title('승객연령별 승차시간(stacked)', size = 10, fontweight = 'bold')

plt.show()
# -

# - 전체적으로 일반 연령이신분들이 버스를 많이 이용한다.
# - 청소년은 오후 2시~5시에 버스를 가장 많이 이용한다.
#     - 중고등학교가 끝나는 시간을 고려해볼 수 있다.
#
# - 어린이는 오전 11시, 오후 1시, 오후 6시에 많이 이용한다.
#
#     - 초등학교 끝나는 시간에 맞춰서 버스 이용률을 확인할 수 있다
#     - 저녁 6시엔 주로 학원이 끝나고 올 때 탔을 가능성도 생각해볼 수 있다.

# ## 정류장별 승차승객수
# - colormap : https://matplotlib.org/stable/tutorials/colors/colormaps.html

# +
#정류장별 승차승객수 TOP 10
labels = df['승차정류장'].value_counts()[:9,].index.tolist()
ratio = df['승차정류장'].value_counts()[:9,].values.tolist()

#색상 선택
cmap = plt.get_cmap("Set3")
colors= cmap(np.array([0,1,2,3,4,5,6,7,8,9]))

plt.figure(figsize=(30, 5))
plt.pie(ratio, 
        labels=labels,
        autopct='%.0f%%',
        startangle=90, # 축이 시작되는 각도 설정
        counterclock=True, # True: 시계방향순 , False:반시계방향순
        explode=[0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05], # 중심에서 벗어나는 정도 표시
        shadow=True, # 그림자 표시 여부
        colors= colors,
        wedgeprops = {'width':0.7,'edgecolor':'w','linewidth':3}
        ) #width: 부채꼴 영역 너비,edgecolor: 테두리 색 , linewidth : 라인 두께
plt.title('정류장별 승차승객수 Top10' , size = 15 , fontweight = 'bold')
plt.show()
# -

# ## 정류장별 하차승객수
# - colormap : https://matplotlib.org/stable/tutorials/colors/colormaps.html

# +
#정류장별 하차승객수 TOP 10
labels = df['하차정류장'].value_counts()[:9,].index.tolist()
ratio = df['하차정류장'].value_counts()[:9,].values.tolist()

#색상 선택
cmap = plt.get_cmap("Paired")
colors= cmap(np.array([0,1,2,3,4,5,6,7,8,9]))

plt.figure(figsize=(30, 5))
plt.pie(ratio, 
        labels=labels,
        autopct='%.0f%%',
        startangle=90, # 축이 시작되는 각도 설정
        counterclock=True, # True: 시계방향순 , False:반시계방향순
        explode=[0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05], # 중심에서 벗어나는 정도 표시
        shadow=True, # 그림자 표시 여부
        colors= colors,
        wedgeprops = {'width':0.7,'edgecolor':'w','linewidth':3}
        ) #width: 부채꼴 영역 너비,edgecolor: 테두리 색 , linewidth : 라인 두께
plt.title('정류장별 하차승객수 Top10' , size = 15 , fontweight = 'bold')
plt.show()
# -

# <승하차승객수가 많은 정류장 top 10>
# - 죽도시장, 시외버스터미널에서 승차, 하차 승객수가 많다.
# - 하차승객수 top10에는 죽도시장, 중앙상가, 오거리가 포함되어 있는걸 확인할 수 있다.
#     - -> 시장, 상가 이용객들이 오후에 많이 움직였다는 걸 유추해볼 수 있다.
#     - -> 환승하는 곳

hot_time = df.loc[(df['하차hour']>= 15) & (df['하차hour'] <=18)]

pd.crosstab(hot_time['하차hour'],hot_time['하차정류장'])

hot_time['하차정류장'].value_counts()

# ## 노선별 승객수 TOP10

# +
#노선별 승객수 TOP 10
labels = df['노선설명'].value_counts()[:9,].index.tolist()
ratio = df['노선설명'].value_counts()[:9,].values.tolist()

#색상 선택
cmap = plt.get_cmap("Set3")
colors= cmap(np.array([0,1,2,3,4,5,6,7,8,9]))

plt.figure(figsize=(30, 5))
plt.pie(ratio, 
        labels=labels,
        autopct='%.0f%%',
        startangle=90, # 축이 시작되는 각도 설정
        counterclock=True, # True: 시계방향순 , False:반시계방향순
        explode=[0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05,0.05], # 중심에서 벗어나는 정도 표시
        shadow=True, # 그림자 표시 여부
        colors= colors,
        wedgeprops = {'width':0.7,'edgecolor':'w','linewidth':3}
        ) #width: 부채꼴 영역 너비,edgecolor: 테두리 색 , linewidth : 라인 두께
plt.title('노선별 승객수 Top10' , size = 15 , fontweight = 'bold')
plt.show()
# -

# - 노선에 시외 또는 고속 터미널이 많이 포함되어 있다 ( 10개중 6개의 노선에 터미널이 포함됨)
# - 구청/시청 그리고 양학도 좀 보인다

# ## folium 이용하여 지도에 정류장 좌표 표시해보기

pohang_map = folium.Map(location=[36.0190178, 129.3434808], zoom_start= 12)
pohang_map

# 포항시 지도에 승차정류장 마커 표시
for stop, lat, lng in zip(df.승차정류장,df.승차정류장_GPS_Y,df.승차정류장_GPS_X):
    folium.CircleMarker([lat,lng],
                        radius= 10, #원의 반지름
                        color = 'brown', #원 둘레 색상
                        fill = True,
                        fill_color = 'coral', # 원 내부 색상
                        fill_opacity = 0.7, # 원 투명도
                        popup=stop # 누르면 승차정류장 이름 뜨게하기
    ).add_to(pohang_map)

# 지도를 html 파일로 저장 -> jupyter notebook 코드 작성한 폴더에 파일 생성됨(절대경로 지정 안했을때)
pohang_map.save('pohang_getin_station.html')

pohang_map #누르면 승차정류장 이름이 팝업으로 뜬다

# +
# 포항시 지도가 나오도록 초기 위도,경도와 줌인정도를 설정
m = folium.Map(location=[36.0190178, 129.3434808], zoom_start= 12)

# 행정구역결계 좌표가 들어있는 json 파일을 불러와 지도에 추가하기
import json
with open("포항행정구역경계.json",mode='rt',encoding='utf-8') as f:
    geo = json.loads(f.read())
    f.close()

folium.GeoJson(
    geo,
    name='pohang_municipalities'
).add_to(m)

m
