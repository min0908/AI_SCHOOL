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

# + [markdown] id="AYveGuUoLL9k"
# # 국민동의청원 데이터 수집하기
# - 🐰사이트 URL (모든 청원) : https://petitions.assembly.go.kr/closed/agreeEnded
#
# - 🐰 requests url : inspect > network > header > RequestURL
#
# - 🐰 inspect > Network에서 requests Headers를 확인해보면 'Accept: application/json, text/plain, */*'으로 나타난다. 
#      
#     - json 타입으로 데이터를 받기 위해 json()을 사용 

# + [markdown] id="ZFqA2cM_9V6u"
# ## 라이브러리 불러오기

# + id="m3axYWuQLWNl"
import pandas as pd
import requests
import time
import datetime 
from tqdm import trange

import matplotlib.pyplot as plt
import seaborn as sns
# -

# ## 쿼리 값 세팅

# +
headers = {"user-agent": "Mozilla/5.0"}
page_no = 1
count_per_page = 8

# 기간은 2022-01-01 ~ 2022-12-31으로 고정
begin_date = 20220101
end_date = 20221231
# -

# ## url 세팅

base_url = f'https://petitions.assembly.go.kr/api/petits?pageIndex={page_no}&recordCountPerPage={count_per_page}&sort=AGRE_END_DE-&searchCondition=sj&searchKeyword=&petitRealmCode=&sttusCode='
base_url = f'{base_url}PETIT_FORMATN,CMIT_FRWRD,PETIT_END&resultCode=BFE_OTHBC_WTHDRAW,PROGRS_WTHDRAW,PETIT_UNACPT,APPRVL_END_DSUSE,ETC_TRNSF&notInColumn='
base_url = f'{base_url}RESULT_CODE&beginDate={begin_date}&endDate={end_date}&ageCd='


# ## GET OK 200 확인

base_response = requests.get(base_url, headers=headers)
base_response.status_code

# ## Columns 매핑

# +
col = ["petrNm", "petitSj", "petitObjet", "petitCn", 
     "petitRealmNm", "resultCodeNm","petitEndDt", "agreBeginDe", "agreEndDe", "agreCo"]


columns={"petrNm":"청원인", "petitSj": "청원명", "petitObjet":"청원의 취지",
        "petitCn":"청원의 내용", "petitRealmNm":"청원분야", 
        "resultCodeNm":"청원결과","petitEndDt":"청원종료일", 
        "agreBeginDe":"청원동의시작일", "agreEndDe":"청원동의종료일", "agreCo":"청원 동의수"}


# -

# ## 한 페이지 내용을 가져오는 함수
# - 🐰 앞에서 일일히 각 항목의 리스트를 구하면 데이터 수집하는데 시간이 너무 오래걸리는 것을 확인했다.
#
# - 🐰 각 게시물 페이지 안에서 청원의 취지를 포함한 데이터를 한번에 구한다.
#
# - 🐰 게시물의 url을 이용하여 반복문을 돌릴 때 enumerate를 사용하여 간결하게 한다.
#
# - 🐰 결과적으로 반복문은 1개로 끝낼 수 있어 함수를 돌리는 시간을 많이 단축시킬 수 있었다.

# 페이지 number을 매개변수로 받아 청원정보를 크롤링하는 함수
def petition_crawler(page_no):
    try:
        # 청원 목록 url을 json 형식으로 requests
        base_url = f'https://petitions.assembly.go.kr/api/petits?pageIndex={page_no}&recordCountPerPage={count_per_page}&sort=AGRE_END_DE-&searchCondition=sj&searchKeyword=&petitRealmCode=&sttusCode='
        base_url = f'{base_url}PETIT_FORMATN,CMIT_FRWRD,PETIT_END&resultCode=BFE_OTHBC_WTHDRAW,PROGRS_WTHDRAW,PETIT_UNACPT,APPRVL_END_DSUSE,ETC_TRNSF&notInColumn='
        base_url = f'{base_url}RESULT_CODE&beginDate={begin_date}&endDate={end_date}&ageCd='

        headers = {"user-agent": "Mozilla/5.0"}
        base_response = requests.get(base_url, headers=headers)
        base_json=base_response.json()

        # 각 게시물별 url을 구하기위해 페이지 고유번호를 수집하기
        # enumerate를 돌리기 위해 series → list로 변환하기 (파이썬스럽게!)
        base_df = pd.DataFrame(base_json)
        base_df = list(base_df['petitId'])

        # 각 게시물별 내용을 수집하기 위해 page url 수집하고 한번에 데이터 출력
        content_list = []
        for i , letter in enumerate(base_df):
            content_url = 'https://petitions.assembly.go.kr/api/petits/' + letter
            content_response = requests.get(content_url, headers=headers)
            content_json=content_response.json()
            content_list.append(content_json)
            time.sleep(0.01)
        
        # 데이터를 담은 리스트를 데이터프레임으로 변환
        df = pd.DataFrame(content_list)
        

        # 전체 데이터에서 분석에 필요한 변수들을 선택하고, 보기편하도록 한글 변수명으로 바꿔주기
        col = ["petrNm", "petitSj", "petitObjet", "petitCn", 
           "petitRealmNm", "resultCodeNm","petitEndDt", "agreBeginDe", "agreEndDe", "agreCo"]
        df = df[col]

        df.rename(columns={"petrNm":"청원인", "petitSj": "청원명", "petitObjet":"청원의 취지",
                         "petitCn":"청원의 내용", "petitRealmNm":"청원분야", 
                         "resultCodeNm":"청원결과","petitEndDt":"청원종료일", 
                         "agreBeginDe":"청원동의시작일", "agreEndDe":"청원동의종료일", 
                         "agreCo":"청원 동의수"}, inplace=True)

        return df

    except Exception as e:
        print(f"페이지를 다시 입력해주세요.")


