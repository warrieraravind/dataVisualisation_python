from flask import Flask
from flask import render_template
from pymongo import MongoClient
from sklearn.decomposition import PCA
from bson import json_util
from sklearn import preprocessing
from scipy.spatial.distance import cdist, pdist
from sklearn.cluster import KMeans
from sklearn import metrics as SK_Metrics
from sklearn.manifold import MDS

import json
import random
import numpy as np
import math


app = Flask(__name__)

host = "localhost"
port = 27017
db_name = "data_db"
collection_name = "data_comm"
random_sample = 0
stratified_sample = 0

normalized_random_sample = 0
normalized_stratified_sample = 0

random_correlation_matrix = 0
stratified_correlation_matrix = 0

random_pca_sum_squared = 0
random_pca_result = 0
stratified_pca_sum_squared = 0
stratified_pca_result = 0

transformed_random_pc = 0
transformed_stratified_pc = 0

eigen_value_random = 0
eigen_value_stratified = 0

whole_data = 0
wcss = 0

mds_random_euclidean = 0
mds_stratified_euclidean = 0
mds_random_correlation = 0
mds_stratified_correlation = 0

fields = {
    "_id" :  False,
	"radius_mean" : True,
	"texture_mean" : True,
	"perimeter_mean" : True,
	"area_mean" : True,
	"smoothness_mean" : True,
	"compactness_mean" : True,
	"concavity_mean" : True,
	"concave points_mean" : True,
	"symmetry_mean" : True,
    "fractal_dimension_mean": True
}

field_index = {
    "radius_mean" : 0,
	"texture_mean" : 1,
	"perimeter_mean" : 2,
	"area_mean" : 3,
	"smoothness_mean" : 4,
	"compactness_mean" : 5,
	"concavity_mean" : 6,
	"concave points_mean" : 7,
	"symmetry_mean" : 8,
    "fractal_dimension_mean": 9
}

@app.route("/")
def index():
    return render_template ( "dashboard.html" )



@app.route("/scatter_tab")
def route_scatter():
    twing = {
        "random": {
            "transformed_random_pc": transformed_random_pc.tolist()
        },
        "stratified": {
            "transformed_stratified_pc": transformed_stratified_pc.tolist()
        }
    }

    return json.dumps(twing, default=json_util.default)


@app.route("/scree_tab")
def route_scree():
    twing = {
        "random": {
            "random_pca_sum_squared": random_pca_sum_squared
        },
        "stratified": {
            "stratified_pca_sum_squared": stratified_pca_sum_squared
        }
    }

    return json.dumps(twing, default=json_util.default)

@app.route("/intrinsic_tab")
def route_intrinsic():
    twing = {
        "random": {
            "eigen_value_random": eigen_value_random.tolist()
        },
        "stratified": {
            "eigen_value_stratified": eigen_value_stratified.tolist()
        }
    }

    return json.dumps(twing, default=json_util.default)

@app.route("/elbow_tab")
def route_elbow():
    global wcss

    twing = {
        "elbow": wcss
    }

    return json.dumps(twing, default=json_util.default)

@app.route('/mds_correlation_tab')
def route_mds_correlation():
    global mds_random_correlation
    global mds_stratified_correlation

    twing = {
        "random": {
            "mds_random_correlation": mds_random_correlation.tolist()
        },
        "stratified": {
            "mds_stratified_correlation" : mds_stratified_correlation.tolist()
        }
    }

    return json.dumps(twing, default=json_util.default)

@app.route('/mds_euclidean_tab')
def route_mds_euclidean():
    global mds_random_euclidean
    global mds_stratified_euclidean

    twing = {
        "random": {
            "mds_random_euclidean": mds_random_euclidean.tolist()
        },
        "stratified": {
            "mds_stratified_euclidean": mds_stratified_euclidean.tolist()
        }
    }

    return json.dumps(twing, default=json_util.default)

@app.route('/matrix_random_tab')
def route_matrix_random():
    global normalized_random_sample

    twing = {
        "normalized_random_sample": normalized_random_sample.tolist(),
        "indices": [field_index[random_pca_sum_squared[0][0]], field_index[random_pca_sum_squared[1][0]],
                    field_index[random_pca_sum_squared[2][0]]],
        "labels": [random_pca_sum_squared[0][0], random_pca_sum_squared[1][0], random_pca_sum_squared[2][0]]
    }

    return json.dumps(twing, default=json_util.default)

@app.route('/matrix_stratified_tab')
def route_matrix_stratified():
    global normalized_stratified_sample
    twing = {
        "normalized_stratified_sample": normalized_stratified_sample.tolist(),
        "indices": [field_index[stratified_pca_sum_squared[0][0]], field_index[stratified_pca_sum_squared[1][0]],
                    field_index[stratified_pca_sum_squared[2][0]]],
        "labels": [stratified_pca_sum_squared[0][0], stratified_pca_sum_squared[1][0], stratified_pca_sum_squared[2][0]]
    }

    return json.dumps(twing, default=json_util.default)

def do_kmeans_clustering():
    new_arr = []
    global whole_data
    global fields
    global wcss
    n = 25
    for item in whole_data:
        x = []
        for field in fields:
            if field is not '_id':
                x.append(item[field])
        new_arr.append(x)

    kMeansVar = [KMeans(n_clusters=k).fit(new_arr) for k in range(1, n)]
    centroids = [X.cluster_centers_ for X in kMeansVar]
    k_euclid = [cdist(new_arr, cent) for cent in centroids]
    dist = [np.min(ke, axis=1) for ke in k_euclid]
    wcss = [sum(d ** 2) for d in dist]

