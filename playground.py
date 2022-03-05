import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import os
from pandasql import sqldf

df = pd.read_csv("results/3x3.csv")
df['Result'] = df['Result'].astype('float')
df['Date'] = pd.to_datetime(df['Date'])

names = df.Name.unique()

mdf = df[df['Name'] == 'Mayank Agarwal']

px.line(mdf, x='Date', y='Result', markers=True, title="Mayank Agarwal")

# +
# for name in names:
#     tdf = df[df['Name'] == name]
#     if len(tdf) < 5:
#         continue
#     fig = px.line(tdf, x='Date', y='Result', title=name, markers=True)
#     fig.show()
# -

sns.lineplot(x=mdf['Date'], y=df['Result'], markers=True)
plt.show()

files = os.listdir("results")
events = [f.rstrip(".csv") for f in files]

df['Event'] = ['3x3' for i in range(len(df))]
df

# +
frames = []
for f in files:
    df = pd.read_csv(os.path.join("results", f))
    df['Date'] = pd.to_datetime(df['Date'])
#     df['Result'] = df['Result'].astype('float')
    df['Event'] = [f.rstrip(".csv") for i in range(len(df))]
    frames.append(df)

cdf = pd.concat(frames)
# -

cdf

mcdf = cdf[cdf['Name'] == 'Mayank Agarwal']

px.line(mcdf, x='Date', y='Result', color='Event', markers=True)

selected_events = ['2x2', '4x4']

cdf

name = "Yash Jakhmola"

cdf[cdf['Name'] == name]['Institute'].iloc[0]

a = mcdf['Event'].value_counts()

cdf['Name'].value_counts()

mcdf[mcdf['Result'] != 'DNF'].sort_values('Result').groupby('Event').get_group('3x3').iloc[0][['Date', 'Result', 'Event']]


