# Specifying a plot and mapping data
import seaborn.objects as so

so.Plot(penguins, x="bill_length_mm", y="bill_depth_mm").add(so.Dot())

so.Plot(penguins, x="bill_length_mm", y="bill_depth_mm").add(so.Dot(color="g", pointsize=4))


so.Plot(penguins, x="bill_length_mm", y="bill_depth_mm",
        color="species", pointsize="body_mass_g").add(so.Dot())

so.Plot(penguins, x="bill_length_mm", y="bill_depth_mm",
        edgecolor="sex", edgewidth="body_mass_g").add(so.Dot(color=".8"))

# Defining groups
so.Plot(healthexp, x="Year", y="Life_Expectancy", color="Country").add(so.Line())

so.Plot(healthexp, x="Year", y="Life_Expectancy", group="Country").add(so.Line())

# Transforming data before plotting
so.Plot(penguins, x="species", y="body_mass_g").add(so.Bar(), so.Agg())

so.Plot(penguins, x="species", y="body_mass_g").add(so.Dot(pointsize=10), so.Agg())

so.Plot(penguins, x="species", y="body_mass_g", color="sex").add(so.Dot(pointsize=10), so.Agg())

# Resolving overplotting
so.Plot(penguins, x="species", y="body_mass_g", color="sex").add(so.Bar(), so.Agg())

so.Plot(penguins, x="species", y="body_mass_g", color="sex").add(so.Bar(), so.Agg(), so.Dodge())

so.Plot(penguins, x="species", y="body_mass_g", color="sex").add(so.Dot(), so.Dodge())

so.Plot(penguins, x="species", y="body_mass_g", color="sex").add(so.Dot(), so.Dodge(), so.Jitter(.3))


# Creating variables through transformation
so.Plot(penguins, x="species").add(so.Bar(), so.Hist())

so.Plot(penguins, x="flipper_length_mm").add(so.Bars(), so.Hist())

so.Plot(penguins, x="body_mass_g", y="species", color="sex").add(so.Range(), so.Est(errorbar="sd"), so.Dodge()).add(so.Dot(), so.Agg(), so.Dodge())



# Orienting marks and transforms
so.Plot(penguins, x="body_mass_g", y="species", color="sex").add(so.Bar(), so.Agg(), so.Dodge())

so.Plot(tips, x="total_bill", y="size", color="time").add(so.Bar(), so.Agg(), so.Dodge(), orient="y")



#Building and displaying the plot
(so.Plot(tips, x="total_bill", y="tip")
    .add(so.Dots())
    .add(so.Line(), so.PolyFit())
)

so.Plot(tips, x="total_bill", y="tip", color="time").add(so.Dots()).add(so.Line(), so.PolyFit()) 


#Layer-specific mappings
so.Plot(tips, x="total_bill", y="tip"
       ).add(so.Dots(), color="time"
            ).add(so.Line(color=".2"), so.PolyFit())


so.Plot(tips, x="total_bill", y="tip", color="time"
       ).add(so.Dots()
            ).add(so.Line(color=".2"), so.PolyFit(), color=None)


# Faceting and pairing subplots

so.Plot(penguins, x="flipper_length_mm"
		).facet("species"
			).add(so.Bars(), so.Hist())


so.Plot(penguins, x="flipper_length_mm"
		).facet(col="species", row="sex"
			).add(so.Bars(), so.Hist())

so.Plot(healthexp, x="Year", y="Life_Expectancy"
		).facet(col="Country", wrap=3
			).add(so.Line())

so.Plot(healthexp, x="Year", y="Life_Expectancy"
		).facet("Country", wrap=3
			).add(so.Line(alpha=.3), group="Country", col=None
				).add(so.Line(linewidth=3))

so.Plot(penguins, y="body_mass_g", color="species"
		).pair(x=["bill_length_mm", "bill_depth_mm"]).add(so.Dots())


so.Plot(penguins, y="body_mass_g", color="species"
		).pair(x=["bill_length_mm", "bill_depth_mm"]
			).facet(row="sex").add(so.Dots())



# Integrating with matplotlib
f = mpl.figure.Figure(figsize=(8, 4))
sf1, sf2 = f.subfigures(1, 2)

so.Plot(penguins, x="body_mass_g", y="flipper_length_mm"
       ).add(so.Dots()).on(sf1).plot()

so.Plot(penguins, x="body_mass_g"
       ).facet(row="sex").add(so.Bars(), so.Hist()).on(sf2).plot()



# Building and displaying the plot

p = so.Plot(healthexp, "Year", "Spending_USD", color="Country")

p.add(so.Line())

p.add(so.Area(), so.Stack())

# Customizing the appearance
# Parameterizing scales

so.Plot(diamonds, x="carat", y="price"
       ).add(so.Dots()).scale(y="log")

so.Plot(diamonds, x="carat", y="price", color="clarity"
       ).add(so.Dots()).scale(color="flare")

so.Plot(diamonds, x="carat", y="price", color="clarity", pointsize="carat"
       ).add(so.Dots()).scale(color=("#88c", "#555"), pointsize=(2, 10))


so.Plot(diamonds, x="carat", y="price", color="carat", marker="cut"
       ).add(so.Dots()).scale(
        color=so.Continuous("crest", norm=(0, 3), trans="sqrt"),
        marker=so.Nominal(["o", "+", "x"], order=["Ideal", "Premium", "Good"]),)

# Customizing legends and ticks

so.Plot(diamonds, x="carat", y="price", color="carat"
       ).add(so.Dots()).scale(
        x=so.Continuous().tick(every=0.5),
        y=so.Continuous().label(like="${x:.0f}"),
        color=so.Continuous().tick(at=[1, 2, 3, 4]),
    )

# Customizing limits, labels, and titles
 so.Plot(penguins, x="body_mass_g", y="species", color="island"
	).facet(col="sex").add(so.Dot(), so.Jitter(.5)
			      ).share(x=False).limit(y=(2.5, -.5)
						    ).label(
        x="Body mass (g)", y="",
        color=str.capitalize,
        title="{} penguins".format,
    )


# Theme customization
from seaborn import axes_style
so.Plot().theme({**axes_style("whitegrid"), "grid.linestyle": ":"})