def do_random_sampling (arr):
    """
    This function does the random sampling
    :param arr:
    :return:
    """
    return random.sample (arr, 286)


def do_stratified_sampling (arr):
    """
    This function does the stratified sampling
    :param arr:
    :return:
    """
    new_arr = []
    for item in arr:
        x = []
        for i in item:
            x.append(item[i])
        new_arr.append(x)

    kMeansVar = KMeans(n_clusters=3).fit(new_arr)

    label_points = {
        "0": list(),
        "1": list(),
        "2": list()
    }

    for i in range(len(new_arr)):
        label_points[str(kMeansVar.labels_[i])].append(arr[i])

    return_list = list()

    for i in label_points:
        data_points_for_i = label_points[i]
        number_of_samples = len(data_points_for_i) * 0.50
        x = random.sample(data_points_for_i, math.ceil(number_of_samples))
        return_list = return_list + x

    return return_list

def do_mds():
    global mds_random_euclidean
    global mds_stratified_euclidean
    global mds_random_correlation
    global mds_stratified_correlation
    global normalized_stratified_sample
    global normalized_random_sample


    mds_random_euclidean = calculate_mds(normalized_random_sample, 'euclidean')
    mds_stratified_euclidean = calculate_mds(normalized_stratified_sample, 'euclidean')

    mds_random_correlation = calculate_mds(normalized_random_sample, 'correlation')
    mds_stratified_correlation = calculate_mds(normalized_stratified_sample, 'correlation')

def calculate_mds(data, type):
    distance_matrix = SK_Metrics.pairwise_distances(data, metric=type)
    mds = MDS(n_components=2, dissimilarity='precomputed')
    return mds.fit_transform(distance_matrix)

def convert_mds_to_object(mds_data):
    str_arr = str(mds_data).split("\n")[1:]
    return_arr = []
    for string in str_arr:
        return_arr.append(string.split(' ')[3:])

    return return_arr

def calculate_pca(arr, num_of_pc = None):
    """
    This method does the PCA and returns the PC's that have
    eigen values more than 1.
    :param arr:
    :return:
    """
    if num_of_pc is None:

        P, D, Q = np.linalg.svd(arr, full_matrices=False)
        pc_components_len = len([index for index, value in enumerate(D) if value > 1])

        pca = PCA(n_components=pc_components_len)
        pca_result = pca.fit_transform(arr)

        squared_pca_result = [square_func(value) for index, value in enumerate(pca_result)]
        sum_squared_pca_result = [sum(value) for index, value in enumerate(squared_pca_result)]

        field_rms_pca_result = dict()
        index = 0

        for field in fields:
            if field is not '_id':
                field_rms_pca_result[field] = (sum_squared_pca_result[index]/pc_components_len) ** 0.5
                index += 1

        field_rms_pca_result = sorted(field_rms_pca_result.items(), key=lambda x: x[1] * -1)

        return field_rms_pca_result, pca_result, D


def square_func(x):
    return_arr = []
    for i in x:
        return_arr.append(i*i);
    return return_arr


def normalize_data(data):
    data_arr = []

    for datum in data:
        arr = []
        for field in fields:
            if field is not '_id':
                arr.append(datum[field])
        data_arr.append(arr)

    return preprocessing.scale(np.array(data_arr))

@app.route("/setup")
def setup():
    """
    This function does the setting up. It includes the following:
        1. Random Sampling
        2. Stratified Sampling
    :return:

    """
    global random_sample
    global stratified_sample
    global normalized_random_sample
    global normalized_stratified_sample

    global random_correlation_matrix
    global stratified_correlation_matrix

    global random_pca_sum_squared
    global random_pca_result
    global stratified_pca_sum_squared
    global stratified_pca_result

    global transformed_random_pc
    global transformed_stratified_pc

    global eigen_value_random
    global eigen_value_stratified

    global whole_data

    connection = MongoClient(host, port)
    collection = connection[db_name][collection_name]

    return_arr = []
    items = collection.find(projection = fields)
    for item in items:
        return_arr.append ( item )

    # return_arr = json.dumps(return_arr, default=json_util.default)
    whole_data = return_arr
    random_sample = do_random_sampling(return_arr)
    stratified_sample = do_stratified_sampling(return_arr)

    do_kmeans_clustering()

    normalized_random_sample = normalize_data(random_sample)
    normalized_stratified_sample = normalize_data(stratified_sample)

    random_correlation_matrix = np.corrcoef(normalized_random_sample, rowvar=False)
    stratified_correlation_matrix = np.corrcoef(normalized_stratified_sample, rowvar=False)

    random_pca_sum_squared, random_pca_result, eigen_value_random = calculate_pca(random_correlation_matrix)
    stratified_pca_sum_squared, stratified_pca_result, eigen_value_stratified = calculate_pca(stratified_correlation_matrix)

    transformed_stratified_pc = np.dot(normalized_stratified_sample, stratified_pca_result)
    transformed_random_pc = np.dot(normalized_random_sample, random_pca_result)

    do_mds()

    twing = {
        "random": {
            "transformed_random_pc": transformed_random_pc.tolist()
        },
        "stratified" : {
            "transformed_stratified_pc": transformed_stratified_pc.tolist()
        }
    }

    return json.dumps(twing, default=json_util.default)

if __name__ == "__main__":
    app.run(debug = True)