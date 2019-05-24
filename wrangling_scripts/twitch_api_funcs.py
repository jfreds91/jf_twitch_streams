from twitch import TwitchClient
from twitch.helix.api import TwitchHelix

import pandas as pd
import datetime
import time

client_id = 'o77c1kh7o8s52pt3dtzj8xaypu0699'


def get_v5(client_id = client_id):
    return TwitchClient(client_id=client_id)


def get_helix(client_id = client_id):
    return TwitchHelix(client_id = client_id)
    

def get_top_games(v5_client = get_v5(), limit = 10):
    '''
    Gets top 10 games' viewer and stream count
    INPUTS:
        v5_client: twitch v5 client
        limit (int): number of records to return
    RETURNS:
        df (DataFrame): dataframe containing timestamped results
    '''
    
    curr_timestamp = datetime.datetime.now()
    
    top_games = v5_client.games.get_top(limit = limit)
    game_results = []
    for game in top_games:
        game_results.append((curr_timestamp, game['game']['name'], game['viewers'], game['channels']))
    df = pd.DataFrame(game_results, columns=['time', 'game', 'viewers', 'streams'])
    
    return df


def get_top_streams(helix_client = get_helix(), v5_client = get_v5(), n_streams = 10):
    '''
    Gets top streamers and what games they are playing
    
    INPUTS:
        v5_client: twitch v5 client
        helix_client: twitch helix client
        n_streams (int): how many streamers to return
        
    RETURNS:
        df (DataFrame): dataframe containing top 10 streamers and what games they are playing
    '''
    
    curr_timestamp = datetime.datetime.now()
    
    stream_results = []
    streams = helix_client.get_streams(page_size=n_streams)
    for i in range(n_streams):
        stream_results.append((curr_timestamp, streams[i]['user_name'], streams[i]['game_id'], streams[i]['viewer_count']))
    
    # Query API for games by ID
    game_ids = []
    for game_id in [i[2] for i in stream_results]: # cleans existing game_ids
        if game_id != '':
            game_ids.append(game_id)
    game_id_response = helix_client.get_games(game_ids) # returns list of games by ids
    
    # transform reponse into simple dictionary mapping
    game_id_mapping = dict()
    for i in range(len(game_id_response)):
        game_id_mapping[game_id_response[i]['id']] = game_id_response[i]['name']
        
    # create new stream results from game_id mapping
    streams_with_games = []

    for i in stream_results:
        if i[2] in game_id_mapping:
            streams_with_games.append([i[0], i[1], game_id_mapping[i[2]], i[3]])
        else:
            streams_with_games.append([i[0], i[1], 'N/A', i[3]])
            
    # convert to df
    df = pd.DataFrame(streams_with_games, columns=['time', 'streamer', 'game', 'viewers'])
    return df