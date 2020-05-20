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

saida_direita = pd.read_csv('saida_direita.csv', index_col='object')
corredor = pd.read_csv('corredor.csv', index_col='object')
dataset = pd.concat([saida_direita, corredor], axis=0, ignore_index=True)
dataset.head()

dataset['label'] = dataset['label'].replace('saida_direita',0)
dataset['label'] = dataset['label'].replace('corredor',1)

datasetNoLabel = dataset.drop(columns=['label'])
print(datasetNoLabel)

from sklearn.preprocessing import normalize
datasetNoLabel = normalize(datasetNoLabel)

dend = shc.dendrogram(shc.linkage(datasetNoLabel, method='ward'))
plt.axhline(y=10, color='r', linestyle='--')

cluster = AgglomerativeClustering(n_clusters=2, affinity='euclidean', linkage='ward')
cluster.fit_predict(datasetNoLabel)
print(cluster.labels_)

plt.figure(figsize=(10, 7))
plt.scatter(dataset.index, cluster.labels_, c=dataset['label'], cmap='rainbow')
plt.xlabel('object')
plt.ylabel('cluster')
plt.savefig('teste_corredor_saida_direita.pdf')
plt.show()




