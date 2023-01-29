# Postprocessing evaluation data
# For each player, an evaluation file has been stored with all information in Pickle format. This script filters incomplete data records and generates as CSV file, figures and tables for the thesis in LaTeX.

# Imports & Filepaths
import pickle
import os
import configparser
from turtle import color
import pandas as pd
import matplotlib.pyplot as P
import numpy as np
import itertools

from statistics import mean

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'task_config.ini'))

ROOT_DIRPATH = config['EVAL']['ROOT']
EVAL_RESULT_PATH = ROOT_DIRPATH + config['EVAL']['RESULTS']
EVAL_XLSX_FILE = ROOT_DIRPATH + config['EVAL']['XLSX']
EVAL_TABLE_PATH = ROOT_DIRPATH + config['EVAL']['TABLES']
EVAL_PLOT_PATH = ROOT_DIRPATH + config['EVAL']['PLOTS']
EVAL_SUMMARY_PATH = ROOT_DIRPATH + config['EVAL']['USER_SUMMARIES']

# Descriptive terms for survey results, partly already formatted for LaTeX processing
ueq = [
    ['annoying', 'enjoyable'],
    ['not understandable', 'understandable'],
    ['creative', 'dull'],
    ['easy to learn', 'difficult to learn'],
    ['valuable', 'inferior'],
    ['boring', 'exciting'],
    ['not interesting', 'interesting'],
    ['unpredictable', 'predictable'],
    ['fast', 'slow'],
    ['inventive', 'conventional'],
    ['obstructive', 'supportive'],
    ['good', 'bad'],
    ['complicated', 'easy'],
    ['unlikable', 'pleasing'],
    ['usual', 'leading edge'],
    ['unpleasant', 'pleasant'],
    ['secure', 'not secure'],
    ['motivating', 'demotivating'],
    ['meets expectations', 'does not meet expectations'],
    ['inefficient', 'efficient'],
    ['clear', 'confusing'],
    ['impractical', 'practical'],
    ['organized', 'cluttered'],
    ['attractive', 'unattractive'],
    ['friendly', 'unfriendly'],
    ['conservative', 'innovative'],
]

sus = [
    [
        'Strongly Disagree',
        'Strongly Agree',
        'I think that I would like to use the tool frequently.',
    ],
    [
        'Strongly Disagree',
        'Strongly Agree',
        'I found the tool unnecessarily complex.',
    ],
    [
        'Strongly Disagree',
        'Strongly Agree',
        'I thought the tool was easy to use.',
    ],
    [
        'Strongly Disagree',
        'Strongly Agree',
        'I think that I would need the support of a technical person to be able to use the tool.',
    ],
    [
        'Strongly Disagree',
        'Strongly Agree',
        'I found the various functions in the tool were well integrated.',
    ],
    [
        'Strongly Disagree',
        'Strongly Agree',
        'I thought there was too much inconsistency in the tool.',
    ],
    [
        'Strongly Disagree',
        'Strongly Agree',
        'I would imagine that most people would learn to use the tool very quickly.',
    ],
    [
        'Strongly Disagree',
        'Strongly Agree',
        'I found the tool very cumbersome (awkward) to use.',
    ],
    [
        'Strongly Disagree',
        'Strongly Agree',
        'I felt very confident using the tool.',
    ],
    [
        'Strongly Disagree',
        'Strongly Agree',
        'I needed to learn a lot of things before I could get going with the tool.',
    ],
]

knowledgeScale = [
    ['No \\mbox{knowledge}', 'Expert', 'Data Mining'],
    ['No \\mbox{knowledge}', 'Expert', 'Data Analytics'],
    ['No \\mbox{knowledge}', 'Expert', 'Social Network Analysis'],
    ['No \\mbox{knowledge}', 'Expert', 'Player Communities in video games'],
    ['No \\mbox{knowledge}', 'Expert', 'League Of Legends']
]

table_taskdescs = [
  ['Task 1', 'View the provided tools in the different tabs and feel free to play around. Try to understand what they are for and how they can be used.', '-'],
  ['Task 2', 'Try to find out the Identified Regulation (IDE) value as well as the age of the player with ID 1273.', 'Age: 19, IDE: 2'],
  ['Task 3', 'One player has got an exceptional high mean tie strength. Find out how many matches this player participated in are included in the used dataset.', 'Match Count: 241'],
  ['Task 4', 'Can you find common connections, dependencies or correlations between the psychological data and the social network data of the players? Use the clustering features of the tool for solving this task.', '-'],
  ['Task 5', 'View the network graph of the player with the ID 1149. Can you spot some features and derive information about that player’s play style or social connections based on the given numerical features?', '-'],
  ['Task 6', 'Which player features do you think are most important for clustering? Which can be easily omitted or may even distort a meaningful result? Which clustering method works best for you?', '-'],
]

