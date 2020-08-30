import math
from functools import wraps
from time import time
import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import OPTICS
from scipy.spatial import distance
from dtw import *
import plotly.express as px


def timer(function):
    @wraps(function)
    def _time_it(*args, **kwargs):
        start = int(round(time() * 1000))
        try:
            return function(*args, **kwargs)
        finally:
            end_ = int(round(time() * 1000)) - start
            name = function.__name__
            print(f"Total execution time of {name} was: {end_ if end_ > 0 else 0} ms")
    return _time_it


@timer
def get_db(csv):
    db_df = pd.read_csv(csv, index_col=0)
    xs = []
    ys = []
    ids = []
    id = -1
    distances = []
    for reading in db_df.values:
        id += 1
        for degree in range(len(reading)):
            xs.append(reading[degree] * math.cos(math.radians(degree - 90)))
            ys.append(reading[degree] * math.sin(math.radians(degree - 90)))
            ids.append(id)
            distances.append(reading[degree])
    db = pd.DataFrame(data={'x': xs, 'y': ys, 'distance': distances, 'id': ids})
    db.to_csv('DB.csv')


@timer
def dbscan_x_y():
    db_df = pd.read_csv('DB.csv', index_col=0)
    labels = []
    for i in range(int(len(db_df) / 360)):
        x_y_df = db_df.loc[db_df['id'] == i][['x', 'y']]
        dbscan = DBSCAN(eps=3, min_samples=3, metric='euclidean').fit(x_y_df)
        for label in dbscan.labels_:
            labels.append(label)
    db_df['dbscan_x_y_label'] = labels
    db_df.to_csv('DB.csv')


@timer
def animation():
    db_df = pd.read_csv('DB.csv', index_col=0)
    fig = px.scatter(db_df, x='x', y='y', color='dbscan_x_y_label', animation_frame='id', range_x=[-45, 45], range_y=[-45, 45])
    fig.update_yaxes(dtick=1)
    fig.update_xaxes(dtick=1)
    fig.update_layout(height=500, width=500, title_text="Animacao dos pontos no corredor")
    fig.show()


@timer
def optics():
    db_df = pd.read_csv('DB.csv', index_col=0).iloc[::10]
    optics = OPTICS().fit(db_df)
    reachability = optics.reachability_[optics.ordering_]
    fig = px.scatter(reachability)
    fig.show()


@timer
def dbscan():
    db_df = pd.read_csv('DB.csv', index_col=0)
    distance_complete = []
    for i in range(int(len(db_df) / 360)):
        distance_complete.append(db_df.loc[db_df['id'] == i]['distance'].values)
    distance_df = pd.DataFrame(distance_complete)
    dbscan = DBSCAN(eps=3).fit(distance_df)
    labels = []
    for label in dbscan.labels_:
        for each in range(1, 361):
            labels.append(label)
    fig = px.scatter(dbscan.labels_)
    fig.show()
    db_df['dbscan_label'] = labels
    db_df.to_csv('DB.csv')


class Neuron:
    def __init__(self, receivedPattern, alphaZero, clId, distance=distance.euclidean):
        self.centroid = receivedPattern
        self.alphaCluster = alphaZero  # alphaCluster == Minimum similarity degree
        self.averageRadius = -np.log(alphaZero)
        self.distance = distance
        # Add a cluster ID and update the total number of clusters
        self.clusterId = clId

    def activation(self, pattern):
        return np.exp(-self.distance(self.centroid, pattern))


    def adaptCluster(self, pattern, gamma, omega):
        # Before updating the centroid, get the previous vector to compute p
        previousCentroid = self.centroid.copy()
        # Adapting centroid
        self.centroid = self.centroid * (1 - gamma) + gamma * pattern
        # Before updating the radius, get the previous value to compute p
        previousAverageRadius = self.averageRadius
        # Adapting average radius
        self.averageRadius = (1-omega) * previousAverageRadius + omega * self.distance(pattern, previousCentroid)
        # Calculating value of p
        p = np.abs((self.averageRadius-previousAverageRadius) / np.maximum(self.averageRadius, previousAverageRadius))
        # Updating the activation value for the neuron
        self.alphaCluster = np.minimum((1 + p) * self.alphaCluster, np.exp(-self.averageRadius * (1 + p)))

    def getCentroid(self):
        return self.centroid

    def getClusterId(self):
        return self.clusterId

    def getAlpha(self):
        return self.alphaCluster

    def __str__(self):
        string = ""
        string += "Cluster ID: " + str(self.clusterId)
        string += "\nCentroid: " + str(self.centroid)
        string += "\nAlpha Cluster: " + str(self.alphaCluster)
        string += "\nAverageRadius: " + str(self.averageRadius)
        return string


class Sonde:
    clustersIds = 1

    def __init__(self, alphaZero=0.5, gamma=0.1, omega=0.1, distance=distance.euclidean):
        self.alphaZero = alphaZero
        self.gamma = gamma
        self.omega = omega
        self.distance = distance
        self.listNeurons = []
        Sonde.clustersIds = 1

    def execute(self, pattern):
        bmu = -np.inf
        bestNeuron = None
        for neuron in self.listNeurons:
            # Calculating the distance and the activation function
            # Choosing the best neuron
            activationValue = neuron.activation(pattern)
            if activationValue > neuron.getAlpha() and activationValue > bmu:
                bestNeuron = neuron
        # If we found the best neuron
        if bestNeuron != None:
            bestNeuron.adaptCluster(pattern, self.gamma, self.omega)
        else:
            bestNeuron = Neuron(pattern, self.alphaZero, Sonde.clustersIds, self.distance)
            self.listNeurons.append(bestNeuron)
            Sonde.clustersIds += 1
        return bestNeuron.getClusterId()

    def getListOfNeurons(self):
        return self.listNeurons


def dtw_metric(x, y):
    return dtw(x, y, keep_internals=True, step_pattern=rabinerJuangStepPattern(6, "c")).distance


@timer
def sonde_stage_3():
    db_df = pd.read_csv('DB.csv', index_col=0)
    sonde = Sonde(alphaZero=0.0001, gamma=0.00000000000000001, omega=0.00000000000000001, distance=dtw_metric)
    listClusters = []
    for i in range(len(db_df)):
      instance = db_df.iloc[i]
      clusterResult = sonde.execute(instance)
      listClusters.append(clusterResult)
    fig = px.scatter(listClusters, y=listClusters)
    fig.show()


@timer
def teste(csv):
    leitura_df = pd.read_csv(csv + '.csv', index_col=0)
    leitura_df = pd.DataFrame(MinMaxScaler(feature_range=(0, 1)).fit_transform(leitura_df))
    lista = []
    for i in range(len(leitura_df)):
        lista.append(dtw(leitura_df.iloc[30], leitura_df.iloc[i], keep_internals=True, step_pattern=rabinerJuangStepPattern(6, "c")).distance)
    fig = px.scatter(lista, y=lista)
    fig.show()
    # dtw(leitura_df.iloc[30], leitura_df.iloc[2300], keep_internals=True, step_pattern=rabinerJuangStepPattern(6, "c")).plot(type="twoway", offset=-2)
    # print(dtw(labels_df.iloc[311], labels_df.iloc[580], keep_internals=True, step_pattern=rabinerJuangStepPattern(6, "c")).distance)


get_db('leitura2.csv')
dbscan_x_y()
animation() #450000ms
# optics() #5->2659690  #10->10 min
# dbscan()
