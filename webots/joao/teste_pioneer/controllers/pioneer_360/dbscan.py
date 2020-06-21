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

corredor_df = pd.read_csv('corredor.csv', index_col=0)

# -------------------------------------------------------------------------------------------------------------------------

# DBSCAN 1 e 2 com organização dos clusters de forma antihorária + preparo da animação

# labels = []
# x_animacao = []
# y_animacao = []
# id_animacao = []
# id = -1
# labels_animacao = []
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
#     labels.append(labels_temp)
#     for each in x:
#         x_animacao.append(each)
#     for each in y:
#         y_animacao.append(each)
#     for each in [id] * len(line):
#         id_animacao.append(each)
#     for each in labels_temp:
#         labels_animacao.append(each)
# labels_df = pd.DataFrame(labels)
# labels_df.to_csv('labels_df.csv')
# x_y_df_animacao = pd.DataFrame(data={'x': x_animacao, 'y': y_animacao, 'id': id_animacao, 'label': labels_animacao})
# x_y_df_animacao.to_csv('x_y_df_animacao.csv')

# -------------------------------------------------------------------------------------------------------------------------

# Gera animação das leituras

# x_y_df_animacao = pd.read_csv('x_y_df_animacao.csv', index_col=0)
# print(x_y_df_animacao)
#
# fig = px.scatter(x_y_df_animacao, x='x', y='y', color='label', animation_frame='id', range_x=[-5, 5], range_y=[-5, 5])
# fig.update_yaxes(dtick=0.5)
# fig.update_xaxes(dtick=0.5)
# fig.update_layout(height=500, width=500, title_text="Corredor")
# fig.show()

# -------------------------------------------------------------------------------------------------------------------------

# Gerar grafico de labels de 50 em 50 leituras

# labels_df = pd.read_csv('labels_df.csv', index_col=0)
#
# fig = make_subplots(rows=13, cols=2)
# for i in range(1, 13):
#     fig.add_trace(
#         go.Scatter(y=labels_df.values[i*50]),
#         row=i, col=1
#     )
#     fig.add_trace(
#         go.Scatter(y=labels_df.values[i * 100]),
#         row=i, col=2
#     )
# fig.add_trace(
#     go.Scatter(y=labels_df.values[1250]),
#     row=13, col=1
# )
# fig.add_trace(
#     go.Scatter(y=labels_df.values[1299]),
#     row=13, col=2
# )
# fig.update_layout(height=1200, width=1250, title_text="Evolução das leituras")
# fig.show()

# labels_df = pd.read_csv('labels_df.csv', index_col=0)
# dbscan = DBSCAN(eps=0.1, metric='correlation').fit(labels_df)
# labels_df['label'] = dbscan.labels_
#
# fig = px.scatter(labels_df, x=labels_df.index, y='label')
# fig.show()

# -------------------------------------------------------------------------------------------------------------------------

# PCA

# pca = PCA(n_components=3)
# pca.fit(labels_df)
# X = pca.transform(labels_df)
#
# fig = px.scatter_3d(X, x=0, y=1, z=2)
# fig.show()

# -------------------------------------------------------------------------------------------------------------------------

# OPTICS

# optics = OPTICS(metric='euclidean').fit(labels_df)
# reachability_ = pd.DataFrame(optics.reachability_[optics.ordering_])
# reachability_.index = optics.ordering_
# reachability_.to_csv('reachability_.csv')
#
# reachability_ = pd.read_csv('reachability_.csv')
# fig = px.scatter(reachability_, x=reachability_.index, y='0')
# fig.show()

# -------------------------------------------------------------------------------------------------------------------------
