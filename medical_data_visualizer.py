import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')

# Add 'overweight' column
df['overweight'] = ((df.weight / ((df.height / 100) ** 2)) > 25).astype(int)

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholestorol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.

# normalize cholesterol
# if cholesterol is normal(1) mark as good(0)
# do this first so we don't confuse the data, i.e. order matters
df.loc[df['cholesterol'] == 1, ['cholesterol']] = 0
# if cholesterol is above normal(2,3) mark as bad(1)
df.loc[df['cholesterol'] > 1, ['cholesterol']] = 1

# normalize gluc
# if gluc is normal(1) mark as good(0)
# do this first so we don't confuse the data, i.e. order matters
df.loc[df['gluc'] == 1, ['gluc']] = 0
# if gluc is above normal(2,3) mark as bad(1)
df.loc[df['gluc'] > 1, ['gluc']] = 1

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = df.melt(id_vars=['cardio'], value_vars=['cholesterol', 'gluc', 'alco', 'active', 'overweight', 'smoke'])

    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the collumns for the catplot to work correctly.
    df_cat = df_cat.groupby(['cardio', 'variable', 'value'], as_index=False).size().rename(columns={"size": "total"})

    # Draw the catplot with 'sns.catplot()'
    g = sns.catplot(x="variable", y="total", hue="value", data=df_cat, col="cardio", kind="bar")
    fig = g.fig

    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df.loc[(df['ap_lo'] <= df['ap_hi']) & (df['height'] >= df['height'].quantile(0.025)) & (df['height'] <= df['height'].quantile(0.975)) & (df['weight'] >= df['weight'].quantile(0.025)) & (df['weight'] <= df['weight'].quantile(0.975))]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr))



    # Set up the matplotlib figure
    fig, ax = plt.subplots()

    # Draw the heatmap with 'sns.heatmap()'
    ax = sns.heatmap(corr, vmin=-0.16, vmax=0.32,annot=True, fmt="0.1f", mask=mask, ax=ax)

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