# 1페이지 내용 불러오기
petition_crawler(page_no)

# + colab={"base_uri": "https://localhost:8080/"} id="6w283gNcLWNl" outputId="a2f9fa8c-fb0e-453e-d571-9df1b599b2ed"
# 마지막 페이지는 43 → 에러메세지
page_no = 104
petition_crawler(page_no)


# -

# ## 모든 데이터 내용을 가져오는 함수
# - 🐰 2022년 일년동안의 청원을 수집해보려한다.(마지막 페이지: 43 page) - 1분 16초
#
# - 🐰 tqdm의 trange를 이용하여 진행결과를 알 수 있도록 나타낸다.
#
# - 🐰 petition_list를 만든 뒤에 pandas의 concat을 이용하여 최종 dataframe을 생성한다

def get_all_data(lastpage_no):
    
    # 경고메시지가 있으면 tqdm 로그가 너무 많이 찍히기 때문에 경고메시지를 제거합니다. 
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

    petition_list = []
    for page_no in trange(1,lastpage_no + 1):
        result = petition_crawler(page_no)
        petition_list.append(result)
        time.sleep(0.01)
    
    result = pd.concat(petition_list)
    return result


# +
#마지막 페이지
lastpage_no = 43

df_petition= get_all_data(lastpage_no)
df_petition
# -

df_petition.shape

# ## csv파일로 저장하고 확인하기

# + id="GT9yOkAXLWNm"
# csv 파일로 저장하고 확인
# excel로 열어보면 한글이 깨지므로 인코딩
# sig"는 "signature의 준말

file_name = "국민동의청원.csv"
df_petition.to_csv(file_name, encoding="utf-8-sig", index = False)

# + colab={"base_uri": "https://localhost:8080/", "height": 1000} id="25cExulfLWNm" outputId="d4d1942d-0194-4d45-a7e3-39c48068415d"
pd.read_csv(file_name)

# + [markdown] id="EU8MW_LN9beK"
# # 데이터 전처리
# -

# ##  데이터 요약 
#
# - 🐰 데이터 타입 및 기초통계 확인

df_petition.info()

# 범주형 변수 기초통계
df_petition.describe(include="O")

# 수치형 변수 기초통계
df_petition.describe()

# ## 이상치 확인
#
# - 🐰 수치형 변수(청원 동의수)의 이상치 확인
#
# - 🐰 청원 동의수가 50000이 되어야 청원이 성립되므로, 이상치라고 해서 바로 값을 제거하면 안된다. 

