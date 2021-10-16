# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

# %% [markdown]
# # Networks
#
# Clustering and visualization of player data is not only based on their numerical features but also on structural (network) features that must be created an prepared beforehand.
#
# __SUBJECT TO CHANGE - CHECK VALUES w/ SUPERVISOR BEFORE FULL DUMP__
# %% [markdown]
# ## Imports

# %%

import os
import configparser
import json
import random
import itertools
import pickle
from pandas import DataFrame

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'task_config.ini'))

ROOT_DIRPATH = config['GENERAL']['ROOT']
TARGET_DIRPATH = config['GENERAL']['TARGET']
EGO_DIRPATH = ROOT_DIRPATH + config['API']['EGOS']
DICT_FILEPATH = ROOT_DIRPATH + config['API']['DICT']
SURVEY_FILEPATH = ROOT_DIRPATH + config['SURVEY']['COMBINED']
RESULT_FILEPATH = TARGET_DIRPATH + config['RESULT']['PLAYERS']
RESULT_FILE = TARGET_DIRPATH + config['RESULT']['OVERALL']
RESULT_DICT = TARGET_DIRPATH + config['RESULT']['DICT']
COUNT_SRC = ROOT_DIRPATH + config['HELPER']['MATCHNUMBER']
COUNT_TARGET = TARGET_DIRPATH + config['HELPER']['MATCHNUMBER']

# %% [markdown]
# ### Load ID Dictionary
#
# The ID Dictionary maps Summoner IDs to their filepath in the API Data

# %%
with open(DICT_FILEPATH, 'rb') as iddict:
    ids = pickle.load(iddict)
with open(SURVEY_FILEPATH, 'rb') as surveyData:
    survey = pickle.load(surveyData)

# %% [markdown]
# ### Save processed player data
#
# A method for storing processed player data in the specified filepath as well as a method for retrieving the right filepath having a summoner id.

# %%


def save_result(filepath, result):
    if not os.path.exists(os.path.dirname(filepath)):
        try:
            os.makedirs(os.path.dirname(filepath))
        except OSError as exc:  # Guard against race condition
            if exc.errno != exc.errno.EEXIST:
                raise
    with open(filepath, 'wb') as f:
        pickle.dump(result, f, pickle.HIGHEST_PROTOCOL)


def get_result_filepath(summoner_id):
    puuid = ids[summoner_id].split('/')[1]
    return RESULT_FILEPATH + puuid[0:2] + '/' + puuid + '.pickle'

# %% [markdown]
# ### Method: Create Player
#
# This method creates Python dictionaries containing details of a specific player and it's connections to other players.

# %%


