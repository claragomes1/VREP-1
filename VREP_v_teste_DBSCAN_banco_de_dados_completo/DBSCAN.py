import pandas as pd
from sklearn.cluster import DBSCAN
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.cluster import adjusted_rand_score

corredorDf = pd.read_csv('corredor.csv', index_col='object')
saida_direitaDf = pd.read_csv('saida_direita.csv', index_col='object')

corredorDf['label'] = ['corredor'] * len(corredorDf)
saida_direitaDf['label'] = ['saida_direita'] * len(saida_direitaDf)

dfComplet = saida_direitaDf.append(corredorDf, ignore_index=True)
dfComplet.dropna(inplace=True)

dfCompletNoLabel = dfComplet.drop(columns=['label'])
scaler = MinMaxScaler(copy=False)
scaler.fit(dfCompletNoLabel)
scaler.transform(dfCompletNoLabel)
dbscan = DBSCAN(eps=0.12, metric='correlation').fit(dfCompletNoLabel)   # eps=0.017 cosine / eps=0.12 correlation / eps=1.2 euclidean
dfComplet['cluster'] = dbscan.labels_

score = adjusted_rand_score(dfComplet['label'], dfComplet['cluster'])

dfComplet['object'] = dfComplet.index
fig = px.scatter(dfComplet, x='object', y="cluster", color=dfComplet['label'], title=str(score))
fig.show()
