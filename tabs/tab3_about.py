import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

tab_3_layout = html.Div( 
    [dbc.Jumbotron(
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
            html.Hr(),
            html.Br(),
            html.Br(),
            # html.P(dbc.Button("Start exploring", color="primary", id="ExploreButton"), className="lead"),
            dbc.Row(
                dbc.Col(
                    html.Div([
                        html.P(
                            "We always value your feedback & suggestions to improve FPL DASH.",
                            className="lead",
                        ),
                        dbc.Textarea(
                            valid=True,
                            bs_size="sm",
                            className="mb-3",
                            placeholder="Let us know what you'd like to see.",
                        ),
                        html.Div(
                            [dbc.Button("Send", id="feedback-button", className="mr-2", color="success"),],
                            style={"float": "right"}
                        ),
                    ], id='feedback-box'), width={"size": 8, "offset": 2}
                )
            ),            
            dbc.Row(
                dbc.Col(
                    html.Div([
                        html.P(
                            "Thank you for your feedback.",
                            className="lead",
                        ),
                    ], id="thankyou-box"), 
                    width={"size": 8, "offset": 2}
                )
            ),
        ]),

    ])