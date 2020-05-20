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

# optics = OPTICS().fit(dfCompletNoLabel)
#
# cluster_hierarchy_ = pd.DataFrame(optics.cluster_hierarchy_)
# cluster_hierarchy_.to_csv('cluster_hierarchy_.csv')
# labels_ = pd.DataFrame(optics.labels_)
# labels_.to_csv('labels_.csv')
# reachability_ = pd.DataFrame(optics.reachability_[optics.ordering_])
# reachability_.to_csv('reachability_.csv')


# cluster_hierarchy_ = pd.read_csv('cluster_hierarchy_.csv')
# labels_ = pd.read_csv('labels_.csv')
reachability_ = pd.read_csv('reachability_.csv')

fig = px.scatter(reachability_, y='0')
fig.show()

# fig = ff.create_dendrogram(cluster_hierarchy_)
# fig.update_layout(width=1000, height=1000)
# fig.show()

# dfComplet['cluster'] =
# score = adjusted_rand_score(dfComplet['label'], dfComplet['cluster'])
# dfComplet['object'] = dfComplet.index
# fig = px.scatter(dfComplet, x='object', y="cluster", color='label', title=str(score))
# fig.show()

#-------------------------------------------------------------------------------------------------------------------------

# pca = decomposition.PCA(n_components=3)
# pca.fit(dfCompletNoLabel)
# X = pca.transform(dfCompletNoLabel)
# PCA_df = pd.DataFrame(X)
# PCA_df['label'] = dfComplet['label']
#
# fig = px.scatter_3d(PCA_df, x=0, y=1, z=2, color='label')
# fig.show()
