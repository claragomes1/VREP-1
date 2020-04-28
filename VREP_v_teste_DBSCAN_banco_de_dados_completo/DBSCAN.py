import pandas as pd
from sklearn.cluster import DBSCAN
import plotly.express as px

corredorDf = pd.read_csv('corredor.csv', index_col='object')
saida_direitaDf = pd.read_csv('saida_direita.csv', index_col='object')

corredorDf['label'] = ['corredor'] * len(corredorDf)
saida_direitaDf['label'] = ['saida_direita'] * len(saida_direitaDf)

dfComplet = saida_direitaDf.append(corredorDf, ignore_index=True)
dfComplet.dropna(inplace=True)

dfCompletNoLabel = dfComplet.drop(columns=['label'])
dbscan = DBSCAN(eps=0.086, metric='correlation').fit(dfCompletNoLabel)       # eps=0.00928 cosine / eps=0.08640 correlation
dfComplet['cluster'] = dbscan.labels_

dfComplet['object'] = dfComplet.index
fig = px.scatter(dfComplet, x='object', y="cluster", color=dfComplet['label'])
fig.show()
