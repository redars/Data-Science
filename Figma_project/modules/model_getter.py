# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 15:30:27 2023

@author: arsko
"""
import pickle
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def GetMaxClusterSize(label):
  res = 0
  for i in range(0,9):
    iterRes =0
    for el in label:
      if el == i:
        iterRes +=1
    if iterRes > res :
      res = iterRes
  return res

def Get_models(df):
    scaling=StandardScaler()
    scaling.fit(df)
    Scaled_data=scaling.transform(df)
    result_pcamodels = []
    result_kmeansmodels = []
    
    with open('data.pickle', 'rb') as f:
      check_data = pickle.load(f)
      
    for n_components in range(2,24):
      pca_model=PCA(n_components=n_components).fit(Scaled_data)
      data_transformed=pca_model.transform(Scaled_data)
      test_data=pca_model.transform(np.array([8 for i in range(24)]).reshape(1, -1))
      test_data_2=pca_model.transform(np.array([10,10,3,5,57,8,2,6,9,34,1,4,6,3,4,0,0,0,0,2,3,0,5,0]).reshape(1, -1))
      check_data_tranformed=pca_model.transform(check_data)
      scores = []
      kmeans_labels = []
      kmean_models = []
      for n_clusters in range(2,15):
        kmeans_model = KMeans(init="random", n_clusters=n_clusters, n_init=10, random_state=1)
        kmeans_model.fit(data_transformed)
        kmean_models.append(kmeans_model)
        pred = kmeans_model.predict(data_transformed)
        score = silhouette_score(data_transformed, pred)
        scores.append(score)
        kmeans_labels.append(kmeans_model.labels_)
      kmean_label = kmeans_labels[scores.index(max(scores))]
      size = GetMaxClusterSize(kmean_label)
      if size >= 45:
        result_kmeansmodels.append(kmean_models[scores.index(max(scores))])
        result_pcamodels.append(pca_model)
        for i in range (0,n_components):
          for j in range(0,n_components):
            if i == j:
              continue
            if (i == 1 and j == 3) or (i == 1 and j == 5) or (i == 5 and j == 1) or (i == 5 and j == 3):
              plt.figure(figsize=(10,10))
              plt.scatter(data_transformed[n_components:,i],data_transformed[n_components:,j],c=['blue'],cmap='plasma',label="Копии")
              plt.scatter(test_data[0][i],test_data[0][j],c=['darkred'], cmap='plasma',label="Похожий проект, но не копия")
              plt.scatter(test_data_2[0][i],test_data_2[0][j],c=['darkred'], cmap='plasma')
              plt.scatter(check_data_tranformed[0][i],check_data_tranformed[0][j],c=['orange'], cmap='plasma',label="Новая копия")
              plt.title(f"Зависимость двух компонент при рассмотрении модели PCA {n_components} параметров")
              plt.legend()
              plt.xlabel(f"Количество рассматриваемых параметров: {i+1}")
              plt.ylabel(f"Количество рассматриваемых параметров: {j+1}")
    
    pca_1 = result_pcamodels[0]
    pca_2 = result_pcamodels[1]
    kmeans_1 = result_kmeansmodels[0]
    kmeans_2 = result_kmeansmodels[1]
    with open('pca_model_1.pickle', 'wb') as f:
      pickle.dump(pca_1, f)
    with open('pca_model_2.pickle', 'wb') as f:
      pickle.dump(pca_2, f)
    with open('kmean_model_1.pickle', 'wb') as f:
      pickle.dump(kmeans_1, f)
    with open('kmean_model_2.pickle', 'wb') as f:
      pickle.dump(kmeans_2, f)