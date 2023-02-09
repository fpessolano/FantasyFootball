# experiment file

import pandas as pd
import unidecode

fifa_data = pd.read_csv('../assets/FIFA21_official_data.csv')
# print(fifa_data.info())
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#     print(fifa_data.loc[86])

remove_columns = ["Photo", "Flag", "Club Logo", "Body Type", "Real Face", "Position", "Club"]
unicode_translation = ["Name", "Club"]

chelsea = pd.DataFrame(fifa_data.loc[fifa_data["Club"] == "Chelsea"]).sort_values('Jersey Number', ascending=True)
chelsea['Growth'] = chelsea['Potential'] - chelsea['Overall']

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

print(team)

# above extraction is useless. best use df instead of dict


# columns = [
#   'Name', 'Age', 'Nationality', 'Overall', 'Potential', 'Skill Moves',
#   'Work Rate', 'Special', 'Position'
# ]
# chelsea = pd.DataFrame(fifa_data.loc[fifa_data["Club"] == "Chelsea"],
#                        columns=columns)
# chelsea['Growth'] = chelsea['Potential'] - chelsea['Overall']
# print(chelsea.describe())
# chelsea = chelsea.sort_values('Growth', ascending=False)
# print(chelsea.sort_values('Growth', ascending=False).head())
# print()
# print(chelsea.sort_values('Overall', ascending=False)['Name'])
# print()

# arsenal = pd.DataFrame(fifa_data.loc[fifa_data["Club"] == "Arsenal"],
#                        columns=columns)
# arsenal['Growth'] = arsenal['Potential'] - arsenal['Overall']
# print(arsenal.sort_values('Growth', ascending=False).head())
# print()
# print(arsenal.sort_values('Overall', ascending=False).head())
# print(arsenal["Position"])
# print()

