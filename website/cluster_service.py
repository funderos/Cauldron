import pickle
import configparser
import json
import os
import io
from multiprocessing import Process
from pandas import DataFrame
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import seaborn as sns
from matplotlib import pyplot as plt
import numpy as np


here = os.path.dirname(__file__)
config = configparser.ConfigParser()
config.read(os.path.join(here, 'config.ini'))

ROOT_DIRPATH = config['DATA']['ROOT']
EGO_DIRPATH = ROOT_DIRPATH + config['DATA']['EGOS']
DICT_FILEPATH = ROOT_DIRPATH + config['DATA']['DICT']
RESULT_FILEPATH = ROOT_DIRPATH + config['DATA']['RESULTS']
RESULT_FILEPATH_FILE = ROOT_DIRPATH + config['DATA']['RESULTFILE']

with open(DICT_FILEPATH, 'rb') as iddict:
    ids = pickle.load(iddict)

with open(RESULT_FILEPATH_FILE, 'rb') as f:
    statistics = pickle.load(f)
    statFields = set(key for item in statistics for key in item)

with open(ROOT_DIRPATH + "egomatchnumbers.pickle", 'rb') as f:
    matchnumbers = pickle.load(f)


def get_ego_ids():
    return matchnumbers


def get_stat_fields(prefix=''):
    statFieldsRenamed = []
    for field in statFields:
        statFieldsRenamed.append(prefix + field.replace(' ', ''))
    return statFieldsRenamed


def get_statistics():
    statsRefactored = dict()
    for field in statFields:
        statsRefactored[field] = []
    for stat in statistics:
        for key, value in stat.items():
            if (value == value):
                statsRefactored[key].append(value)
    return statsRefactored


def prepare_data(args):
    with open(RESULT_FILEPATH_FILE, 'rb') as f:
        cols_of_interest = []
        for label in statFields:
            for userlabel in args['labels'].split(','):
                if userlabel.lower() in label.lower():
                    cols_of_interest.append(label)
        df = DataFrame(statistics)[cols_of_interest]
        if (args['preprocess'] == 'standard'):
            df = StandardScaler().fit_transform(df)
        if (args['preprocess'] == 'minmax'):
            df = MinMaxScaler().fit_transform(df)
    return df


def get_elbow(args):
    df = prepare_data(args)
    sse = []
    k_rng = range(1, 10)
    for k in k_rng:
        km = KMeans(n_clusters=k)
        km.fit(df)
        sse.append(km.inertia_)
    plt.figure()
    plt.xlabel('K')
    plt.ylabel('Sum of squared error')
    plt.plot(k_rng, sse)
    sio = io.BytesIO()
    plt.savefig(sio, format='svg')
    svg = sio.getvalue()
    return svg

def prepare_pca(n_components, data, kmeans_labels):
    names = ['x', 'y', 'z']
    matrix = PCA(n_components=n_components).fit_transform(data)
    df_matrix = DataFrame(matrix)
    df_matrix.rename({i:names[i] for i in range(n_components)}, axis=1, inplace=True)
    df_matrix['labels'] = kmeans_labels
    
    return df_matrix

def get_clustering(args):
    df = prepare_data(args)
    km = KMeans(n_clusters=int(args['k']))
    y_kmeans = km.fit_predict(df)
    
    pca_df = prepare_pca(3, df, km.labels_)
    plt.figure()
    sns.scatterplot(x=pca_df.x, y=pca_df.y, hue=pca_df.labels, palette="Set2")
    sio = io.BytesIO()
    plt.savefig(sio, format='svg')
    svg = sio.getvalue()
    return svg
    # return [cols_of_interest] + km.cluster_centers_.tolist()
