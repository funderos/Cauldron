# Preparing psychological Data (Survey)
# A range of psychological data from players that act as egos in this project has been evaluated in the summer of 2018 is available in CSV format.
# The paper Motivational Profiling of League of Legends Players and information about data can be found at: https://osf.io/ue82s/
# The CSV file available for download does only contain ananonymized subset of the original collected data. A full data CSV file as well as the final motivational profiles in a separate CSV file have been provided for this project.

# Imports & Filepaths
# The CSV files will be imported in Python using _pandas_, converted to a Python dictionary and dumped in a Pickle file. Therefore, the corresponding Python imports as well as the import and export filepaths get specified first:
import configparser
import pandas
import pickle

config = configparser.ConfigParser()
config.read('task_config.ini')

rootDir = config['GENERAL']['ROOT']
importFileFull = rootDir + config['SURVEY']['FULL_CSV']
importFileProfiles = rootDir + config['SURVEY']['PROFILE_CSV']
exportFile = rootDir + config['SURVEY']['COMBINED']

# Importing the CSV files with the Pandas Library
# For reading in the full data CSV, the column and decimal delimiters have to be specified as the CSV follows German formatting. The internal ID will be specified as index for linking the motivational profile data in the next step.
# Also, most attributes (columns) will be omitted as we are are only interested in mean values besides age, gender and the unencrypted summoner ID retrieved from the API which will be used as key for linking the data with the new data retrieved in 2019 and 2020.

full_df = pandas.read_csv(
    filepath_or_buffer=importFileFull,
    delimiter=';',
    decimal=',',
    index_col='id',
    usecols=[
        'id','Age','Gender','mean_AMO','mean_EXT','mean_INJ','mean_IDE','mean_INT','mean_IMO',
        'api_summonerID_unranked','mean_IMI_enj','mean_IMI_tens','PANAS_score_PA','PANAS_score_NA','mean_PENS_rel','mean_PENS_com','mean_PENS_aut',
        'mean_ACH_GOAL_perf_ap','mean_ACH_GOAL_perf_av','mean_ACH_GOAL_mast_ap','mean_ACH_GOAL_mast_av','mean_Vitality','mean_PASSION_hp','mean_PASSION_op'
        ]
    )

# For this CSV, we only specify the id as index for joining the resulting dataframe with the full data object we created beforehand. No additional arguments are required as the CSV is already correctly formatted.
profile_df = pandas.read_csv(filepath_or_buffer=importFileProfiles, index_col='id')

# At last, the dataframes are joined, the summoner Id is set as the new index and the resulting Pandas dataframe object will be converted to a Python dictionary which gets dumped to the export filepath via Pickle.
result_df = pandas.concat([full_df, profile_df], axis=1)
result_df = result_df.reset_index().set_index('api_summonerID_unranked')

playerEntries = result_df.to_dict('index')

with open(exportFile, 'wb') as f:
    pickle.dump(playerEntries, f, pickle.HIGHEST_PROTOCOL)
