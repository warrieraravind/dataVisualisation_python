from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist, pdist
from pymongo import MongoClient
from sklearn.decomposition import PCA

import numpy as np
from scipy import linalg as LA
import matplotlib.pyplot as plt
import matplotlib

def do_pca_analysis(arr):
    fields = [
        "radius_mean",
        "texture_mean",
        "perimeter_mean",
        "area_mean",
        "smoothness_mean",
        "compactness_mean",
        "concavity_mean",
        "concave points_mean",
        "symmetry_mean"
    ]
    new_arr = []

    for item in arr:
        x = []
        for i in range(len(fields)):
            x.append(item[fields[i]])
        new_arr.append(x)

    correlation_matrix = np.corrcoef(new_arr, rowvar=False)

    U, eig_vals, V = np.linalg.svd(correlation_matrix)

    print(U)
    # print (V)


    print('***')
    # print(eig_vals)
    # plt.plot(eig_vals)
    # plt.show()

    pca = PCA(n_components=3)
    pca.fit(correlation_matrix)
    X = pca.transform(correlation_matrix)
    print(X)

if __name__ == '__main__':
    host = "localhost"
    port = 27017
    db_name = "data_db"
    collection_name = "data_comm"
    connection = MongoClient(host, port)
    collection = connection[db_name][collection_name]
    return_arr = []

    fields = {
        "_id": False,
        # "diagnosis" : True,
        "radius_mean": True,
        "texture_mean": True,
        "perimeter_mean": True,
        "area_mean": True,
        "smoothness_mean": True,
        "compactness_mean": True,
        "concavity_mean": True,
        "concave points_mean": True,
        "symmetry_mean": True
    }

    items = collection.find(projection=fields)
    for item in items:
        return_arr.append(item)

    do_pca_analysis(return_arr)