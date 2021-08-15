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
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    with open(filepath, 'wb') as f:
        pickle.dump(result, f, pickle.HIGHEST_PROTOCOL)

def get_result_filepath(summonerId):
    puuid = ids[summonerId].split('/')[1]
    return RESULT_FILEPATH + puuid[0:2] + '/' + puuid + '.pickle'

# %% [markdown]
# ### Method: Create Player
# 
# This method creates Python dictionaries containing details of a specific player and it's connections to other players.

# %%
def create_player(summonerId):
    playerPath = ROOT_DIRPATH + '/' + ids[summonerId] + '/'
    result = {'id': summonerId, 'puuid': playerPath.split("/")[-2], 'alters': dict(), 'stats': dict()}

    with open (playerPath + 'summoner.json', 'r') as summonerinput:
        ego = json.load(summonerinput)
        result['name'] = ego['name']
        result['platform'] = ego['platformId']
        result['level'] = ego['summonerLevel']
        if 'linkId' in ego and int(ego['linkId']) in survey:
            result['surveyData'] = survey[int(ego['linkId'])]
            result['custId'] = result['surveyData']['id']

    kda = []
    kp = []
    teamGold = []
    teamDamage = []
    ckpm = []
    won = 0
    killsWon = 0
    lost = 0
    deathsLost = 0

    for matchfile in os.listdir(playerPath):
        if matchfile in ['summoner.json', 'rankedstats.json', 'matchhistory.json']:
            continue
        with open(playerPath + matchfile, 'r') as matchinput:
            match = json.load(matchinput)
            teams = {str(100): dict(), str(200): dict()}
            teamIds = {str(100): [], str(200): []}
            playerTeam = -1
            totalDamage = 0
            totalGold = 0
            totalKills = 0
            for participant in match['participants']:
                teams[str(participant['teamId'])][participant['participantId']] = participant['stats']
            for partIdendity in match['participantIdentities']:
                if 'player' in partIdendity and 'summonerId' in partIdendity['player']:
                    for key, values in teams.items():
                        if partIdendity['participantId'] in values:
                            if partIdendity['player']['summonerId'] == ego['id']:
                                playerTeam = key
                                egoKills = values[partIdendity['participantId']]['kills']
                                egoAssists = values[partIdendity['participantId']]['assists']
                                egoDeaths = values[partIdendity['participantId']]['deaths']
                                egoDamage = values[partIdendity['participantId']]['totalDamageDealt']
                                egoGold = values[partIdendity['participantId']]['goldEarned']
                                totalKills = totalKills + egoKills
                                totalDamage = totalDamage + egoDamage
                                totalGold = totalGold + egoGold
                                if values[partIdendity['participantId']]['win']:
                                    won = won + 1
                                    killsWon = killsWon + egoKills
                                else:
                                    lost = lost + 1
                                    deathsLost = deathsLost + egoDeaths
                            else:
                                teamIds[key].append((partIdendity['player']['summonerId'], partIdendity['player']['currentPlatformId'], partIdendity['player']['summonerName'], values[partIdendity['participantId']]['kills'], values[partIdendity['participantId']]['totalDamageDealt'], values[partIdendity['participantId']]['goldEarned']))
            if int(playerTeam) > 0:
                for key, values in teamIds.items():
                    for participantTuple in values:
                        result['alters'].setdefault(participantTuple[0], {'platform': participantTuple[1], 'name': participantTuple[2], 'team': [], 'vs': []})['vs' if key != playerTeam else 'team'].append(match['gameId'])
                        if key == playerTeam:
                            totalKills = totalKills + participantTuple[3]
                            totalDamage = totalDamage + participantTuple[4]
                            totalGold = totalGold + participantTuple[5]
                kda.append(((egoKills + egoAssists) / egoDeaths) if egoDeaths else 1)
                if totalKills > 0:
                    kp.append((egoKills + egoAssists) / totalKills)
                if totalGold > 0:
                    teamGold.append(egoGold / totalGold)
                if totalDamage > 0:
                    teamDamage.append(egoDamage / totalDamage)
                if match['gameDuration']:
                    ckpm.append((egoKills + egoDeaths) * 60 / match['gameDuration'])

    
    result['stats']['kda'] = sum(kda) / len(kda) if (len(kda)) else 0
    result['stats']['kp'] = sum(kp) / len(kp) if (len(kp)) else 0
    result['stats']['teamGold'] = sum(teamGold) / len(teamGold) if (len(teamGold)) else 0
    result['stats']['teamDamage'] = sum(teamDamage) / len(teamDamage) if (len(teamDamage)) else 0
    result['stats']['ckpm'] = sum(ckpm) / len(ckpm) if (len(ckpm)) else 0
    result['stats']['winrate'] = won / (won + lost) if won + lost else 0
    result['stats']['kpw'] = killsWon / won if won else 0
    result['stats']['dpl'] = deathsLost / lost if lost else 0

    if 'level' not in result:
        return create_player(summonerId)

    return result

