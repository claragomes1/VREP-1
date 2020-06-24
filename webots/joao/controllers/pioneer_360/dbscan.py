import math
import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
from sklearn.cluster import OPTICS
from sklearn.metrics.cluster import adjusted_rand_score
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# -------------------------------------------------------------------------------------------------------------------------

# Carrega dados

# corredor_df = pd.read_csv('corredor.csv', index_col=0)

# -------------------------------------------------------------------------------------------------------------------------

# DBSCAN 1 e 2 com organização dos clusters de forma antihorária + preparo da animação

# x_complete = []
# y_complete = []
# id_complete = []
# id = -1
# labels_complete = []
# for line in corredor_df.values:
#     id += 1
#     x = []
#     y = []
#     for i in range(len(line)):
#         x.append(line[i] * math.cos(math.radians(i - 90)))
#         y.append(line[i] * math.sin(math.radians(i - 90)))
#     x_y_df = pd.DataFrame(data={'x': x, 'y': y})
#     dbscan = DBSCAN(eps=0.3, metric='euclidean').fit(x_y_df)
#     labels_temp = [-1] * len(dbscan.labels_)
#     label_counter = 0
#     visited = 0
#     while visited < len(dbscan.labels_):
#         cluster = dbscan.labels_[np.where(dbscan.labels_ != -2)[0][0]]
#         index_list = np.where(dbscan.labels_ == cluster)[0]
#         for index in index_list:
#             if cluster != -1:
#                 labels_temp[index] = label_counter
#             dbscan.labels_[index] = -2
#             visited += 1
#         if cluster != -1:
#             label_counter += 1
#     for each in x:
#         x_complete.append(each)
#     for each in y:
#         y_complete.append(each)
#     for each in [id] * len(line):
#         id_complete.append(each)
#     for each in labels_temp:
#         labels_complete.append(each)
# topography_df = pd.DataFrame(data={'x': x_complete, 'y': y_complete, 'id': id_complete, 'label': labels_complete})
# topography_df.to_csv('topography_df.csv')

# -------------------------------------------------------------------------------------------------------------------------

# Gera animação das leituras

# topography_df = pd.read_csv('topography_df.csv', index_col=0)
# fig = px.scatter(topography_df, x='x', y='y', color='label', animation_frame='id', range_x=[-5, 5], range_y=[-5, 5])
# fig.update_yaxes(dtick=0.5)
# fig.update_xaxes(dtick=0.5)
# fig.update_layout(height=500, width=500, title_text="Animacao dos pontos no corredor")
# fig.show()

# -------------------------------------------------------------------------------------------------------------------------

# PCA

# pca = PCA(n_components=3)
# pca.fit(<????????>)
# X = pca.transform(<???????>)
#
# fig = px.scatter_3d(X, x=0, y=1, z=2)
# fig.show()

# -------------------------------------------------------------------------------------------------------------------------

# OPTICS

# optics = OPTICS(metric='euclidean').fit(<?????>)
# reachability_ = pd.DataFrame(optics.reachability_[optics.ordering_])
# reachability_.index = optics.ordering_
# reachability_.to_csv('reachability_.csv')
#
# reachability_ = pd.read_csv('reachability_.csv')
# fig = px.scatter(reachability_, x=reachability_.index, y='0')
# fig.show()

# -------------------------------------------------------------------------------------------------------------------------
