import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from sklearn import decomposition
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.cluster import adjusted_rand_score
from sklearn.cluster import OPTICS
from sklearn.cluster import DBSCAN

corredor_df = pd.read_csv('corredor.csv')

#-------------------------------------------------------------------------------------------------------------------------

delta_y = []
delta_y_complete = []
for line in corredor_df.values:
	weight = list(range(90))
	counter = -1
	sinal = 1
	for i in range(len(line)-1):
		counter += sinal
		if counter == 90 or counter == -1:
			sinal *= -1
			counter += sinal
		counter += sinal
		delta_y.append((line[i] - line[i+1]) * weight[counter])
	delta_y_complete.append(delta_y)
	delta_y = []

fig = px.scatter(y=delta_y_complete[0])
fig.show()

# delta_y_df = pd.DataFrame(delta_y_complete)
# delta_y_df.to_csv('delta_y.csv')
#
# dbscan = DBSCAN(eps=5, metric='euclidean').fit(delta_y_df)
# delta_y_df['cluster'] = dbscan.labels_
#
# fig = px.scatter(delta_y_df, x=delta_y_df.index, y="cluster")
# fig.show()

#-------------------------------------------------------------------------------------------------------------------------

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