# %% [markdown]
# ### Method: Get Alter
# 
# A method for retrieving player details of an alter. It will check the existance of persisted data and return it, otherwise delegates to the create player method for creating and storing it.

# %%
def get_alter(summonerId):
    resultFile = get_result_filepath(summonerId)
    if os.path.exists(resultFile):
        with open(resultFile, 'rb') as f:
            return pickle.load(f)
    result = create_player(summonerId)
    save_result(resultFile, result)
    return result

# %% [markdown]
# ### Get Ego by PUUID
# 
# Similar to the Get Alter method, a stored copy of a processed object is queried before creating it. Player details of egos also contain all data relevant for 2-level ego networks and their features.

# %%
def get_ego_by_puuid(puuid):
    resultFile = RESULT_FILEPATH + puuid[0:2] + '/' + puuid + '.pickle'
    if os.path.exists(resultFile):
        with open(resultFile, 'rb') as f:
            result = pickle.load(f)
            if 'network' in result:
                return result
            summonerId = result['id']
    else:
        with open (EGO_DIRPATH + puuid + '/' + 'summoner.json', 'r') as summonerinput:
            ego = json.load(summonerinput)
            summonerId = ego['id']
            result = create_player(summonerId)

    if 'custId' not in result:
        save_result(resultFile, result)
        return result

    result['edgesEgo'] = []
    result['nodesAlters'] = []
    result['edgesAlters'] = []
    result['nodes2nd'] = []
    result['edges2nd'] = []
    
    result['altersTeam'] = []
    result['altersVs'] = []

    result['nodesEgo'] = {"id": summonerId, "value": 30, "label": result['custId']}

    alters = set(result['alters'])
    remainingAlters = alters.copy()
    components = list([a] for a in alters)
    stored2ndLevel = set()
    missingAlters = dict()
    

    for alterId in alters:
        alterInfo = result['alters'][alterId]

        teamCount = len(alterInfo['team'])
        vsCount = len(alterInfo['vs'])
        if teamCount:
            result['altersTeam'].append(alterId)
            result['edgesEgo'].append({"from": summonerId, "to": alterId, "value": teamCount, "title": teamCount, "color": "0000FF"})
        if vsCount:
            result['altersVs'].append(alterId)
            result['edgesEgo'].append({"from": summonerId, "to": alterId, "value": vsCount, "title": vsCount, "color": "FF0000"})

        if alterId not in ids:
            result['nodesAlters'].append({"id": alterId, "value": 10, "label": alterInfo['name'] if len(alterInfo['name']) < 9 else alterInfo['name'][:7] + '...'})
            for match in alterInfo['team']:
                missingAlters.setdefault(match, {'team': [], 'vs': []})['team'].append(alterId)
            for match in alterInfo['vs']:
                missingAlters.setdefault(match, {'team': [], 'vs': []})['vs'].append(alterId)
            continue
        
        remainingAlters.remove(alterId)
        alter = get_alter(alterId)

        result['nodesAlters'].append({"id": alterId, "value": 20 if 'custId' in alter else 10, "label": alter['custId'] if 'custId' in alter else alterInfo['name'] if len(alterInfo['name']) < 9 else alterInfo['name'][:7] + '...'})
        
        merged = [sublist for sublist in components for a in sublist if a in set(alter['alters'])]
        excl = [sublist for sublist in components if sublist not in merged]
        components = excl + [list(set(element for sublist in merged for element in sublist))]

        commonAlterIds = set(alter['alters']) & remainingAlters

        for alterAlterId in commonAlterIds:
            matchInfo = alter['alters'][alterAlterId]
            #result['alterTies'][str((alterId, alterAlterId))] = {key:matchInfo[key] for key in matchInfo if key == 'team' or key == 'vs'}
            
            teamCount = len(matchInfo['team'])
            vsCount = len(matchInfo['vs'])
            if teamCount:
                result['edgesAlters'].append({"from": alterId, "to": alterAlterId, "value": teamCount, "title": teamCount, "color": "0000FF"})
            if vsCount:
                result['edgesAlters'].append({"from": alterId, "to": alterAlterId, "value": vsCount, "title": vsCount, "color": "FF0000"})

        alters2ndLevel = set(alter['alters']) - alters
        if summonerId in alters2ndLevel:
            alters2ndLevel.remove(summonerId)

        for alter2ndLevelId in alters2ndLevel:
            matchInfo = alter['alters'][alter2ndLevelId]
            if alter2ndLevelId not in stored2ndLevel:
                result['nodes2nd'].append({"id": alter2ndLevelId, "value": 5, "label": matchInfo['name'] if len(matchInfo['name']) < 9 else matchInfo['name'][:7] + '...'})
                stored2ndLevel.add(alter2ndLevelId)
            
            teamCount = len(matchInfo['team'])
            vsCount = len(matchInfo['vs'])
            if teamCount:
                result['edges2nd'].append({"from": alterId, "to": alter2ndLevelId, "value": teamCount, "title": teamCount, "color": "0000FF"})
            if vsCount:
                result['edges2nd'].append({"from": alterId, "to": alter2ndLevelId, "value": vsCount, "title": vsCount, "color": "FF0000"})

    coopMatches = []
    vsMatches = []
    for matchId, match in missingAlters.items():
        match['team'].sort()
        match['vs'].sort()
        for pair in itertools.combinations(match['team'], 2):
            coopMatches.append(pair)
        for pair in itertools.combinations(match['vs'], 2):
            coopMatches.append(pair)
        for id1 in match['team']:
            for id2 in match['vs']:
                vsPlayers = [id1, id2]
                vsPlayers.sort()
                vsMatches.append(tuple(vsPlayers))
        merged = [sublist for sublist in components for a in sublist if a in set(match['team'] + match['vs'])]
        excl = [sublist for sublist in components if sublist not in merged]
        components = excl + [list(set(element for sublist in merged for element in sublist))]
    
    for playerTuple in set(coopMatches):
        result['edgesAlters'].append({"from": playerTuple[0], "to": playerTuple[1], "value": coopMatches.count(playerTuple), "title": coopMatches.count(playerTuple), "color": "0000FF"})
    for playerTuple in set(vsMatches):
        result['edgesAlters'].append({"from": playerTuple[0], "to": playerTuple[1], "value": vsMatches.count(playerTuple), "title": vsMatches.count(playerTuple), "color": "FF0000"})

    numberOfAlters = len(alters) # = Degree
    numberOfTies = len(result['edgesAlters'])
    meanTieStrength = sum(edge['value'] for edge in result['edgesEgo']) / len(result['edgesEgo'])
    density = numberOfTies / (numberOfAlters * (numberOfAlters - 1))
    componentRatio = (len(components) - 1) / (numberOfAlters - 1)
    fragmentationIndex = 1 - sum(len(component) * (len(component) - 1) for component in components) / (numberOfAlters * (numberOfAlters - 1))

    result["network"] = {"Degree": numberOfAlters, "Mean Tie Strength": meanTieStrength, "Density": density, "Components": len(components), "Component Ratio": componentRatio, "Fragmentation Index": fragmentationIndex}

    save_result(resultFile, result)
    return result

# %% [markdown]
# ### Get Ego by Summoner ID
# 
# Processes the summoner ID and delegates to the _Get Ego by PUUID_ method.

# %%
def get_ego_by_summonerId(summonerId):
    return get_ego_by_puuid(ids[summonerId].split("/")[1])    


# %%
results = []
internalIdDict = {}
with open(ROOT_DIRPATH + "egomatchnumbers.pickle", 'rb') as f:
    for puuid, alterNumber in pickle.load(f):
        if alterNumber > 0:
            print(alterNumber)
            ego = get_ego_by_puuid(puuid)
            if 'surveyData' in ego:
                internalIdDict[ego['custId']] = puuid
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
    pickle.dump(internalIdDict, f, pickle.HIGHEST_PROTOCOL)
