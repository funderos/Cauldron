import pickle
import configparser
import json
import os
import random

here = os.path.dirname(__file__)
config = configparser.ConfigParser()
config.read(os.path.join(here, '../config.ini'))

ROOT_DIRPATH = config['DATA']['ROOT']
EVAL_DIRPATH = ROOT_DIRPATH + config['DATA']['EVALUATION']
DICT_FILEPATH = ROOT_DIRPATH + config['DATA']['DICT']

with open(DICT_FILEPATH, 'rb') as iddict:
    ids = pickle.load(iddict)

def get_eval_file(userId):
    with open(EVAL_DIRPATH + userId + '.pickle', 'rb') as f:
        return pickle.load(f)

def write_eval_file(userId, eval_file):
    with open(EVAL_DIRPATH + userId + '.pickle', 'wb') as f:
        pickle.dump(eval_file, f, pickle.HIGHEST_PROTOCOL)

def create_eval_file(userId):
    write_eval_file(userId, {'progress': 1})

def get_eval_progress(userId):
    eval_file = get_eval_file(userId)
    return eval_file['progress']

def increment_progress(userId):
    eval_file = get_eval_file(userId)
    eval_file['progress'] += 1
    write_eval_file(userId, eval_file)

def write_eval_request_log(userId, request):
    eval_file = get_eval_file(userId)
    eval_file.setdefault(eval_file['progress'],{'requests': []})['requests'].append(request)
    write_eval_file(userId, eval_file)