#DFP project
#Cluster Neighborhood2
#Author: Yuwei Zhu

############################
#import module
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from sklearn import preprocessing

data = pd.read_csv('clean_all.csv')
del data['Unnamed: 0']

#drop columns that do not need
del data['Pop % of City']
del data['Street']
del data['Park']
del data['Playground']
del data['Maintenance_responsibility']
del data['Address']

data = data.dropna()
neighbor = data['Neighborhood'].tolist()
del data['Neighborhood']

#cluastering setting

def cluster_result():
    k = 8
    iteration = 100
    data_scaled = preprocessing.scale(data)
    model = KMeans(n_clusters = k, max_iter = iteration, n_init = 1, init='random')
    model.fit(data_scaled)

    label = model.labels_

    cluster = dict(zip(neighbor,label))
    return cluster


