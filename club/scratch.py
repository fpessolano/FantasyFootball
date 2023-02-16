# experiment file

import pandas as pd
import unidecode
import player as pl

fifa_data = pd.read_csv('../assets/FIFA21_official_data.csv')
# print(fifa_data.info())
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#     print(fifa_data.loc[86])

remove_columns = [
  "Photo", "Flag", "Club Logo", "Body Type", "Real Face", "Position", "Club"
]
unicode_translation = ["Name", "Club"]

chelsea = pd.DataFrame(
  fifa_data.loc[fifa_data["Club"] == "Chelsea"]).sort_values('Jersey Number',
                                                             ascending=True)
# chelsea['Growth'] = chelsea['Potential'] - chelsea['Overall']

team = {}
for _, player in chelsea.iterrows():
  #print(player)
  player_redux = {}
  for col, value in player.items():
    if col in unicode_translation:
      player_redux[col] = unidecode.unidecode(value)
    elif col not in remove_columns:
      player_redux[col] = value
  team[int(player["Jersey Number"])] = player_redux

Kepa = pl.Player(team[1])
# print(Kepa.stats())
null_kepa = Kepa + Kepa
print(null_kepa.stats())