request_keys = {
    1: [],
    2: ['t2.1', 't2.2'],
    3: ['t3'],
    4: ['t4'],
    5: ['t5'],
    6: ['t6.1', 't6.2', 't6.3'],
    7: ['7.1', '7.2', '7.3', '7.4', '7.5', '7.6', '7.7', '7.8', '7.9', '7.10', '7.11', '7.12', '7.13', '7.14', '7.15', '7.16', '7.17', '7.18', '7.19', '7.20', '7.21', '7.22', '7.23', '7.24', '7.25', '7.26'],
    8: ['8.1', '8.2', '8.3', '8.4', '8.5', '8.6', '8.7', '8.8', '8.9', '8.10'],
    9: ['9.1', '9.1t', '9.2', '9.2t', '9.3', '9.3t', '9.4', '9.4t', '9.5', '9.5t'],
    10: ['10.1', '10.2', '10.3', '10.4', '10.5', '10.6', '10.7', '10.7t']
}

# Method for creating boxplots that represent numerical survey results in tables
def create_boxplot(data, filename, scalemin=-1, scalemax=-1):
    if scalemin < 0:
        scalemin = min(data) - 0.1
    if scalemax < 0:
        scalemax = max(data) + 0.1
    P.boxplot(data, vert=False, showfliers=False)
    for i in data:
        P.scatter(i, np.random.normal(1, 0.02, 1), alpha=0.3, c='b')
    P.xlim(scalemin, scalemax)
    P.ylim(0.9, 1.1)
    P.xticks(np.arange(scalemin + 0.1, scalemax - 0.1 +
             1, int((scalemax - scalemin) / 30) + 1))
    P.yticks([])
    P.box(False)
    P.gca().set_aspect((scalemax-scalemin) / 3 * 1.4)
    P.savefig(filename, bbox_inches='tight', pad_inches=0.15, transparent=True)
    P.clf()
    P.close()

# Method to crate LaTeX-formatted tables
def create_table_strings(headers, data, name):
    with open(EVAL_TABLE_PATH + name + '.txt', 'w') as f:
        if len(headers):
            f.write(
                '\\hline\n' + ' & '.join(['\\textbf{' + h + '}' for h in headers]) + ' \\\\\n')
        f.write('\\hline\n')
        for row in data:
            f.write(' & '.join(row) + ' \\\\\n\\hline\n')

# Iterate through all evaluation files, filter incomplete records and create helper lists and dictonaries with summarized statistics
eval_indices = []
eval_desc = []

request_numbers = {}
request_times = {}
table_info = {}

for tasknumber, keys in request_keys.items():
    for key in keys:
        if key[0] == 't':
            eval_indices.append(key[1:])
        else:
            eval_indices.append(key)
        if tasknumber in [2, 3]:
            table_info[key] = []
        if tasknumber == 6:
            table_info[key] = []
        if tasknumber in [7, 8, 10]:
            table_info[key] = []
    if tasknumber == 2:
        eval_desc.append('Age of Player 1273 (Solution: 19)')
        eval_desc.append('IDE of Player 1273 (Solution: 2)')
    if tasknumber == 3:
        eval_desc.append(
            'Match Count of Player with high mean tie strength (Solution: 241)')
    if tasknumber == 4:
        eval_desc.append('Clustering Feature Findings')
    if tasknumber == 5:
        eval_desc.append('Network Graph Feature Findings')
    if tasknumber == 6:
        eval_desc.append('Relevant Clustering Features')
        eval_desc.append('Irrelevant Clustering Features')
        eval_desc.append('Best Clustering Algorithm')
    if tasknumber < 7:
        eval_indices.append(str(tasknumber) + 'r')
        eval_indices. append(str(tasknumber) + 's')
        request_numbers[str(tasknumber)] = []
        request_times[str(tasknumber)] = []
        eval_desc.append('Request Number - Task ' + str(tasknumber))
        eval_desc.append('Time (seconds) - Task ' + str(tasknumber))
    if tasknumber == 7:
        for ueq_scale in ueq:
            eval_desc.append(
                'Scale: ' + ueq_scale[0] + ' (1) -> ' + ueq_scale[1] + ' (7)')
    if tasknumber == 8:
        for sus_scale in sus:
            eval_desc.append(
                sus_scale[2] + ': ' + sus_scale[0] + ' (1) -> ' + sus_scale[1] + ' (5)')
    if tasknumber == 9:
        eval_desc.append('Prior Knowledge')
        eval_desc.append('Prior Knowledge explained')
        eval_desc.append('Interesting findings')
        eval_desc.append('Interesting findings explained')
        eval_desc.append('Specific Domains')
        eval_desc.append('Specific Domains explained')
        eval_desc.append('Missing features')
        eval_desc.append('Missing features explained')
        eval_desc.append('Additional feedback')
        eval_desc.append('Additional feedback explained')
    if tasknumber == 10:
        for kl_scale in knowledgeScale:
            eval_desc.append(
                kl_scale[2] + ' Experience: ' + kl_scale[0] + ' (1) -> ' + kl_scale[1] + ' (5)')
        eval_desc.append('Participant Age')
        eval_desc.append('Participant Gender')
        eval_desc.append('Participant Gender explained')

