# -*- coding: utf-8 -*-
"""Assigment3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13pUIISPD2zHdS5vaVuw81aAUsE4k3H1o
"""

#imports
!pip install --upgrade scikit-learn
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
from keras.datasets import fashion_mnist
from matplotlib import pyplot as plt
from sklearn import metrics
from sklearn import cluster
from sklearn.decomposition import PCA
from sklearn.cluster import BisectingKMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import Birch

#define a performance evaluation function
def performance_score(input_values, cluster_indexes):
  # sklearn.metrics.rand_score(labels_true, labels_pred)
    try:
        silh_score = metrics.silhouette_score(input_values, cluster_indexes)
        print(' .. Silhouette Coefficient score is {:.2f}'.format(silh_score))
        #print( ' ... -1: incorrect, 0: overlapping, +1: highly dense clusts.')
    except:
        print(' .. Warning: could not calculate Silhouette Coefficient score.')
        silh_score = -999

    try:
        ch_score =\
         metrics.calinski_harabasz_score(input_values, cluster_indexes)
        print(' .. Calinski-Harabasz Index score is {:.2f}'.format(ch_score))
        #print(' ... Higher the value better the clusters.')
    except:
        print(' .. Warning: could not calculate Calinski-Harabasz Index score.')
        ch_score = -999

    try:
        db_score = metrics.davies_bouldin_score(input_values, cluster_indexes)
        print(' .. Davies-Bouldin Index score is {:.2f}'.format(db_score))
        #print(' ... 0: Lowest possible value, good partitioning.')
    except:
        print(' .. Warning: could not calculate Davies-Bouldin Index score.')
        db_score = -999

    try:
        
        n_samples = []
        for i in range(len(input_values)):
          n_samples.append(input_values[i][0])

        rand_score = metrics.rand_score(n_samples, cluster_indexes)
        print(' .. Rand Index score is {:.2f}'.format(rand_score))
        #print(' ... 0: Lowest possible value, good partitioning.')
    except:
        print(' .. Warning: could not calculate Rand Index score.')
        rand_score = -999
    

    return silh_score, ch_score, db_score, rand_score

#Next let's plot the first 100 of these to recall exactly what we're looking at:
def plot_fashion(data):
    fig, ax = plt.subplots(10, 10, figsize=(28, 28),
                           subplot_kw=dict(xticks=[], yticks=[]))
    fig.subplots_adjust(hspace=0.05, wspace=0.05)
    for i, axi in enumerate(ax.flat):
        im = axi.imshow(data[i], cmap='binary')
        im.set_clim(0, 16)

def my_plot_func(clusterLabels):
  fig = plt.figure(figsize=(20,20))
  for clusterIdx in range(10):
      # cluster = cm[r].argmax()
      for c, val in enumerate(X_test[clusterLabels == clusterIdx][0:10]):
          fig.add_subplot(10, 10, 10*clusterIdx+c+1)
          plt.imshow(val.reshape((28,28)))
          plt.gray()
          plt.xticks([])
          plt.yticks([])
          plt.xlabel('cluster: '+str(cluster))
          plt.ylabel('cluster index: '+str(clusterIdx))

#2
#train-test split
(X_train, Y_train), (X_test, Y_test) = fashion_mnist.load_data()

#validation split
X_train, X_validate, y_train, y_validate = train_test_split(X_train, Y_train, test_size=0.1, random_state=1)

#3
#now run a PCA, preserving 98% of variance
pca = PCA(0.98, whiten=True)
#remember: PCA takes as input a 2d matrix: n paradigms x m features
pca_created_data = pca.fit_transform(
          X_train.reshape(X_train.shape[0], (X_train.shape[1]*X_train.shape[2]))
                        )
pca_created_data.shape

#4
#apply the existing PCA transform to new data; i.e. on Validation SET

pca_projected_data_validate_set = pca.transform(
    X_validate.reshape(X_validate.shape[0], (X_validate.shape[1]*X_validate.shape[2]))
                        )
