import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from sklearn.preprocessing import RobustScaler
from sklearn.metrics.cluster import adjusted_rand_score
from sklearn.cluster import OPTICS
from sklearn.cluster import DBSCAN
import math

corredor_df = pd.read_csv('corredor.csv', index_col=0)

#-------------------------------------------------------------------------------------------------------------------------

x_list = []
y_list = []
id_list = []
cluster_list = []
for i in range(len(corredor_df.values)):
    x_temp = []
    y_temp = []
    for j in range(len(corredor_df.values[i])):
        x = corredor_df.values[i][j] * math.cos(math.radians(j - 90))
        y = corredor_df.values[i][j] * math.sin(math.radians(j - 90))
        x_temp.append(x)
        y_temp.append(y)
        x_list.append(x)
        y_list.append(y)
        id_list.append(i)
    x_y_df_temp = pd.DataFrame(data={'x': x_temp, 'y': y_temp})
    dbscan = DBSCAN(eps=0.4, metric='euclidean').fit(x_y_df_temp)
    for label in dbscan.labels_:
        cluster_list.append(label)

x_y_df = pd.DataFrame(data={'x': x_list, 'y': y_list, 'id': id_list, 'cluster': cluster_list})

fig = px.scatter(x_y_df, x='x', y='y', color='cluster', animation_frame='id', range_x=[-5, 5], range_y=[-5, 5])
fig.update_yaxes(dtick=0.5)
fig.update_xaxes(dtick=0.5)
fig.update_layout(height=500, width=500, title_text="Corredor")
fig.show()

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
#     dbscan = DBSCAN(eps=0.2, metric='euclidean').fit(x_y_df)
#     labels.append(dbscan.labels_)
# labels_df = pd.DataFrame(labels)
# dbscan = DBSCAN(eps=0.1, metric='correlation').fit(labels_df)
# labels_df['cluster'] = dbscan.labels_

# fig = px.scatter(labels_df, x=labels_df.index, y='cluster')
# fig.show()

# fig = px.scatter(topography_map_df, x='x', y='y', color='label', range_x=[-5, 5], range_y=[-5, 5])
# fig.update_yaxes(dtick=0.5)
# fig.update_xaxes(dtick=0.5)
# fig.update_layout(height=500, width=500, title_text="Corredor")
# fig.show()

#-------------------------------------------------------------------------------------------------------------------------

# delta_y_complete = []
# for line in corredor_df.values:
# 	delta_y = []
# 	for i in range(len(line)-1):
# 		delta_y.append((line[i] - line[i+1]))
# 	delta_y_complete.append(delta_y)

# delta_y_df = pd.DataFrame(delta_y_complete)
# delta_y_df.to_csv('delta_y.csv')

# delta_y_df = pd.read_csv('delta_y.csv')
# pca = decomposition.PCA(n_components=5)
# pca.fit(delta_y_df)
# pca_df = pd.DataFrame(pca.transform(delta_y_df))
# pca_df.to_csv('pca_df.csv')
#
# dbscan = DBSCAN(eps=5, metric='euclidean').fit(pca_df)
# pca_df['cluster'] = dbscan.labels_
#
# fig = px.scatter(pca_df, x=pca_df.index, y="cluster")
# fig.show()

#-------------------------------------------------------------------------------------------------------------------------

# pca = decomposition.PCA(n_components=5)
# pca.fit(delta_y_complete_df_no_label)
# delta_y_pca_no_label = pca.transform(delta_y_complete_df_no_label)
# delta_y_pca_df = pd.DataFrame(delta_y_pca_no_label)
# delta_y_pca_df['label'] = label_list
# delta_y_pca_df.index.name = 'object'
# delta_y_pca_df.to_csv('delta_y_pca_df.csv')
#
# delta_y_pca_df = pd.read_csv('delta_y_pca_df.csv', index_col='object')
# delta_y_pca_df_no_label = delta_y_pca_df.drop(columns=['label'])
#
# fig = px.line(delta_y_pca_df_no_label.values[10861], y=delta_y_pca_df_no_label.values[10861])
# fig.show()

#-------------------------------------------------------------------------------------------------------------------------

# optics = OPTICS(metric='euclidean').fit(delta_y_pca_df_no_label)
# reachability_ = pd.DataFrame(optics.reachability_[optics.ordering_])
# reachability_['label'] = label_list
# reachability_.index = optics.ordering_
# reachability_.to_csv('reachability_.csv')
#
# reachability_ = pd.read_csv('reachability_.csv')
# fig = px.scatter(reachability_, x=reachability_.index, y='0', color='label')
# fig.show()
#
# # delta_y_complete_df['cluster'] = optics.labels_[optics.ordering_]
# # delta_y_complete_df.index = optics.ordering_
# # score = adjusted_rand_score(delta_y_complete_df['label'], delta_y_complete_df['cluster'])
# # fig = px.scatter(delta_y_complete_df, x=delta_y_complete_df.index, y="cluster", color='label', title=str(score))
# # fig.show()

#-------------------------------------------------------------------------------------------------------------------------

# dbscan = DBSCAN(eps=20, metric='euclidean').fit(delta_y_pca_df_no_label)
#
# delta_y_pca_df_no_label['cluster'] = dbscan.labels_
# delta_y_pca_df_no_label['label'] = label_list
# score = adjusted_rand_score(delta_y_pca_df_no_label['label'], delta_y_pca_df_no_label['cluster'])
#
# fig = px.scatter(delta_y_pca_df_no_label, x=delta_y_pca_df_no_label.index, y="cluster", color='label', title=str(score))
# fig.show()