# + [markdown] id="fKQjj9vSCWsg"
# ![image.png](data:image/png;base64,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AQDogoABAOiCgAEA6IKAAQDogoABAOiCgAEA6IKAAQDogoABAOiCgAEA6IKAAQDogoABAOiCgAEA6IKAAQDogoABAOiCgAEA6IKAAQDogoABAOiCgAEA6IKAAQDogoABAOgi4oA5derUtm3bHnnkkT/96U+KoqiqqkdZAIDRLoKA0bLkxIkTb7/9ttPp3L9/PwEDALiSyFowfX19x48f//zzzx0OR2pqqiAIoijqUxgAYHSLIGB6enr+53/+JxgMPvzww4mJiRFdRpZloggA4kq4AePz+S5evPjhhx9ardbbbrvNbDZfvXNMUZS2trbGxkaXy9XY2NjU1KQoSjAYjEbNAIBRwBDmcRcvXjx06JDNZps0adKkSZNkWb56Wng8np07d7711luffPKJxWLp7u6+7rrrCBgAiB9fBUxXV9fLL7984cKF/v7+gX1ZqqomJSXdeeedBw8edLlc991337x58yRJkiTJYDAYjcYrZUZiYuLNN988efLkBx980Gq1bt++/fjx45LErGgAiBdfBYzf729oaDh9+nRfX9+ggElOTv7Od77zxRdf7N+//5577rl06dKFCxf6+vrOnz9/+PDhadOmJSYmXj6+YjKZcnNzc3NztR8bGhoaGhpG5iMBAL4NvgqY1NTU//zP/7w8J0RR7O/vv3Dhwttvv/3pp59+73vfE0UxGAx2dXVt2rSpurr6D3/4Q15e3jeO+fv9fvrHACCu/HUMRpblIY8wGo1paWmPPPLIggULzGazwWBobW391a9+dfPNNz/00EPXXXed2WweqWoBAKPGNw/yS5JktVpvuummm266SdvT0dHx3HPPzZs374EHHggGg8w/BgBcbjij7h6Px+12d3V1+Xw+RVGiXhMAYAwId5ryQKmpqRs2bJg+fbrRaIx6QQCAsWE4AWO1Wh966KGolwIAGEtYmAIA0AUBAwDQBQEDANAFAQMA0AUBAwDQBQEDANAFAQMA0AUBAwDQBQEDANAFAQMA0AUBAwDQBQEDANAFAQMA0AUBA8SXiooKaYAhH+mkKIr2qsvlCvNtwzxl0NU1W7ZsGfKlgW919bIvf8+IiodOCBggXrjdbkmSnE5ne3u7qqp+v18QBKPRePkX8aOPPhrpm0d0Snl5uTrAmjVrBEGorKzUSgodUFhYGFHZobdtb28XBKGoqEiLLsQKAQPEC4fDIQjC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)
#
# 출처: https://seong6496.tistory.com/285

# + colab={"base_uri": "https://localhost:8080/"} id="sAIypND-_s7R" outputId="feedb439-df9f-4503-a6a7-a8422e455f0c"
#IQR = Q3- Q1 을 이용하여 이상치의 개수를 구해보기
q3 = df_petition["청원 동의수"].quantile(0.75) 
q1 = df_petition["청원 동의수"].quantile(0.25)

iqr = q3 - q1
out_cut = iqr * 1.5

# lower , upper bound
lower , upper = q1 - out_cut , q3 + out_cut

out_agree1 = df_petition["청원 동의수"] > upper
out_agree2 = df_petition["청원 동의수"] < lower
count_true = sum(out_agree1) + sum(out_agree2)

print(f"총 이상치의 개수는 {count_true}개 입니다.")

# + colab={"base_uri": "https://localhost:8080/", "height": 295} id="OD7dVfH8CMrF" outputId="40487832-d914-425f-97a2-cdcb79c7c712"
# boxplot으로 시각화해보기
# %matplotlib inline 

plt.figure(figsize=(6,5))
plt.boxplot(df_petition["청원 동의수"])
plt.xlabel('Agreements')
plt.title('Boxplot of the number of petition agreements')
plt.show()

# + [markdown] id="IfKYshGMFIqE"
# ## 이상치 처리
# - 🐰 청원 동의수가 50000개가 되면 청원 성립이 되기 때문에 50000보다 클 수 없음
# - 🐰 100000개의 값이 하나 있으므로 분석을 하기 위해선 이를 50000으로 변경해줘야한다.

# + id="rOORmwR2GQeK"
# 청원 동의수 100000 → 50000으로 변경
df_petition.loc[df_petition["청원 동의수"]== 100000, "청원 동의수"] = 50000

# + colab={"base_uri": "https://localhost:8080/", "height": 295} id="GNmWoG5QGJRD" outputId="86eb50e7-b07e-45ac-bf5b-3ad9dfc9497b"
# 100000의 값이 boxplot에서 사라졌음을 확인할 수 있다.
plt.figure(figsize=(6,5))
plt.boxplot(df_petition["청원 동의수"])
plt.xlabel('Agreements')
plt.title('Boxplot of the number of petition agreements')
plt.show()

# + [markdown] id="1y7J95V1LWNm"
# ##  결측값 확인

# + colab={"base_uri": "https://localhost:8080/"} id="VJViZGFhLWNm" outputId="f37bb90f-1518-4c1f-bb7a-aa9b327dd16d"
# null값이 있는 경우를 count 시켜줌. → 없음
df_petition.isnull().sum()

