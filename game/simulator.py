import random

# TODO define types of matches
#  match modifier:
#  60 for World Cup finals;
#  50 for continental championship finals and major intercontinental tournaments;
#  40 for World Cup and continental qualifiers and major tournaments;
#  30 for all other tournaments;
#  20 for friendly matches.
from game.team import Team


class MatchType():
    """
    Constants for match types
    """

    def __init__(self):
        pass

    @classmethod
    def WorldCupFinal(cls):
        return 60

    @classmethod
    def Finals(cls):
        return 50

    @classmethod
    def MajorTournaments(cls):
        return 40

    @classmethod
    def MinorDivision(cls):
        return 30

    @classmethod
    def Friendly(cls):
        return 20


def matchResult(homeWinProbability, awayWinProbability):
    homeShoots = round(random.randint(0, 5) * homeWinProbability)
    awayShoots = round(random.randint(0, 5) * awayWinProbability)

    if homeWinProbability < awayWinProbability / 4 and homeShoots == 0:
        homeShoots += 1

    if awayWinProbability < homeWinProbability / 4 and awayShoots == 0:
        awayShoots += 1

    homeGoals = 0
    awayGoals = 0

    for _ in range(homeShoots):
        attack = 5 * random.random() + 5 * homeWinProbability * random.random()
        defence = 5 * random.random() + 5 * awayWinProbability * random.random(
        )
        if attack > defence:
            homeGoals += 1

    for _ in range(awayShoots):
        attack = 10 * random.random() + awayWinProbability
        defence = 10 * random.random() + homeWinProbability
        if attack > defence:
            awayGoals += 1

    return homeGoals, awayGoals


def playMatch(homeTeam: Team, awayTeam: Team, matchModifier=40, homeOffset=50):
    homeWinningProbability = Team.winningProbability(homeTeam, awayTeam, homeOffset)
    awayWiningProbability = Team.winningProbability(awayTeam, homeTeam, 0)
    homeGoals, awayGoals = matchResult(homeWinningProbability, awayWiningProbability)
    homeTeam.newRating(matchModifier, homeGoals - awayGoals, homeWinningProbability)
    awayTeam.newRating(matchModifier, awayGoals - homeGoals, awayWiningProbability)
    homeTeam.addMatch(homeGoals, awayGoals)
    awayTeam.addMatch(awayGoals, homeGoals)
    return homeGoals, awayGoals
