# Statistical estimation and error bars

def plot_errorbars(arg, **kws):
    np.random.seed(sum(map(ord, "error_bars")))
    x = np.random.normal(0, 1, 100)
    f, axs = plt.subplots(2, figsize=(7, 2), sharex=True, layout="tight")
    sns.pointplot(x=x, errorbar=arg, **kws, capsize=.3, ax=axs[0])
    sns.stripplot(x=x, jitter=.3, ax=axs[1])


# Measures of data spread

## Standard deviation error bars
plot_errorbars("sd")

## Percentile interval error bars
plot_errorbars(("pi", 50))

# Measures of estimate uncertainty
## Standard error bars
plot_errorbars("se")

## Confidence interval error bars
plot_errorbars("ci")

plot_errorbars(("se", 2))

plot_errorbars("ci", estimator="median")

plot_errorbars("ci", n_boot=5000, seed=10)

## Custom error bars
plot_errorbars(lambda x: (x.min(), x.max()))

## Error bars on regression fits
x = np.random.normal(0, 1, 50)
y = x * 2 + np.random.normal(0, 2, size=x.size)
sns.regplot(x=x, y=y)


# Estimating regression fits
## Functions for drawing linear regression models
tips = sns.load_dataset("tips")
sns.regplot(x="total_bill", y="tip", data=tips);

sns.lmplot(x="total_bill", y="tip", data=tips);

sns.lmplot(x="size", y="tip", data=tips);

sns.lmplot(x="size", y="tip", data=tips, x_jitter=.05);


sns.lmplot(x="size", y="tip", data=tips, x_estimator=np.mean);


## Fitting different kinds of models
anscombe = sns.load_dataset("anscombe")
sns.lmplot(x="x", y="y", data=anscombe.query("dataset == 'I'"),
           ci=None, scatter_kws={"s": 80});

sns.lmplot(x="x", y="y", data=anscombe.query("dataset == 'II'"),
           ci=None, scatter_kws={"s": 80});

sns.lmplot(x="x", y="y", data=anscombe.query("dataset == 'II'"),
           order=2, ci=None, scatter_kws={"s": 80});

sns.lmplot(x="x", y="y", data=anscombe.query("dataset == 'III'"),
           ci=None, scatter_kws={"s": 80});


sns.lmplot(x="x", y="y", data=anscombe.query("dataset == 'III'"),
           robust=True, ci=None, scatter_kws={"s": 80});

tips["big_tip"] = (tips.tip / tips.total_bill) > .15
sns.lmplot(x="total_bill", y="big_tip", data=tips,
           y_jitter=.03);

sns.lmplot(x="total_bill", y="big_tip", data=tips,
           logistic=True, y_jitter=.03);

sns.lmplot(x="total_bill", y="tip", data=tips,
           lowess=True, line_kws={"color": "C1"});

sns.residplot(x="x", y="y", data=anscombe.query("dataset == 'I'"),
              scatter_kws={"s": 80});

sns.residplot(x="x", y="y", data=anscombe.query("dataset == 'II'"),
              scatter_kws={"s": 80});


## Conditioning on other variables
sns.lmplot(x="total_bill", y="tip", hue="smoker", data=tips);

sns.lmplot(x="total_bill", y="tip", hue="smoker", data=tips,
           markers=["o", "x"], palette="Set1");

sns.lmplot(x="total_bill", y="tip", hue="smoker", col="time", data=tips);

sns.lmplot(x="total_bill", y="tip", hue="smoker",
           col="time", row="sex", data=tips, height=3);

## Plotting a regression in other contexts
sns.jointplot(x="total_bill", y="tip", data=tips, kind="reg");

sns.pairplot(tips, x_vars=["total_bill", "size"], y_vars=["tip"],
             height=5, aspect=.8, kind="reg");

sns.pairplot(tips, x_vars=["total_bill", "size"], y_vars=["tip"],
             hue="smoker", height=5, aspect=.8, kind="reg"); 




