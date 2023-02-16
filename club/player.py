import pandas as pd
import player_stats as ps

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
               reference_stats: pd.DataFrame,
               current_stats: pd.DataFrame = None,
               year=None):
    self.__reference_stats = ps.PlayerStats(reference_stats, year)
    if current_stats:
      self.__game_stats = ps.PlayerStats(current_stats, year)
    else:
      self.__game_stats = ps.PlayerStats(reference_stats, year)

  def stats(self, actual=True):
    if actual:
      return self.__game_stats.stats()
    return self.__reference_stats.stats()
