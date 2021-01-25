#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd, numpy as np 
import os, glob, subprocess

######## Load the data ########
cwd = 'Fantasy-Premier-League/data/2020-21/'
all_players_raw = pd.read_csv(os.path.join(cwd, 'players_raw.csv'))

output_file = 'latest_gw.csv'
all_gw = pd.read_csv(output_file)

def latest_stats(weeks=6, sort_by="threat", func_name="sum", gw=all_gw, df=all_players_raw):
    """Retrieve the latest gw stats. 

    Avg: 
        gw: Gameweek data. 
        weeks: Number of weeks
        sort_by: column name
        func_name: (average, median, sum)

    Returns:
        latest_gw 
    """
    func_dict = {"average": np.mean, 
            "median": np.median, 
            "sum": np.sum}
    latest_gw = np.sort(gw['round'].unique())[-(weeks-1):]
    latest_gw = gw.query("round >= @latest_gw[0] and round < = @latest_gw[-1]")
    latest_gw = latest_gw.groupby("id").apply(func_dict[func_name]).sort_values(by=sort_by, ascending=False)
    latest_gw.index = latest_gw.index.astype(str).map(dict(zip(df.id.astype(str), df.web_name)))
    latest_gw = latest_gw.drop(columns=['id'])
    latest_gw = latest_gw.reset_index().rename(columns={latest_gw.index.name:'Player Name'})
    latest_gw = latest_gw[['Player Name', 'total_points', 'goals_scored', 'assists', 'bonus', 'influence', 'creativity', 'threat', 'ict_index', 'minutes', 'clean_sheets', 'saves']].round(decimals=0)
    return latest_gw

df = latest_stats(weeks=6, sort_by="threat", func_name = "sum")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# app.layout = dash_table.DataTable(
table = dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict('records'),

    page_size=30,
    
    sort_action='native',

    style_table={'overflowX': 'auto'},
    style_cell={
        # 'height': '16px',
        # all three widths are needed
        # 'minWidth': '25px', 'width': '140px', 'maxWidth': '180px',
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
        # 'whiteSpace': 'normal'
    }
)

# https://dash-bootstrap-components.opensource.faculty.ai/examples/graphs-in-tabs/
app.layout = dbc.Container(
    [
        dcc.Store(id="store"),
        html.H1("FPL Latest N-weeks Average Dashboard"),
        html.Hr(),
        html.Div([
            dbc.Col([
                html.P("Choose aggregation method: "),
                ], className="col-4"),

            dbc.Col([            
                dcc.Dropdown(
                    id='method',
                    options=[
                        {'label': 'Average', 'value': 'average'},
                        {'label': 'Median', 'value': 'median'},
                        {'label': 'Sum', 'value': 'sum'}
                    ],
                    value='sum',
                    clearable=False,
                ),
            ], className="col-6"),
            dbc.Col([  
            html.Div(id='dd-output-container', style={'display': 'none'})
            ]),
        ], className="row"),
        html.Div([
            dbc.Col([  
                html.P("Choose weeks to average over: "),
            ], className="col-4"),
            dbc.Col([  
                dcc.Slider(
                    id='slider',
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
            dbc.Col([  
                html.Div(id='slider-output-container', style={'display': 'none'})
            ]),
        ], className="row"),
        dbc.Tabs(
            [
                dbc.Tab(label="Latest FPL Data", tab_id="scatter"),
                # dbc.Tab(label="Histograms", tab_id="histogram"),
            ],
            id="tabs",
            active_tab="scatter",
        ),
        html.Div(id="tab-content", className="p-4"),
    ]
)

@app.callback(
    dash.dependencies.Output('tab-content', 'children'),
    [dash.dependencies.Input('slider', 'value'),
    dash.dependencies.Input('method', 'value'), 
    ])
def update_table(value, method):
    df = latest_stats(weeks=value, sort_by="total_points", func_name = method)
    table = dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),

        page_size=30,
        
        sort_action='native',

        style_table={'overflowX': 'auto'},
        style_cell={
            # 'height': '16px',
            # all three widths are needed
            'minWidth': '25px', 'width': '140px', 'maxWidth': '180px',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            # 'whiteSpace': 'normal'
        }
        )
    return table

@app.callback(
    dash.dependencies.Output('slider-output-container', 'children'),
    [dash.dependencies.Input('slider', 'value')])
def update_slider_output(value):
    return 'You have selected "{}"'.format(value)

@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('method', 'value')])
def update_dd_output(value):
    return 'You have selected "{}"'.format(value)

# @app.callback(
#     [dash.dependencies.Output('tab-content', 'children'), dash.dependencies.Output('slider-output-container', 'children')],
#     [dash.dependencies.Input('my-slider', 'value')])
# def update_output(value):
#     df = latest_stats(weeks=value, sort_by="threat", func_name = "sum")
#     table = dash_table.DataTable(
#         id='table',
#         columns=[{"name": i, "id": i} for i in df.columns],
#         data=df.to_dict('records'),

#         page_size=30,
        
#         sort_action='native',

#         style_table={'overflowX': 'auto'},
#         style_cell={
#             # 'height': '16px',
#             # all three widths are needed
#             'minWidth': '25px', 'width': '140px', 'maxWidth': '180px',
#             'overflow': 'hidden',
#             'textOverflow': 'ellipsis',
#             # 'whiteSpace': 'normal'
#         }
#     )
#     return table, 'You have selected "{}"'.format(value)


# @app.callback(
#     Output("tab-content", "children"),
#     [Input("tabs", "active_tab")],
# )
# def render_tab_content(active_tab):
#     """
#     This callback takes the 'active_tab' property as input, as well as the
#     stored graphs, and renders the tab content depending on what the value of
#     'active_tab' is.
#     """
#     if active_tab is not None:
#         if active_tab == "scatter":
#             return table
#         elif active_tab == "histogram":
#             return dbc.Row(
#                 [
#                     table
#                 ]
#             )
#     return "No tab selected"

# # assume you have a "long-form" data frame
# # see https://plotly.com/python/px-arguments/ for more options
# df = pd.DataFrame({
#     "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#     "Amount": [4, 1, 2, 2, 4, 5],
#     "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
# })

# fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

# app.layout = html.Div(children=[
#     html.H1(children='Hello Dash'),

#     html.Div(children='''
#         Dash: A web application framework for Python.
#     '''),

#     dcc.Graph(
#         id='example-graph',
#         figure=fig
#     )
# ])

if __name__ == '__main__':
    app.run_server(debug=True
    , host="localhost"
    )