# + [markdown] id="XahJo24D91ee"
# ## 중복값 확인
#

# + colab={"base_uri": "https://localhost:8080/", "height": 111} id="5f3UtKAj95FH" outputId="195cf883-30a8-48e1-dfa1-edab5cd583b7"
df_petition[df_petition.duplicated()] # 중복값 없음

# + [markdown] id="o9pk6bVtLWNn"
# # 데이터 시각화

# + [markdown] id="Rl8h8w8NJ94G"
# 🐰 히스토그램

# + colab={"base_uri": "https://localhost:8080/", "height": 470} id="Oz52ltpjLWNn" outputId="41018129-17b1-47b9-fc32-aafd96cbc3d0"
plt.figure(figsize=(6,5))
plt.style.use('classic') # 스타일서식 지정
df_petition.hist(color='coral')
plt.title('Histogram of the number of petition agreements')
plt.xlabel('Agreements')
plt.show()

# +
# 원그래프 (지원님 code) 
sns.set(font="NanumGothic")

df_petition['청원분야'].value_counts().plot.pie(autopct='%1.1f%%', figsize=(8, 8))
plt.title('2022년 국민 청원 분야 분포')
plt.ylabel('')

# + [markdown] id="IzEu9FhfKhbn"
# #  데이터 분석

# + [markdown] id="tGPgLjmfLWNn"
# ##  2022년도 청원들 중에 성립된 청원은 어떤것인지 찾아보기

# + colab={"base_uri": "https://localhost:8080/", "height": 1000} id="QfQV_ngbLWNn" outputId="8677e8dc-1fd7-476b-d09d-f4779552f206"
# 동의수 == 50000건이면 국민청원이 성립된다.
df_yes = df_petition.loc[df_petition['청원 동의수'] == 50000]
df_yes

# + [markdown] id="KLLDV3hJLNN6"
# ## 성립된 청원들 중에 어느 분야에서 청원이 가장 많이 성립되었을까?
#
# - 1위 : 수사/ 법무/사법제도 (6개)
# - 2위 : 인권/ 성평등/ 노동 (5개)
# - 3위 : 보건의료 (4개)

# + colab={"base_uri": "https://localhost:8080/", "height": 426} id="_zf1mgXQMcu-" outputId="a029e218-9880-4187-fffc-cd5c6cac7708"
# 청원분야와 청원결과의 교차표(crosstable) 만들기
pd.crosstab(df_yes["청원분야"],df_yes["청원결과"])
# -

sns.countplot(y=df_yes["청원분야"], hue=df_yes["청원결과"], data=df_yes)
plt.show()

# + [markdown] id="MuPv7vWwTCG8"
# ## 2022년도 청원들 중에 미성립된 청원은 어떤것인지 찾아보기

# + colab={"base_uri": "https://localhost:8080/", "height": 1000} id="RLfgbuPFQ_mI" outputId="20d060bd-3288-4598-87b6-71ea161f142a"
# 동의수 < 50000건이면 국민청원이 성립되지 않는다.
df_no = df_petition.loc[df_petition['청원 동의수'] < 50000]
df_no

# + [markdown] id="R90rMGrZTYlm"
# ##  미성립된 청원들 중에 어느 분야의 청원이 많을까?
# - 1위 : 보건의료 (53개)
# - 2위 : 국토/해양/교통(40개)
# - 3위 : 수사/법무/사법제도(30개)

# + colab={"base_uri": "https://localhost:8080/", "height": 645} id="Psdb-AEkTOnJ" outputId="f575119b-5e88-487a-9508-bb40146e9641"
# 청원분야와 청원결과의 교차표(crosstable) 만들기
pd.crosstab(df_no["청원분야"],df_no["청원결과"])

# + [markdown] id="uv8yfNzoUC_Y"
# ##  미성립된 청원들 중에 동의수를 가장 많이 받은 Top 3 게시물

# + colab={"base_uri": "https://localhost:8080/", "height": 500} id="KKZ8Rv4xWkiH" outputId="7e7268f3-5bd1-41b2-db0a-9d5fc0d768c7"
df_no.sort_values("청원 동의수",ascending = False).head(3)

# + [markdown] id="Hl89rTzEXAyu"
# ##  미성립된 청원들 중에 동의수를 가장 적게 받은 Top 3 게시물
#
# - 3개 다 국토/해양/교통 분야의 청원이다.

# + colab={"base_uri": "https://localhost:8080/", "height": 430} id="e9P5WE2wXC9F" outputId="3e6c2773-887b-4cd9-f2be-4c312ce23c80"
df_no.sort_values("청원 동의수",ascending = True).head(3)
