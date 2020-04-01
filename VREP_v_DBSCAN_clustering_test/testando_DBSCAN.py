import pandas as pd
from sklearn.cluster import DBSCAN
import plotly.express as px

df = pd.read_csv("data_2020_4_1_1_34_21.csv")
for i in list(df.columns):
	column = df.drop(columns=[str(i)])
	db = DBSCAN(eps=3, min_samples=5).fit(column)
	df["labels" + str(i)] = db.labels_

fig = px.scatter(df, y='0', color="labels0")
fig.for_each_trace(lambda trace: trace.update(name=trace.name.replace("=", ": ")),)
fig.show()

