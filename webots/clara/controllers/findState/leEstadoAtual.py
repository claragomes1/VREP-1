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
import statistics


def create_df():
    saida_direita = pd.read_csv('saida_direita.csv')
    saida_esquerda = pd.read_csv('saida_esquerda.csv')
    saida_direita_esquerda = pd.read_csv('saida_direita_esquerda.csv')
    encruzilhada_esquerda = pd.read_csv('encruzilhada_esquerda.csv')
    encruzilhada_direita = pd.read_csv('encruzilhada_direita.csv')
    encruzilhada = pd.read_csv('encruzilhada.csv')
    corredor = pd.read_csv('corredor.csv')
    # teste = pd.read_csv('corredor_encruzilhada_corredor_esquerda.csv', index_col='object')
    # teste = pd.read_csv('corredor_edireita_corredor_sdireita.csv', index_col='object')
    ##teste = pd.read_csv('encruzilhadaEsquerda_corredor_ee_c_saidaEsquerda.csv', index_col='object')
    # teste = pd.read_csv('teste.csv', index_col='object')
    # testesd = pd.read_csv('testesd.csv', index_col='object')

    dataset = pd.concat(
        [saida_direita, saida_esquerda, saida_direita_esquerda, encruzilhada_esquerda, encruzilhada_direita,
         encruzilhada, corredor], axis=0, ignore_index=True)
    dataset.head()

    dataset['label'] = dataset['label'].replace('saida_direita', 0)
    dataset['label'] = dataset['label'].replace('saida_esquerda', 1)
    dataset['label'] = dataset['label'].replace('saida_direita_esquerda', 2)
    dataset['label'] = dataset['label'].replace('encruzilhada_esquerda', 3)
    dataset['label'] = dataset['label'].replace('encruzilhada_direita', 4)
    dataset['label'] = dataset['label'].replace('encruzilhada', 5)
    dataset['label'] = dataset['label'].replace('corredor', 6)

    datasetNoObject = dataset.drop(columns=['object'])
    datasetNoLabel = datasetNoObject.drop(columns=['label'])
    #print(datasetNoLabel)

    datasetNoLabel = pd.DataFrame(datasetNoLabel)
    datasetNoLabel = datasetNoLabel.astype(str)

    return datasetNoLabel;


def leEstado(dataset):
    # dataset2 = dataset
    # dataset2.append(rangeImageCompleteDf)
    # dataset2 = pd.DataFrame(datasetAux)
    # dataset2.head()

    # dataset2['label'] = dataset2['label'].replace('saida_direita',0)
    # dataset2['label'] = dataset2['label'].replace('saida_esquerda',1)
    # dataset2['label'] = dataset2['label'].replace('saida_direita_esquerda',2)
    # dataset2['label'] = dataset2['label'].replace('encruzilhada_esquerda',3)
    # dataset2['label'] = dataset2['label'].replace('encruzilhada_direita',4)
    # dataset2['label'] = dataset2['label'].replace('encruzilhada',5)
    # dataset2['label'] = dataset2['label'].replace('corredor',6)

    # atasetNoLabel2 = dataset2.drop(columns=['label'])
    # print(datasetNoLabel2)'''

    dataset = normalize(dataset)

    #plt.figure(figsize=(25, 20))
    # plt.title('Hierarchical Clustering Dendrogram')
    # plt.xlabel('sample index')
    # plt.ylabel('distance')
    #dend = shc.dendrogram(shc.linkage(datasetNoLabel2, method='ward'), truncate_mode='lastp', leaf_rotation=45., leaf_font_size=10., show_contracted=True )
    # plt.axhline(y=10, color='r', linestyle='--')

    cluster2 = AgglomerativeClustering(n_clusters=7, affinity='euclidean', linkage='ward')
    cluster2.fit_predict(dataset)
    #print(cluster2.labels_)

    tamanhoLista = len(cluster2.labels_)
    inicioTamanho = tamanhoLista - 51

    print(tamanhoLista)
    print(inicioTamanho)

    s1 = statistics.mode(cluster2.labels_[0:999])
    s2 = statistics.mode(cluster2.labels_[1000:1999])
    s3 = statistics.mode(cluster2.labels_[2000:2999])
    s4 = statistics.mode(cluster2.labels_[3000:3999])
    s5 = statistics.mode(cluster2.labels_[4000:4999])
    s6 = statistics.mode(cluster2.labels_[5000:5999])
    s7 = statistics.mode(cluster2.labels_[6000:6999])
    newS = statistics.mode(cluster2.labels_[inicioTamanho:tamanhoLista])

    if newS == s1:
        return 0;
    if newS == s2:
        return 1;
    if newS == s3:
        return 2;
    if newS == s4:
        return 3;
    if newS == s5:
        return 4;
    if newS == s6:
        return 5;
    if newS == s7:
        return 6;
    else:
        return 7;
''' if newS == s1:
     print("saida direita")  # return 0
 if newS == s2:
     print("saida_esquerda")
 if newS == s3:
     print("saida_direita_esquerda")
 if newS == s4:
     print("encruzilhada_esquerda")
 if newS == s5:
     print("encruzilhada_direita")
 if newS == s6:
     print("encruzilhada")
 if newS == s7:
     print("corredor")

'''


# plt.figure(figsize=(10, 7))
# plt.scatter(dataset.index, cluster.labels_, c=dataset['label'], cmap='rainbow')
# plt.title('teste_corredor_encruzilhada_corredor_sEsquerda')
# plt.xlabel('object')
# plt.ylabel('cluster')

# plt.savefig('teste_1.pdf')
# plt.show()

# metrics.adjusted_rand_score(cluster.labels_, dataset['label'])
