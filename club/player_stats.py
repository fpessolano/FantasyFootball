import pandas as pd
import sys
import pprint as pp

sys.path.append('../')
from support.helpers import copy_keys

# in progress
#  need to ditch DICT for DataFrame including also modifiers and alike


class PlayerStats:
  """
  Object containing statistics of a generic player
  """

  def __init__(self, stats: pd.DataFrame):

    self.rating = {}
    copy_keys(source=stats,
              destination=self.rating,
              key_list=["Overall", "Potential", "Best Overall Rating"],
              key_rename_list=["current", "potential", "best"],
              if_absent=0)

    self.ball_skills = {}
    copy_keys(
      source=stats,
      destination=self.ball_skills,
      key_list=["Dribbling", "BallControl", "Preferred Foot", "Weak Foot"],
      key_rename_list=["dribbling", "control", "preferred_foot", "weak_foot"],
      if_absent=0)

    self.defending = {}
    copy_keys(source=stats,
              destination=self.defending,
              key_list=[
                "Marking", "StandingTackle", "SlidingTackle",
                "DefensiveAwareness"
              ],
              key_rename_list=[
                "marking", "standing_tackle", "sliding_tackle", "awareness"
              ],
              if_absent=0)

    self.mental = {}
    copy_keys(source=stats,
              destination=self.mental,
              key_list=[
                "Aggression", "Reactions", "Positioning", "Interceptions",
                "Vision", "Composure"
              ],
              key_rename_list=[
                "agression", "positioning", "interceptions", "vision",
                "composure"
              ],
              if_absent=0)
    self.mental["confidence"] = 100

    self.physical = {}
    copy_keys(source=stats,
              destination=self.physical,
              key_list=[
                "Acceleration", "Stamina", "Strength", "SprintSpeed",
                "Balance", "Jumping", "Agility"
              ],
              key_rename_list=[
                "acceleration", "stamina", "strength", "sprint_speed",
                "balance", "jumping", "agility"
              ],
              if_absent=0)
    self.physical["form"] = 100
    self.physical["recovery_time_days"] = 0

    self.passing = {}
    copy_keys(source=stats,
              destination=self.passing,
              key_list=["Crossing", "ShortPassing", "LongPassing"],
              key_rename_list=["crossing", "short", "long"],
              if_absent=0)

    self.shooting = {}
    copy_keys(source=stats,
              destination=self.shooting,
              key_list=[
                "HeadingAccuracy", "ShotPower", "Finishing", "LongShots"
                "Curve", "FKAccuracy", "Penalties", "Volleys"
              ],
              key_rename_list=[
                "heading", "power", "finishing", "long_shots"
                "curve", "accuracy", "penalties", "volleys"
              ],
              if_absent=0)
    self.shooting["streak_booster"] = 1

    self.goalkeeping = {}
    copy_keys(source=stats,
              destination=self.goalkeeping,
              key_list=[
                "GKDiving", "GKHandling", "GKKicking", "GKPositioning"
                "GKReflexes"
              ],
              key_rename_list=[
                "diving", "handling", "kicking", "positioning"
                "reflexes"
              ],
              if_absent=0)
    self.goalkeeping["streak_booster"] = 1

    # this will need to be adjusted to be useful
    # for the time being it will be ignored
    self.others = {}
    copy_keys(source=stats,
              destination=self.others,
              key_list=["Special", "Skill Moves", "Work Rate"],
              key_rename_list=["special", "skills", "work_rate"],
              if_absent=0)

  def stats(self):
    return {
      "rating": self.rating,
      "ball_skills": self.ball_skills,
      "defending": self.defending,
      "mental": self.mental,
      "physical": self.physical,
      "passing": self.passing,
      "shooting": self.shooting,
      "goalkeeping": self.goalkeeping,
      "others": self.others
    }

  def __add__(self, other):
    cumulative_player = PlayerStats(pd.DataFrame())
    for key in cumulative_player.rating.keys():
      cumulative_player.rating[key] = self.rating[key] + other.rating[key]
    cumulative_player.ball_skills["dribbling"] = self.ball_skills[
      "dribbling"] + other.ball_skills["dribbling"]
    cumulative_player.ball_skills[
      "control"] = self.ball_skills["control"] + other.ball_skills["control"]
    for key in cumulative_player.defending.keys():
      cumulative_player.defending[
        key] = self.defending[key] + other.defending[key]
    for key in cumulative_player.mental.keys():
      cumulative_player.mental[key] = self.mental[key] + other.mental[key]
    for key in cumulative_player.physical.keys():
      cumulative_player.physical[
        key] = self.physical[key] + other.physical[key]
    for key in cumulative_player.passing.keys():
      cumulative_player.passing[key] = self.passing[key] + other.passing[key]
    for key in cumulative_player.shooting.keys():
      cumulative_player.shooting[
        key] = self.shooting[key] + other.shooting[key]
    for key in cumulative_player.goalkeeping.keys():
      cumulative_player.goalkeeping[
        key] = self.goalkeeping[key] + other.goalkeeping[key]
    return cumulative_player

  def workout(self, type, intensity, duration):
    pass

  def rest(self, intensity, duration):
    pass
