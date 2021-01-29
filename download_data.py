#!/usr/bin/env python
import subprocess
import os
import glob
import pandas as pd, numpy as np

############# Clone the repo. #############
try:
    print("Fetching submodule")
    cmd = "git clone https://github.com/vaastav/Fantasy-Premier-League"
    subprocess.call(cmd, shell=True)
except:
    pass

############# Preprocess the player data. #############
cwd = 'Fantasy-Premier-League/data/2020-21/'
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

latest_gw = pd.read_csv(output_file)
last_gw = np.sort(latest_gw['round'].unique())[-1]
print(np.sort(latest_gw['round'].unique()))
print(f"Recent up to GW: {last_gw}")