import pandas as pd
import datetime
import sys

sys.path.append('../')
from support.helpers import copy_keys


class PlayerStats:
    """
    Object containing statistics of a generic player
    """

  def __init__(self, stats: pd.DataFrame, year=None):

    if not year:
      self.year = int(datetime.date.today().year)
    else:
      self.year = year

    self.basic_info = {}
    copy_keys(source=stats,
              destination=self.basic_info,
              key_list=[
                "Name", "Age", "Nationality", "Height", "Weight",
                "Best Position"
              ],
              key_rename_list=[
                "name", "age", "nationality", "height", "weight", "position"
              ],
              if_absent="")

    self.contract = {}
    copy_keys(source=stats,
              destination=self.contract,
              key_list=[
                "Value", "Wage", "Release Clause", "Contract Valid Until",
                "Joined", "Loaned From"
              ],
              key_rename_list=[
                "value", "wage", "release_clause", "expiry", "joined",
                "loaned_from"
              ],
              if_absent=0)

    self.role = {}
    copy_keys(source=stats,
              destination=self.role,
              key_list=["Jersey Number", "position"],
              key_rename_list=["jersey", "position"],
              if_absent=None)

    self.ball_skills = {}
    copy_keys(
      source=stats,
      destination=self.ball_skills,
      key_list=["Dribbling", "BallControl", "Preferred Foot", "Weak Foot"],
      key_rename_list=["dribbling", "control", "preferred_foot", "weak_foot"],
      if_absent=0)

    self.rating = {}
    copy_keys(source=stats,
              destination=self.rating,
              key_list=["Overall", "Potential", "Best Overall Rating"],
              key_rename_list=["current", "potential", "best"],
              if_absent=0)

    self.reputation = {}
    copy_keys(
      source=stats,
      destination=self.reputation,
      key_list=["International Reputation", "International Reputation"],
      key_rename_list=["national", "international"],
      if_absent=None)

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

    self.others = {}
    copy_keys(source=stats,
              destination=self.others,
              key_list=["Special", "Skill Moves", "Work Rate"],
              key_rename_list=["special", "skills", "work_rate"],
              if_absent=0)
