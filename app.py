#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd, numpy as np 
import os, glob, subprocess
from tabs import tab1_table
from tabs import tab2_scatter
from tabs import tab3_about
from firebase import firebase
from utils import TABLE_COLUMNS, latest_stats

firebase = firebase.FirebaseApplication('https://fpldash-bbf95-default-rtdb.firebaseio.com/', None)

######## Load the data ########
cwd = 'Fantasy-Premier-League/data/2020-21/'
all_players_raw = pd.read_csv(os.path.join(cwd, 'players_raw.csv'))
# for position
element_type_dict = {1:"GK", 2:"DEF", 3:"MID", 4:"FWD"}
all_players_raw["Position"] = all_players_raw['element_type'].apply(lambda x: element_type_dict[x])

# latest_gw
output_file = 'latest_gw.csv'
all_gw = pd.read_csv(output_file)
latest_round = np.sort(all_gw['round'].unique())[-1]

# understat
understat = pd.read_csv("understat_player.csv", engine="python")
understat.fplid = understat.fplid.astype(str)

df = latest_stats(weeks=6, sort_by="threat", func_name = "sum", understat=understat)

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

    <!-- Default Statcounter code for fpldash
    http://www.fpldash.com -->
    <script type="text/javascript">
    var sc_project=12475179; 
    var sc_invisible=1; 
    var sc_security="6533ba56"; 
    </script>
    <script type="text/javascript"
    src="https://www.statcounter.com/counter/counter.js"
    async></script>
    <noscript><div class="statcounter"><a title="Web Analytics"
    href="https://statcounter.com/" target="_blank"><img
    class="statcounter"
    src="https://c.statcounter.com/12475179/0/6533ba56/1/"
    alt="Web Analytics"></a></div></noscript>
    <!-- End of Statcounter Code -->
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
                dbc.Tab(label="About", tab_id="about"),
            ],
            id="tabs",
            active_tab="table",
        ),
        html.Div(id="tab-content", className="p-4"),
        
        html.Hr(),
        html.Footer([
            html.Div(f"Latest up to 2020-21 GW {latest_round}", id="last-update"),
            html.A("Data from vaastav", href="https://github.com/vaastav/Fantasy-Premier-League", className="text-dark", style={"float": "right", "margin-right": "30px", "vertical-align": "middle"}),
            html.A("Created by Jin", href="http://jinhyuncheong.com", className="text-dark", style={"float": "right", "margin-right": "30px", "vertical-align": "middle"}),
            html.A("Contribute", href="https://github.com/jcheong0428/FPL_DASH", className="text-dark", style={"float": "right", "margin-right": "30px", "vertical-align": "middle"}),
        ], id="footer", className="justify-content-center text-center", style={"background-color": "rgba(0, 0, 0, 0.2)"})
    ]
)

@app.callback(
    Output('table-content', 'children'),
    [Input('tab1-slider', 'value'),
    Input('tab1-method', 'value'), 
    ])
def update_table(value, method):
    df = latest_stats(weeks=value, sort_by="total_points", func_name = method, understat=understat)
    table.data = df[TABLE_COLUMNS].to_dict('records')
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
        elif active_tab == "about":
            return tab3_about.tab_3_layout
    return "No tab selected"

@app.callback(
    Output('player-graph', 'figure'),
    [Input('xaxis-column', 'value'),
    Input('yaxis-column', 'value'), 
    Input('tab2-slider', 'value'),
    Input('tab2-method', 'value'),],
)
def update_graph(xaxis_column_name, yaxis_column_name, value, method):
    df = latest_stats(weeks=value, sort_by="total_points", func_name = method, understat=understat)
    df = df[TABLE_COLUMNS]
    fig = px.scatter(df, 
                    x=xaxis_column_name,
                    y=yaxis_column_name,
                    hover_name='Player Name',
                    color="Position",
                    trendline="ols",
                    text="Player Name"
                    )
    fig.update_traces(textposition='top left')
    return fig

@app.callback([Output('thankyou-box', 'style'), Output('feedback-box', 'style')],
              Input('feedback-button', 'n_clicks'),
              State('message', 'value'))
def display_confirm(n, msg):
    if n is not None:
        firebase.post("/feedback", {"msg": msg})
        return [{"display": "block"}, {"display": "none"}]
    return [{"display": "none"}, {"display": "block"}]

ON_HEROKU = os.environ.get('ON_HEROKU')
if ON_HEROKU:
    # get the heroku port
    port = int(os.environ.get('PORT', 17995))  # as per OP comments default is 17995
else:
    port = 5000

if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0", port=port)