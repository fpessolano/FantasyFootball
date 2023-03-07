import pandas as pd
import numpy as np
"""
  TODO:
 - IT DOES NOT MAKE sense, training needs to help improvo state also.
 - THIS NEEDS A TOTAL RETHINK starting from a stats class (like nim version)
 - how to use and determine boosters
 - how to have the max in season change over time
 - how to estimate the next season stats (use age and end of season max)
 - skills max also need to depend on training somwhow but much much slower
 - workrate also needs to affect things
"""

MATCH_TIME_UNIT_MIN = 5
TRAINING_TIME_UNIT_MIN = 5
REST_TIME_UNIT_DAY = 1


class ActivePlayer:
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
      "training_modifier": [0.2] * 7 + [-0.5],
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
  def __stats_action(
    cls,
    stats,
    coefficient,
    time_units,
    match=True,
  ):
    if match:
      modifier = stats["match_modifier"]
    else:
      modifier = stats["training_modifier"]
    try:
      stats["current"] = (stats["current"] -
                          coefficient * time_units * modifier).round(
                            decimals=0)
      stats["current"] = np.where(stats["current"] <= 0, 0, stats["current"])
      stats["current"] = np.where(stats["current"] > stats["maximum"],
                                  stats["maximum"], stats["current"])
      return stats["current"]
    except:
      # this should never happen
      return None

  @classmethod
  def __stats_rest(cls, stats, coefficient, time_units):
    try:
      stats["current"] = (
        stats["current"] +
        coefficient * time_units * stats["rest_modifier"]).round(decimals=0)
      stats["current"] = np.where(stats["current"] > stats["maximum"],
                                  stats["maximum"], stats["current"])
      return stats["current"]
    except:
      # this should never happen
      return None

  def __plays(self, time_units, match, coeff_modifier=1):
    # stats are influenced by the stamina decrease during a match.
    # The rate of decrease is determined in the modifier field of each stat
    stamina = self.physical.loc[self.physical["name"] ==
                                "stamina"]["current"].values[0]
    stamina_coeff = ActivePlayer.___stamina_coeff(stamina) * coeff_modifier

    self.ball_skills["current"] = ActivePlayer.__stats_action(self.ball_skills,
                                                              stamina_coeff,
                                                              time_units,
                                                              match=match)

    self.defending["current"] = ActivePlayer.__stats_action(self.defending,
                                                            stamina_coeff,
                                                            time_units,
                                                            match=match)

    self.mental["current"] = ActivePlayer.__stats_action(self.mental,
                                                         stamina_coeff,
                                                         time_units,
                                                         match=match)

    self.physical["current"] = ActivePlayer.__stats_action(self.physical,
                                                           stamina_coeff,
                                                           time_units,
                                                           match=match)

    self.passing["current"] = ActivePlayer.__stats_action(self.passing,
                                                          stamina_coeff,
                                                          time_units,
                                                          match=match)

    self.shooting["current"] = ActivePlayer.__stats_action(self.shooting,
                                                           stamina_coeff,
                                                           time_units,
                                                           match=match)

    self.goalkeeping["current"] = ActivePlayer.__stats_action(self.goalkeeping,
                                                              stamina_coeff,
                                                              time_units,
                                                              match=match)

  def adjust_to_match_action(self,
                             elapsed_time_min,
                             number_attacks=0,
                             number_defences=0):

    # TODO add effect of number_attacks and number_defences
    # to adjust stamina considering also work rate values
    time_units = elapsed_time_min / MATCH_TIME_UNIT_MIN
    self.__plays(time_units=time_units, match=True)

  def adjust_to_rest(self, elapsed_time_day, type="post-match"):
    # TODO best split things and depending on the restform changes (too long is holidays)
    type_modifiers = {
      "post-match": {
        "coeff": 1,  # affects the stats recovery
        "form_coeff": 0.5,  # affects the form recovery (together with coeff)
        "form_cap": 0.95  # limits the maximum form value
      },
      "injury": {
        "coeff": 0,  # injury stats will not change till in recover
        "form_coeff": 0.1,
        "form_cap": 0.5
      },
      "injury-recover": {
        "coeff": 0.1,
        "form_coeff": 0.5,
        "form_cap": 1
      },
      "holidays": {
        "coeff": 0.08,
        "form_coeff": 0.1,
        "form_cap": 0.7
      }
    }

    time_units = elapsed_time_day / REST_TIME_UNIT_DAY

    # form_stats = self.physical[self.physical["name"] == "form"]

    self.ball_skills["current"] = ActivePlayer.__stats_rest(
      self.ball_skills, type_modifiers[type]["coeff"], time_units)
    self.defending["current"] = ActivePlayer.__stats_rest(
      self.defending, type_modifiers[type]["coeff"], time_units)
    self.mental["current"] = ActivePlayer.__stats_rest(
      self.mental, type_modifiers[type]["coeff"], time_units)
    self.physical["current"] = ActivePlayer.__stats_rest(
      self.physical, type_modifiers[type]["coeff"], time_units)
    self.passing["current"] = ActivePlayer.__stats_rest(
      self.passing, type_modifiers[type]["coeff"], time_units)
    self.shooting["current"] = ActivePlayer.__stats_rest(
      self.shooting, type_modifiers[type]["coeff"], time_units)
    self.goalkeeping["current"] = ActivePlayer.__stats_rest(
      self.goalkeeping, type_modifiers[type]["coeff"], time_units)

    # form_max = (form_stats["maximum"] * type_modifiers[type]["form_cap"]).values[0]

    # if form_stats["current"].values[0] < form_max:
    #   form = min(
    #     (form_stats["current"] +
    #      type_modifiers[type]["coeff"] * type_modifiers[type]["form_coeff"] *
    #      time_units * form_stats["rest_modifier"]).values[0],
    #     (form_stats["maximum"] * type_modifiers[type]["form_cap"]).values[0])
    # else:
    #   form = form_stats["current"].values[0]

    # self.physical.loc[self.physical["name"] == "form", ["current"]]=form

  def injured(self, severity=0.5, focus=None):
    self.ball_skills["current"] *= severity
    self.defending["current"] *= severity
    self.mental["current"] *= severity
    self.physical["current"] *= severity
    self.passing["current"] *= severity
    self.shooting["current"] *= severity
    self.goalkeeping["current"] *= severity

  def adjust_to_training_action(self,
                                elapsed_time_min,
                                intensity=1,
                                focus=None):
    # TODO add effect of intensity and focus
    # to adjust stamina considering also work rate values
    time_units = elapsed_time_min / TRAINING_TIME_UNIT_MIN
    self.__plays(time_units=time_units, match=False)
