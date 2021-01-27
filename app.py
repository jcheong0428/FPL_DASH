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
from tabs import tab1_table
from tabs import tab2_scatter

######## Load the data ########
cwd = 'Fantasy-Premier-League/data/2020-21/'
all_players_raw = pd.read_csv(os.path.join(cwd, 'players_raw.csv'))
# for position
element_type_dict = {1:"GK", 2:"DEF", 3:"MID", 4:"FWD"}
all_players_raw["Position"] = all_players_raw['element_type'].apply(lambda x: element_type_dict[x])

output_file = 'latest_gw.csv'
all_gw = pd.read_csv(output_file)

# for value
value_dict = {}
for id in all_gw.id.unique():
  value_dict[str(id)] = all_gw.query("id==@id").sort_values(by='round').iloc[-1].value/10

def latest_stats(weeks=6, sort_by="threat", func_name="sum", gw=all_gw, df=all_players_raw, value_dict=value_dict):
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
    latest_gw_list = np.sort(gw['round'].unique())[-weeks:]
    latest_gw = gw.query("round >= @latest_gw_list[0] and round < = @latest_gw_list[-1]")
    latest_gw = latest_gw.groupby("id").apply(func_dict[func_name]).sort_values(by=sort_by, ascending=False)
    latest_gw['value'] = latest_gw.index.astype(str).map(value_dict)
    latest_gw['Player Name'] = latest_gw.index.astype(str).map(dict(zip(df.id.astype(str), df.web_name)))
    latest_gw['Position'] = latest_gw.index.astype(str).map(dict(zip(df.id.astype(str), df.Position)))
    latest_gw = latest_gw.reset_index(drop=True)
    latest_gw = latest_gw[['Player Name', 'Position', 'total_points', 'minutes', 'goals_scored', 'assists', 'bonus', 'influence', 'creativity', 'threat', 'ict_index', 'clean_sheets', 'saves', 'value']].round(decimals=1)
    # for col in ['influence', 'creativity', 'threat', 'ict_index', 'value']:
    #     latest_gw[col] = latest_gw[col].map('{:.1f}'.format)
    return latest_gw

df = latest_stats(weeks=6, sort_by="threat", func_name = "sum")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX, "custom.css"])
app.config['suppress_callback_exceptions'] = True

server = app.server
app.title = "FPL DASH"
app.index_string = """<!DOCTYPE html>
<html>
    <head>
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-RQ02DDS4VZ"></script>
        <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());

        gtag('config', 'G-RQ02DDS4VZ');
        </script>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>"""

table = dash_table.DataTable(
    id='table',
    columns=[{"name": i.replace("_", " "), "id": i} for i in df.columns],
    data=df.to_dict('records'),

    page_size=30,
    
    sort_action='native',
    filter_action='native',
    style_table={'overflowX': 'auto'},
    style_cell={
        'height': 'auto',
        # all three widths are needed
        'minWidth': '60px', 'width': 'auto', 'maxWidth': '120px',
        'overflow': 'hidden',
        'textOverflow': 'ellipsis',
        'whiteSpace': 'normal'
    }
)

# https://dash-bootstrap-components.opensource.faculty.ai/examples/graphs-in-tabs/
app.layout = dbc.Container(
    [
        dcc.Store(id="store"),
        html.H1("FPL Latest N-weeks Average Dashboard"),
        html.Hr(),
        dbc.Tabs(
            children = [
                dbc.Tab(label="Latest FPL Data", tab_id="table"),
                dbc.Tab(label="Graph", tab_id="scatter"),
            ],
            id="tabs",
            active_tab="table",
        ),
        html.Div(id="tab-content", className="p-4"),
        html.Hr(),
        html.Footer([
            html.A("Data from vaastav", href="https://github.com/vaastav/Fantasy-Premier-League", className="text-dark", style={"float": "right", "margin-right": "30px", "vertical-align": "middle"}),
            html.A("Created by Jin", href="http://jinhyuncheong.com", className="text-dark", style={"float": "right", "margin-right": "30px", "vertical-align": "middle"}),
        ], id="footer", className="justify-content-center text-center", style={"background-color": "rgba(0, 0, 0, 0.2)"})
    ]
)

@app.callback(
    Output('table-content', 'children'),
    [Input('tab1-slider', 'value'),
    Input('tab1-method', 'value'), 
    ])
def update_table(value, method):
    df = latest_stats(weeks=value, sort_by="total_points", func_name = method)
    table.data = df.to_dict('records')
    return table 

@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab")],
)
def render_tab_content(active_tab):
    """
    This callback takes the 'active_tab' propert`y as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    if active_tab is not None:
        if active_tab == "table":
            return tab1_table.tab_1_layout
        elif active_tab == "scatter":
            return tab2_scatter.tab_2_layout
    return "No tab selected"

@app.callback(
    Output('player-graph', 'figure'),
    [Input('xaxis-column', 'value'),
    Input('yaxis-column', 'value'), 
    Input('tab2-slider', 'value'),
    Input('tab2-method', 'value'),],
)
def update_graph(xaxis_column_name, yaxis_column_name, value, method):
    df = latest_stats(weeks=value, sort_by="total_points", func_name = method)
    fig = px.scatter(df, 
                    x=xaxis_column_name,
                    y=yaxis_column_name,
                    hover_name='Player Name',
                    color="Position",
                    trendline="ols"
                    )
    fig.data[1].line.color = 'red'
    return fig

if __name__ == '__main__':
    app.run_server(debug=True
    , host="localhost"
    )