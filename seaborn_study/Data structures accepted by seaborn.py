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

# Messy data
anagrams = sns.load_dataset("anagrams")
anagrams_long = anagrams.melt(id_vars=["subidr", "attnr"], var_name="solutions", value_name="score")
anagrams_long.head()

sns.catplot(data=anagrams_long, x="solutions", y="score", hue="attnr", kind="point")

flights_dict = flights.to_dict()
sns.relplot(data=flights_dict, x="year", y="passengers", hue="month", kind="line")

flights_avg = flights.groupby("year").mean()
sns.relplot(data=flights_avg, x="year", y="passengers", kind="line")

flights_avg = flights.groupby("year").mean()

year = flights_avg.index
passengers = flights_avg["passengers"]
sns.relplot(x=year, y=passengers, kind="line")

sns.relplot(x=year.to_numpy(), y=passengers.to_list(), kind="line")


# Options for visualizeing wide-form data
flights_wide_list = [col for _, col in flights_wide.items()]
sns.relplot(data=flights_wide_list, kind="line")

two_series = [flights_wide.loc[:1955, "Jan"], flights_wide.loc[1952:, "Aug"]]
sns.relplot(data=two_series, kind="line")

two_arrays = [s.to_numpy() for s in two_series]
sns.relplot(data=two_arrays, kind="line")

two_arrays_dict = {s.name: s.to_numpy() for s in two_series}
sns.relplot(data=two_arrays_dict, kind="line")

flights_array = flights_wide.to_numpy()
sns.relplot(data=flights_array, kind="line")





