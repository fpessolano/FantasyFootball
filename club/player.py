import datetime
import pandas as pd
import player_stats as ps
import sys

sys.path.append('../')
from support.helpers import copy_keys

# in progress


class Player:
  """
  this class model the single player (stats and stats evolution)
  """
  """
    TODO:
   - how to use and determine boosters
   - yearly stats updates
   - match stats decline
   - rest day recovery
   - injury and injury recovery
   - form modifier for match stats decline
   - ...
   """

  def __init__(self,
               start_season_stats: pd.DataFrame,
               season_stats: pd.DataFrame = None,
               year=None):

    if not year:
      self.year = int(datetime.date.today().year)
    else:
      self.year = year

    self.basic_info = {}
    copy_keys(source=start_season_stats,
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
    copy_keys(source=start_season_stats,
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
    copy_keys(source=start_season_stats,
              destination=self.role,
              key_list=["Jersey Number", "position"],
              key_rename_list=["jersey", "position"],
              if_absent=None)

    self.reputation = {}
    copy_keys(
      source=start_season_stats,
      destination=self.reputation,
      key_list=["International Reputation", "International Reputation"],
      key_rename_list=["national", "international"],
      if_absent=None)

    self.__reference_stats = ps.PlayerStats(start_season_stats)
    if season_stats:
      self.__game_stats = ps.PlayerStats(season_stats)
    else:
      self.__game_stats = ps.PlayerStats(start_season_stats)

  def stats(self, actual=True):
    if actual:
      return self.__game_stats.stats()
    return self.__reference_stats.stats()

  def __add__(self, other):
    return self.__game_stats + other.__game_stats
