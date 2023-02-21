import datetime
import pandas as pd

# import player_stats as ps
# import sys
# sys.path.append('../')
# from support.helpers import copy_keys

# in progress
# needs to be fully changed ans player stats is no longer needed as class


class OwnPlayer:
  """
  this class model the single player (stats and stats evolution)
  """
  """
    TODO:
   - separate types of stats from other data
   - how to use and determine boosters
   - yearly stats updates
   - match stats decline
   - rest day recovery
   - injury and injury recovery
   - form modifier for match stats decline
   - ...
   """

  def __init__(self, player_data: pd.DataFrame, running=False):
    """
    Initialise the player by specifying the stats from the beginning or during a season.
    :PARAM player_data: all player data in a DataFrame format
    :PARAM running: if true player_data containt the data from a running season and not the reduced season start one
    """

    # IN PROGRESS
    # turn data variables into DataFrames
    # then copy the data from start_season_stats if given)
    # what to do with 'special', 'skills', 'work rate'?
    # how to have the max in season change over time
    # how to estimate the next season stats (use age and end of season max)

    self.basic_info = {}
    self.basic_info["name"] = player_data["name"]
    self.basic_info["age"] = player_data["age"]
    self.basic_info["nationality"] = player_data["nationality"]
    self.basic_info["height"] = player_data["height"]
    self.basic_info["weight"] = player_data["weight"]

    self.contract = {}
    self.contract["value"] = player_data["value"]
    self.contract["wage"] = player_data["wage"]
    self.contract["release"] = player_data["release clause"]
    self.contract["expiry"] = player_data["contract valid until"]
    self.contract["joined"] = player_data["joined"]
    self.contract["loaned from"] = player_data["loaned from"]

    self.role = {}
    self.role["jersey"] = player_data["jersey number"]
    self.role["position"] = player_data["best position"]

    self.reputation = {}
    self.reputation["international"] = player_data["international reputation"]
    self.reputation["national"] = player_data["international reputation"]

    self.rating = {}
    self.rating["current"] = player_data["current"]
    self.rating["potential"] = player_data["potential"]

    data_ball_skills = {
      "name": ["dribbling", "control", "preferred foot", "weak foot"],
      "start": [
        player_data["dribbling"], player_data["ball control"],
        player_data["preferred foot"], player_data["weak foot"]
      ],
      "match_modifier": [0.5] * 4,
      "training_modifier": [0.2] * 4,
      "rest_modifier": [1.5] * 4,
      "streak_modifier": [0.2] * 4
    }
    data_ball_skills["maximum"] = data_ball_skills["start"]
    data_ball_skills["current"] = data_ball_skills["start"]

    data_defending = {
      "name":
      ["marking", "standing tackle", "sliding tackle", "defensive awareness"],
      "start": [
        player_data["marking"], player_data["standing tackle"],
        player_data["sliding tackle"], player_data["defensive awareness"]
      ],
      "match_modifier": [0.5] * 4,
      "training_modifier": [0.2] * 4,
      "rest_modifier": [1.5] * 4,
      "streak_modifier": [0.2] * 4
    }
    data_defending["maximum"] = data_defending["start"]
    data_defending["current"] = data_defending["start"]

    data_mental = {
      "name": [
        "aggression", "positioning", "interceptions", "vision", "composure",
        "reactions"
      ],
      "start": [
        player_data["aggression"], player_data["positioning"],
        player_data["interceptions"], player_data["vision"],
        player_data["composure"], player_data["reactions"]
      ],
      "match_modifier": [0.5] * 6,
      "training_modifier": [0.1] * 6,
      "rest_modifier": [2] * 6,
      "streak_modifier": [0.1] * 6
    }
    data_mental["maximum"] = data_mental["start"]
    data_mental["current"] = data_mental["start"]

    data_physical = {
      "name": [
        "acceleration", "stamina", "strength", "sprint speed", "balance",
        "jumping", "agility"
      ],
      "start": [
        player_data["acceleration"], player_data["stamina"],
        player_data["strength"], player_data["sprint speed"],
        player_data["balance"], player_data["jumping"], player_data["agility"]
      ],
      "match_modifier": [0.5] * 7,
      "training_modifier": [0.2] * 7,
      "rest_modifier": [1.5] * 7,
      "streak_modifier": [0.2] * 7
    }
    data_physical["maximum"] = data_physical["start"]
    data_physical["current"] = data_physical["start"]

    data_passing = {
      "name": ["crossing", "short passing", "long passing"],
      "start": [
        player_data["crossing"], player_data["short passing"],
        player_data["long passing"]
      ],
      "match_modifier": [0.5] * 3,
      "training_modifier": [0.2] * 3,
      "rest_modifier": [1.5] * 3,
      "streak_modifier": [0.2] * 3
    }
    data_passing["maximum"] = data_passing["start"]
    data_passing["current"] = data_passing["start"]

    data_shooting = {
      "name": [
        "heading accuracy", "shot power", "finishing", "long shots"
        "curve", "accuracy", "penalties", "volleys"
      ],
      "start": [
        player_data["heading accuracy"], player_data["shot power"],
        player_data["finishing"], player_data["long shots"],
        player_data["curve"], player_data["accuracy"],
        player_data["penalties"], player_data["volleys"]
      ],
      "match_modifier": [0.5] * 8,
      "training_modifier": [0.2] * 8,
      "rest_modifier": [1.5] * 8,
      "streak_modifier": [0.2] * 8
    }
    data_shooting["maximum"] = data_shooting["start"]
    data_shooting["current"] = data_shooting["start"]

    data_goalkeeping = {
      "name": ["diving", "handling", "kicking", "gkpositioning"
               "reflexes"],
      "start": [
        player_data["diving"], player_data["handling"], player_data["kicking"],
        player_data["gkpositioning"], player_data["reflexes"]
      ],
      "match_modifier": [0.5] * 5,
      "training_modifier": [0.2] * 5,
      "rest_modifier": [1.5] * 5,
      "streak_modifier": [0.2] * 5
    }
    data_goalkeeping["maximum"] = data_goalkeeping["start"]
    data_goalkeeping["current"] = data_goalkeeping["start"]

    if running:
      # TODO
      # update the from the provided one from the running game (TBD what it means)
      pass
