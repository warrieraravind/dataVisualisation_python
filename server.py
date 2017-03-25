from flask import Flask
from flask import render_template
from pymongo import MongoClient
from sklearn.decomposition import PCA
from bson import json_util
from bson.json_util import dumps
from sklearn import preprocessing

from scipy.spatial.distance import cdist, pdist
from sklearn.cluster import KMeans

import json
import random
import matplotlib.pyplot as plt
import numpy as np
import math
import pandas as pd

app = Flask(__name__)
host = "localhost"
port = 27017
db_name = "data_db"
collection_name = "data_comm"

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


@app.route("/")
def index():
    return render_template ( "index.html" )


def do_random_sampling (arr):
    """
    This function does the random sampling
    :param arr:
    :return:
    """
    return random.sample (arr, 115)


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
        number_of_samples = len(data_points_for_i) * 0.20
        x = random.sample(data_points_for_i, math.ceil(number_of_samples))
        return_list = return_list + x

    return return_list


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

        print(P)
        print('***')

        pca = PCA(n_components=pc_components_len)
        pca_result = pca.fit_transform(arr)
        print(pca_result)

        squared_pca_result = [square_func(value) for index, value in enumerate(pca_result)]
        sum_squared_pca_result = [sum(value) for index, value in enumerate(squared_pca_result)]

        field_sum_squared_pca_result = dict()
        index = 0
        for field in fields:
            if field is not '_id':
                field_sum_squared_pca_result[field] = sum_squared_pca_result[index]
                index += 1

        return field_sum_squared_pca_result, pca_result


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
    connection = MongoClient(host, port)
    collection = connection[db_name][collection_name]

    return_arr = []
    items = collection.find(projection = fields)
    for item in items:
        return_arr.append ( item )

    # return_arr = json.dumps(return_arr, default=json_util.default)
    random_sample = do_random_sampling(return_arr)
    stratified_sample = do_stratified_sampling(return_arr)

    normalized_random_sample = normalize_data(random_sample)
    normalized_stratified_sample = normalize_data(stratified_sample)

    random_correlation_matrix = np.corrcoef(normalized_random_sample, rowvar=False)
    stratified_correlation_matrix = np.corrcoef(normalized_stratified_sample, rowvar=False)

    random_pca_sum_squared, random_pca_result = calculate_pca(random_correlation_matrix)
    stratified_pca_sum_squared, stratified_pca_result = calculate_pca(stratified_correlation_matrix)

    transformed_random_pc = np.dot(normalized_stratified_sample, stratified_pca_result)
    transformed_stratified_pc =  np.dot(normalized_stratified_sample, random_pca_result)

    twing = {
        "aravind": {
            "warrier": 1
        }
    }

    return json.dumps(twing, default=lambda o: o.__dict__)

if __name__ == "__main__":
    app.run(debug = True)