#try the inverse transform, just to demonstate the outcomes
inversed_pca_data = pca.inverse_transform(pca_projected_data_validate_set)

print('validate set data projected sucessfully.')
print(pca_projected_data_validate_set.shape)

#5
# np.random.shuffle(X_validate)
plot_fashion(X_validate)


plot_fashion(inversed_pca_data.reshape(inversed_pca_data.shape[0],\
                                      X_validate.shape[1],
                                      X_validate.shape[2]))

#6
#apply the existing PCA transform to new data; i.e. on Test SET
pca_projected_data_test_set = pca.transform(
    X_test.reshape(X_test.shape[0], (X_test.shape[1]*X_test.shape[2])))

print('test set data projected sucessfully.')
print(pca_projected_data_test_set.shape)

#7 8 9
nsamples, nx, ny = X_test.shape

d2_X_test_dataset = X_test.reshape((nsamples,nx*ny))

# raw
print("RAW BisectingKMeans")
print("----------------------------------------")
for numOfClust in range (3,12):
  print('Currently testing', str(numOfClust),\
        'number of clusters')
  kmeans_raw = BisectingKMeans(n_clusters=numOfClust, random_state=0).fit(d2_X_test_dataset)
  clusterLabels_kmeans_raw = kmeans_raw.labels_
  silh_score, ch_score, db_score, rand_score = \
  performance_score(Y_test.reshape(-1, 1), clusterLabels_kmeans_raw)


kmeans_raw = BisectingKMeans(n_clusters=10, random_state=0).fit(d2_X_test_dataset)
clusterLabels_kmeans_raw = kmeans_raw.labels_

my_plot_func(clusterLabels_kmeans_raw)


print("PCA BisectingKMeans")
print("----------------------------------------")
#PCA transormed data
for numOfClust in range (3,12):
  print('Currently testing', str(numOfClust),\
        'number of clusters')
  kmeans_tr = BisectingKMeans(n_clusters=numOfClust, random_state=0).fit(pca_projected_data_test_set)
  clusterLabels_kmeans_tr = kmeans_tr.labels_
  silh_score, ch_score, db_score, rand_score = \
  performance_score(Y_test.reshape(-1, 1), clusterLabels_kmeans_tr)

kmeans_tr = BisectingKMeans(n_clusters=10, random_state=0).fit(pca_projected_data_test_set)
clusterLabels_kmeans_tr = kmeans_tr.labels_

my_plot_func(clusterLabels_kmeans_tr)

#7 8 9
# Agglomerative Clustering

# raw
print("RAW AgglomerativeClustering")
print("----------------------------------------")
for numOfClust in range (3,12):
  print('Currently testing', str(numOfClust),\
        'number of clusters')
  clusteringAG_raw = AgglomerativeClustering(n_clusters = numOfClust).fit(d2_X_test_dataset)
  clusteringAG_raw_labels = clusteringAG_raw.labels_
  silh_score, ch_score, db_score, rand_score = \
  performance_score(Y_test.reshape(-1, 1), clusteringAG_raw_labels)



clusteringAG_raw = AgglomerativeClustering(n_clusters = 10).fit(d2_X_test_dataset)
clusteringAG_raw_labels = clusteringAG_raw.labels_
my_plot_func(clusteringAG_raw_labels)


# pca tranformed
print("PCA AgglomerativeClustering")
print("----------------------------------------")
for numOfClust in range (3,12):
  print('Currently testing', str(numOfClust),\
        'number of clusters')
  clusteringAG_tr = AgglomerativeClustering(n_clusters = numOfClust).fit(pca_projected_data_test_set)
  clusteringAG_tr_labels = clusteringAG_tr.labels_
  silh_score, ch_score, db_score, rand_score = \
  performance_score(Y_test.reshape(-1, 1), clusteringAG_tr_labels)



