import pandas as pd
import plotly.graph_objs as go
from twitch import TwitchClient
from twitch.helix.api import TwitchHelix

def return_figures():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing plotly visualizations

    """
###################### CHART 1 ########################
    # initialize client
    client_id='o77c1kh7o8s52pt3dtzj8xaypu0699'
    client = TwitchClient(client_id=client_id)
    
    # use client to query games (returns top 10 by default)
    games = client.games.get_top()
    
    # parse returned structure for vars
    game_results = []
    game_images = []
    for game in games:
        game_results.append((game['game']['name'], game['viewers'], game['channels']))
        game_images.append(game['game']['box']['medium'])
        
     # convert values to plotly format
    x = [i[0] for i in game_results]
    y1_vals = [i[1] for i in game_results]
    y2_vals = [i[2] for i in game_results]
    y2_max = max(y2_vals)
    
    # Develop Viewing and Streaming plot
    trace1 = go.Bar(
        x=x,
        y=y1_vals,
        offset=-.1,
        width = .5,
        name='Viewers',
        marker=dict(
            color='rgb(55, 83, 109)'
        )
    )
    trace2 = go.Bar(
        x=x,
        y=y2_vals,
        name='Streamers',
        yaxis='y2',
        offset = .1,
        width = .5,
        marker=dict(
            color='rgb(158, 88, 201)'
        )
    )

    trace_one = [trace1, trace2]

    layout_one = go.Layout(
        title="Top 10 games on Twitch",
        barmode='group',
        yaxis=dict(
            title='Viewers'),
        yaxis2=dict(
            title='Streamers',
            overlaying='y',
            side='right',
            range=[0, y2_max*1.2],
            tickfont=dict(
                color='rgb(158, 88, 201)'
            )),
        legend=dict(x=.85, y=1.1)
    )

################################### CHART 2 ################################

    helixclient = TwitchHelix(client_id = client_id)
    n_streams = 10
    streams = helixclient.get_streams(page_size=n_streams)

    stream_results = []
    for i in range(n_streams):
        stream_results.append((streams[i]['user_name'], streams[i]['game_id'], streams[i]['viewer_count']))

    # Query API for games by ID
    game_ids = []
    for game_id in [i[1] for i in stream_results]:
        if game_id != '':
            game_ids.append(game_id)
    game_id_response = helixclient.get_games(game_ids)

    # transform reponse into simple dictionary mapping
    game_id_mapping = dict()
    for i in range(len(game_id_response)):
        game_id_mapping[game_id_response[i]['id']] = game_id_response[i]['name']
    game_id_mapping

    # create new stream results from game_id mapping
    streams_with_games = []

    for i in stream_results:
        if i[1] in game_id_mapping:
            streams_with_games.append([i[0], game_id_mapping[i[1]], i[2]])
        else:
            streams_with_games.append([i[0], 'N/A', i[2]])
            
    # Getting games with helix does not show viewers. Use v5
    games_25 = client.games.get_top(limit = 25)

    # Transform output
    games_25_results = []

    for game in games_25:
        games_25_results.append([game['game']['name'], game['viewers']])

    # lump together bottom 15
    other_games = ['other_games', 0]
    for game in games_25_results[10:]:
        other_games[1] += game[1]

    sankey_games = games_25_results[:10]
    sankey_games.append(other_games)
            
    # replace any top 10 streamer not playing a top 10 game with "other_games"

    top_10_games = [x[0] for x in sankey_games[:10]]
    for stream in streams_with_games:
        if stream[1] not in top_10_games:
            stream[1] = 'other_games'

    row = []
    for game in sankey_games:
        for stream in streams_with_games:
            if stream[1] == game[0]:
                game[1]-=stream[2]
                #          source    target     value
                row.append([game[0], stream[0], stream[2]])
        row.append([game[0], 'other_streamers', game[1]])        
       
    source_0 = [x[0] for x in row]
    target_0 = [x[1] for x in row]
    value = [x[2] for x in row]

    labels = list(set(source_0)) + list(set(target_0))

    source = [0]*len(source_0)
    target = [0]*len(target_0)

    for i in range(len(source)):
        source[i] = labels.index(source_0[i])

    for i in range(len(target)):
        target[i] = labels.index(target_0[i])
            
    # Build Plot
    data_two = dict(
        type='sankey',
        node = dict(
          pad = 15,
          thickness = 20,
          line = dict(
            color = "black",
            width = 0.5
          ),
          label = labels,
          color = []
        ),
        link = dict(
          source = source,
          target = target,
          value = value
      ))

    layout_two =  dict(
        title = "Game Viewership by Streamer<br>Considering top 25 Games",
        font = dict(
          size = 10
        )
    )
    
    # append all charts to the figures list
    figures = []
    figures.append(dict(data=trace_one, layout=layout_one))
    figures.append(dict(data=[data_two], layout=layout_two))
    #figures.append(dict(data=graph_three, layout=layout_three))
    #figures.append(dict(data=graph_four, layout=layout_four))

    return figures