import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd, numpy as np 
import os, glob, subprocess

tab_1_layout = html.Div([
                html.Div([
                    dbc.Col([
                        html.P("Choose aggregation method: "),
                        ], className="col-4"),

                    dbc.Col([            
                        dcc.Dropdown(
                            id='tab1-method',
                            options=[
                                {'label': 'Average', 'value': 'average'},
                                {'label': 'Sum', 'value': 'sum'}
                            ],
                            value='sum',
                            clearable=False,
                        ),
                    ], className="col-6"),
                ], className="row"),
                html.Div([
                    dbc.Col([  
                        html.P("Choose weeks to average over: "),
                    ], className="col-4"),
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
                    ], className="col-6"),
                ], className="row"),
                html.Div(id="table-content", className="p-4")
            ])