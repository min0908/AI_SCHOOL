import seaborn as sns
import matplotlib.pyplot as plt

#1) stack graphs -----------------------
penguins = sns.load_dataset("penguins")
penguins.info()

sns.histplot(data = penguins,
             x='flipper_length_mm',
             hue = 'species',
             multiple = 'stack')
plt.show()

sns.kdeplot(data = penguins,
            x= 'flipper_length_mm',
            hue = 'species',
            multiple = 'stack')
plt.show()

#2) ------------------------
sns.displot(data = penguins,
            x = 'flipper_length_mm',
            hue = 'species',
            multiple='stack')
plt.show()

# hue, col 동일한 컬럼 -> 각 열별로 그림 생성
sns.displot(data=penguins, x="flipper_length_mm",
            hue="species", col="species")
plt.show()

#3) Axes-level ----------------------------------
f, axs = plt.subplots(1, 2, figsize = (8,4) ,
                       gridspec_kw = dict(width_ratio = [4,3]))
sns.scatterplot(data=penguins, x="flipper_length_mm",
                y="bill_length_mm", hue="species", ax=axs[0])
#shrink : 막대의 너비 
sns.histplot(data=penguins, x="species", hue="species",
             shrink=.8, alpha=.8, legend=False, ax=axs[1])
#f.tight_layout() # 여백과 관련된 레이아웃, 빈칸일땐 기본값
plt.show()


#4)Figure-level------------------------------------------
tips = sns.load_dataset("tips")
g = sns.relplot(data=tips, x="total_bill", y="tip")
g.ax.axline(xy1=(10, 2), slope=.2, color="b", dashes=(5, 2))

g = sns.relplot(data=penguins, x="flipper_length_mm", y="bill_length_mm", col="sex")
g.set_axis_labels("Flipper length (mm)", "Bill length (mm)")


f, ax = plt.subplots()
f, ax = plt.subplots(1, 2, sharey=True)

g = sns.FacetGrid(penguins)
g = sns.FacetGrid(penguins, col="sex")
g = sns.FacetGrid(penguins, col="sex", height=3.5, aspect=.75)


#5)Multiple views------------------------------------------
sns.jointplot(data=penguins, x="flipper_length_mm", y="bill_length_mm", hue="species")

sns.pairplot(data=penguins, hue="species")

sns.jointplot(data=penguins, x="flipper_length_mm", y="bill_length_mm", hue="species", kind="hist")
