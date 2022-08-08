# import required libraries
import os
import pandas as pd

#%%

# Find ids and corresponding names of laliga teams
from socceraction.data.wyscout import PublicWyscoutLoader 

# load public wyscout data
wyscout_data = PublicWyscoutLoader()

# Spain 17/18, competition_id = 795, season_id = 181144
laliga_games = wyscout_data.games(competition_id = 795, season_id = 181144)["game_id"]

# find all team data from games
ll_team_names = pd.DataFrame()
for i in laliga_games:
    df = wyscout_data.teams(i)
    ll_team_names = pd.concat([ll_team_names, df])
    
#%%

# retrieve unique team data using 'groupby' 
ll_team_names = ll_team_names.groupby(by = ['team_id', 'team_name_short', 'team_name']) \
    .count().reset_index()

#%%

ll_team_names.loc[ll_team_names['team_id'] == 677, 'team_name_short'] = 'Deportivo La Coruna'
ll_team_names.loc[ll_team_names['team_id'] == 679, 'team_name_short'] = 'Atletico Madrid'
ll_team_names.loc[ll_team_names['team_id'] == 683, 'team_name_short'] = 'Malaga'
ll_team_names.loc[ll_team_names['team_id'] == 696, 'team_name_short'] = 'Deportivo Alaves'
ll_team_names.loc[ll_team_names['team_id'] == 712, 'team_name_short'] = 'Leganes'

#%%

# save as .csv file
ll_team_names.to_csv('data/laliga/team_names.csv', index = False)

#%%

# list all laliga games in directory
laliga_games = os.listdir('laliga_game_players')
all_ll_games = pd.DataFrame()
for i in laliga_games:
    game = pd.read_csv('laliga_game_players/' + i)
    all_ll_games = pd.concat([all_ll_games, game])

    
#%%

# retrieve unique player data using 'groupby'
ll_player_names = all_ll_games.groupby(by = ['player_id', 'nickname']).count() \
.reset_index().loc[:, ('player_id', 'nickname')]

# save as .csv file
ll_player_names.to_csv('data/laliga/player_names.csv', index = False)
    
    
    
    
    

