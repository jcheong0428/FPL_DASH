#!/usr/bin/env python
import subprocess
import os
import glob
import pandas as pd

############# Clone the repo. #############
try:
    cmd = "git submodule add https://github.com/vaastav/Fantasy-Premier-League Fantasy-Premier-League"
    subprocess.call(cmd, shell=True)
except:
    pass

try:
    cmd = "git submodule update --recursive"
    subprocess.call(cmd, shell=True)
except:
    pass

############# Preprocess the player data. #############
cwd = 'Fantasy-Premier-League/data/2020-21/'
df = pd.read_csv(os.path.join(cwd, 'players_raw.csv'))
player_idlist = pd.read_csv(os.path.join(cwd, "player_idlist.csv"))
output_file = 'latest_gw.csv'
if os.path.exists(output_file):
    os.remove(output_file)

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