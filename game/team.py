import random


class Team:
    """
    Objects describing a team by means of name, statistics and playing characteristics
    """

    def __init__(self, name, elo=1500):
        self.name = name
        self.elo = elo
        self.played = 0
        self.goals = [0, 0, 0]
        self.stats = [0, 0, 0]

    def data(self):
        return {
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

    def attackScore(self):
        return random.randint(0, 10)

    def defenceScore(self):
        return random.randint(0, 10)

    def middlefieldScore(self):
        return random.randint(0, 10)
