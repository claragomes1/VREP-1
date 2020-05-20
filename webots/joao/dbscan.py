import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
from sklearn import decomposition
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.cluster import adjusted_rand_score
from sklearn.cluster import OPTICS
from sklearn.cluster import DBSCAN

dfComplet = pd.read_csv('complete.csv')
dfCompletNoLabel = dfComplet.drop(columns=['label'])
dfCompletNoLabel = dfCompletNoLabel.abs()
scaler = MinMaxScaler(copy=False)
scaler.fit(dfCompletNoLabel)
scaler.transform(dfCompletNoLabel)

#-------------------------------------------------------------------------------------------------------------------------

# dbscan = DBSCAN(eps=1.9, metric='euclidean').fit(dfCompletNoLabel)
# dfComplet['cluster'] = dbscan.labels_
# score = adjusted_rand_score(dfComplet['label'], dfComplet['cluster'])
# dfComplet['object'] = dfComplet.index
#
# fig = px.scatter(dfComplet, x='object', y="cluster", color=dfComplet['label'], title=str(score))
# fig.show()

#-------------------------------------------------------------------------------------------------------------------------

optics = OPTICS().fit(dfCompletNoLabel)
rangeImageCompleteDf = pd.DataFrame(optics.cluster_hierarchy_)
rangeImageCompleteDf.to_csv('optics_cluster_hierarchy_.csv')
fig = ff.create_dendrogram(optics.cluster_hierarchy_)
fig.show()

# dfComplet['cluster'] = optics.labels_
# score = adjusted_rand_score(dfComplet['label'], dfComplet['cluster'])
# dfComplet['object'] = dfComplet.index
#
# fig = px.scatter(dfComplet, x='object', y="cluster", color=dfComplet['label'], title=str(score))
# fig.show()

#-------------------------------------------------------------------------------------------------------------------------

# pca = decomposition.PCA(n_components=3)
# pca.fit(dfCompletNoLabel)
# X = pca.transform(dfCompletNoLabel)
# PCA_df = pd.DataFrame(X)
# PCA_df['cluster'] = optics.labels_
#
# fig = px.scatter_3d(PCA_df, x=0, y=1, z=2, color='cluster')
# fig.show()
