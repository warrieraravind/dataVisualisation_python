from flask import Flask
from flask import render_template
from pymongo import MongoClient
from bson import json_util
from bson.json_util import dumps

from scipy.spatial.distance import cdist, pdist
from sklearn.cluster import KMeans

import json
import random
import matplotlib.pyplot as plt
import numpy as np
import math

app = Flask(__name__)
host = "localhost"
port = 27017
db_name = "data_db"
collection_name = "data_comm"

fields = {
    "_id" :  False,
    # "diagnosis" : True,
	"radius_mean" : True,
	"texture_mean" : True,
	"perimeter_mean" : True,
	"area_mean" : True,
	"smoothness_mean" : True,
	"compactness_mean" : True,
	"concavity_mean" : True,
	"concave points_mean" : True,
	"symmetry_mean" : True
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



@app.route("/setup")
def setup():
    """
    This function does the setting up. It includes the following:
        1. Random Sampling
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


    twing = {
        "aravind": {
            "warrier": "1"
        }
    }

    return json.dumps(twing, default=lambda o: o.__dict__)

if __name__ == "__main__":
    app.run(debug = True)