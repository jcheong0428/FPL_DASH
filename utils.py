import numpy as np
import pandas as pd
import os, glob

FPL_COLUMNS = ['Player Name', 'Position', 'team', 'total_points', 'minutes', 'goals_scored', 'assists', 'bonus', 'influence', 'creativity', 'threat', 'ict_index', 'clean_sheets', 'saves', 'value']
UNDERSTAT_COLUMNS = ['xG', 'xG90', 'xA', 'xA90', 'shots', 'key_passes', 'npg', 'npxG', 'npxG90','xGChain', 'xGBuildup']
TABLE_COLUMNS = FPL_COLUMNS + UNDERSTAT_COLUMNS
TABLE_EXTENDED_COLUMNS = FPL_COLUMNS + UNDERSTAT_COLUMNS + [c+'90' for c in ['goals_scored', 'assists', 'attacking_return']] +['minutes_to_attacking_return']


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

# for value
value_dict = {}
for id in all_gw.id.unique():
  value_dict[str(id)] = all_gw.query("id==@id").sort_values(by='round').iloc[-1].value/10

# teams
teams = pd.read_csv(os.path.join(cwd, "teams.csv"))

# understat
understat_path = os.path.join(cwd, "understat/understat_player.csv")
understat = pd.read_csv(understat_path, engine="python")

def latest_stats(weeks=6, sort_by="threat", func_name="sum", gw=all_gw, df=all_players_raw, teams = teams, value_dict=value_dict, understat = understat, preprocess=False, divide_minutes=True):
    """Retrieve the latest gw stats. 

    Arg: 
        weeks: Number of gameweeks to average. 
        sort_by: column name
        func_name: (average, median, sum)
        gw: Gameweek data.
        df:  all player data from vaastav FPL repo
        teams: team information data
        value_dict: latest player value data. 
        understat: understat df
        preprocess: whether to include first_name, second_name to match with understat data. 
        divide_minutes: whether to provide data/minutes data. 
    Returns:
        latest_gw 
    """
    func_dict = {"average": np.mean, "median": np.median, "sum": np.sum}
    latest_gw_list = np.sort(gw['round'].unique())[-weeks:]
    latest_gw = gw.query("round >= @latest_gw_list[0] and round < = @latest_gw_list[-1]")
    latest_gw = latest_gw.groupby("id").apply(func_dict[func_name]).sort_values(by=sort_by, ascending=False)
    # merge with latest value
    latest_gw['value'] = latest_gw.index.astype(str).map(value_dict)
    # merge player name
    latest_gw['Player Name'] = latest_gw.index.astype(str).map(dict(zip(df.id.astype(str), df.web_name)))
    if preprocess:
        latest_gw['first_name'] = latest_gw.index.astype(str).map(dict(zip(df.id.astype(str), df.first_name)))
        latest_gw['second_name'] = latest_gw.index.astype(str).map(dict(zip(df.id.astype(str), df.second_name)))
    # merge team
    latest_gw['team_code'] = latest_gw.index.astype(str).map(dict(zip(all_players_raw.id.astype(str), all_players_raw.team_code.astype(str))))
    latest_gw['team'] = latest_gw.team_code.map(dict(zip(teams.code.astype(str), teams.short_name.astype(str))))
    # merge position
    latest_gw['Position'] = latest_gw.index.astype(str).map(dict(zip(df.id.astype(str), df.Position)))
    latest_gw['id'] = latest_gw.index.astype(str)
    latest_gw = latest_gw.reset_index(drop=True)
    # # merge with understat
    if not preprocess:
        understat.fplid = understat.fplid.astype(str)
        latest_gw = latest_gw.merge(understat[UNDERSTAT_COLUMNS+['fplid']], how="inner", left_on="id", right_on="fplid")[TABLE_COLUMNS]
    if divide_minutes:
        for col in ['goals_scored', 'assists']:
            latest_gw[col+'90'] = latest_gw[col].astype(float) / (latest_gw['minutes']/90)
        latest_gw['attacking_return90'] = (latest_gw['goals_scored'] + latest_gw['assists']) / (latest_gw['minutes']/90)
        latest_gw['minutes_to_attacking_return'] = latest_gw['minutes'] / (latest_gw['goals_scored'] + latest_gw['assists'])
    return latest_gw.round(decimals=1)