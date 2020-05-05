import pandas as pd
from sklearn.cluster import DBSCAN
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.cluster import adjusted_rand_score

dfComplet = pd.read_csv('complete.csv')

dfCompletNoLabel = dfComplet.drop(columns=['label'])
dfCompletNoLabel = dfCompletNoLabel.abs()
scaler = MinMaxScaler(copy=False)
scaler.fit(dfCompletNoLabel)
scaler.transform(dfCompletNoLabel)

dbscan = DBSCAN(eps=0.56, metric='euclidean').fit(dfCompletNoLabel)
dfComplet['cluster'] = dbscan.labels_
score = adjusted_rand_score(dfComplet['label'], dfComplet['cluster'])

dfComplet['object'] = dfComplet.index
fig = px.scatter(dfComplet, x='object', y="cluster", color=dfComplet['label'], title=str(score))
fig.show()
