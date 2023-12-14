# app.py

import pandas as pd
from dash import Dash, dcc, html
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
        html.H1(children='Hello Dash'),

        html.Div(children='''
            Dash: A web application framework for Python.
        '''),

        dcc.Graph(
            id='graph2',
            figure=fig2
        ),  
    ]),
])

app.run_server(debug=True)
