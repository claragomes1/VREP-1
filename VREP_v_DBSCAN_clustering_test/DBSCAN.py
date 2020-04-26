import pandas as pd
from sklearn.cluster import DBSCAN
import plotly.express as px

db = pd.read_csv('db.csv', index_col='object')
dbTest = db.drop(columns=["label"])
dbscan = DBSCAN(eps=11).fit(dbTest)
dbTest["label"] = dbscan.labels_
fig = px.scatter(dbTest, y="label")
fig.show()
