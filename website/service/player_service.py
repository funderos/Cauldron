import pickle
import configparser
import os

here = os.path.dirname(__file__)
config = configparser.ConfigParser()
config.read(os.path.join(here, '../config/config.ini'))

statCats = configparser.ConfigParser()
statCats.optionxform = str
statCats.read(os.path.join(here, 'stats.ini'))

ROOT_DIRPATH = config['DATA']['ROOT']
DICT_FILEPATH = ROOT_DIRPATH + config['DATA']['DICT']
RESULT_FILEPATH = ROOT_DIRPATH + config['DATA']['RESULTS']

with open(DICT_FILEPATH, 'rb') as iddict:
    ids = pickle.load(iddict)

with open(ROOT_DIRPATH + 'egomatchnumbers.pickle', 'rb') as countdict:
    numberids = {int(key): value for key, value in pickle.load(countdict).items()}

def get_ego_ids():
    return ids

def get_count_ids():
    return numberids

def get_network(internalid, args):
    puuid = ids[int(internalid)]
    resultFile = RESULT_FILEPATH + puuid[0:2] + '/' + puuid + '.pickle'
    if os.path.exists(resultFile):
        with open(resultFile, 'rb') as f:
            network = pickle.load(f)
            if not args['mode'] or args['mode'] == 'all':
                return network
            response = {}
            if args['mode'] == 'details':            
                response['name'] = "hidden"
                response['platform'] = network['platform']
                response['level'] = network['level']
                response['matchcount'] = network['matchcount']
                for key, value in (network['stats'] | network['network'] | network['surveyData']).items():
                    response[key.replace(" ", "")] = value
                return response
            if args['viscon'] == 'team':
                network['altersTeam'].append(network['id'])
                response['nodes'] = list(node for node in network['nodesAlters'] if node['id'] in network['altersTeam'])
                response['nodes'].append(network['nodesEgo'])
                response['edges'] = list(edge for edge in network['edgesAlters'] + network['edgesEgo'] if edge['from'] in network['altersTeam'] and edge['to'] in network['altersTeam'] )
            elif args['viscon']  == 'vs':
                network['altersVs'].append(network['id'])
                response['nodes'] = list(node for node in network['nodesAlters'] if node['id'] in network['altersVs'])
                response['nodes'].append(network['nodesEgo'])
                response['edges'] = list(edge for edge in network['edgesAlters'] + network['edgesEgo'] if edge['from'] in network['altersVs'] and edge['to'] in network['altersVs'] )
            else:
                response['nodes'] = network['nodesAlters'].copy()
                response['edges'] = network['edgesAlters'].copy()
            if not args['viscom'] or args['viscom'] == 'false':
                response['nodes'].append(network['nodesEgo'])
                response['edges'].extend(network['edgesEgo'])
            if args['mode'] == 'extended':
                response['nodes'].extend(network['nodes2nd'])
                response['edges'].extend(network['edges2nd'])
            return response
    return {'Error': 'Player data for ID ' + internalid + ' not found.'}