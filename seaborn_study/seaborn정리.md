# Seaborn 시각화 튜토리얼 정리
matplotlib 기반의 파이썬 시각화 라이브러리

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
## 2. figure-level & axes-level

1. figure-level 함수  
matplotlib 와 별개로 seaborn 의 figure를 만들어 그곳에 plotting하기  
figure-level 함수를 사용하여 seaborn 을 사용한 경우에는 facetgrid(seaborn의 figure)를 통해 레이아웃을 변경할 수 있음  

ex) relplot, displot, catplot  

2. axes-level 함수  
axes 수준에 plotting 을 한다는 것인데, figure-level 과는 다르게 matplotlib 의 axes에 그림  
plt.figure() 와 같은 메소드로 레이아웃을 변경함  

ex) scatterplot, histplot등 위의 사진에서 하위상자에 해당  


