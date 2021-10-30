#!/usr/bin/env python
import subprocess
import os
import glob
import pandas as pd, numpy as np
from utils import latest_stats

"""
This script preprocesses the data. 
- combine player data into one file. 
- prints last updated gameweek. 
- add fpl player id to understat data. 
"""

############# Preprocess the player data. #############
cwd = 'Fantasy-Premier-League/data/2021-22/'
df = pd.read_csv(os.path.join(cwd, 'players_raw.csv'))
player_idlist = pd.read_csv(os.path.join(cwd, "player_idlist.csv"))
output_file = 'latest_gw.csv'
if os.path.exists(output_file):
    print("Found existing latest gw file. removing...")
    os.remove(output_file)
    print("Removing complete")

print("Filtering data...")
player_gw_files = glob.glob(os.path.join(cwd, 'players/*/gw.csv'))
latest_gw = pd.DataFrame()
for player_gw in player_gw_files:
  player_id = player_gw.split('/')[-2].split('_')[-1]
  _gw = pd.read_csv(player_gw)
  _gw['id'] = player_id
  if not os.path.exists(output_file):
    _gw.to_csv(output_file, mode='w', index=False, header=True)
  else:
    _gw.to_csv(output_file, mode='a', index=False, header=False)
print("Filtering complete.")

################## Connect FPL and understat data ##############
all_gw = pd.read_csv(output_file)
last_gw = np.sort(all_gw['round'].unique())[-1]
print(np.sort(all_gw['round'].unique()))
print(f"Recent up to GW: {last_gw}")

df = latest_stats(weeks=6, sort_by="threat", func_name = "sum", gw= all_gw, preprocess=True)
teams = pd.read_csv(os.path.join(cwd, "teams.csv"))

understat_path = os.path.join(cwd, "understat/understat_player.csv")
understat = pd.read_csv(understat_path, engine="python")

replace_list = [("Romain Saiss", "Romain Saïss"),
                ("Ahmed Elmohamady", "Ahmed El Mohamady"),
                ("Emile Smith-Rowe", "Emile Smith Rowe"),
                ("Jack O&#039;Connell", "Jack O'Connell"),
                ("Daniel N&#039;Lundulu", "Daniel N'Lundulu"),
                ("Franck Zambo", "André-Frank	Zambo Anguissa"),
                ("Rodrigo", "Rodrigo Moreno"),
                ("Rodri", "Rodrigo Hernandez")]
for (usname,fplname) in replace_list:
  understat.replace(usname, fplname, inplace=True)

understat_to_fplid = {660: "395"} # Ben Davies at TOT
for rowix, row in understat.iterrows(): 
  player_name = row.player_name
  understat_id = int(row.id)

  try:
    first_name, second_name = player_name.split(" ")
  except:
    try: 
      first_name = player_name.split(" ")[0]
      second_name = " ".join(player_name.split(" ")[1:])
    except:
      print("UNDERSTAT WRONG")

  # match names
  try: 
    # try second names
    matched = matched = df.query("`Player Name` == @second_name")
    assert(len(matched)==1)
    understat_to_fplid[understat_id] = matched.id.values[0]
  except:
    try:
      # Try first name
      matched = df.query("`Player Name` == @first_name")
      assert(len(matched)==1)
      understat_to_fplid[understat_id] = matched.id.values[0]
    except:
      try: 
        # match both names 
        matched = df.query("first_name==@first_name and second_name==@second_name")
        assert(len(matched)==1)
        understat_to_fplid[understat_id] = matched.id.values[0]
      except:
        try: 
          # match webname = first + last name
          matched = df.query("`Player Name` == @first_name+' '+@second_name")
          assert(len(matched)==1)
          understat_to_fplid[understat_id] = matched.id.values[0]
        except:
          # match firstname[0] and secondname[-1]
          try: 
            matched = df.query("(first_name.str.contains(@first_name)) and (second_name.str.contains(@second_name))", engine="python")
            assert(len(matched)==1)
            understat_to_fplid[understat_id] = matched.id.values[0]
          except:
            try:
              # match firstnames 
              matched = df.query("(first_name.str.contains(@first_name))", engine="python")
              assert(len(matched)==1)
              understat_to_fplid[understat_id] = matched.id.values[0]
            except:
              print("player not connected", player_name, first_name, second_name)

understat['fplid'] = understat.id.map(understat_to_fplid)
understat['xG90'] = understat['xG']/(understat['time']/90)
understat['npxG90'] = understat['npxG']/(understat['time']/90)
understat['xA90'] = understat['xA']/(understat['time']/90)

understat.to_csv("understat_player.csv", index=False)
print("FPL to Understat connection success.")