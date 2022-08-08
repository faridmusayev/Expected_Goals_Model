# import required libraries
import os
import pandas as pd

#%%

# Find ids and corresponding names of serie a teams
from socceraction.data.wyscout import PublicWyscoutLoader 

# load public wyscout data
wyscout_data = PublicWyscoutLoader()

# Italy 17/18, competition_id = 524, season_id = 181248
seriea_games = wyscout_data.games(competition_id = 524, season_id = 181248)["game_id"]

# find all team data from games
sa_team_names = pd.DataFrame()
for i in seriea_games:
    df = wyscout_data.teams(i)
    sa_team_names = pd.concat([sa_team_names, df])
    
#%%

# retrieve unique team data using 'groupby' 
sa_team_names = sa_team_names.groupby(by = ['team_id', 'team_name_short', 'team_name']) \
    .count().reset_index()

#%%

# save as .csv file
sa_team_names.to_csv('data/seriea/team_names.csv', index = False)

#%%

# list all serie a games in directory
seriea_games = os.listdir('seriea_game_players/')
all_sa_games = pd.DataFrame()
for i in seriea_games:
    game = pd.read_csv('seriea_game_players/' + i)
    all_sa_games = pd.concat([all_sa_games, game])

#%%

# retrieve unique player data using 'groupby'
sa_player_names = all_sa_games.groupby(by = ['player_id', 'nickname']).count() \
.reset_index().loc[:, ('player_id', 'nickname')]
#%%

# save as .csv file
sa_player_names.to_csv('data/seriea/player_names.csv', index = False)




