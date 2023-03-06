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