eval_data = []
eval_requests = []
eval_data.append(eval_desc)

for evalfile in os.listdir(EVAL_RESULT_PATH):
    if evalfile[-6:] == 'pickle':
        with open(EVAL_RESULT_PATH + evalfile, 'rb') as f:
            evalf = pickle.load(f)
            if evalf['progress'] > 10:
                user_data = []
                user_requests = []
                last_timestamp = -1
                for line, desc in evalf.items():
                    if line != 'progress':
                        result = desc['requests'][-1]
                        for request_key in request_keys[line]:
                            user_data.append(
                                ','.join(result['args'].getlist(request_key)))
                            if line in [2, 3]:
                                table_info[request_key].append(
                                    result['args'].get(request_key))
                            if line == 6:
                                table_info[request_key].append(
                                    [config['FEATURES'][feature] for feature in result['args'].getlist(request_key)])
                            if line in [7, 8, 10] and request_key not in ['10.6', '10.7', '10.7t']:
                                table_info[request_key].append(
                                    int(result['args'].get(request_key)))
                        if line < 7:
                            request_number = len(desc['requests']) - 2
                            user_data.append(str(request_number))
                            request_numbers[str(line)].append(request_number)
                            request_time = result['timestamp'] - \
                                desc['requests'][0]['timestamp']
                            user_data.append(str(request_time))
                            request_times[str(line)].append(request_time)
                            
                        for req in desc['requests']:
                            arguments = req['args'].to_dict(flat=False) if 'args' in req else {}
                            user_requests.append([
                                line,
                                req['method'],
                                req['route'],
                                req['timestamp'] - last_timestamp if last_timestamp > 0 else '0',
                                ' | '.join([key + ': ' + ','.join(values) for key, values in arguments.items()])
                            ])
                            last_timestamp = req['timestamp']
                eval_data.append(user_data)
                eval_requests.append(user_requests)

# Create XLSX file containing a summary of all evaluation data
table_individual_req_cols = ['Task Number', 'Method', 'Route', 'Delta Time (seconds)', 'GET Query Parameters/POST Body Attributes']
with pd.ExcelWriter(EVAL_XLSX_FILE) as writer:
    df = pd.DataFrame(eval_data, columns=eval_indices)
    df.to_excel(writer, sheet_name='Overview', index=False)
    store_userid = 1
    for user_requests in eval_requests:
        user_df = pd.DataFrame(user_requests, columns=table_individual_req_cols)
        user_df.to_excel(writer, sheet_name='Requests User ' + str(store_userid), index=False)
        store_userid = store_userid + 1

# Create LaTeX table for average task completion times
table_request_stats_cols = [
    'Task Number', 'Number of requests', '\\diameter\\hspace{1mm}Completion time']
table_request_stats = []

for key, value in request_numbers.items():
    filename = 'Task_' + key[0] + '_requests.png'
    create_boxplot(value, EVAL_PLOT_PATH + filename)
    table_request_stats.append(['Task ' + key, '\\tableboxplot{Plots/' + filename + '}', str(
        round(mean(request_times[key]), 2)) + ' seconds'])

create_table_strings(table_request_stats_cols, table_request_stats, 'taskstats')

