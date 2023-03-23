# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="darkgrid")
%matplotlib inline

# %% [markdown]
# # Relating variables with scatter plots

# %%
tips = sns.load_dataset("tips")
sns.relplot(data=tips, x="total_bill", y="tip")

# %%
sns.relplot(data=tips, x="total_bill", y="tip", hue="smoker")

# %%
sns.relplot(
    data=tips,
    x="total_bill", y="tip", hue="smoker", style="smoker")

# %%
sns.relplot(
    data=tips, x="total_bill", y="tip", hue="size")

# %%
sns.relplot(
    data=tips,
    x="total_bill", y="tip",
    hue="size", palette="ch:r=-.5,l=.75")

# %%
sns.relplot(data=tips, x="total_bill", y="tip", size="size")

# %%
sns.relplot(
    data=tips, x="total_bill", y="tip",
    size="size", sizes=(15, 200))

# %% [markdown]
# # Emphasizing continuity with line plots

# %%
dowjones = sns.load_dataset("dowjones")
sns.relplot(data=dowjones, x="Date", y="Price", kind="line")

# %% [markdown]
# ## Aggregation and representing uncertainty

# %%
fmri = sns.load_dataset("fmri")
sns.relplot(data=fmri, x="timepoint", y="signal", kind="line")

# %%
sns.relplot(
    data=fmri, kind="line",
    x="timepoint", y="signal", errorbar=None)

# %%
sns.relplot(
    data=fmri, kind="line",
    x="timepoint", y="signal", errorbar="sd")

# %%
sns.relplot(
    data=fmri, kind="line",
    x="timepoint", y="signal",
    estimator=None)

# %% [markdown]
# ## Plotting subsets of data with semantic mappings

# %%
sns.relplot(
    data=fmri, kind="line",
    x="timepoint", y="signal", hue="event")

# %%
sns.relplot(
    data=fmri, kind="line",
    x="timepoint", y="signal",
    hue="region", style="event")

# %%
sns.relplot(
    data=fmri, kind="line",
    x="timepoint", y="signal", hue="region", style="event",
    dashes=False, markers=True)

# %%
sns.relplot(
    data=fmri, kind="line",
    x="timepoint", y="signal", hue="event", style="event")

# %%
sns.relplot(
    data=fmri.query("event == 'stim'"), kind="line",
    x="timepoint", y="signal", hue="region",
    units="subject", estimator=None)

# %%
dots = sns.load_dataset("dots").query("align == 'dots'")
sns.relplot(
    data=dots, kind="line",
    x="time", y="firing_rate",
    hue="coherence", style="choice")

# %%
palette = sns.cubehelix_palette(light=.8, n_colors=6)
sns.relplot(
    data=dots, kind="line",
    x="time", y="firing_rate",
    hue="coherence", style="choice", palette=palette)

# %%
from matplotlib.colors import LogNorm
palette = sns.cubehelix_palette(light=.7, n_colors=6)
sns.relplot(
    data=dots.query("coherence > 0"), kind="line",
    x="time", y="firing_rate",
    hue="coherence", style="choice",
    hue_norm=LogNorm())

# %%
sns.relplot(
    data=dots, kind="line",
    x="time", y="firing_rate",
    size="coherence", style="choice")

# %%
sns.relplot(
    data=dots, kind="line",
    x="time", y="firing_rate",
    hue="coherence", size="choice", palette=palette)

# %% [markdown]
# ## Controlling sorting and orientation

# %%
healthexp = sns.load_dataset("healthexp").sort_values("Year")
sns.relplot(
    data=healthexp, kind="line",
    x="Spending_USD", y="Life_Expectancy", hue="Country",
    sort=False)

# %%
sns.relplot(
    data=fmri, kind="line",
     x="signal", y="timepoint", hue="event",
    orient="y")

# %% [markdown]
# # Showing multiple relationships with facets

# %%
sns.relplot(
    data=tips,
    x="total_bill", y="tip", hue="smoker", col="time")

# %%
sns.relplot(
    data=fmri, kind="line",
    x="timepoint", y="signal", hue="subject",
    col="region", row="event", height=3,
    estimator=None)

# %%
sns.relplot(
    data=fmri.query("region == 'frontal'"), kind="line",
    x="timepoint", y="signal", hue="event", style="event",
    col="subject", col_wrap=5,
    height=3, aspect=.75, linewidth=2.5)

# %% [markdown]
# # Plotting univariate histograms

# %%
penguins = sns.load_dataset("penguins")
sns.displot(penguins, x="flipper_length_mm")

# %%
sns.displot(penguins, x="flipper_length_mm", binwidth=3)

# %%
sns.displot(penguins, x="flipper_length_mm", bins=20)

# %%
tips = sns.load_dataset("tips")
sns.displot(tips, x="size")

