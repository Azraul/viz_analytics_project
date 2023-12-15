# app.py

import dash_bootstrap_components as dbc
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


RadioButtons = ['All', 'Summer', 'Winter']

# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CYBORG]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# app = Dash(__name__)

markdown_text = '''Made by Kristoffer Kuvaja Adolfsson, Vizual Analytics 2023'''


app.layout = html.Div(children=[
    # Distribution of athletes, teams and competitions
    html.Div([
        html.Div([
            # Summer / Winter distribution
            dcc.Graph(
                id='host-country',
                figure=functions.host_by_country(data)
            ),
        ], style={'width': '26%', 'display': 'inline-block'}),
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
                tooltip={"placement": "bottom", "always_visible": True},
                id='year-slider'
            )
        ], style={'width': '32%', 'display': 'inline-block', }),
        html.Div([
            dcc.Graph(
                id='summer-winter-games',
                figure=functions.summer_winter_games(data)
            ),
        ], style={'width': '14%', 'display': 'inline-block'}),
        html.Div([

            dcc.Dropdown(
                data['country'].unique(),
                value="Finland",
                id='country-select-1'
            ),            dcc.Graph(
                id='country-1'
            ),
        ], style={'width': '14%', 'display': 'inline-block'})]),
    # Geo map
    html.Div([
        html.H1(children='World map, medals per country',
                style={'textAlign': 'center'}),

        html.Div(children='''
            Pick Olympic Games type and update the year using the options below
        ''', style={'textAlign': 'center'}),
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
        )], style={'width': '50%', 'margin-left':'25%'}),
    html.Div([
        dcc.Graph(
            id='geo_map'
        ),
    ]),
    dcc.Markdown(children=markdown_text, style={'textAlign': 'center'})
])


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


app.run_server(debug=True)
