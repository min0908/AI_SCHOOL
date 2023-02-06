# import seaborn
import seaborn as sns
import matplotlib.pyplot as plt
# Apply the default theme
sns.set_theme()

#Load an example dataset
tips = sns.load_dataset("tips")

tips.info()

# Create a visualization
# 1) relplot: 산점도와 선그래프 모두 가능----------------
# 장점: return값이 FacetGrid(여러개의 Axessubplot을 포함)
fig = plt.figure()
sns.relplot(data= tips,
            x='total_bill',
            y = 'tip',
            col = 'time',
            hue = 'smoker',
            style = 'smoker',
            size = 'size')
plt.show()

# 2) ------------------------------------------------
dots = sns.load_dataset("dots")
dots.info()
fig = plt.figure()
sns.relplot(data = dots,
            kind = "line", #산점도 없애고 선그래프만
            x="time",
            y="firing_rate",
            col="align",
            hue = 'choice',
            size= 'coherence', # 선의 너비로 구별
            style='choice', # 모양으로 구별
            facet_kws= dict(sharex = False))
plt.show()

# 3) -------------------------------------------------
fmri = sns.load_dataset('fmri')
fmri.info()
fig = plt.figure()
sns.relplot(data = fmri,
            kind ='line',
            x='timepoint',
            y='signal',
            col='region',
            hue='event',
            style='event')
plt.show()

# 4) 선형회귀모델을 포함한 산점도 : lmplot ------------------------
sns.lmplot(data=tips, x="total_bill", y="tip", col="time", hue="smoker")
plt.show()

# 5) 분포 : displot ---------------------------------------------
#kde : 커널밀도추정 그래프도 포함
sns.displot(data=tips, x="total_bill", col="time", kde=True)
plt.show()

# ecdf : 누적화된 분포
sns.displot(data=tips, kind="ecdf", x="total_bill", col="time",
            hue="smoker", rug=True)
plt.show()

# 6) catplot :categorical plot--------------------------------
sns.catplot(data=tips, kind="swarm",
            x="day", y="total_bill", hue="smoker")
plt.show()

sns.catplot(data=tips, kind="violin",
            x="day", y="total_bill", hue="smoker", split=True)
plt.show()

sns.catplot(data=tips, kind="bar",
            x="day", y="total_bill", hue="smoker")
plt.show()

# 7) jointplot : 다변량 ----------------------------------------
penguins = sns.load_dataset("penguins")
sns.jointplot(data=penguins, x="flipper_length_mm",
              y="bill_length_mm", hue="species")
plt.show()

sns.pairplot(data=penguins, hue="species")
plt.show()

#8) pairgrid : 대각선을 기준으로 위, 아래에 대해 각각의 시각화도구를 적용
# corner : 대각선 기준 한쪽은 삭제
g = sns.PairGrid(penguins, hue="species", corner=True)
g.map_lower(sns.kdeplot, hue=None, levels=5, color=".2")
g.map_lower(sns.scatterplot, marker="+")
g.map_diag(sns.histplot, element="step", linewidth=0, kde=True)
g.add_legend(frameon=True) # 범례
g.legend.set_bbox_to_anchor((.61, .6)) #범례 위치
plt.show()

# 9) ----------------------------------------------------------------
sns.relplot(
    data=penguins,
    x="bill_length_mm", y="bill_depth_mm", hue="body_mass_g")
plt.show()
#10) --------------------------------------------------------------
sns.set_theme(style="ticks", font_scale=1.25)
g = sns.relplot(
    data=penguins,
    x="bill_length_mm", y="bill_depth_mm", hue="body_mass_g",
    palette="crest", marker="x", s=100,
)
g.set_axis_labels("Bill length (mm)", "Bill depth (mm)", labelpad=10)#x축,y축
g.legend.set_title("Body mass (g)") # 범례제목
g.figure.set_size_inches(6.5, 4.5) #범례 위치
g.ax.margins(.15)
g.despine(trim=True) #축 테두리 제거
plt.show()
