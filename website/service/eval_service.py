import pickle
import configparser
import json
import os
import random

here = os.path.dirname(__file__)
config = configparser.ConfigParser()
config.read(os.path.join(here, '../config/config.ini'))

ROOT_DIRPATH = config['DATA']['ROOT']
EVAL_DIRPATH = ROOT_DIRPATH + config['DATA']['EVALUATION']
DICT_FILEPATH = ROOT_DIRPATH + config['DATA']['DICT']

with open(DICT_FILEPATH, 'rb') as iddict:
    ids = pickle.load(iddict)

def get_ego_ids():
    return ids.keys()

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

def write_eval_answer_for_progress(userId, answer):
    eval_file = get_eval_file(userId)
    eval_file.setdefault(eval_file['progress'],{})['answer'] = answer
    eval_file['progress'] += 1
    write_eval_file(userId, eval_file)
    return eval_file['progress']

def get_survey_data(userId, progress):
    header7 = "Please rate the website/it's features according to the following Likert scales:"
    q7_1 = {'type': ['likert-custom'], 'label1': 'fast', 'label2': 'slow'}
    q7_2 = {'type': ['likert-custom'], 'label1': 'inventive', 'label2': 'conventional'}
    q7_3 = {'type': ['likert-custom'], 'label1': 'obstructive', 'label2': 'supportive'}
    q7_4 = {'type': ['likert-custom'], 'label1': 'unpleasant', 'label2': 'pleasant'}
    q7_5 = {'type': ['likert-custom'], 'label1': 'meets expectations', 'label2': 'does not meet expectations'}
    q7_6 = {'type': ['likert-custom'], 'label1': 'inefficient', 'label2': 'efficient'}
    q7_7 = {'type': ['likert-custom'], 'label1': 'inconsistent', 'label2': 'consistent'}
    q7_8 = {'type': ['likert-custom'], 'label1': 'clear', 'label2': 'confusing'}
    q7_9 = {'type': ['likert-custom'], 'label1': 'impractical', 'label2': 'practical'}
    q7_10 = {'type': ['likert-custom'], 'label1': 'organized', 'label2': 'cluttered'}
    seven = {'header': header7, 'items': [q7_1, q7_2, q7_3, q7_4, q7_5, q7_6, q7_7, q7_8, q7_9, q7_10]}

    header8 = "How strong do you agree/disagree to the following statements:"
    q8_1 = {'type': ['likert'], 'label': 'I think that I would like to use this website frequently'}
    q8_2 = {'type': ['likert'], 'label': 'I think that I would need the support of a technical person to be able to use this website'}
    q8_3 = {'type': ['likert'], 'label': 'I would imagine that most people would learn to use the features on this website very quickly'}
    q8_4 = {'type': ['likert'], 'label': 'I felt very confident using the website'}
    q8_5 = {'type': ['likert'], 'label': 'I think there is a lot of prior knowledge required to use this website'}
    q8_6 = {'type': ['likert', 'textarea'], 'label': 'I had interesting findings when using this website', 'question': 'Specify your findings (optional):'}
    q8_7 = {'type': ['likert', 'textarea'], 'label': 'I can imagine using the features of this website for a specific usecase/domain', 'question': 'Specify the usecase/domain (optional):'}
    q8_8 = {'type': ['likert', 'textarea'], 'label': 'I am missing some features/tools on this website', 'question': 'Which tools are missing (optional)?'}
    q8_9 = {'type': ['textarea'], 'question': 'Would you like to give us some additional feedback (optional)?'}
    eight = {'header': header8, 'items': [q8_1, q8_2, q8_3, q8_4, q8_5, q8_6, q8_7, q8_8, q8_9]}

    header9 = "For this final page, we would like to ask kindly for some personal details:"
    q9_1 = {'type': ['textfield'], 'question': 'Age'}
    q9_2 = {'type': ['textfield'], 'question': 'Gender'}
    q9_3 = {'type': ['checkboxes'], 'label': 'I am working or studying currently in the following domains:'}
    q9_4 = {'type': ['likert'], 'label': 'I have prior knowledge/experience in Data Mining:'}
    q9_5 = {'type': ['likert'], 'label': 'I have prior knowledge/experience in Data Analytics:'}
    q9_6 = {'type': ['likert'], 'label': 'I have prior knowledge/experience in Social Network Analysis:'}
    q9_7 = {'type': ['likert'], 'label': 'I have prior knowledge/experience in Player Communities in video games:'}
    q9_8 = {'type': ['likert'], 'label': 'I have prior knowledge/experience in League Of Legends:'}
    nine = {'header': header9, 'items': [q9_1, q9_2, q9_3, q9_4, q9_5, q9_6, q9_7, q9_8]}

    survey_data = {7: seven, 8: eight, 9: nine}

    return survey_data[progress]