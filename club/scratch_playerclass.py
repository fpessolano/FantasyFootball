# experiment file

import pandas as pd
# import unidecode
import own_player as opl

# df = pd.read_csv('../assets/stats.csv')

# print(list(set(df.columns.values)))
# print(list(set(df["work rate"])))

# player = df.loc[[6]]
# player = opl.OwnPlayer(player)
# print(player.mental)
# print(player.ball_skills)
# player.adjust_to_match_action(90)
# print()
# print(player.ball_skills)

# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#     print(fifa_data.loc[86])

# remove_columns = [
#   "Photo", "Flag", "Club Logo", "Body Type", "Real Face", "Position", "Club"
# ]
# unicode_translation = ["Name", "Club"]

# chelsea = pd.DataFrame(
#   fifa_data.loc[fifa_data["Club"] == "Chelsea"]).sort_values('Jersey Number',
#                                                              ascending=True)
# chelsea['Growth'] = chelsea['Potential'] - chelsea['Overall']

# team = {}
# for _, player in chelsea.iterrows():
#   #print(player)
#   player_redux = {}
#   for col, value in player.items():
#     if col in unicode_translation:
#       player_redux[col] = unidecode.unidecode(value)
#     elif col not in remove_columns:
#       player_redux[col] = value
#   team[int(player["Jersey Number"])] = player_redux

# Kepa = pl.Player(team[1])
# print(Kepa.stats())
# null_kepa = Kepa + Kepa
# print(null_kepa.stats())

df = pd.read_csv('../assets/stats.csv')

player = df.loc[[6]]
player = opl.OwnPlayer(player)

player.adjust_to_match_action(90)
stats = pd.concat([
  player.ball_skills, player.defending, player.mental, player.physical,
  player.passing, player.shooting, player.goalkeeping],
  ignore_index=True)
result_stats = stats[["name", "maximum", "current"]]

player.adjust_to_rest(20, type="holidays")
stats = pd.concat([
  player.ball_skills, player.defending, player.mental, player.physical,
  player.passing, player.shooting, player.goalkeeping],
  ignore_index=True)
result_stats["rested"] = stats["current"].copy()
print(result_stats)
