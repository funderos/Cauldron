# Code/ideas partly taken/inspired from https://towardsdatascience.com/visualising-high-dimensional-datasets-using-pca-and-t-sne-in-python-8ef87e7915b

import pickle
import configparser
import json
import os
import io
import pandas
import uuid
from sklearn.cluster import KMeans, DBSCAN, SpectralClustering, OPTICS
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from matplotlib import pyplot as plt

here = os.path.dirname(__file__)
config = configparser.ConfigParser()
config.read(os.path.join(here, '../config/config.ini'))

ROOT_DIRPATH = config['DATA']['ROOT']
DICT_FILEPATH = ROOT_DIRPATH + config['DATA']['DICT']
RESULT_FILEPATH = ROOT_DIRPATH + config['DATA']['RESULTS']
RESULT_FILEPATH_FILE = ROOT_DIRPATH + config['DATA']['RESULTFILE']

statCats = configparser.ConfigParser()
statCats.optionxform = str
statCats.read(os.path.join(here, '../config/stats.ini'))
categorizedStatFields = {}
for category in statCats:
    categorizedStatFields[category] = {}
    for item in statCats[category]:
        categorizedStatFields[category][statCats[category][item]] = item.replace("__", " ")

statTooltips = configparser.ConfigParser()
statTooltips.optionxform = str
statTooltips.read(os.path.join(here, '../config/stats_tooltips.ini'))
categorizedStatFieldTooltips = {}
for category in statTooltips:
    categorizedStatFieldTooltips[category] = {}
    for item in statTooltips[category]:
        categorizedStatFieldTooltips[category][statTooltips[category][item]] = item.replace("__", " ")

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
    statFieldsRenamed = list(prefix + key.replace(' ', '') for key in statFields)
    #for field in statFields:
    #    statFieldsRenamed.append(prefix + field.replace(' ', ''))
    return statFieldsRenamed

def get_categorized_stat_fields(prefix=''):
    statFieldsRenamed = {}
    for category in categorizedStatFields:
        statFieldsRenamed[category] = {prefix + categorizedStatFields[category][key].replace(' ', '') : key for key in categorizedStatFields[category]}
    return statFieldsRenamed

def get_stat_field_tooltips(prefix=''):
    statFieldsRenamed = {}
    for category in categorizedStatFieldTooltips:
        statFieldsRenamed[category] = {prefix + categorizedStatFieldTooltips[category][key].replace(' ', '') : key for key in categorizedStatFieldTooltips[category]}
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

def get_csv(labels):
    df = pandas.DataFrame(statistics)
    df['clusternumber'] = labels
    return df.to_csv()

def prepare_data(args):
    with open(RESULT_FILEPATH_FILE, 'rb') as f:
        cols_of_interest = []
        for label in statFields:
            for userlabel in args['labels'].split(','):
                if userlabel.lower() in label.lower():
                    cols_of_interest.append(label)
        df = pandas.DataFrame(statistics)[cols_of_interest]
        pandas.set_option('display.max_columns', None)
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

def prepare_graph(method, n_components, data, model_labels):
    names = ['x', 'y', 'z']
    if (method == 'pca'):
        matrix = PCA(n_components=n_components).fit_transform(data)
    elif (method == 'tsne'):
        matrix = TSNE(n_components=n_components).fit_transform(data)
    df_matrix = pandas.DataFrame(matrix)
    df_matrix.rename({i:names[i] for i in range(n_components)}, axis=1, inplace=True)
    df_matrix['labels'] = [str(label) for label in model_labels]
    df_matrix['ids'] = list(stat['id'] for stat in statistics)
    
    return df_matrix

def get_clustering(args):
    df = prepare_data(args)
    if (args['clustertype'] == 'kmeans'):
        model = KMeans(n_clusters=int(args['kmk']))
    elif (args['clustertype'] == 'dbscan'):
        min_samples = df.shape[1] + 1
        model = DBSCAN(eps=float(args['dbe']), min_samples=min_samples)
    elif (args['clustertype'] == 'spectral'):
        model = SpectralClustering(n_clusters=int(args['spn']))
    elif (args['clustertype'] == 'optics'):
        model = OPTICS(min_samples=int(args['ops']))
    else:
        return {}
    model.fit_predict(df)
    reduced_df = prepare_graph(args['dimreduce'], 3, df, model.labels_)
    result = reduced_df.groupby('labels')[['x', 'y', 'z', 'ids']].apply(lambda g: g.to_dict('list')).to_dict()
    result['labels'] = reduced_df['labels'].to_list()
    result['exportfn'] = args['clustertype'] + "-" + str(uuid.uuid4()) + "-export.csv"
    return result
