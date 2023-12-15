# app.py

import pandas as pd
from dash import Dash, dcc, html, Input, Output, callback
import functions

# load the data
data = (
    pd.read_csv("olympic_games.csv")
)

# Data cleaning and reshaping
data = functions.set_country_names(data)
data = functions.clean_olympics(data)
data = functions.set_countries_alpha(data, "country")
data = functions.set_olympic_medals(data)

# Initialize the app - incorporate a Dash Bootstrap theme
app = Dash(__name__)

# Custom variables
title = '''
# Olympic Games Dashboard
Countries and medals from 1896 to 2022
'''

credits = '''
Made by Kristoffer Kuvaja Adolfsson, Vizual Analytics 2023
'''
RadioButtons = ['All', 'Summer', 'Winter']

# dash app layout, plain and simple html elements

app.layout = html.Div(children=[
    dcc.Markdown(children=title, style={'textAlign': 'center'}),
    # top div
    html.Div([
        # Distribution of athletes, teams and competitions
        html.Div([
            dcc.Graph(id='other_distributions'),
            "Pick Olympic Games type",
            dcc.RadioItems(
                RadioButtons,
                'Summer',
                id='distributions-game-type',
                inline=True
            ),
            dcc.RangeSlider(
                data['year'].min(),
                data['year'].max(),
                value=[data['year'].min(), data['year'].max()],
                marks=None,
                tooltip={"placement": "bottom",
                         "always_visible": True},
                id='year-slider'
            )
        ], style={'width': '32%', 'display': 'inline-block', }),
        # Times hosted by country
        html.Div([
            dcc.Graph(
                id='host-country',
                figure=functions.host_by_country(data)
            ),
        ], style={'width': '26%', 'display': 'inline-block'}),
        # Summer / Winter distribution
        html.Div([
            dcc.Graph(
                id='summer-winter-games',
                figure=functions.summer_winter_games(data)
            ),
        ], style={'width': '14%', 'display': 'inline-block'}),
        # Medals by country
        html.Div([
            dcc.Dropdown(
                data['country'].unique(),
                value="Finland",
                id='country-select-1'
            ),            dcc.Graph(
                id='country-1'
            ),
        ], style={'width': '14%', 'display': 'inline-block'})
    ]),
    # bottom div
    html.Div([
        # Geo map
        html.Div([
            html.H1(children='World map, medals per country',
                    style={'textAlign': 'center'}),
            html.Div(children='''
            Pick Olympic Games type and update the year using the options below
        ''', style={'textAlign': 'center'}),
            dcc.Graph(
                id='geo_map'
            ),
            dcc.RadioItems(
                RadioButtons,
                'All',
                id='geo-game-type',
                inline=True,
                style={'textAlign': 'center'}),
            dcc.RangeSlider(
                data['year'].min(),
                data['year'].max(),
                value=[data['year'].min(), data['year'].max()],
                marks=None,
                tooltip={"placement": "bottom", "always_visible": True},
                id='geo-year-slider'
            )], style={'width': '50%', 'margin-left': '25%'}),

    ]),
    dcc.Markdown(children=credits, style={'textAlign': 'center'})
])

# dash callback functions for making figures
@callback(
    Output('country-1', 'figure'),
    Input('country-select-1', 'value'))
def update_country_1(country):
    fig = functions.pie_plot_medals(data, country=country)
    fig['layout']['uirevision'] = 'Do not change'
    return fig


@callback(
    Output('other_distributions', 'figure'),
    Input('year-slider', 'value'),
    Input('distributions-game-type', 'value'))
def update_other_distributions(selected_years, game_type):
    fig = functions.bar_distribution_maker(
        data, selected_years=selected_years, game_type=game_type)
    fig['layout']['uirevision'] = 'Do not change'
    return fig


@callback(
    Output('geo_map', 'figure'),
    Input('geo-game-type', 'value'),
    Input('geo-year-slider', 'value'))
def update_geo_map(game_type, selected_years):
    if game_type == "Overall":
        game_type = None
    fig = functions.make_geo_map(data, selected_years, game_type)
    fig['layout']['uirevision'] = 'Do not change'
    return fig


# run the app
app.run_server(debug=True)
