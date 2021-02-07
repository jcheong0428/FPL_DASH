import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

available_indicators = ['total_points', 'minutes', 'goals_scored', 'assists', 'bonus', 'influence', 'creativity', 'threat', 'ict_index', 'clean_sheets', 'saves', 'value', 'xG', 'xA', 'xG90', 'xA90', 'shots', 'key_passes', 'npg', 'npxG', 'npxG90', 'xGChain', 'xGBuildup']

tab_2_layout = html.Div([
    html.H1('Graph'),
    html.Div([
        html.P("Y axis"),
        dcc.RadioItems(
            id='yaxis-column',
            options=[{'label': i, 'value': i} for i in available_indicators],
            value='total_points',
            labelClassName='radioButtons'
        ),
        ], style={'width': '40%', 'display': 'inline-block'}),
    html.Div([
        html.P("X axis"),
        dcc.RadioItems(
            id='xaxis-column',
            options=[{'label': i, 'value': i} for i in available_indicators],
            value='minutes',
            labelClassName='radioButtons'
        ),
        ],style={'width': '40%', 'float': 'right', 'display': 'inline-block'}),
    html.Div([
        dbc.Col([
            html.P("Choose aggregation method: "),
            ], className="col-4"),

        dbc.Col([            
            dcc.Dropdown(
                id='tab2-method',
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
                id='tab2-slider',
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
            ),
        ], className="col-6"),
    ], className="row"),
    html.Div(
        dbc.Row([
            dbc.Col([
                dcc.Graph(id="player-graph" ),
            ])
        ])
    ),
    html.Br(),
    html.Br(),
    html.Div([
        html.P("xG, xA, shots, key passes, npg, npxG, xG Chain, xG Buildup are always estimated for the entire season.")
        ], id="disclaimer", className="disclaimer")
])