def create_player(summoner_id):
    player_path = ROOT_DIRPATH + '/' + ids[summoner_id] + '/'
    result = {'id': summoner_id, 'puuid': player_path.split(
        "/")[-2], 'alters': dict(), 'stats': dict()}

    with open(player_path + 'summoner.json', 'r') as summoner_input:
        ego = json.load(summoner_input)
        result['name'] = ego['name']
        result['platform'] = ego['platformId']
        result['level'] = ego['summonerLevel']
        if 'linkId' in ego and int(ego['linkId']) in survey:
            result['surveyData'] = survey[int(ego['linkId'])]
            result['custId'] = result['surveyData']['id']

    kda = []
    kp = []
    team_gold = []
    team_damage = []
    ckpm = []
    won = 0
    kills_won = 0
    lost = 0
    deaths_lost = 0
    match_count = 0

    for matchfile in os.listdir(player_path):
        if matchfile in ['summoner.json', 'rankedstats.json', 'matchhistory.json']:
            continue
        match_count = match_count + 1
        with open(player_path + matchfile, 'r') as matchinput:
            match = json.load(matchinput)
            teams = {str(100): dict(), str(200): dict()}
            team_ids = {str(100): [], str(200): []}
            player_team = -1
            total_damage = 0
            total_gold = 0
            total_kills = 0
            for participant in match['participants']:
                teams[str(participant['teamId'])
                      ][participant['participantId']] = participant['stats']
            for part_idendity in match['participantIdentities']:
                if 'player' in part_idendity and 'summonerId' in part_idendity['player']:
                    for key, values in teams.items():
                        if part_idendity['participantId'] in values:
                            if part_idendity['player']['summonerId'] == ego['id']:
                                player_team = key
                                ego_kills = values[part_idendity['participantId']]['kills']
                                ego_assists = values[part_idendity['participantId']]['assists']
                                ego_deaths = values[part_idendity['participantId']]['deaths']
                                ego_damage = values[part_idendity['participantId']
                                                    ]['totalDamageDealt']
                                ego_gold = values[part_idendity['participantId']
                                                  ]['goldEarned']
                                total_kills = total_kills + ego_kills
                                total_damage = total_damage + ego_damage
                                total_gold = total_gold + ego_gold
                                if values[part_idendity['participantId']]['win']:
                                    won = won + 1
                                    kills_won = kills_won + ego_kills
                                else:
                                    lost = lost + 1
                                    deaths_lost = deaths_lost + ego_deaths
                            else:
                                team_ids[key].append((part_idendity['player']['summonerId'], part_idendity['player']['currentPlatformId'], part_idendity['player']['summonerName'],
                                                     values[part_idendity['participantId']]['kills'], values[part_idendity['participantId']]['totalDamageDealt'], values[part_idendity['participantId']]['goldEarned']))
            if int(player_team) > 0:
                for key, values in team_ids.items():
                    for participant_tuple in values:
                        result['alters'].setdefault(participant_tuple[0], {'platform': participant_tuple[1], 'name': participant_tuple[2], 'team': [
                        ], 'vs': []})['vs' if key != player_team else 'team'].append(match['gameId'])
                        if key == player_team:
                            total_kills = total_kills + participant_tuple[3]
                            total_damage = total_damage + participant_tuple[4]
                            total_gold = total_gold + participant_tuple[5]
                kda.append(((ego_kills + ego_assists) / ego_deaths)
                           if ego_deaths else 1)
                if total_kills > 0:
                    kp.append((ego_kills + ego_assists) / total_kills)
                if total_gold > 0:
                    team_gold.append(ego_gold / total_gold)
                if total_damage > 0:
                    team_damage.append(ego_damage / total_damage)
                if match['gameDuration']:
                    ckpm.append((ego_kills + ego_deaths) *
                                60 / match['gameDuration'])

    result['stats']['kda'] = sum(kda) / len(kda) if (len(kda)) else 0
    result['stats']['kp'] = sum(kp) / len(kp) if (len(kp)) else 0
    result['stats']['teamGold'] = sum(
        team_gold) / len(team_gold) if (len(team_gold)) else 0
    result['stats']['teamDamage'] = sum(
        team_damage) / len(team_damage) if (len(team_damage)) else 0
    result['stats']['ckpm'] = sum(ckpm) / len(ckpm) if (len(ckpm)) else 0
    result['stats']['winrate'] = won / (won + lost) if won + lost else 0
    result['stats']['kpw'] = kills_won / won if won else 0
    result['stats']['dpl'] = deaths_lost / lost if lost else 0

    result['matchcount'] = match_count

    return result

# %% [markdown]
# ### Method: Get Alter
#
# A method for retrieving player details of an alter. It will check the existance of persisted data and return it, otherwise delegates to the create player method for creating and storing it.

# %%


def get_alter(summoner_id):
    result_file = get_result_filepath(summoner_id)
    if os.path.exists(result_file):
        with open(result_file, 'rb') as f:
            return pickle.load(f)
    result = create_player(summoner_id)
    save_result(result_file, result)
    return result

# %% [markdown]
# ### Get Ego by PUUID
#
# Similar to the Get Alter method, a stored copy of a processed object is queried before creating it. Player details of egos also contain all data relevant for 2-level ego networks and their features.

# %%


