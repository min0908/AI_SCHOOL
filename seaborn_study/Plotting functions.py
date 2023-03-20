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

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="darkgrid")
# %matplotlib inline

# # Relating variables with scatter plots

tips = sns.load_dataset("tips")
sns.relplot(data=tips, x="total_bill", y="tip")

sns.relplot(data=tips, x="total_bill", y="tip", hue="smoker")

sns.relplot(
    data=tips,
    x="total_bill", y="tip", hue="smoker", style="smoker")

sns.relplot(
    data=tips, x="total_bill", y="tip", hue="size")

sns.relplot(
    data=tips,
    x="total_bill", y="tip",
    hue="size", palette="ch:r=-.5,l=.75")

sns.relplot(data=tips, x="total_bill", y="tip", size="size")

sns.relplot(
    data=tips, x="total_bill", y="tip",
    size="size", sizes=(15, 200))

# # Emphasizing continuity with line plots

dowjones = sns.load_dataset("dowjones")
sns.relplot(data=dowjones, x="Date", y="Price", kind="line")

# ## Aggregation and representing uncertainty

fmri = sns.load_dataset("fmri")
sns.relplot(data=fmri, x="timepoint", y="signal", kind="line")

sns.relplot(
    data=fmri, kind="line",
    x="timepoint", y="signal", errorbar=None)

sns.relplot(
    data=fmri, kind="line",
    x="timepoint", y="signal", errorbar="sd")

sns.relplot(
    data=fmri, kind="line",
    x="timepoint", y="signal",
    estimator=None)

# ## Plotting subsets of data with semantic mappings

sns.relplot(
    data=fmri, kind="line",
    x="timepoint", y="signal", hue="event")

sns.relplot(
    data=fmri, kind="line",
    x="timepoint", y="signal",
    hue="region", style="event")

sns.relplot(
    data=fmri, kind="line",
    x="timepoint", y="signal", hue="region", style="event",
    dashes=False, markers=True)

sns.relplot(
    data=fmri, kind="line",
    x="timepoint", y="signal", hue="event", style="event")

sns.relplot(
    data=fmri.query("event == 'stim'"), kind="line",
    x="timepoint", y="signal", hue="region",
    units="subject", estimator=None)

dots = sns.load_dataset("dots").query("align == 'dots'")
sns.relplot(
    data=dots, kind="line",
    x="time", y="firing_rate",
    hue="coherence", style="choice")

palette = sns.cubehelix_palette(light=.8, n_colors=6)
sns.relplot(
    data=dots, kind="line",
    x="time", y="firing_rate",
    hue="coherence", style="choice", palette=palette)

from matplotlib.colors import LogNorm
palette = sns.cubehelix_palette(light=.7, n_colors=6)
sns.relplot(
    data=dots.query("coherence > 0"), kind="line",
    x="time", y="firing_rate",
    hue="coherence", style="choice",
    hue_norm=LogNorm())

sns.relplot(
    data=dots, kind="line",
    x="time", y="firing_rate",
    size="coherence", style="choice")

sns.relplot(
    data=dots, kind="line",
    x="time", y="firing_rate",
    hue="coherence", size="choice", palette=palette)

# ## Controlling sorting and orientation




