import pandas as pd
import datetime

# in progress

# dict_keys(['ID', 'Name', 'Age', 'Nationality', 'Overall', 'Potential', 'Club', 'Value', 'Wage', 'Special', 'Preferred Foot', 'International Reputation', 'Weak Foot', 'Skill Moves', 'Work Rate', 'Jersey Number', 'Joined', 'Loaned From', 'Contract Valid Until', 'Height', 'Weight', 'Crossing', 'Finishing', 'HeadingAccuracy', 'ShortPassing', 'Volleys', 'Dribbling', 'Curve', 'FKAccuracy', 'LongPassing', 'BallControl', 'Acceleration', 'SprintSpeed', 'Agility', 'Reactions', 'Balance', 'ShotPower', 'Jumping', 'Stamina', 'Strength', 'LongShots', 'Aggression', 'Interceptions', 'Positioning', 'Vision', 'Penalties', 'Composure', 'Marking', 'StandingTackle', 'SlidingTackle', 'GKDiving', 'GKHandling', 'GKKicking', 'GKPositioning', 'GKReflexes', 'Best Position', 'Best Overall Rating', 'Release Clause', 'DefensiveAwareness'])


class Player:
  """
  this class model the single player (stats and stats evolution)
  """

  def __init__(self, player_stats: pd.DataFrame, year=None):
    # TODO need to decide how to handle missing information ... right now it will just crash

    self.__basic_info = {}
    if not year:
      self.__stats_year = int(datetime.date.today().year)
    else:
      self.__stats_year = year
    self.__basic_info["name"] = player_stats["Name"]
    self.__basic_info["age"] = player_stats["Age"]
    self.__basic_info["nationality"] = player_stats["Nationality"]
    self.__basic_info["height"] = player_stats["Height"]
    self.__basic_info["weight"] = player_stats["Weight"]
    self.__basic_info["position"] = player_stats["Best Position"]

    self.__contract = {}
    self.__contract["value"] = player_stats["Value"]
    self.__contract["wage"] = player_stats["Wage"]
    self.__contract["release_clause"] = player_stats["Release Clause"]
    self.__contract["expiry"] = player_stats["Contract Valid Until"]
    self.__contract["joined"] = player_stats["Joined"]
    self.__contract["loaned_from"] = player_stats["Loaned From"]

    self.__Jersey = player_stats["Jersey Number"]

    self.__ball_skills = {}
    self.__ball_skills["dribbling"] = player_stats["Dribbling"]
    self.__ball_skills["control"] = player_stats["BallControl"]
    self.__ball_skills["preferred_foot"] = player_stats["Preferred Foot"]
    self.__ball_skills["weak_foot"] = player_stats["Weak Foot"]

    self.__rating = {}
    self.__rating["current"] = player_stats["Overall"]
    self.__rating["potential"] = player_stats["Potential"]
    self.__rating["best"] = player_stats["Best Overall Rating"]

    self.__reputation = {}
    self.__reputation["national"] = player_stats["International Reputation"]
    self.__reputation["international"] = player_stats[
      "International Reputation"]

    self.__defending = {}
    self.__defending["marking"] = player_stats["Marking"]
    self.__defending["standing_tackle"] = player_stats["StandingTackle"]
    self.__defending["sliding_tackle"] = player_stats["SlidingTackle"]
    self.__defending["awareness"] = player_stats["DefensiveAwareness"]

    self.__mental = {}
    self.__mental["agression"] = player_stats["Aggression"]
    self.__mental["reactions"] = player_stats["Reactions"]
    self.__mental["positioning"] = player_stats["Positioning"]
    self.__mental["interceptions"] = player_stats["Interceptions"]
    self.__mental["vision"] = player_stats["Vision"]
    self.__mental["composure"] = player_stats["Composure"]

    self.__physical = {}
    self.__physical["acceleration"] = player_stats["Acceleration"]
    self.__physical["stamina"] = player_stats["Stamina"]
    self.__physical["strength"] = player_stats["Strength"]
    self.__physical["sprint_speed"] = player_stats["SprintSpeed"]
    self.__physical["balance"] = player_stats["Balance"]
    self.__physical["jumping"] = player_stats["Jumping"]
    self.__physical["agility"] = player_stats["Agility"]

    self.__passing = {}
    self.__passing["crossing"] = player_stats["Crossing"]
    self.__passing["short"] = player_stats["ShortPassing"]
    self.__passing["long"] = player_stats["LongPassing"]

    self.__shooting = {}
    self.__physical["heading"] = player_stats["HeadingAccuracy"]
    self.__physical["power"] = player_stats["ShotPower"]
    self.__physical["finmishing"] = player_stats["Finishing"]
    self.__physical["long_shots"] = player_stats["LongShots"]
    self.__physical["curve"] = player_stats["Curve"]
    self.__physical["accuracy"] = player_stats["FKAccuracy"]
    self.__physical["penalties"] = player_stats["Penalties"]
    self.__physical["volleys"] = player_stats["Volleys"]

    self.__goalkeeper = {}
    self.__goalkeeper["diving"] = player_stats["GKDiving"]
    self.__goalkeeper["handling"] = player_stats["GKHandling"]
    self.__goalkeeper["kicking"] = player_stats["GKKicking"]
    self.__goalkeeper["positioning"] = player_stats["GKPositioning"]
    self.__goalkeeper["reflexes"] = player_stats["GKReflexes"]

    self.__others = {}
    self.__others["special"] = player_stats["Special"]
    self.__others["skills"] = player_stats["Skill Moves"]
    self.__others["work_rate"] = player_stats["Work Rate"]

  def basics(self):
    return self.__basic_info
  
  def others(self):
    return self.__others
