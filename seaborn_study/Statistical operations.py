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


