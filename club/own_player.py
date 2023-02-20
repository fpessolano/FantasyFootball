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
   - creaqtes dataframe stats with modifier, history, etc
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
    # crete a properly initialised player from scratch
    # then copy the data from start_season_stats if given

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

    # ['Unnamed: 0', 'name', 'age', 'nationality', 'current', 'potential', 'club', 'value', 'wage', 'special', 'preferred foot', 'international reputation', 'weak foot', 'skills', 'work rate', 'jersey number', 'joined', 'loaned from', 'contract valid until', 'height', 'weight', 'crossing', 'finishing', 'heading accuracy', 'short passing', 'volleys', 'dribbling', 'curve', 'accuracy', 'long passing', 'ball control', 'acceleration', 'sprint speed', 'agility', 'reactions', 'balance', 'shot power', 'jumping', 'stamina', 'strength', 'long shots', 'aggression', 'interceptions', 'positioning', 'vision', 'penalties', 'composure', 'marking', 'standing tackle', 'sliding tackle', 'diving', 'handling', 'kicking', 'gkpositioning', 'reflexes', 'best position', 'best overall rating', 'release clause', 'defensive awareness']

    data_ball_skills = {
      "name": ["dribbling", "control", "preferred foot", "weak foot"],
      "start": [
        player_data["dribbling"], player_data["dribbling"],
        player_data["preferred foot"], player_data["weak foot"]
      ],
      "match_modifier": [0.5, 0.5, 0.5, 0.5],
      "training_modifier": [0.2, 0.2, 0.2, 0.2],
      "rest_modifier": [1.5, 1.5, 1.5, 1.5],
      "streak_modifier": [1, 1, 1, 1]
    }
    data_ball_skills["maximum"] = data_ball_skills["start"]
    data_ball_skills["current"] = data_ball_skills["start"]

    data_defending = {
      "name":
      ["marking", "standing tackle", "sliding tackle", "defensive awareness"],
      "start": [0],
      "match_modifier": [0],
      "training_modifier": [0],
      "rest_modifier": [0],
      "streak_modifier": [0]
    }
    data_defending["maximum"] = data_defending["start"]
    data_defending["current"] = data_defending["start"]

    data_mental = {
      "name":
      ["agression", "positioning", "interceptions", "vision", "composure"],
      "start": [0],
      "match_modifier": [0],
      "training_modifier": [0],
      "rest_modifier": [0],
      "streak_modifier": [0]
    }
    data_mental["maximum"] = data_mental["start"]
    data_mental["current"] = data_mental["start"]

    data_physical = {
      "name": [
        "acceleration", "stamina", "strength", "sprint_speed", "balance",
        "jumping", "agility"
      ],
      "start": [0],
      "match_modifier": [0],
      "training_modifier": [0],
      "rest_modifier": [0],
      "streak_modifier": [0]
    }
    data_physical["maximum"] = data_physical["start"]
    data_physical["current"] = data_physical["start"]

    data_passing = {
      "name": ["Crossing", "ShortPassing", "LongPassing"],
      "start": [0],
      "match_modifier": [0],
      "training_modifier": [0],
      "rest_modifier": [0],
      "streak_modifier": [0]
    }
    data_passing["maximum"] = data_passing["start"]
    data_passing["current"] = data_passing["start"]

    data_shooting = {
      "name": [
        "heading", "power", "finishing", "long_shots"
        "curve", "accuracy", "penalties", "volleys"
      ],
      "start": [0],
      "match_modifier": [0],
      "training_modifier": [0],
      "rest_modifier": [0],
      "streak_modifier": [0]
    }
    data_shooting["maximum"] = data_shooting["start"]
    data_shooting["current"] = data_shooting["start"]

    data_goalkeeping = {
      "name": ["diving", "handling", "kicking", "positioning"
               "reflexes"],
      "start": [0],
      "match_modifier": [0],
      "training_modifier": [0],
      "rest_modifier": [0],
      "streak_modifier": [0]
    }
    data_goalkeeping["maximum"] = data_goalkeeping["start"]
    data_goalkeeping["current"] = data_goalkeeping["start"]

    # TODO what to do with specials

    if running:
      # TODO
      # update the from the provided one from the running game (TBD what it means)
      pass
