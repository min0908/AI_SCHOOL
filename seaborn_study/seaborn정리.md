# Seaborn 시각화 튜토리얼 정리 
matplotlib 기반의 파이썬 시각화 라이브러리 

*****
![image](https://user-images.githubusercontent.com/94737255/218521242-eda45bd8-80e4-4b92-9715-aa954ac50cb9.png)

**1. relplot: 두가지 변수의 관계를 나타내기 위한 그래프**
- scatterplot
- lineplot

**2. displot: 변수 하나 혹은 두개의 값 "분포"를 나타내기 위한 그래프**
- histplot
- kdeplot
- ecdfplot
- rugplot

**3. catplot: 범주형 변수와 연속형 변수간의 관계를 나타내기 위한 그래프**
- stripplot
- boxplot
- violinplot
- pointplot
- barplot

**4. Regression: 회귀 분석 결과를 나타내기 위한 그래프**
- regplot
- lmplot
- residplot

**5. Matrix: 연속형 변수간의 관계 비율을 시각화하기 위한 그래프**
- heatmap
- clustermap

**6. Multi-plot: 여러 그래프를 함께 그려 비교하기 위한 그래프**
- FacetGrid
- pairplot
- PairGrid
- jointplot
- JointGrid

*****
## 2. figure_level & axes_level

**1. figure-level 함수**
- matplotlib 와 별개로 seaborn 의 figure를 만들어 그곳에 plotting하기  
- figure-level 함수를 사용하여 seaborn 을 사용한 경우에는 facetgrid(seaborn의 figure)를 통해 레이아웃을 변경할 수 있음  
- label이 그래프 밖에 위치함
- col 파라미터로 groupby가 가능함  
ex) relplot, displot, catplot  

```python
# figure-level

# 라이브러리
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
%matplotlib inline

# 데이터
penguins = sns.load_dataset("penguins")

# figure-level함수인 displot으로 figure 확보 → kind를 통해 세부함수 선택, default값은 histplot
sns.displot(data=penguins, x="flipper_length_mm", hue="species", multiple="stack")
```
![image](https://user-images.githubusercontent.com/94737255/218624014-44534706-dbc5-4e9a-a52b-827488350b70.png)


```python
# figure-level함수인 displot으로 figure 확보 → kind를 통해 세부함수 선택, default값은 histplot
sns.displot(data=penguins, x="flipper_length_mm", hue="species", multiple="stack", kind="kde") 
```
![image](https://user-images.githubusercontent.com/94737255/218624243-03e8336d-aaea-4ad9-81f3-87a47026ad8c.png)


```python
# col 지정하여 groupby 사용
sns.displot(data=penguins, x="flipper_length_mm", hue="species", col="species", kind="kde")
```
![image](https://user-images.githubusercontent.com/94737255/218624279-b279b89d-ad29-4de9-b148-bad88decd3e6.png)



**2. axes-level 함수**  
- axes 수준에 plotting 을 한다는 것인데, figure-level 과는 다르게 matplotlib 의 axes에 그림
- ax 파라미터를 통해 plotting 할 곳을 지정  
- plt.figure() 와 같은 메소드로 레이아웃을 변경함
- label이 그래프 안에 위치함  
ex) scatterplot, histplot등 위의 사진에서 하위상자에 해당


*****
## 3. Multiple views
**1. jointplot**
- 2가지 plot을 한번에 확인해볼 수 있음
- kind 메소드를 이용하여 plot 종류 선택

```python
# 안쪽엔 scatter plot이 default
sns.jointplot(data=penguins, x="flipper_length_mm", y="bill_length_mm", hue="species")
```
![image](https://user-images.githubusercontent.com/94737255/218637556-52fce43d-3885-454b-b6a0-8608add25580.png)


**2. pairplot**
- 두 가지 변수 조합을 한번에 확인

```python
sns.pairplot(data=penguins, hue="species")
```
![image](https://user-images.githubusercontent.com/94737255/218637547-91b31d49-2f0d-4b1b-8e8b-c3780ee4db65.png)

*****

## 4. 그래프별 정리

### 1) 두 가지 변수의 관계 파악

#### scatterplot(산점도)
`sns.scatterplot(x, y, data)`

- 옵션
  - hue : 의미에 따라 점의 색깔을 변경
  - style: 모양 변경


```python
# 아무 설정없는 기본 산점도
tips = sns.load_dataset("tips")
sns.scatterplot(x='total_bill', y='tip', data=tips)
```  
![image](https://user-images.githubusercontent.com/94737255/218914481-d8089570-c0b6-45ac-a142-706218946724.png)


```python
sns.scatterplot(x='total_bill', y='tip', data=tips, hue='day', style='time')
```  
![image](https://user-images.githubusercontent.com/94737255/218914504-b2f905e8-89d3-4d27-aadd-bac035bb0631.png)


#### lineplot
`sns.lineplot(x, y, data)`

- 데이터가 연속형인 경우 주로 사용됨
- 선 주변 색깔 칠해진 부분: 신뢰구간, `ci` 파라미터로 조절가능
- 옵션
  - hue : 의미에 따라 점의 색깔을 변경
  - style: 모양 변경

```python
# 아무 설정없는 기본 라인그래프
fmri = sns.load_dataset("fmri")
sns.lineplot(x='timepoint', y='signal', data=fmri)
```  
![image](https://user-images.githubusercontent.com/94737255/218914521-8dae6ec1-ab61-42db-941c-f6691bc14a6d.png)


```python
sns.lineplot(x='timepoint', y='signal', data=fmri, hue='event', style='event', ci=None)
```  
![image](https://user-images.githubusercontent.com/94737255/218914542-bb57cf87-d5f9-4138-ab67-0aef1561a0b7.png)


#### relplot
`sns.relplot(x, y, data)`

- `kind` 파라미터를 통해 scatter / line 형식 변경 가능 (default : scatter)
- relplot은 앞의 두 그래프와 달리 `FaceGrid`를 반환함 (scatter/line은 `AxeSubplot`을 반환)
- `FaceGrid`면 여러 그래프를 한번에 그릴 수 있음
- 옵션
  - hue : 의미에 따라 점의 색깔을 변경
  - style: 모양 변경
 
 ```python
# 아무 설정없는 기본 relplot
tips = sns.load_dataset("tips")
sns.relplot(x='total_bill', y='tip', kind='scatter', hue='time', data=tips)
```  
![image](https://user-images.githubusercontent.com/94737255/218914553-388b209a-b93a-4a66-bdcd-e0ca3891ec8b.png)


### 2) 변수 하나 혹은 두개의 분포를 나타내기 위한 그래프(Distribution)
#### histplot(히스토그램)  
`sns.histplot(x, data)`

- y축은 데이터의 빈도를 나타냄
- 옵션
  - hue : 레이블 구분
  - multiple: (multiple = 'stack')으로 하면 hue로 분류된 레이블을 중첩되게 설정

- 2차원으로 그리기(y값 설정)  
`sns.histplot(x, y, data)`

#### kdeplot(커널 밀도 추정 그래프)  
`sns.kdeplot(x, data)`

- 히스토그램 y축: count(절대량) / kdeplot y축: 비율(상대량)
- 옵션
  - hue : 레이블 구분
  - multiple: (multiple = 'stack')으로 하면 hue로 분류된 레이블을 중첩되게 설정

- 2차원으로 그리기(y값 설정)  
`sns.histplot(x, y, data)`

- histplot과 kdeplot 함께 사용하기  
`sns.histplot(x,data,kde=True)`



