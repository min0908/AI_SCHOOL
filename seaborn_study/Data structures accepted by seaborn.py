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

import seaborn as sns
import matplotlib.pyplot as plt
# %matplotlib inline

# Long-term data
flights = sns.load_dataset("flights")
flights.head()

sns.relplot(data=flights, x="year", y="passengers", hue="month", kind="line")

# wide-form data
flights_wide = flights.pivot(index="year", columns="month", values="passengers")
flights_wide.head()

sns.relplot(data=flights_wide, kind="line")

sns.relplot(data=flights, x="month", y="passengers", hue="year", kind="line")

sns.relplot(data=flights_wide.transpose(), kind="line")

sns.catplot(data=flights_wide, kind="box")






