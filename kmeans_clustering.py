from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist, pdist
from pymongo import MongoClient

import numpy as np
import matplotlib.pyplot as plt

def do_stratified_sampling (arr):
    """
    This function does the stratified sampling
    :param arr:
    :return:
    """
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
    n = 10
    new_arr = []
    for item in arr:
        x = []
        for i in range(len(fields)):
            x.append(item[fields[i]])
        new_arr.append(x)

    kMeansVar = [KMeans(n_clusters=k).fit(new_arr) for k in range(1, n)]
    centroids = [X.cluster_centers_ for X in kMeansVar]
    k_euclid = [cdist(new_arr, cent) for cent in centroids]
    dist = [np.min(ke, axis=1) for ke in k_euclid]
    wcss = [sum(d ** 2) for d in dist]
    print(wcss)
    plt.plot(wcss)
    plt.show()

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

    do_stratified_sampling(return_arr)

