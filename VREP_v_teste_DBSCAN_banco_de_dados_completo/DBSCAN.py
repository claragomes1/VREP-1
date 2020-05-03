import pandas as pd
from sklearn.cluster import DBSCAN
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.cluster import adjusted_rand_score

corredorDf = pd.read_csv('corredor.csv', index_col='object')
encruzilhada_direitaDf = pd.read_csv('encruzilhada_direita.csv', index_col='object')
encruzilhada_esquerdaDf = pd.read_csv('encruzilhada_esquerda.csv', index_col='object')

corredorDf['label'] = ['corredor'] * len(corredorDf)
encruzilhada_direitaDf['label'] = ['encruzilhada_direita'] * len(encruzilhada_direitaDf)
encruzilhada_esquerdaDf['label'] = ['encruzilhada_esquerda'] * len(encruzilhada_esquerdaDf)

dfComplet = encruzilhada_direitaDf.append(corredorDf, ignore_index=True)
dfComplet = encruzilhada_esquerdaDf.append(dfComplet, ignore_index=True)
dfComplet.dropna(inplace=True)

dfCompletNoLabel = dfComplet.drop(columns=['label'])
scaler = MinMaxScaler(copy=False, feature_range=(0,10))
scaler.fit(dfCompletNoLabel)
scaler.transform(dfCompletNoLabel)
dbscan = DBSCAN(eps=0.036, metric='correlation').fit(dfCompletNoLabel)
dfComplet['cluster'] = dbscan.labels_

score = adjusted_rand_score(dfComplet['label'], dfComplet['cluster'])

dfComplet['object'] = dfComplet.index
fig = px.scatter(dfComplet, x='object', y="cluster", color=dfComplet['label'], title=str(score))
fig.show()
