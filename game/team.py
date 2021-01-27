import random


# TODO add injury and injury tracking
#  hide elo (call it rating)
#  re-order anc clean methids

class Team:
    """
    Objects describing a team by means of name, statistics and playing characteristics
    """

    __minElo = 1000
    __eloHalfStep = 100

    def __init__(self, name, elo=1500):
        self.name = name
        self.__elo = elo
        self.__oldEdo = elo
        self.played = 0
        self.goals = [0, 0, 0]
        self.stats = [0, 0, 0]
        self.stars = 0

    def data(self, showStars=False):
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
        if showStars:
            data["STARS"] = self.stars
        return data

    def addMatch(self, scored, conceived):
        self.played += 1
        if scored > conceived:
            self.stats[0] += 1
        elif scored == conceived:
            self.stats[1] += 1
        else:
            self.stats[2] += 1
        self.goals[0] += scored
        self.goals[1] += conceived
        self.goals[2] += scored - conceived

    def reset(self):
        self.played = 0
        self.goals = [0, 0, 0]
        self.stats = [0, 0, 0]
        self.adjustRating()

    @classmethod
    def calculateStars(cls, teamList):
        eloList = []
        for el in teamList:
            eloList.append(el.__elo)
        maxElo = max(eloList)
        cls.__eloHalfStep = (maxElo - cls.__minElo) / 10
        for el in teamList:
            el.stars = max(((el.__elo - cls.__minElo) // cls.__eloHalfStep) / 2, 0.5)

    # @classmethod
    # def eloFromStars(cls, stars, team):
    #     team.__oldEdo = team.__elo
    #     team.__elo = cls.__minElo + 2.05 * stars * cls.__eloHalfStep
    #     team.stars = stars

    def eloFromStars(self, stars, reset):
        newElo = Team.__minElo + 2.05 * stars * Team.__eloHalfStep
        if reset:
            self.__oldEdo = newElo
        else:
            self.__oldEdo = self.__elo
        self.__elo = newElo
        self.stars = stars

    # todo use to adjust elo at the end of the season
    #  test
    def adjustRating(self):
        elo = self.__elo
        self.__elo = self.__oldEdo + (self.__elo - self.__oldEdo) / 3
        self.__oldEdo = elo

    def rating(self):
        return self.__elo

    def __injuries(self):
        # TODO make a proper model
        return random.uniform(0.85, 1)

    @classmethod
    def winningProbability(cls, homeTeam, awayTeam, homeOffset):
        deltaElo = (homeTeam.__elo + homeOffset) * homeTeam.__injuries() - awayTeam.__elo
        return float(1 / (10 ** (deltaElo / -400) + 1))

    def newRating(self, matchModifier, goalDifference, winProbability):
        if goalDifference > 0:
            result = 1
        elif goalDifference == 0:
            result = 0.5
        else:
            result = 0
        if goalDifference < 2:
            modifier = 1
        elif goalDifference == 2:
            modifier = 1.5
        else:
            modifier = 1 + (3 / 4 + (goalDifference - 3) / 8)
        self.__elo = float(self.__elo + matchModifier * modifier *
                           (result - winProbability))
