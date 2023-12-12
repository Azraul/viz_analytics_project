# app.py

import pandas as pd
from dash import Dash, dcc, html

data = (
    pd.read_csv("olympic_games.csv")
)

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
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)