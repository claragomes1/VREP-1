import pandas as pd
import plotly.express as px
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
from sklearn.cluster import OPTICS
from sklearn.metrics.cluster import adjusted_rand_score
import math

#-------------------------------------------------------------------------------------------------------------------------

# Carrega dados

# corredor_df = pd.read_csv('corredor.csv', index_col=0)

#-------------------------------------------------------------------------------------------------------------------------

# Gera animação

# x_list = []
# y_list = []
# id_list = []
# cluster_list = []
# for i in range(len(corredor_df.values)):
#     x_temp = []
#     y_temp = []
#     for j in range(len(corredor_df.values[i])):
#         x = corredor_df.values[i][j] * math.cos(math.radians(j - 90))
#         y = corredor_df.values[i][j] * math.sin(math.radians(j - 90))
#         x_temp.append(x)
#         y_temp.append(y)
#         x_list.append(x)
#         y_list.append(y)
#         id_list.append(i)
#     x_y_df_temp = pd.DataFrame(data={'x': x_temp, 'y': y_temp})
#     dbscan = DBSCAN(eps=0.4, metric='euclidean').fit(x_y_df_temp)
#     for label in dbscan.labels_:
#         cluster_list.append(label)
#
# x_y_df = pd.DataFrame(data={'x': x_list, 'y': y_list, 'id': id_list, 'cluster': cluster_list})
#
# fig = px.scatter(x_y_df, x='x', y='y', color='cluster', animation_frame='id', range_x=[-5, 5], range_y=[-5, 5])
# fig.update_yaxes(dtick=0.5)
# fig.update_xaxes(dtick=0.5)
# fig.update_layout(height=500, width=500, title_text="Corredor")
# fig.show()

#-------------------------------------------------------------------------------------------------------------------------

# DBSCAN 1 e 2

# labels = []
# for line in corredor_df.values:
#     x = []
#     y = []
#     for i in range(len(line)):
#         x.append(line[i] * math.cos(math.radians(i - 90)))
#         y.append(line[i] * math.sin(math.radians(i - 90)))
#     x_y_df = pd.DataFrame()
#     x_y_df['x'] = x
#     x_y_df['y'] = y
#     dbscan = DBSCAN(eps=0.3, metric='euclidean').fit(x_y_df)
#     labels.append(dbscan.labels_)
# labels_df = pd.DataFrame(labels)
# labels_df.to_csv('labels_df.csv')

labels_df = pd.read_csv('labels_df.csv', index_col=0)
# dbscan = DBSCAN(eps=0.08, metric='correlation').fit(labels_df)
# labels_df['cluster'] = dbscan.labels_
#
# fig = px.scatter(labels_df, x=labels_df.index, y='cluster')
# fig.show()

#-------------------------------------------------------------------------------------------------------------------------

# PCA

# pca = PCA(n_components=3)
# pca.fit(labels_df)
# X = pca.transform(labels_df)
#
# fig = px.scatter_3d(X, x=0, y=1, z=2)
# fig.show()

#-------------------------------------------------------------------------------------------------------------------------

#OPTICS

# optics = OPTICS(metric='euclidean').fit(labels_df)
# reachability_ = pd.DataFrame(optics.reachability_[optics.ordering_])
# reachability_.index = optics.ordering_
# reachability_.to_csv('reachability_.csv')
#
# reachability_ = pd.read_csv('reachability_.csv')
# fig = px.scatter(reachability_, x=reachability_.index, y='0')
# fig.show()

#-------------------------------------------------------------------------------------------------------------------------

# TODO:

# 1- Fixar um ponto e gerar clusters de acordo com o angulo associado a eles.
