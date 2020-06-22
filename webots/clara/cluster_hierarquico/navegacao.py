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

saida_direita = pd.read_csv('saida_direita.csv', index_col='object')
saida_esquerda = pd.read_csv('saida_esquerda.csv', index_col = 'object')
saida_direita_esquerda = pd.read_csv('saida_direita_esquerda.csv', index_col='object')
encruzilhada_esquerda = pd.read_csv('encruzilhada_esquerda.csv', index_col='object')
encruzilhada_direita = pd.read_csv('encruzilhada_direita.csv', index_col='object')
encruzilhada = pd.read_csv('encruzilhada.csv', index_col='object')
corredor = pd.read_csv('corredor.csv', index_col='object')
#teste = pd.read_csv('corredor_encruzilhada_corredor_esquerda.csv', index_col='object')
#teste = pd.read_csv('corredor_edireita_corredor_sdireita.csv', index_col='object')
#teste = pd.read_csv('encruzilhadaEsquerda_corredor_ee_c_saidaEsquerda.csv', index_col='object')


dataset = pd.concat([saida_direita, saida_esquerda, saida_direita_esquerda, encruzilhada_esquerda, encruzilhada_direita, encruzilhada, corredor], axis=0, ignore_index=True)
dataset.head()

dataset['label'] = dataset['label'].replace('saida_direita',0)
dataset['label'] = dataset['label'].replace('saida_esquerda',1)
dataset['label'] = dataset['label'].replace('saida_direita_esquerda',2)
dataset['label'] = dataset['label'].replace('encruzilhada_esquerda',3)
dataset['label'] = dataset['label'].replace('encruzilhada_direita',4)
dataset['label'] = dataset['label'].replace('encruzilhada',5)
dataset['label'] = dataset['label'].replace('corredor',6)


datasetNoLabel = dataset.drop(columns=['label'])
print(datasetNoLabel)

datasetNoLabel = normalize(datasetNoLabel)


plt.figure(figsize=(25, 20))
plt.title('Hierarchical Clustering Dendrogram')
plt.xlabel('sample index')
plt.ylabel('distance')
dend = shc.dendrogram(shc.linkage(datasetNoLabel, method='ward'), truncate_mode='lastp', leaf_rotation=45., leaf_font_size=10., show_contracted=True )
plt.axhline(y=10, color='r', linestyle='--')

cluster = AgglomerativeClustering(n_clusters=7, affinity='euclidean', linkage='ward')
cluster.fit_predict(datasetNoLabel)
print(cluster.labels_)

tamanhosCluster = [];
indiceCluster = [];
indice = 0;
var = [];
for  valor in cluster.labels_:
    var.append(valor);
    if indice == 0:
        valorAnt = valor;
    if valorAnt != valor :
        for x in indiceCluster:
            if valorAnt == x:
                continue
            else:
                tamanhosCluster.append(indice - 1);
                indiceCluster.append(valorAnt);
        
        indice = 0;
    indice = indice + 1;
    valorAnt = valor;
    
dataset2 = pd.concat([saida_direita,saida_direita, saida_esquerda, saida_direita_esquerda, encruzilhada_esquerda, encruzilhada_direita, encruzilhada, corredor], axis=0, ignore_index=True)
dataset2.head()

dataset2['label'] = dataset2['label'].replace('saida_direita',0)
dataset2['label'] = dataset2['label'].replace('saida_esquerda',1)
dataset2['label'] = dataset2['label'].replace('saida_direita_esquerda',2)
dataset2['label'] = dataset2['label'].replace('encruzilhada_esquerda',3)
dataset2['label'] = dataset2['label'].replace('encruzilhada_direita',4)
dataset2['label'] = dataset2['label'].replace('encruzilhada',5)
dataset2['label'] = dataset2['label'].replace('corredor',6)


datasetNoLabel2 = dataset2.drop(columns=['label'])
print(datasetNoLabel2)

datasetNoLabel2 = normalize(datasetNoLabel2)


plt.figure(figsize=(25, 20))
plt.title('Hierarchical Clustering Dendrogram')
plt.xlabel('sample index')
plt.ylabel('distance')
dend = shc.dendrogram(shc.linkage(datasetNoLabel2, method='ward'), truncate_mode='lastp', leaf_rotation=45., leaf_font_size=10., show_contracted=True )
plt.axhline(y=10, color='r', linestyle='--')

cluster2 = AgglomerativeClustering(n_clusters=7, affinity='euclidean', linkage='ward')
cluster2.fit_predict(datasetNoLabel2)
print(cluster2.labels_)

NtamanhosCluster = [];
NindiceCluster = [];

indice = 0;
var2 = [];
for valor2 in cluster2.labels_:
    var2.append(valor2);
    if indice == 0:
        valorAnt2 = valor2;
    if valorAnt2 != valor2 :
        NtamanhosCluster.append(indice - 1);
        NindiceCluster.append(valorAnt2);
    valorAnt2 = valor2;
    indice = indice + 1;

#v = [];

#for pos in range(6):
#    v.append(NtamanhosCluster[pos] - tamanhosCluster[pos]);












plt.figure(figsize=(10, 7))
plt.scatter(dataset.index, cluster.labels_, c=dataset['label'], cmap='rainbow')
plt.title('teste_corredor_encruzilhada_corredor_sEsquerda')
plt.xlabel('object')
plt.ylabel('cluster')

#plt.savefig('teste_1.pdf')
plt.show()

metrics.adjusted_rand_score(cluster.labels_, dataset['label'])


