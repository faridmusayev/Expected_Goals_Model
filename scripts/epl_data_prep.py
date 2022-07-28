# libraries
import ast
import numpy as np
import pandas as pd
from socceraction.data.wyscout import PublicWyscoutLoader 

# load public wyscout data
wyscout_data = PublicWyscoutLoader()

# England 17/18, competition_id = 364, season_id = 181150
epl_games = wyscout_data.games(competition_id = 364, season_id = 181150)["game_id"]

# download all premier league matches and save as a single .csv
events = pd.DataFrame()
for i in epl_games:
    df = wyscout_data.events(i)
    events = pd.concat([events, df])

# save as .csv file
events.to_csv('data/epl/events.csv', index = False)

# upload 'events' dataframe that includes all events of all 380 EPL games
df = pd.read_csv('data/epl/events.csv')

# remove columns 'event id' and 'milliseconds'
rm_col_ind = np.r_[0, 3]
df = df.drop(columns = df.columns[rm_col_ind])

# convert strings into python lists
df['tags'] = df['tags'].apply(ast.literal_eval)
df['positions'] = df['positions'].apply(ast.literal_eval)

# make 'type_name' and 'subtype_name' columns lowercase 
df['type_name'] = df['type_name'].str.lower()
df['subtype_name'] = df['subtype_name'].str.lower()

# create separate initial(start) and final(end) coordinates from 'positions' column
# if action has only 'start' coordinates set 'end' coordinates to 'nan'
df['x_start'] = df['positions'].apply(lambda x: x[0]['x'])
df['y_start'] = df['positions'].apply(lambda x: x[0]['y'])
df['x_end'] = df['positions'].apply(lambda x: x[1]['x'] if len(x) == 2 else np.nan)
df['y_end'] = df['positions'].apply(lambda x: x[1]['y'] if len(x) == 2  else np.nan) 

# import tags for encode subevents in event data
tags = pd.read_csv('data/wyscout_tags.csv', sep = ';')

# make all descriptions lowercase
tags['Description'] = tags['Description'].str.lower()

# transform tags data frame into dictionary
tags = dict(zip(tags['Tag'], tags['Description']))

# use dictionaries and list comprehensions to convert tags into tag ids and their descriptions 
df['tag_id'] = df['tags'].apply(lambda x: [value for d in x for value in d.values()])
df['tag_name'] = df['tag_id'].apply(lambda x: [tags[i] for i in x])

# drop redundant column 'positions'
df.drop(columns = ['positions', 'tags'], inplace = True)

# rearrange columns using only required indices and passing them into np.r_
rearr_cols = np.r_[0:8, 12, 13, 8:12]
df = df.iloc[:, rearr_cols]

# save 'df' as 'refined_events.csv' dataframe
df.to_csv('data/epl/refined_events.csv', index = False)

# free kicks are not included (penalties are also part of free kicks)
shots = df[df['type_name'] == 'shot']    

# save 'df' as 'refined_events.csv' dataframe
shots.to_csv('data/epl/shots.csv', index = False)    