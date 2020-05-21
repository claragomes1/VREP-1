#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 15:53:16 2020

@author: clara
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2020

@author: clara
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.cluster.hierarchy as shc
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import normalize
from sklearn import metrics

saida_direita = pd.read_csv('saida_direita1.csv', index_col='object')
saida_esquerda = pd.read_csv('saida_esquerda1.csv', index_col = 'object')
encruzilhada_esquerda = pd.read_csv('encruzilhada_esquerda1.csv', index_col='object')
corredor = pd.read_csv('corredor.csv', index_col='object')


dataset = pd.concat([saida_direita, saida_esquerda, encruzilhada_esquerda, corredor], axis=0, ignore_index=True)
dataset.head()

dataset['label'] = dataset['label'].replace('saida_direita',0)
dataset['label'] = dataset['label'].replace('saida_esquerda',1)
dataset['label'] = dataset['label'].replace('encruzilhada_esquerda',2)
dataset['label'] = dataset['label'].replace('corredor',3)



datasetNoLabel = dataset.drop(columns=['label'])
print(datasetNoLabel)
aux = []
datasetNoLabel = normalize(datasetNoLabel)
for item in datasetNoLabel:
    aux.append(item)

plt.figure(figsize=(25, 20))
plt.title('Hierarchical Clustering Dendrogram')
plt.xlabel('sample index')
plt.ylabel('distance')
dend = shc.dendrogram(shc.linkage(datasetNoLabel, method='ward'), truncate_mode='lastp', leaf_rotation=45., leaf_font_size=10., show_contracted=True )
plt.axhline(y=10, color='r', linestyle='--')

cluster = AgglomerativeClustering(n_clusters=4, affinity='euclidean', linkage='ward')
cluster.fit_predict(datasetNoLabel)
print(cluster.labels_)
var = []


for item in cluster.labels_:
    var.append(item)
        
    




plt.figure(figsize=(10, 7))
plt.scatter(dataset.index, cluster.labels_, c=dataset['label'], cmap='rainbow')
plt.xlabel('object')
plt.ylabel('cluster')
plt.show()

metrics.adjusted_rand_score(cluster.labels_, dataset['label'])
