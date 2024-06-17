import os
import pandas as pd
import sys
sys.path.append(".")

def readChoicesData():
    parent_folder = './output/keyResults/SimulationSet_240608_1607/independent'

    columns_to_extract = [
        'player_1', 'player_2', 'player_3', 'player_4', 'player_5', 
        'player_6', 'player_7', 'player_8', 'player_9', 'player_10',
        'player_11', 'player_12', 'player_13', 'player_14', 'player_15', 
        'player_16', 'player_17', 'player_18', 'player_19', 'player_20',
        'player_21', 'player_22', 'player_23', 'player_24'
    ]

    players_values = []

    for subdir, _, files in os.walk(parent_folder):
        for file in files:
            if file == 'overview.csv':
                file_path = os.path.join(subdir, file)
                df = pd.read_csv(file_path)
                players_values.extend(df.iloc[0][columns_to_extract].tolist())

    print(players_values)
    return players_values
