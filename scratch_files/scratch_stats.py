# experiment file

import pandas as pd
from unidecode import unidecode
import club as fc

fifa_data = pd.read_csv('../assets/FIFA21_official_data.csv')
# print(fifa_data.info())
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#     print(fifa_data.loc[86])

remove_columns = ["Photo", "Flag", "Club Logo", "Body Type", "Real Face", "Position", "Club"]
# unicode_translation = ["Name", "Club"]

team = pd.DataFrame(fifa_data.loc[fifa_data["Club"] == "Chelsea"]).sort_values("Jersey Number", ascending=True)
team = team.drop(remove_columns, axis=1)

team["Name"] = team["Name"].apply(unidecode)
#print(team["Name"])
# print(team.head())

team["Name"] = team["Name"].apply(unidecode)
chelsea = fc.Club("Chelsea", team)

team = pd.DataFrame(fifa_data.loc[fifa_data["Club"] == "Arsenal"]).sort_values("Jersey Number", ascending=True)
team = team.drop(remove_columns, axis=1)
team["Name"] = team["Name"].apply(unidecode)

arsenal = fc.Club("Arsenal", team)

# dict_keys(['ID', 'Name', 'Age', 'Nationality', 'Overall', 'Potential', 'Club', 'Value', 'Wage', 'Special', 'Preferred Foot', 'International Reputation', 'Weak Foot', 'Skill Moves', 'Work Rate', 'Jersey Number', 'Joined', 'Loaned From', 'Contract Valid Until', 'Height', 'Weight', 'Crossing', 'Finishing', 'HeadingAccuracy', 'ShortPassing', 'Volleys', 'Dribbling', 'Curve', 'FKAccuracy', 'LongPassing', 'BallControl', 'Acceleration', 'SprintSpeed', 'Agility', 'Reactions', 'Balance', 'ShotPower', 'Jumping', 'Stamina', 'Strength', 'LongShots', 'Aggression', 'Interceptions', 'Positioning', 'Vision', 'Penalties', 'Composure', 'Marking', 'StandingTackle', 'SlidingTackle', 'GKDiving', 'GKHandling', 'GKKicking', 'GKPositioning', 'GKReflexes', 'Best Position', 'Best Overall Rating', 'Release Clause', 'DefensiveAwareness'])