import pandas as pd
import plotly.graph_objs as go
from twitch import TwitchClient

# Use this file to read in your data and prepare the plotly visualizations. The path to the data files are in
# `data/file_name.csv`

def return_data():
    # initialize client
    client  = TwitchClient(client_id='o77c1kh7o8s52pt3dtzj8xaypu0699')
    
    # use client to query games (returns top 10 by default)
    games = client.games.get_top()
    
    # parse returned structure for vars
    game_results = []
    game_images = []
    for game in games:
        game_results.append((game['game']['name'], game['viewers'], game['channels']))
        game_images.append(game['game']['box']['medium'])

    return game_results


def return_figures():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """

    # initialize client
    client  = TwitchClient(client_id='o77c1kh7o8s52pt3dtzj8xaypu0699')
    
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

    trace_data = [trace1, trace2]

    layout_data = go.Layout(
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
        legend=dict(x=-.1, y=1.1)
    )

    # a line chart
    graph_one = []    
    graph_one.append(
      go.Scatter(
      x = [0, 1, 2, 3, 4, 5],
      y = [0, 2, 4, 6, 8, 10],
      mode = 'lines'
      )
    )

    layout_one = dict(title = 'Chart One',
                xaxis = dict(title = 'x-axis label'),
                yaxis = dict(title = 'y-axis label'),
                )

# second chart plots ararble land for 2015 as a bar chart    
    graph_two = []

    graph_two.append(
      go.Bar(
      x = ['a', 'b', 'c', 'd', 'e'],
      y = [12, 9, 7, 5, 1],
      )
    )

    layout_two = dict(title = 'Chart Two',
                xaxis = dict(title = 'x-axis label',),
                yaxis = dict(title = 'y-axis label'),
                )


# third chart plots percent of population that is rural from 1990 to 2015
    graph_three = []
    graph_three.append(
      go.Scatter(
      x = [5, 4, 3, 2, 1, 0],
      y = [0, 2, 4, 6, 8, 10],
      mode = 'lines'
      )
    )

    layout_three = dict(title = 'Chart Three',
                xaxis = dict(title = 'x-axis label'),
                yaxis = dict(title = 'y-axis label')
                       )
    
# fourth chart shows rural population vs arable land
    graph_four = []
    
    graph_four.append(
      go.Scatter(
      x = [20, 40, 60, 80],
      y = [10, 20, 30, 40],
      mode = 'markers'
      )
    )

    layout_four = dict(title = 'Chart Four',
                xaxis = dict(title = 'x-axis label'),
                yaxis = dict(title = 'y-axis label'),
                )
    
    # append all charts to the figures list
    figures = []
    figures.append(dict(data=trace_data, layout=layout_data)
    #figures.append(dict(data=graph_one, layout=layout_one))
    #figures.append(dict(data=graph_two, layout=layout_two))
    #figures.append(dict(data=graph_three, layout=layout_three))
    #figures.append(dict(data=graph_four, layout=layout_four))

    return figures