clusteringAG_tr = AgglomerativeClustering(n_clusters = 10).fit(pca_projected_data_test_set)
clusteringAG_tr_labels = clusteringAG_tr.labels_
my_plot_func(clusteringAG_tr_labels)

# 7 8 9
# Birch

# raw
print("RAW Birch")
print("----------------------------------------")


for numOfClust in range (3,12):
  print('Currently testing', str(numOfClust),\
        'number of clusters')
  clusteringB_raw = Birch(n_clusters=numOfClust)
  clusteringB_raw.fit(d2_X_test_dataset)
  clusteringB_raw_labels = clusteringB_raw.labels_ 
  silh_score, ch_score, db_score, rand_score = \
  performance_score(Y_test.reshape(-1, 1), clusteringB_raw_labels)



clusteringB_raw = Birch(n_clusters=10)
clusteringB_raw.fit(d2_X_test_dataset)
clusteringB_raw_labels = clusteringB_raw.labels_ 

my_plot_func(clusteringB_raw_labels)


# pca tranformed
print("PCA Birch")
print("----------------------------------------")
for numOfClust in range (3,12):
  print('Currently testing', str(numOfClust),\
        'number of clusters')
  
  clusteringB_tr = Birch(n_clusters=numOfClust)
  clusteringB_tr.fit(pca_projected_data_test_set)
  clusteringB_tr_labels = clusteringB_tr.labels_ 
  silh_score, ch_score, db_score, rand_score = \
  performance_score(Y_test.reshape(-1, 1), clusteringB_tr_labels)



clusteringB_tr = Birch(n_clusters=10)
clusteringB_tr.fit(pca_projected_data_test_set)
clusteringB_tr_labels = clusteringB_tr.labels_ 
my_plot_func(clusteringB_tr_labels)

# Running the models again with 3 cluster to get the best results

# BisectingKMeans

kmeans_raw = BisectingKMeans(n_clusters=3, random_state=0).fit(d2_X_test_dataset)
clusterLabels_kmeans_raw = kmeans_raw.labels_
print("RAW BisectingKMeans")
performance_score(Y_test.reshape(-1, 1), clusterLabels_kmeans_raw)
my_plot_func(clusterLabels_kmeans_raw)

kmeans_tr = BisectingKMeans(n_clusters=3, random_state=0).fit(pca_projected_data_test_set)
clusterLabels_kmeans_tr = kmeans_tr.labels_

print("PCA BisectingKMeans")
performance_score(Y_test.reshape(-1, 1), clusterLabels_kmeans_tr)

my_plot_func(clusterLabels_kmeans_tr)

# Agglomerative Clustering

clusteringAG_raw = AgglomerativeClustering(n_clusters = 3).fit(d2_X_test_dataset)
clusteringAG_raw_labels = clusteringAG_raw.labels_
print("RAW Agglomerative Clustering")
performance_score(Y_test.reshape(-1, 1), clusteringAG_raw_labels)
my_plot_func(clusteringAG_raw_labels)


clusteringAG_tr = AgglomerativeClustering(n_clusters = 3).fit(pca_projected_data_test_set)
clusteringAG_tr_labels = clusteringAG_tr.labels_
print("PCA Agglomerative Clustering")
performance_score(Y_test.reshape(-1, 1), clusteringAG_tr_labels)
my_plot_func(clusteringAG_tr_labels)

# Birch

clusteringB_raw = Birch(n_clusters=3)
clusteringB_raw.fit(d2_X_test_dataset)
clusteringB_raw_labels = clusteringB_raw.labels_ 
print("RAW Birch")
performance_score(Y_test.reshape(-1, 1), clusteringB_raw_labels)
my_plot_func(clusteringB_raw_labels)


clusteringB_tr = Birch(n_clusters=3)
clusteringB_tr.fit(pca_projected_data_test_set)
clusteringB_tr_labels = clusteringB_tr.labels_ 
print("PCA Birch")
performance_score(Y_test.reshape(-1, 1), clusteringB_tr_labels)

my_plot_func(clusteringB_tr_labels)