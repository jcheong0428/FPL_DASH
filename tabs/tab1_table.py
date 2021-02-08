import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd, numpy as np 
import os, glob, subprocess

tab_1_layout = html.Div([
                dbc.Row([
                    dbc.Col([
                        html.P("Choose aggregation method: "),
                        ], className="descriptions", width={"size": 4, "offset": 1}
                    ),
                    dbc.Col([            
                        dcc.Dropdown(
                            id='tab1-method',
                            options=[
                                {'label': 'Average', 'value': 'average'},
                                {'label': 'Sum', 'value': 'sum'}
                            ],
                            value='sum',
                            clearable=False,
                        )], width={"size": 6},
                    )
                ]),
                dbc.Row([
                    dbc.Col([  
                        html.P("Choose weeks to average over: "),
                       ], className="descriptions", width={"size": 4, "offset": 1}
                       ),
                    dbc.Col([  
                        dcc.Slider(
                            id='tab1-slider',
                            min=1,
                            max=12,
                            step=1,
                            value=3,
                            marks={
                                1: '1',
                                2: '2',
                                3: '3',
                                4: '4',
                                5: '5',
                                6: '6',
                                7: '7',
                                8: '8',
                                9: '9',
                                10: '10',
                                11: '11',
                                12: '12',
                            },
                            className="custom-slider"
                        ),
                    ], width={"size": 6}),
                ]),
                dcc.Loading(
                    id="loading",
                    type="default",
                    children=html.Div(id="table-content", className="p-4")
                ),
                html.Br(),
                html.Br(),
                html.Div([
                    html.P("xG, xA, shots, key passes, npg, npxG, xG Chain, xG Buildup are always estimated for the entire season.")
                    ], id="disclaimer", className="disclaimer")
            ])