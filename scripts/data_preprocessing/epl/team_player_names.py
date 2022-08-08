# import required libraries
import os
import pandas as pd

#%%

# Find ids and corresponding names of epl teams
from socceraction.data.wyscout import PublicWyscoutLoader 

# load public wyscout data
wyscout_data = PublicWyscoutLoader()

# England 17/18, competition_id = 364, season_id = 181150
epl_games = wyscout_data.games(competition_id = 364, season_id = 181150)["game_id"]

# find all team data from games
epl_team_names = pd.DataFrame()
for i in epl_games:
    df = wyscout_data.teams(i)
    epl_team_names = pd.concat([epl_team_names, df])

#%%

# retrieve unique team data using 'groupby' 
epl_team_names = epl_team_names.groupby(by = ['team_id', 'team_name_short', 'team_name']) \
    .count().reset_index()

# save as .csv file
epl_team_names.to_csv('data/epl/team_names.csv', index = False)

#%%

# list all epl games in directory
epl_games = os.listdir('epl_game_players')
all_epl_games = pd.DataFrame()
for i in epl_games:
    game = pd.read_csv('epl_game_players/' + i)
    all_epl_games = pd.concat([all_epl_games, game])

#%%

# retrieve unique player data using 'groupby'
epl_player_names = all_epl_games.groupby(by = ['player_id', 'nickname']).count() \
.reset_index().loc[:, ('player_id', 'nickname')]

# save as .csv file
epl_player_names.to_csv('data/epl/player_names.csv', index = False)









