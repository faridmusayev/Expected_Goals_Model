# import required libraries
import os
import pandas as pd

#%%

# Find ids and corresponding names of bundsliga teams
from socceraction.data.wyscout import PublicWyscoutLoader 

# load public wyscout data
wyscout_data = PublicWyscoutLoader()

# Germany 17/18, competition_id = 426, season_id = 181137
bundesliga_games = wyscout_data.games(competition_id = 426, season_id = 181137)["game_id"]

# find all team data from games
bl_team_names = pd.DataFrame()
for i in bundesliga_games:
    df = wyscout_data.teams(i)
    bl_team_names = pd.concat([bl_team_names, df])
    
#%%

# retrieve unique team data using 'groupby' 
bl_team_names = bl_team_names.groupby(by = ['team_id', 'team_name_short', 'team_name']) \
    .count().reset_index()
#%%

# rename Bayern Munich
bl_team_names.loc[bl_team_names['team_id'] == 2444, 'team_name_short'] = 'Bayern Munich'
bl_team_names.loc[bl_team_names['team_id'] == 2444, 'team_name'] = 'Bayern Munich'

# rename Köln
bl_team_names.loc[bl_team_names['team_id'] == 2463, 'team_name_short'] = 'Köln'
bl_team_names.loc[bl_team_names['team_id'] == 2463, 'team_name'] = 'Köln'

# save as .csv file
bl_team_names.to_csv('data/bundesliga/team_names.csv', index = False)
    
#%%

# list all bundesliga games in directory
bundesliga_games = os.listdir('bundesliga_game_players')
all_bl_games = pd.DataFrame()
for i in bundesliga_games:
    game = pd.read_csv('bundesliga_game_players/' + i)
    all_bl_games = pd.concat([all_bl_games, game])
    
#%%

# retrieve unique player data using 'groupby'
bl_player_names = all_bl_games.groupby(by = ['player_id', 'nickname']).count() \
.reset_index().loc[:, ('player_id', 'nickname')]

# save as .csv file
bl_player_names.to_csv('data/bundesliga/player_names.csv', index = False)






