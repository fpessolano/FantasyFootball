import random

from modules.team import Team


class Simulator:
    def __init__(self):
        pass

    @classmethod
    def playMatch(cls, home: Team, away: Team):
        maxShots = random.randint(0, 10)
        homeAttacks = random.randint(0, maxShots)
        awayAttacks = random.randint(0, maxShots)
        homeGoals = 0
        awayGoals = 0
        for _ in range(homeAttacks):
            if home.attackScore() > away.defenceScore():
                homeGoals += 1
        for _ in range(awayAttacks):
            if away.attackScore() > home.defenceScore():
                awayGoals += 1
        home.addMatch(homeGoals, awayGoals)
        away.addMatch(awayGoals, homeGoals)
        return [homeGoals, awayGoals, home, away]