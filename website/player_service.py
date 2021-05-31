import pickle
import configparser
import json
import os
from multiprocessing import Process


here = os.path.dirname(__file__)
config = configparser.ConfigParser()
config.read(os.path.join(here, 'config.ini'))

ROOT_DIRPATH = config['DATA']['ROOT']
EGO_DIRPATH = ROOT_DIRPATH + config['DATA']['EGOS']
DICT_FILEPATH = ROOT_DIRPATH + config['DATA']['DICT']
RESULT_FILEPATH = ROOT_DIRPATH + config['DATA']['RESULTS']

with open(DICT_FILEPATH, 'rb') as iddict:
    ids = pickle.load(iddict)

def get_ego_ids():
    with open(ROOT_DIRPATH + 'egomatchnumbers.pickle', 'rb') as f:
        return pickle.load(f)

def get_network(puuid, content):
    resultFile = RESULT_FILEPATH + puuid[0] + '/' + puuid + '.pickle'
    if os.path.exists(resultFile):
        with open(resultFile, 'rb') as f:
            network = pickle.load(f)
            if not content or content == 'all':
                return network
            network['nodes'] = network['nodesAlters'].copy()
            network['edges'] = network['edgesAlters'].copy()
            if content == 'egonet' or content == 'extended':
                network['nodes'].append(network['nodesEgo'])
                network['edges'].extend(network['edgesEgo'])
            if content == 'extended':
                network['nodes'].extend(network['nodes2nd'])
                network['edges'].extend(network['edges2nd'])
                #network['edges'].extend(network['alterties'])
            del network['nodesAlters']
            del network['edgesAlters']
            del network['nodesEgo']
            del network['edgesEgo']
            del network['nodes2nd']
            del network['edges2nd']
            return network
    return {'Error': 'Player data for PUUID ' + puuid + ' not found.'}