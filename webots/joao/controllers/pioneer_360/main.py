import math
from functools import wraps
from time import time
import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from scipy.spatial import distance
from dtw import *
import plotly.express as px
import matplotlib.pyplot as plt
from matplotlib import animation
from sklearn.decomposition import PCA



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
def get_data():
    return pd.read_csv('corredor_maior/corredor.csv', index_col=0)


@timer
def DBSCAN_stage_1():
    corredor_df = get_data()
    x_complete = []
    y_complete = []
    id_complete = []
    id = -1
    labels_complete = []
    for line in corredor_df.values:
        id += 1
        x = []
        y = []
        for i in range(len(line)):
            x.append(line[i] * math.cos(math.radians(i - 90)))
            y.append(line[i] * math.sin(math.radians(i - 90)))
        x_y_df = pd.DataFrame(data={'x': x, 'y': y})
        dbscan = DBSCAN(eps=0.35, metric='euclidean').fit(x_y_df)
        labels_temp = [-1] * len(dbscan.labels_)
        label_counter = 0
        visited = 0
        while visited < len(dbscan.labels_):
            cluster = dbscan.labels_[np.where(dbscan.labels_ != -2)[0][0]]
            index_list = np.where(dbscan.labels_ == cluster)[0]
            for index in index_list:
                if cluster != -1:
                    labels_temp[index] = label_counter
                dbscan.labels_[index] = -2
                visited += 1
            if cluster != -1:
                label_counter += 1
        for each in x:
            x_complete.append(each)
        for each in y:
            y_complete.append(each)
        for each in [id] * len(line):
            id_complete.append(each)
        for each in labels_temp:
            labels_complete.append(each)
    distance_complete = []
    for reading in range(len(corredor_df)):
        for degree in corredor_df.values[reading]:
            distance_complete.append(degree)
    topography_df = pd.DataFrame(data={'x': x_complete, 'y': y_complete, 'distance': distance_complete, 'id': id_complete, 'label': labels_complete})
    topography_df.to_csv('topography_df.csv')


@timer
def animation_stage_1():
    topography_df = pd.read_csv('topography_df.csv', index_col=0)
    fig = px.scatter(topography_df, x='x', y='y', color='label', animation_frame='id', range_x=[-5, 5], range_y=[-5, 5])
    fig.update_yaxes(dtick=0.5)
    fig.update_xaxes(dtick=0.5)
    fig.update_layout(height=500, width=500, title_text="Animacao dos pontos no corredor")
    fig.show()


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
        self.centroid = self.centroid *(1-gamma) + gamma * pattern
        # Before updating the radius, get the previous value to compute p
        previousAverageRadius = self.averageRadius
        # Adapting average radius
        self.averageRadius = (1-omega)* previousAverageRadius + omega*self.distance(pattern,previousCentroid)
        # Calculating value of p
        p = np.abs((self.averageRadius-previousAverageRadius)/ np.maximum(self.averageRadius, previousAverageRadius))
        # Updating the activation value for the neuron
        self.alphaCluster = np.minimum((1+p)*self.alphaCluster, np.exp(-self.averageRadius*(1+p)))


    def getCentroid(self):
        return self.centroid


    def getClusterId(self):
        return self.clusterId


    def getAlpha(self):
        return self.alphaCluster


    def __str__(self):
        string = ""
        string += "Cluster ID: " + str(self.clusterId)
        #string += "\nCentroid: " + str(self.centroid)
        string += "\nAlpha Cluster: " + str(self.alphaCluster)
        string += "\nAverageRadius: " + str(self.averageRadius)
        return string

class Sonde:
    clustersIds=1
    def __init__(self, alphaZero=0.5, gamma=0.1, omega=0.1, distance=distance.euclidean):
        self.alphaZero = alphaZero
        self.gamma = gamma
        self.omega = omega
        self.distance=distance
        self.listNeurons = []
        Sonde.clustersIds=1


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
            bestNeuron= Neuron(pattern, self.alphaZero, Sonde.clustersIds, self.distance)
            self.listNeurons.append(bestNeuron)
            Sonde.clustersIds += 1
        return bestNeuron.getClusterId()


    def getListOfNeurons(self):
        return self.listNeurons


def dtw_metric(x, y):
    return dtw(x, y, keep_internals=True, step_pattern="symmetric1").distance


@timer
def SONDE_stage_2():
    topography_df = pd.read_csv('topography_df.csv', index_col=0)
    labels_matrix = []
    for i in range(int(len(topography_df) / 360)):
        labels_matrix.append(list(topography_df['label'][i * 360:(i + 1) * 360]))
    labels_df = pd.DataFrame(get_data())
    # Running SONDE without annimation
    # Initialize sonde neural network
    sonde2 = Sonde(alphaZero=0.1, gamma=0.1, omega=0.1, distance=dtw_metric)
    listClusters = []
    for i in range(len(labels_df)):
      instance = labels_df.iloc[i]
      clusterResult = sonde2.execute(instance)
      listClusters.append(clusterResult)
    fig = px.scatter(listClusters, y=listClusters)
    fig.show()

# DBSCAN_stage_1()
# animation_stage_1()
SONDE_stage_2()
