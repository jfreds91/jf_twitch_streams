import pandas as pd
import plotly.graph_objs as go
from twitch import TwitchClient
from twitch.helix.api import TwitchHelix
from wrangling_scripts.twitch_api_funcs import get_top_games, get_top_streams

def return_figures():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing plotly visualizations

    """
###################### CHART 1 ########################
    # call api module function
    plot1_df = get_top_games()
    
    # convert to plotly format
    x = plot1_df['game'].values.tolist()
    y1_vals = plot1_df['viewers'].values.tolist()
    y2_vals = plot1_df['streams'].values.tolist()
    y2_max = max(y2_vals)
    
    # plotly functions
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
    # call api module functions
    streams_with_games = get_top_streams()
    games_25 = get_top_games(limit=25)

    # get sum of bottom 25 games' viewers
    bottom_views = games_25.iloc[10:]['viewers'].sum()
    bottom_streams = games_25.iloc[10:]['streams'].sum()
    # create df with top 10 games: viewers + other_games (15 games):viewers
    sankey_games = games_25[:10]
    other_df = pd.DataFrame([[sankey_games.iloc[0]['time'], 'other_games', bottom_views, bottom_streams]], columns=sankey_games.columns.tolist())
    sankey_games = sankey_games.append(other_df)

    # create top 10 list
    top_10_games = sankey_games.iloc[:10]['game'].values.tolist()
    # replace any top 10 streamer not playing a top 10 game with other_games
    streams_with_games.loc[~streams_with_games['game'].isin(top_10_games), 'game'] = 'other_games'

    # transform final list
    sankey_games_l = sankey_games.values.tolist()
    streams_with_games_l = streams_with_games.values.tolist()

    row = []
    for game in sankey_games_l:
        for stream in streams_with_games_l:
            if stream[2] == game[1]:
                game[2]-=stream[3]
                #          source    target     value
                row.append([game[1], stream[1], stream[3]])
        row.append([game[1], 'other_streamers', game[2]])

    # transform lists for plotly
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