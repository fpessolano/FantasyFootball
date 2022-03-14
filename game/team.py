import random

# TODO add injury and injury tracking
#  hide elo (call it rating)
#  re-order and clean methods
#  use result consistency as modofier


class Team:
    """
    Objects describing a team by means of name, statistics and playing characteristics
    """

    __min_elo = 1000
    __elo_half_step = 100

    def __init__(self, name, elo=1500):
        self.name = name
        self.__elo = elo
        self.__old_edo = elo
        self.played = 0
        self.goals = [0, 0, 0]
        self.stats = [0, 0, 0]
        self.stars = 0
        self.result_streak = 0

    def data(self, show_stars=False):
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
            el.stars = max(
                ((el.__elo - cls.__min_elo) // cls.__elo_half_step) / 2, 0.5)

    # @classmethod
    # def eloFromStars(cls, stars, team):
    #     team.__oldEdo = team.__elo
    #     team.__elo = cls.__minElo + 2.05 * stars * cls.__eloHalfStep
    #     team.stars = stars

    def elo_from_stars(self, stars, reset):
        new_elo = Team.__min_elo + 2.05 * stars * Team.__elo_half_step
        if reset:
            self.__old_edo = new_elo
        else:
            self.__old_edo = self.__elo
        self.__elo = new_elo
        self.stars = stars

    # todo use to adjust elo at the end of the season
    #  test
    def adjust_rating(self):
        elo = self.__elo
        self.__elo = self.__old_edo + (self.__elo - self.__old_edo) / 3
        self.__old_edo = elo

    def rating(self):
        return self.__elo

    def __injuries(self):
        # TODO make a proper model
        return random.uniform(0.85, 1)

    def __form_modifier(self,
                        thresholds=[3, 15],
                        out_of_range_boosters=[0.1, -0.15]):
        # todo - use self.result_streak
        if self.result_streak > thresholds[1]:
            return 1 + out_of_range_boosters[0]
        elif self.result_streak < -1 * thresholds[1]:
            return 1 + out_of_range_boosters[1]
        elif self.result_streak < -1 * thresholds[0]:
            return random.uniform(
                1 + (thresholds[0] + self.result_streak) / 100, 1)
        elif self.result_streak < 0:
            return 1
        elif self.result_streak < thresholds[0]:
            return random.uniform(1, 1 + self.result_streak / 100)
        else:
            return random.uniform(1 - self.result_streak / 100,
                                  1 + thresholds[0] / 100)

    @classmethod
    def winning_probability(cls, home_team, away_team, home_offset):
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
