import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys, difflib
import seaborn as sn

number_of_clusters = 32

np.set_printoptions(threshold=sys.maxsize)  #print data visualisation without truncation

np.random.seed(5)

#reading entire data
df = pd.read_csv("C:\\Users\\Artur\\Desktop\\input\\complete.csv")
x = df.iloc[:, 1:181].values  #collecting only the features

#standardizing the features
from sklearn.preprocessing import StandardScaler
x = StandardScaler().fit_transform(x)	

#transforming features into components using PCA
from sklearn.decomposition import PCA
pca = PCA(n_components=2)
principalComponents = pca.fit_transform(x)
principalDf = pd.DataFrame(data = principalComponents
             , columns = ['principal component 1', 'principal component 2'])

#applying kmeans
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters = number_of_clusters)
y_kmeans = kmeans.fit_predict(x)	#label classification
y_kmeans_dataframe = pd.DataFrame(y_kmeans)	#transformation into dataframe

print('Components variance:', pca.explained_variance_ratio_)

#categorizing the ground truth label for evaluation
from sklearn import preprocessing
le = preprocessing.LabelEncoder()
le.fit(df.label)
groundTruthLabel = le.transform(df.label)
groundTruthLabel_dataframe = pd.DataFrame(groundTruthLabel)	#transforming into dataframe

#using rand index for clustering validation
from sklearn.metrics.cluster import adjusted_rand_score
print('Grouping validation value by rand index is', adjusted_rand_score(groundTruthLabel, y_kmeans)) #validation value between 0 and 1

#merging component columns with label column
finalDf = pd.concat([principalDf, y_kmeans_dataframe], axis = 1)	#insert groundTruthLabel_dataframe instead of y_kmeans_dataframe for ground truth classification

#creating color palette dictionary
from random import randint
targets = []
colors = []
for i in range(number_of_clusters):
	targets.append(i)
	colors.append('#%06X' % randint(0, 0xFFFFFF))

#plotting clustering representation by kmeans algorithm
fig = plt.figure(figsize = (8,8))
ax = fig.add_subplot(1,1,1) 
ax.set_xlabel('Principal Component 1', fontsize = 15)
ax.set_ylabel('Principal Component 2', fontsize = 15)
ax.set_title('2 component PCA - k-means classification', fontsize = 20)
for target, color in zip(targets,colors):
    indicesToKeep = finalDf.iloc[:, 2] == target
    ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1']
               , finalDf.loc[indicesToKeep, 'principal component 2']
               , c = color
               , s = 50)
#ax.legend(targets)
plt.show()

'''
#creating correlation matrix
pd.set_option('display.max_rows', 180)
x_dataframe = pd.DataFrame(x)
corrMatrix = x_dataframe.corr()
sn.heatmap(corrMatrix, annot=True)
#print(corrMatrix.iloc[100,:]) #check an especific row
#plt.show()
'''