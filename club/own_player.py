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
    # then copy the data from start_season_stats (if given)
    # what to do with 'special', 'skills'?
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
        player_data["dribbling"].values[0],
        player_data["ball control"].values[0],
        1 if player_data["preferred foot"].values[0] == "Right" else 0,
        0 if player_data["preferred foot"].values[0] == "Right" else 1
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
        player_data["marking"].values[0],
        player_data["standing tackle"].values[0],
        player_data["sliding tackle"].values[0],
        player_data["defensive awareness"].values[0]
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
        player_data["aggression"].values[0],
        player_data["positioning"].values[0],
        player_data["interceptions"].values[0],
        player_data["vision"].values[0], player_data["composure"].values[0],
        player_data["reactions"].values[0]
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
        player_data["acceleration"].values[0],
        player_data["stamina"].values[0], player_data["strength"].values[0],
        player_data["sprint speed"].values[0],
        player_data["balance"].values[0], player_data["jumping"].values[0],
        player_data["agility"].values[0]
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
        player_data["crossing"].values[0],
        player_data["short passing"].values[0],
        player_data["long passing"].values[0]
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
        player_data["heading accuracy"].values[0],
        player_data["shot power"].values[0],
        player_data["finishing"].values[0],
        player_data["long shots"].values[0], player_data["curve"].values[0],
        player_data["accuracy"].values[0], player_data["penalties"].values[0],
        player_data["volleys"].values[0]
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
        player_data["diving"].values[0], player_data["handling"].values[0],
        player_data["kicking"].values[0],
        player_data["gkpositioning"].values[0],
        player_data["reflexes"].values[0]
      ],
      "match_modifier": [0.5] * 5,
      "training_modifier": [0.2] * 5,
      "rest_modifier": [1.5] * 5,
      "streak_modifier": [0.2] * 5
    }
    data_goalkeeping["maximum"] = data_goalkeeping["start"]
    data_goalkeeping["current"] = data_goalkeeping["start"]

    def rate_equivalence(x):
      return {"low": 0, "medium": 1, "high": 2}[x]

    work_rate = [
      rate_equivalence(x.lower().strip())
      for x in player_data["work rate"].values[0].split("/")
    ]
    data_workrate = {
      "name": ["attacky", "defence", "training"],
      "start": [work_rate[0], work_rate[1],
                max(work_rate)],
      "match_modifier": [0] * 3,
      "training_modifier": [0] * 3,
      "rest_modifier": [0] * 3,
      "streak_modifier": [0] * 3
    }
    data_workrate["maximum"] = data_goalkeeping["start"]
    data_workrate["current"] = data_goalkeeping["start"]

    if running:
      # TODO
      # update the from the provided one from the running game (TBD what it means)
      pass