# %%
sns.displot(tips, x="size", bins=[1, 2, 3, 4, 5, 6, 7])

# %%
sns.displot(tips, x="size", discrete=True)

# %%
sns.displot(tips, x="day", shrink=.8)

# %% [markdown]
# ## Conditioning on other variables

# %%
sns.displot(penguins, x="flipper_length_mm", hue="species")

# %%
sns.displot(penguins, x="flipper_length_mm", hue="species", element="step")

# %%
sns.displot(penguins, x="flipper_length_mm", hue="species", multiple="stack")

# %%
sns.displot(penguins, x="flipper_length_mm", hue="sex", multiple="dodge")

# %%
sns.displot(penguins, x="flipper_length_mm", col="sex")

# %% [markdown]
# ## Normalized histogram statistics

# %%
sns.displot(penguins, x="flipper_length_mm", hue="species", stat="density")

# %%
sns.displot(penguins, x="flipper_length_mm", hue="species", stat="density", common_norm=False)

# %%
sns.displot(penguins, x="flipper_length_mm", hue="species", stat="probability")

# %%
sns.displot(penguins, x="flipper_length_mm", hue="species", stat="probability")

# %% [markdown]
# ## Kernel density estimation

# %%
sns.displot(penguins, x="flipper_length_mm", kind="kde")

# %% [markdown]
# ## Choosing the smoothing bandwidth

# %%
sns.displot(penguins, x="flipper_length_mm", kind="kde", bw_adjust=.25)

# %%
sns.displot(penguins, x="flipper_length_mm", kind="kde", bw_adjust=2)

# %% [markdown]
# ## Conditioning on other variables

# %%
sns.displot(penguins, x="flipper_length_mm", hue="species", kind="kde")

# %%
sns.displot(penguins, x="flipper_length_mm", hue="species", kind="kde", multiple="stack")

# %%
sns.displot(penguins, x="flipper_length_mm", hue="species", kind="kde", fill=True)

# %% [markdown]
# ## Kernel density estimation pitfalls

# %%
sns.displot(tips, x="total_bill", kind="kde")

# %%
sns.displot(tips, x="total_bill", kind="kde", cut=0)

# %%
diamonds = sns.load_dataset("diamonds")
sns.displot(diamonds, x="carat", kind="kde")

# %%
sns.displot(diamonds, x="carat")

# %%
sns.displot(diamonds, x="carat", kde=True)

# %% [markdown]
# # Empirical cumulative distributions

# %%
sns.displot(penguins, x="flipper_length_mm", kind="ecdf")

# %%
sns.displot(penguins, x="flipper_length_mm", hue="species", kind="ecdf")

# %% [markdown]
# # Visualizing bivariate distributions

# %%
sns.displot(penguins, x="bill_length_mm", y="bill_depth_mm")


# %%
sns.displot(penguins, x="bill_length_mm", y="bill_depth_mm", kind="kde")

# %%
sns.displot(penguins, x="bill_length_mm", y="bill_depth_mm", hue="species")

# %%
sns.displot(penguins, x="bill_length_mm", y="bill_depth_mm", hue="species", kind="kde")

# %%
sns.displot(penguins, x="bill_length_mm", y="bill_depth_mm", binwidth=(2, .5))

# %%
sns.displot(penguins, x="bill_length_mm", y="bill_depth_mm", binwidth=(2, .5), cbar=True)

# %%
sns.displot(penguins, x="bill_length_mm", y="bill_depth_mm", kind="kde", levels=[.01, .05, .1, .8])

# %%
sns.displot(diamonds, x="price", y="clarity", log_scale=(True, False))

# %%
sns.displot(diamonds, x="color", y="clarity")

# %% [markdown]
# # Distribution visualization in other settings

# %% [markdown]
# ## Plotting joint and marginal distributions

# %%
sns.jointplot(data=penguins, x="bill_length_mm", y="bill_depth_mm")

# %%
sns.jointplot(
    data=penguins,
    x="bill_length_mm", y="bill_depth_mm", hue="species",
    kind="kde"
)

# %%
g = sns.JointGrid(data=penguins, x="bill_length_mm", y="bill_depth_mm")
g.plot_joint(sns.histplot)
g.plot_marginals(sns.boxplot)

# %%
sns.displot(
    penguins, x="bill_length_mm", y="bill_depth_mm",
    kind="kde", rug=True
)

# %%
sns.relplot(data=penguins, x="bill_length_mm", y="bill_depth_mm")
sns.rugplot(data=penguins, x="bill_length_mm", y="bill_depth_mm")

# %% [markdown]
# ## Plotting many distributions

# %%
sns.pairplot(penguins)

# %%
g = sns.PairGrid(penguins)
g.map_upper(sns.histplot)
g.map_lower(sns.kdeplot, fill=True)
g.map_diag(sns.histplot, kde=True)

# %%



