import random

# TODO define types of matches
#  match modifier:
#  60 for World Cup finals;
#  50 for continental championship finals and major intercontinental tournaments;
#  40 for World Cup and continental qualifiers and major tournaments;
#  30 for all other tournaments;
#  20 for friendly matches.
from game.team import Team


class MatchType:
    """
    Constants for match types
    """

    def __init__(self):
        pass

    @classmethod
    def world_cup_final(cls):
        return 60

    @classmethod
    def finals(cls):
        return 50

    @classmethod
    def major_tournaments(cls):
        return 40

    @classmethod
    def minor_division(cls):
        return 30

    @classmethod
    def friendly(cls):
        return 20


def match_result(home_win_probability, away_win_probability):
    home_shoots = round(random.randint(0, 5) * home_win_probability)
    away_shoots = round(random.randint(0, 5) * away_win_probability)

    if home_win_probability < away_win_probability / 4 and home_shoots == 0:
        home_shoots += 1

    if away_win_probability < home_win_probability / 4 and away_shoots == 0:
        away_shoots += 1

    home_goals = 0
    away_goals = 0

    for _ in range(home_shoots):
        attack = 5 * random.random() + 5 * home_win_probability * random.random()
        defence = 5 * random.random() + 5 * away_win_probability * random.random(
        )
        if attack > defence:
            home_goals += 1

    for _ in range(away_shoots):
        attack = 10 * random.random() + away_win_probability
        defence = 10 * random.random() + home_win_probability
        if attack > defence:
            away_goals += 1

    return home_goals, away_goals


def play_match(home_team: Team, away_team: Team, match_modifier=40, home_offset=50):
    home_winning_probability = Team.winning_probability(home_team, away_team, home_offset)
    away_wining_probability = Team.winning_probability(away_team, home_team, 0)
    home_goals, away_goals = match_result(home_winning_probability, away_wining_probability)
    home_team.new_rating(match_modifier, home_goals - away_goals, home_winning_probability)
    away_team.new_rating(match_modifier, away_goals - home_goals, away_wining_probability)
    home_team.add_match(home_goals, away_goals)
    away_team.add_match(away_goals, home_goals)
    return home_goals, away_goals