# Create LaTeX table for task solve rates
table_solved_cols = ['Task Number', 'Requested attribute', '\\% solved']
table_solved = [
    ['Task 2.1', 'Age', str(100 * mean(1 if x == '19' else 0 for x in table_info['t2.1']))],
    ['Task 2.2', 'IDE', str(100 * mean(1 if x == '2' else 0 for x in table_info['t2.2']))],
    ['Task 3', 'Match Count', str(100 * mean(1 if x == '241' else 0 for x in table_info['t3']))]
]

create_table_strings(table_solved_cols, table_solved, 'taskssolved')

# Create LaTeX table for relevant and irrelevant clustering features as named by evaluation users in the last task
table_preferred_cols = ['\\#', '(Sub-)Set of selected features']

relevant_features = []
for s in table_info['t6.1']:
    for i in range(0, len(s) + 1):
        relevant_features = relevant_features + \
            [frozenset(i) for i in itertools.combinations(s, i)]

irrelevant_features = []
for s in table_info['t6.2']:
    for i in range(0, len(s) + 1):
        irrelevant_features = irrelevant_features + \
            [frozenset(i) for i in itertools.combinations(s, i)]


def sorter(item):
    return (item[1], len(item[0]))


sorted_features = {
    'relevant': dict(sorted({t: relevant_features.count(t) for t in relevant_features if relevant_features.count(t) > 1 and len(t) > 0}.items(), key=sorter, reverse=True)),
    'irrelevant': dict(sorted({t: irrelevant_features.count(t) for t in irrelevant_features if irrelevant_features.count(t) > 1 and len(t) > 0}.items(), key=sorter, reverse=True))
}

table_relevant_features = []
current_count = -1
current_sets = {}
for t, c in sorted_features['relevant'].items():
    if c is not current_count:
        if len(current_sets):
            table_relevant_features.append([str(current_count), ' \\newline \\newline '.join(
                [' | '.join(samelength_sets) for samelength_sets in current_sets.values()])])
        current_count = c
        current_sets = {}
    if len(t) not in current_sets:
        current_sets[len(t)] = []
    current_sets[len(t)].append(', '.join(t))
table_relevant_features.append([str(current_count), ' \\newline \\newline '.join(
    [' | '.join(samelength_sets) for samelength_sets in current_sets.values()])])

create_table_strings(table_preferred_cols,
                     table_relevant_features, 'relevantfeatures')

table_irrelevant_features = []
current_count = -1
current_sets = []
for t, c in sorted_features['irrelevant'].items():
    if c is not current_count:
        if len(current_sets):
            table_irrelevant_features.append(
                [str(current_count), ' | '.join(current_sets)])
        current_count = c
        current_sets = []
    current_sets.append(', '.join(t))
table_irrelevant_features.append(
    [str(current_count), ' | '.join(current_sets)])

create_table_strings(table_preferred_cols,
                     table_irrelevant_features, 'irrelevantfeatures')

# Create LaTeX table for UEQ results
table_ueq = []
i = 1
for stmts in ueq:
    filename = 'Task_7_' + str(i) + '.png'
    create_boxplot(table_info['7.' + str(i)],
                   EVAL_PLOT_PATH + filename, 0.9, 7.1)
    table_ueq.append(
        [stmts[0], '\\tableboxplot{Plots/' + filename + '}', stmts[1]])
    i = i + 1

create_table_strings([], table_ueq, 'ueq')

# Create LaTeX table for SUS results
table_sus = []
i = 1

for stmts in sus:
    filename = 'Task_8_' + str(i) + '.png'
    create_boxplot(table_info['8.' + str(i)],
                   EVAL_PLOT_PATH + filename, 0.9, 5.1)
    table_sus.append(
        [stmts[2], stmts[0], '\\tableboxplot{Plots/' + filename + '}', stmts[1]])
    i = i + 1

create_table_strings([], table_sus, 'sus')

# Create LaTeX table for participant knowledge as specified by them
table_knowledge = []
i = 1

for stmts in knowledgeScale:
    filename = 'Task_10_' + str(i) + '.png'
    create_boxplot(table_info['10.' + str(i)],
                   EVAL_PLOT_PATH + filename, 0.9, 5.1)
    table_knowledge.append(
        [stmts[2], stmts[0], '\\tableboxplot{Plots/' + filename + '}', stmts[1]])
    i = i + 1

create_table_strings([], table_knowledge, 'knowledge')

# Create LaTeX table for task descriptions and solutions
table_taskdescs_cols = ['Task Number', 'Task Description', 'Expected Solution(s)']
create_table_strings(table_taskdescs_cols, table_taskdescs, 'tasksdescs')