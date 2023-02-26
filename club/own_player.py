import pandas as pd
import numpy as np
import math
"""
  TODO:
 - how to use and determine boosters
 - yearly stats updates
 - match stats decline
 - rest day recovery
 - injury and injury recovery
 - form modifier for match stats decline
 - how to have the max in season change over time
 - how to estimate the next season stats (use age and end of season max)
 - form needs to depend on trainings
 - skills max also need to depend on training somwhow but much much slower
 - workrate also needs to affect things
"""

MATCH_TIME_UNIT_MIN = 5
TRAINING_TIME_UNIT_MIN = 5
REST_TIME_UNIT_DAY = 1


class OwnPlayer:
  """
  this class model the single player (stats and stats evolution)
  """

  def __init__(self, player_data: pd.DataFrame, running=False):
    """
    Initialise the player by specifying the stats from the beginning or during a season.
    :PARAM player_data: all player data in a DataFrame format
    :PARAM running: if true player_data containt the data from a running season and not the reduced season start one
    """

    # TODO what to do with 'special', 'skills'?

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
      "match_modifier": [0.7, 0.7, 0, 0],
      "training_modifier": [0.2, 0.2, 0, 0],
      "rest_modifier": [2.5, 2.5, 0, 0],
      "streak_modifier": [0.2, 0.2, 0, 0]
    }
    data_ball_skills["maximum"] = data_ball_skills["start"]
    data_ball_skills["current"] = data_ball_skills["start"]
    self.ball_skills = pd.DataFrame(data_ball_skills)

    data_defending = {
      "name":
      ["marking", "standing tackle", "sliding tackle", "defensive awareness"],
      "start": [
        player_data["marking"].values[0],
        player_data["standing tackle"].values[0],
        player_data["sliding tackle"].values[0],
        player_data["defensive awareness"].values[0]
      ],
      "match_modifier": [1] * 4,
      "training_modifier": [0.2] * 4,
      "rest_modifier": [2.5] * 4,
      "streak_modifier": [0.2] * 4
    }
    data_defending["maximum"] = data_defending["start"]
    data_defending["current"] = data_defending["start"]
    self.defending = pd.DataFrame(data_defending)

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
      "match_modifier": [1, 0.5, 0.7, 0.7, 0.7, 1],
      "training_modifier": [0.1] * 6,
      "rest_modifier": [2.5] * 6,
      "streak_modifier": [0.1] * 6
    }
    data_mental["maximum"] = data_mental["start"]
    data_mental["current"] = data_mental["start"]
    self.mental = pd.DataFrame(data_mental)

    data_physical = {
      "name": [
        "acceleration", "strength", "sprint speed", "balance", "jumping",
        "agility", "stamina", "form"
      ],
      "start": [
        player_data["acceleration"].values[0],
        player_data["strength"].values[0],
        player_data["sprint speed"].values[0],
        player_data["balance"].values[0], player_data["jumping"].values[0],
        player_data["agility"].values[0], player_data["stamina"].values[0], 100
      ],
      "match_modifier": [1] * 7 + [3],
      "training_modifier": [0.2] * 7 + [3],
      "rest_modifier": [2.5] * 7 + [15],
      "streak_modifier": [0.2] * 7 + [0.5]
    }
    data_physical["maximum"] = data_physical["start"]
    data_physical["current"] = data_physical["start"]
    self.physical = pd.DataFrame(data_physical)

    data_passing = {
      "name": ["crossing", "short passing", "long passing"],
      "start": [
        player_data["crossing"].values[0],
        player_data["short passing"].values[0],
        player_data["long passing"].values[0]
      ],
      "match_modifier": [0.7] * 3,
      "training_modifier": [0.2] * 3,
      "rest_modifier": [2.5] * 3,
      "streak_modifier": [0.2] * 3
    }
    data_passing["maximum"] = data_passing["start"]
    data_passing["current"] = data_passing["start"]
    self.passing = pd.DataFrame(data_passing)

    data_shooting = {
      "name": [
        "heading accuracy", "shot power", "finishing", "long shots", "curve",
        "accuracy", "penalties", "volleys"
      ],
      "start": [
        player_data["heading accuracy"].values[0],
        player_data["shot power"].values[0],
        player_data["finishing"].values[0],
        player_data["long shots"].values[0], player_data["curve"].values[0],
        player_data["accuracy"].values[0], player_data["penalties"].values[0],
        player_data["volleys"].values[0]
      ],
      "match_modifier": [0.7, 0.7, 0.7, 0.5, 1, 0.5, 0.5, 0.7],
      "training_modifier": [0.2] * 8,
      "rest_modifier": [2.5] * 8,
      "streak_modifier": [0.2] * 8
    }
    data_shooting["maximum"] = data_shooting["start"]
    data_shooting["current"] = data_shooting["start"]
    self.shooting = pd.DataFrame(data_shooting)

    data_goalkeeping = {
      "name": ["diving", "handling", "kicking", "gkpositioning", "reflexes"],
      "start": [
        player_data["diving"].values[0], player_data["handling"].values[0],
        player_data["kicking"].values[0],
        player_data["gkpositioning"].values[0],
        player_data["reflexes"].values[0]
      ],
      "match_modifier": [0.7, 0.7, 0.7, 0.5, 1],
      "training_modifier": [0.2] * 5,
      "rest_modifier": [2.5] * 5,
      "streak_modifier": [0.2] * 5
    }
    data_goalkeeping["maximum"] = data_goalkeeping["start"]
    data_goalkeeping["current"] = data_goalkeeping["start"]
    self.goalkeeping = pd.DataFrame(data_goalkeeping)

    def rate_equivalence(x):
      return {"low": 0, "medium": 1, "high": 2}[x]

    work_rate = [
      rate_equivalence(x.lower().strip())
      for x in player_data["work rate"].values[0].split("/")
    ]

    self.workrate = {
      "attack": work_rate[0],
      "defence": work_rate[1],
      "training": max(work_rate)
    }

    if running:
      # TODO
      # update the from the provided one from the running game
      # need to first fix the saving format.
      pass

  @classmethod
  def ___stamina_coeff(cls, x):
    # it is the common stats decay formula, centralised in order to sync on future changes
    x /= 100
    return 1 - x**5

  @classmethod
  def __update_stats(cls, stats, coefficient, time_units):
    try:
      stats["current"] = (
        stats["maximum"] -
        coefficient * time_units * stats["match_modifier"]).round(decimals=0)
      stats["current"] = np.where(stats["current"] <= 0, 0, stats["current"])
      stats["current"] = np.where(stats["current"] > stats["maximum"],
                                  stats["maximum"], stats["current"])
      return stats["current"]
    except:
      # this should never happen
      return None

  def adjust_to_match_action(self,
                             elapsed_time_min,
                             number_attacks=0,
                             number_defences=0):
    # stats are influenced by the stamina decrease dring a match.
    # The rate of decrease is determined in the modifier field of each stat
    # TODO add effect of number_attacks and number_defences to adjust stamina considering also work rate values
    stamina = self.physical.loc[self.physical["name"] ==
                                "stamina"]["current"].values[0]
    stamina_coeff = OwnPlayer.___stamina_coeff(stamina)

    self.ball_skills["current"] = OwnPlayer.__update_stats(
      self.ball_skills, stamina_coeff, elapsed_time_min / MATCH_TIME_UNIT_MIN)

    self.defending["current"] = OwnPlayer.__update_stats(
      self.defending, stamina_coeff, elapsed_time_min / MATCH_TIME_UNIT_MIN)

    self.mental["current"] = OwnPlayer.__update_stats(
      self.mental, stamina_coeff, elapsed_time_min / MATCH_TIME_UNIT_MIN)

    self.physical["current"] = OwnPlayer.__update_stats(
      self.physical, stamina_coeff, elapsed_time_min / MATCH_TIME_UNIT_MIN)

    self.passing["current"] = OwnPlayer.__update_stats(
      self.passing, stamina_coeff, elapsed_time_min / MATCH_TIME_UNIT_MIN)

    self.shooting["current"] = OwnPlayer.__update_stats(
      self.shooting, stamina_coeff, elapsed_time_min / MATCH_TIME_UNIT_MIN)

    self.goalkeeping["current"] = OwnPlayer.__update_stats(
      self.goalkeeping, stamina_coeff, elapsed_time_min / MATCH_TIME_UNIT_MIN)

  def adjust_to_training_action(self,
                                elapsed_time_min,
                                intensity=1,
                                focus=None):
    # in progress
    # TODO use intensity and focus to adjust stamina considering also work rate values
    pass

  def adjust_to_rest(self, elapsed_time_day, type="post-match"):
    # in progress - adjust the values in modifiers and manage the cap and form one
    type_modifiers = {
      "post-match": {
        "coeff": 1,  # affects the stats recovery
        "form_coeff": 1,  # affects the form recovery (together with coeff)
        "form_cap": 1  # limits the maximum form value
      },
      "injury": {
        "coeff": 1,
        "form_coeff": 1,
        "form_cap": 1
      },
      "injury-recover": {
        "coeff": 1,
        "form_coeff": 1,
        "form_cap": 1
      },
      "holidays": {
        "coeff": 1,
        "form_coeff": 1,
        "form_cap": 1
      }
    }

    self.ball_skills["current"] = OwnPlayer.__update_stats(
      self.ball_skills, -type_modifiers[type]["coeff"],
      elapsed_time_day / REST_TIME_UNIT_DAY)
    self.defending["current"] = OwnPlayer.__update_stats(
      self.defending, -type_modifiers[type]["coeff"],
      elapsed_time_day / REST_TIME_UNIT_DAY)
    self.mental["current"] = OwnPlayer.__update_stats(
      self.mental, -type_modifiers[type]["coeff"],
      elapsed_time_day / REST_TIME_UNIT_DAY)
    self.physical["current"] = OwnPlayer.__update_stats(
      self.physical, -type_modifiers[type]["coeff"],
      elapsed_time_day / REST_TIME_UNIT_DAY)
    self.passing["current"] = OwnPlayer.__update_stats(
      self.passing, -type_modifiers[type]["coeff"],
      elapsed_time_day / REST_TIME_UNIT_DAY)
    self.shooting["current"] = OwnPlayer.__update_stats(
      self.shooting, -type_modifiers[type]["coeff"],
      elapsed_time_day / REST_TIME_UNIT_DAY)
    self.goalkeeping["current"] = OwnPlayer.__update_stats(
      self.goalkeeping, -type_modifiers[type]["coeff"],
      elapsed_time_day / REST_TIME_UNIT_DAY)
    
    
