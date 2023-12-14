# app.py

import pandas as pd
from dash import Dash, dcc, html, Input, Output, callback
import functions

data = (
    pd.read_csv("olympic_games.csv")
)

# Change names to iso names
data = functions.set_country_names(data)
# Grab iso codes
data = functions.clean_olympics(data)
data = functions.set_countries_alpha(data, "country")
# Make a new column with total amount of medals per row
data = functions.set_olympic_medals(data)

fig = functions.bar_distribution_maker(data)
fig2 = functions.pie_plot_medals(data)

app = Dash(__name__)

markdown_text = '''
### Dash and Markdown

Dash apps can be written in Markdown.
Dash uses the [CommonMark](http://commonmark.org/)
specification of Markdown.
Check out their [60 Second Markdown Tutorial](http://commonmark.org/help/)
if this is your first introduction to Markdown!
'''

app.layout = html.Div(children=[
    # All elements from the top of the page
    html.Div([
        html.H1(children='Hello Dash'),

        html.Div(children='''
            Dash: A web application framework for Python.
        '''),

        dcc.Graph(
            id='graph1',
            figure=fig
        ),  
    ]),
    # New Div for all elements in the new 'row' of the page
    html.Div([
        html.H1(children='Hello Dash', style={'textAlign': 'center', 'color': '#7FDBFF'}),

        html.Div(children='''
            Dash: A web application framework for Python.
        '''),
        dcc.RadioItems(
                ['Overall', 'Summer', 'Winter'],
                'Overall',
                id='game-type',
                inline=True
            ),

        dcc.Graph(
            id='graph2'
        ),  
    ]),
    dcc.Markdown(children=markdown_text)
])

@callback(
    Output('graph2', 'figure'),
    Input('game-type', 'value'))
def update_graph(game_type):
    if game_type == "Overall":
        game_type = None
    fig = functions.make_geo_map(data, game_type)

    return fig

app.run_server(debug=True)
