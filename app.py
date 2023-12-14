# app.py

import pandas as pd
from dash import Dash, dcc, html
from functions import set_countries_alpha, clean_olympics

data = (
    pd.read_csv("olympic_games.csv")
)

data = clean_olympics(data)
data = set_countries_alpha(data, "country")

app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(children="Avocado Analytics"),
        html.P(
            children=(
                "Analyze the behavior of avocado prices and the number"
                " of avocados sold in the US between 2015 and 2018"
            ),
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data["host_country"],
                        "y": data["year"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "Average Price of Avocados"},
            },
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data["host_country"],
                        "y": data["games_type"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "Avocados Sold"},
            },
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": data["host_city"],
                        "y": data["games_type"],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "Avocados solded"},
            },
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
