import random
import json


class Team:
  """
    Objects describing a team by means of name, statistics and playing characteristics
    """

  __min_elo = 1000
  __elo_half_step = 100

  def __init__(self, name="", elo=1500, full_definition=None):
    """
    Declare a team
    :param name: team name
    :param elo: team elo
    :param full_definition: if nto none is includes the complete sent os team stats (name, _Team__elo, 
      _Team__old_elo, played, goals, stats, stars, result_streak)
    """
    try:
      if full_definition:
        self.name = full_definition["name"]
        self.__elo = full_definition["_Team__elo"]
        self.__old_elo = full_definition["_Team__old_elo"]
        self.played = full_definition["played"]
        self.goals = full_definition["goals"]
        self.stats = full_definition["stats"]
        self.stars = full_definition["stars"]
        self.result_streak = full_definition["result_streak"]
        return
    except (KeyError, TypeError) as e:
      print(f"Warning: Invalid team definition provided: {e}")
      pass
    self.name = name
    self.__elo = elo
    self.__old_elo = elo
    self.played = 0
    self.goals = [0, 0, 0]
    self.stats = [0, 0, 0]
    self.stars = 0
    self.result_streak = 0

  def data(self, show_stars=False):
    """
    Returns the team stats
    :param show_stars: if true includes the star rating as well
    """
    data = {
      "NAME": self.name,
      "MP": self.played,
      "W": self.stats[0],
      "D": self.stats[1],
      "L": self.stats[2],
      "GF": self.goals[0],
      "GA": self.goals[1],
      "GD": self.goals[2],
      "PT": self.stats[0] * 3 + self.stats[1],
    }
    if show_stars:
      data["STARS"] = self.stars
    return data

  def print(self):
    print(
      f'Team {self.name} with current ELO of {self.__elo} has played {self.played}'
      f' matches with stats {self.stats} and goal stats {self.goals}')

  def add_match(self, scored, conceived):
    """
    Updates the team stats assuming a match was played
    :param scored: number of scored goals
    :param conceived: number of conceived goals
    """
    self.played += 1
    if scored > conceived:
      self.stats[0] += 1
      if self.result_streak < 0:
        self.result_streak = 1
      else:
        self.result_streak += 1
    elif scored == conceived:
      self.stats[1] += 1
      self.result_streak = 0
    else:
      self.stats[2] += 1
      if self.result_streak > 0:
        self.result_streak = -1
      else:
        self.result_streak -= 1
    self.goals[0] += scored
    self.goals[1] += conceived
    self.goals[2] += scored - conceived

  def reset(self):
    self.played = 0
    self.goals = [0, 0, 0]
    self.stats = [0, 0, 0]
    self.adjust_rating()

  @classmethod
  def calculate_stars(cls, team_list):
    elo_list = []
    for el in team_list:
      elo_list.append(el.__elo)
    maxElo = max(elo_list)
    cls.__elo_half_step = (maxElo - cls.__min_elo) / 10
    for el in team_list:
      el.stars = max(((el.__elo - cls.__min_elo) // cls.__elo_half_step) / 2,
                     0.5)

  # @classmethod
  # def eloFromStars(cls, stars, team):
  #     team.__oldEdo = team.__elo
  #     team.__elo = cls.__minElo + 2.05 * stars * cls.__eloHalfStep
  #     team.stars = stars

  def elo_from_stars(self, stars, reset):
    """
    Calculate the ELO value from the star rating
    :param stars: number of stars
    :param reset: if true the old elo is discarded and the new one used for that as well
    """
    new_elo = Team.__min_elo + 2.05 * stars * Team.__elo_half_step
    if reset:
      self.__old_elo = new_elo
    else:
      self.__old_elo = self.__elo
    self.__elo = new_elo
    self.stars = stars

  # todo use to adjust elo at the end of the season
  #  test
  def adjust_rating(self):
    """
    updates the elo rating based on latest stats
    """
    elo = self.__elo
    self.__elo = self.__old_elo + (self.__elo - self.__old_elo) / 3
    self.__old_elo = elo

  def rating(self):
    return self.__elo

  def __injuries(self, lower_modifier=0.85):
    # TODO make a proper model
    return random.uniform(lower_modifier, 1)

  def __form_modifier(self,
                      thresholds=[3, 15],
                      out_of_range_boosters=[0.1, -0.15]):
    """
    Returns a modified to be used dring a match based on random values ands result stream
    :param thresholds: low and high threshold for streaks
    :param out_of_range_boosters: modified used when out of the threshold range
    """
    if self.result_streak > thresholds[1]:
      return 1 + out_of_range_boosters[0]
    elif self.result_streak < -1 * thresholds[1]:
      return 1 + out_of_range_boosters[1]
    elif self.result_streak < -1 * thresholds[0]:
      return random.uniform(1 + (thresholds[0] + self.result_streak) / 100, 1)
    elif self.result_streak < 0:
      return 1
    elif self.result_streak < thresholds[0]:
      return random.uniform(1, 1 + self.result_streak / 100)
    else:
      return random.uniform(1 - self.result_streak / 100,
                            1 + thresholds[0] / 100)

  @classmethod
  def winning_probability(cls, home_team, away_team, home_offset):
    """
    returns the winning probability based on elo ratinngs and form modifier
    :param home_team: home team
    :param away_team: away team
    :param home_offset: home advantage modifier
    """
    deltaElo = (home_team.__elo + home_offset) * home_team.__injuries(
    ) * home_team.__form_modifier() - away_team.__elo
    return float(1 / (10**(deltaElo / -400) + 1))

  def new_rating(self, match_modifier, goal_difference, win_probability):
    if goal_difference > 0:
      result = 1
    elif goal_difference == 0:
      result = 0.5
    else:
      result = 0
    if goal_difference < 2:
      modifier = 1
    elif goal_difference == 2:
      modifier = 1.5
    else:
      modifier = 1 + (3 / 4 + (goal_difference - 3) / 8)
    self.__elo = float(self.__elo + match_modifier * modifier *
                       (result - win_probability))

  def __iter__(self):
    yield from {
      "name": self.name,
      "elo": self.__elo,
      "old_elo": self.__old_elo,
      "goals": self.goals,
      "stats": self.stats,
      "stars": self.stars,
      "result_streak": self.result_streak
    }.items()

  def __str__(self):
    return json.dumps(dict(self), ensure_ascii=False)

  def __repr__(self):
    return self.__str__()
