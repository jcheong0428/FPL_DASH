import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

tab_3_layout = jumbotron = dbc.Jumbotron(
    [
        html.H1("FPL DASH", className="display-3"),
        html.P(
            "FPL DASH provides YOU the ability to explore Fantasy Premier League data.",
            className="lead",
        ),
        html.Hr(className="my-2"),
        html.P(
            ["Analyze player metrics for the last 3 gameweeks or the last 6."]
        ),
        html.P(
            ["Run quick regressions to see what metrics correlate with goals scored or total points."]
        ),
        # html.P(dbc.Button("Start exploring", color="primary", id="ExploreButton"), className="lead"),
    ]
)