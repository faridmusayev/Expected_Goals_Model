# import required libraries
import os
import pandas as pd

#%%

# Find ids and corresponding names of ligue 1 teams
from socceraction.data.wyscout import PublicWyscoutLoader 

# load public wyscout data
wyscout_data = PublicWyscoutLoader()

# France 17/18, competition_id = 412, season_id = 181189
ligue1_games = wyscout_data.games(competition_id = 412, season_id = 181189)["game_id"]

# find all team data from games
l1_team_names = pd.DataFrame()
for i in ligue1_games:
    df = wyscout_data.teams(i)
    l1_team_names = pd.concat([l1_team_names, df])
    
#%%

# retrieve unique team data using 'groupby' 
l1_team_names = l1_team_names.groupby(by = ['team_id', 'team_name_short', 'team_name']) \
    .count().reset_index()
    
#%%

l1_team_names.loc[l1_team_names['team_id'] == 3782, 'team_name_short'] = 'Saint Etienne'

#%%

# save as .csv file
l1_team_names.to_csv('data/ligue1/team_names.csv', index = False)

#%%

# list all ligue 1 games in directory
ligue1_games = os.listdir('ligue1_game_players')
all_l1_games = pd.DataFrame()
for i in ligue1_games:
    game = pd.read_csv('ligue1_game_players/' + i)
    all_l1_games = pd.concat([all_l1_games, game])

#%%

# retrieve unique player data using 'groupby'
l1_player_names = all_l1_games.groupby(by = ['player_id', 'nickname']).count() \
.reset_index().loc[:, ('player_id', 'nickname')]

# save as .csv file
l1_player_names.to_csv('data/ligue1/player_names.csv', index = False)