def get_ego_by_puuid(puuid):
    result_file = RESULT_FILEPATH + puuid[0:2] + '/' + puuid + '.pickle'
    if os.path.exists(result_file):
        with open(result_file, 'rb') as f:
            result = pickle.load(f)
            if 'network' in result:
                return result
            summoner_id = result['id']
    else:
        with open(EGO_DIRPATH + puuid + '/' + 'summoner.json', 'r') as summonerinput:
            ego = json.load(summonerinput)
            summoner_id = ego['id']
            result = create_player(summoner_id)

    if 'custId' not in result:
        save_result(result_file, result)
        return result

    result['edgesEgo'] = []
    result['nodesAlters'] = []
    result['edgesAlters'] = []
    result['edges2nd'] = []

    result['altersTeam'] = []
    result['altersVs'] = []

    result['nodesEgo'] = {"id": summoner_id,
                          "value": 30, "label": str(result['custId'])}

    alters = set(result['alters'])
    remaining_alters = alters.copy()
    components = list([a] for a in alters)
    stored_2nd_level = dict()
    missing_alters = dict()


    for alter_id in alters:
        alter_info = result['alters'][alter_id]

        team_count = len(alter_info['team'])
        vs_count = len(alter_info['vs'])
        if team_count:
            result['altersTeam'].append(alter_id)
            result['edgesEgo'].append(
                {"from": summoner_id, "to": alter_id, "value": team_count, "title": team_count, "color": "0000FF"})
        if vs_count:
            result['altersVs'].append(alter_id)
            result['edgesEgo'].append(
                {"from": summoner_id, "to": alter_id, "value": vs_count, "title": vs_count, "color": "FF0000"})

        if alter_id not in ids:
            result['nodesAlters'].append({"id": alter_id, "value": 10, "label": alter_info['name'] if len(
                alter_info['name']) < 9 else alter_info['name'][:7] + '...'})
            for match in alter_info['team']:
                missing_alters.setdefault(match, {'team': [], 'vs': []})[
                    'team'].append(alter_id)
            for match in alter_info['vs']:
                missing_alters.setdefault(match, {'team': [], 'vs': []})[
                    'vs'].append(alter_id)
            continue

        remaining_alters.remove(alter_id)
        alter = get_alter(alter_id)

        result['nodesAlters'].append({"id": alter_id, "value": 20 if 'custId' in alter else 10, "label": str(
            alter['custId']) if 'custId' in alter else alter_info['name'] if len(alter_info['name']) < 9 else alter_info['name'][:7] + '...'})

        merged = [sublist for sublist in components for a in sublist if a in set(
            alter['alters'])]
        excl = [sublist for sublist in components if sublist not in merged]
        components = excl + \
            [list(set(element for sublist in merged for element in sublist))]

        common_alter_ids = set(alter['alters']) & remaining_alters

        for alter_alter_id in common_alter_ids:
            match_info = alter['alters'][alter_alter_id]
            #result['alterTies'][str((alterId, alterAlterId))] = {key:matchInfo[key] for key in matchInfo if key == 'team' or key == 'vs'}

            team_count = len(match_info['team'])
            vs_count = len(match_info['vs'])
            if team_count:
                result['edgesAlters'].append(
                    {"from": alter_id, "to": alter_alter_id, "value": team_count, "title": team_count, "color": "0000FF"})
            if vs_count:
                result['edgesAlters'].append(
                    {"from": alter_id, "to": alter_alter_id, "value": vs_count, "title": vs_count, "color": "FF0000"})

        alters_2nd_level = set(alter['alters']) - alters
        if summoner_id in alters_2nd_level:
            alters_2nd_level.remove(summoner_id)

        for alter_2nd_level_id in alters_2nd_level:
            match_info = alter['alters'][alter_2nd_level_id]

            stored_2nd_level.setdefault(alter_2nd_level_id, {"id": alter_2nd_level_id, "value": 5, "parents": [], "label": match_info['name'] if len(
                    match_info['name']) < 9 else match_info['name'][:7] + '...'})['parents'].append(alter_id)
            
            team_count = len(match_info['team'])
            vs_count = len(match_info['vs'])
            if team_count:
                result['edges2nd'].append(
                    {"from": alter_id, "to": alter_2nd_level_id, "value": team_count, "title": team_count, "color": "0000FF"})
            if vs_count:
                result['edges2nd'].append(
                    {"from": alter_id, "to": alter_2nd_level_id, "value": vs_count, "title": vs_count, "color": "FF0000"})
    
    result['nodes2nd'] = list(stored_2nd_level.values())

    coop_matches = []
    vs_matches = []
    for match_id, match in missing_alters.items():
        match['team'].sort()
        match['vs'].sort()
        for pair in itertools.combinations(match['team'], 2):
            coop_matches.append(pair)
        for pair in itertools.combinations(match['vs'], 2):
            coop_matches.append(pair)
        for id1 in match['team']:
            for id2 in match['vs']:
                vs_players = [id1, id2]
                vs_players.sort()
                vs_matches.append(tuple(vs_players))
        merged = [sublist for sublist in components for a in sublist if a in set(
            match['team'] + match['vs'])]
        excl = [sublist for sublist in components if sublist not in merged]
        components = excl + \
            [list(set(element for sublist in merged for element in sublist))]

    for player_tuple in set(coop_matches):
        result['edgesAlters'].append({"from": player_tuple[0], "to": player_tuple[1], "value": coop_matches.count(
            player_tuple), "title": coop_matches.count(player_tuple), "color": "0000FF"})
    for player_tuple in set(vs_matches):
        result['edgesAlters'].append({"from": player_tuple[0], "to": player_tuple[1], "value": vs_matches.count(
            player_tuple), "title": vs_matches.count(player_tuple), "color": "FF0000"})

    number_of_alters = len(alters)  # = Degree
    number_of_ties = len(result['edgesAlters'])
    mean_tie_strength = sum(edge['value']
                            for edge in result['edgesEgo']) / len(result['edgesEgo'])
    density = number_of_ties / (number_of_alters * (number_of_alters - 1))
    component_ratio = (len(components) - 1) / (number_of_alters - 1)
    fragmentation_index = 1 - sum(len(component) * (len(component) - 1)
                                  for component in components) / (number_of_alters * (number_of_alters - 1))

    result["network"] = {"Degree": number_of_alters, "Mean Tie Strength": mean_tie_strength, "Density": density, "Components": len(
        components), "Component Ratio": component_ratio, "Fragmentation Index": fragmentation_index}

    save_result(result_file, result)
    return result

