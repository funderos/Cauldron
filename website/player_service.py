import pickle
import configparser
import json
import os
from multiprocessing import Process


here = os.path.dirname(__file__)
config = configparser.ConfigParser()
config.read(os.path.join(here, 'config.ini'))

ROOT_DIRPATH = config['DATA']['ROOT']
#EGO_DIRPATH = ROOT_DIRPATH + config['DATA']['EGOS']
DICT_FILEPATH = ROOT_DIRPATH + config['DATA']['DICT']
RESULT_FILEPATH = ROOT_DIRPATH + config['DATA']['RESULTS']

with open(DICT_FILEPATH, 'rb') as iddict:
    ids = pickle.load(iddict)

with open(ROOT_DIRPATH + 'egomatchnumbers.pickle', 'rb') as countdict:
    numberids = {key: value for key, value in pickle.load(countdict)}

def get_ego_ids():
    return ids

def get_count_ids():
    return numberids

def get_network(internalid, content):
    puuid = ids[int(internalid)]
    resultFile = RESULT_FILEPATH + puuid[0:2] + '/' + puuid + '.pickle'
    if os.path.exists(resultFile):
        with open(resultFile, 'rb') as f:
            network = pickle.load(f)
            if not content or content == 'all':
                return network
            response = {}
            if content == 'details':
                response['ID'] = network['custId']
                response['Summoner Name'] = network['name']
                response['Platform'] = network['platform']
                response['Level'] = network['level']
                for key, value in (network['stats'] | network['network'] | network['surveyData']).items():
                    response[key] = value
            elif content == 'team':
                network['altersTeam'].append(network['id'])
                response['nodes'] = list(node for node in network['nodesAlters'] if node['id'] in network['altersTeam'])
                response['nodes'].append(network['nodesEgo'])
                response['edges'] = list(edge for edge in network['edgesAlters'] + network['edgesEgo'] if edge['from'] in network['altersTeam'] and edge['to'] in network['altersTeam'] )
            elif content == 'vs':
                network['altersVs'].append(network['id'])
                response['nodes'] = list(node for node in network['nodesAlters'] if node['id'] in network['altersVs'])
                response['nodes'].append(network['nodesEgo'])
                response['edges'] = list(edge for edge in network['edgesAlters'] + network['edgesEgo'] if edge['from'] in network['altersVs'] and edge['to'] in network['altersVs'] )
            else:
                response['nodes'] = network['nodesAlters'].copy()
                response['edges'] = network['edgesAlters'].copy()
            if content == 'egonet' or content == 'extended':
                response['nodes'].append(network['nodesEgo'])
                response['edges'].extend(network['edgesEgo'])
            if content == 'extended':
                response['nodes'].extend(network['nodes2nd'])
                response['edges'].extend(network['edges2nd'])
                #network['edges'].extend(network['alterties'])
            return response
    return {'Error': 'Player data for ID ' + internalid + ' not found.'}