# %% [markdown]
# ### Get Ego by Summoner ID
#
# Processes the summoner ID and delegates to the _Get Ego by PUUID_ method.

# %%


def get_ego_by_summoner_id(summoner_id):
    return get_ego_by_puuid(ids[summoner_id].split("/")[1])


# %%
results = []
internaliddict = {}
matchcount = {}
with open(COUNT_SRC, 'rb') as f:
    for puuid, match_number in pickle.load(f):
        if match_number > 0:
            print(match_number)
            ego = get_ego_by_puuid(puuid)
            if 'surveyData' in ego:
                internaliddict[ego['custId']] = puuid
                matchcount[str(ego['custId'])] = ego['matchcount']
                print(puuid)
                result = {'level': ego['level']}
                for key, value in ego['stats'].items():
                    result[key] = value
                for key, value in ego['surveyData'].items():
                    result[key] = value
                for key, value in ego['network'].items():
                    result[key] = value
                results.append(result)


# %%
df = DataFrame(results)
df.head()


# %%
len(df.index)

# %%
with open(RESULT_FILE, 'wb') as f:
    pickle.dump(results, f, pickle.HIGHEST_PROTOCOL)
with open(RESULT_DICT, 'wb') as f:
    pickle.dump(internaliddict, f, pickle.HIGHEST_PROTOCOL)
with open(COUNT_TARGET, 'wb') as f:
    pickle.dump(matchcount, f, pickle.HIGHEST_PROTOCOL)