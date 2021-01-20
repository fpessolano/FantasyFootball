import math
import pickle
import random

import tabulate

from modules.simulator import Simulator
from modules.team import Team


class League:
    """
    Object that define a league including all teams, calendar, and all related methods
    """

    def __init__(self, numberTeams, relegationZone, loadfile=""):
        if loadfile == "" and ((numberTeams == 0 and relegationZone == 0) or
                               (numberTeams < 2) or (numberTeams < relegationZone)):
            self.valid = False
            return
        # number of teams is forced to be even internally for the schedule calculation
        if numberTeams % 2 != 0:
            self.__fakeTeam = numberTeams
            numberTeams += 1
        else:
            self.__fakeTeam = -1
        self.__numberTeams = numberTeams
        self.__teams = []
        self.__relegationZone = relegationZone
        self.__currentWeek = 0
        if loadfile != "":
            # load from a saved file
            try:
                infile = open(loadfile, 'rb')
                savedState = pickle.load(infile)
                infile.close()
                self.__currentWeek, self.__teams, self.__schedule, self.__relegationZone, self.__fakeTeam = \
                    savedState["week"], savedState["teams"], savedState["calendar"], savedState["relegationZone"], \
                    savedState["spare"]
                self.__numberTeams = len(self.__teams)
                self.valid = True
            except:
                self.valid = False
        else:
            # generate a new league
            self.__generateSchedule()
            self.valid = self.__calendarValid(self.__schedule)
            if self.valid:
                # the league is populated with teams
                teamNames = []
                print("Please provide the teams names.")
                nt = self.__numberTeams
                if self.__fakeTeam != -1:
                    nt -= 1
                for i in range(nt):
                    name = input(f'  team {i + 1} name? ').lower().title()
                    while name == "" or name in teamNames:
                        print("!!! Error: a name must be unique and not empty !!!")
                        name = input(f'  team {i + 1} name? ').lower().title()
                    teamNames.append(name)
                    self.__teams.append(Team(name=name))

    @classmethod
    def generateRandom(cls):
        ct = random.randint(0, 14)
        rz = random.randint(1, 4)
        return cls(ct + rz, rz)

    # calendarCorrectness verifies that the calendar contains no errors
    @classmethod
    def __calendarValid(cls, cal):
        if len(cal) == 0:
            return False
        ok = True
        for team in cal:
            if len(team) != len(set(team)):
                ok = False
                break
        ts = [[cal[j][i] for j in range(len(cal))] for i in range(len(cal[0]))]
        for team in cal:
            if len(team) != len(set(team)):
                ok = False
                break
        return ok

    # calculate the initial reference calendar for a given even number of teams
    # it tries to solve the completed problem for a limited number of tries (maximumTries) before giving up
    # maximumTries set to -1 uses a predefined number of maximum cycles
    # the current version does not step back at team level
    def __generateSchedule(self, maximumTries=-1):
        if maximumTries == -1:
            maximumTries = 200 * (round(math.log(self.__numberTeams, 2)) + 1)
        while True:
            # check the number of tries
            if maximumTries < 0:
                print('ops')
                return []
            maximumTries -= 1
            failed = False
            allSchedules = [[-1 for _ in range(self.__numberTeams - 1)] for _ in range(self.__numberTeams)]
            currentTeam = 0
            while currentTeam < self.__numberTeams:
                remainingOpponents = [x for x in range(self.__numberTeams) if x > currentTeam]
                random.shuffle(remainingOpponents)
                if currentTeam == 0:
                    allSchedules[currentTeam] = remainingOpponents
                    for week, opponent in enumerate(allSchedules[currentTeam]):
                        allSchedules[opponent][week] = currentTeam
                else:
                    lastAssignedWeek = -1
                    unassignedWeek = 0
                    # cycles is used to check on the cycle permutations
                    cycles = [0 for _ in range(self.__numberTeams - 1)]

                    while unassignedWeek + 1 < self.__numberTeams:
                        # we skip assignments that are from previous rows
                        if allSchedules[currentTeam][unassignedWeek] < currentTeam and \
                                allSchedules[currentTeam][unassignedWeek] != -1:
                            unassignedWeek += 1
                            continue

                        # checks if the number of iterations has covered all possible permutations
                        if cycles[unassignedWeek] > self.__numberTeams - 1 - unassignedWeek:
                            if lastAssignedWeek == -1:
                                # the current row is given up with its current predecessors
                                failed = True
                                break
                            else:
                                opponent = allSchedules[currentTeam][lastAssignedWeek]
                                allSchedules[opponent][lastAssignedWeek] = -1
                                remainingOpponents.insert(len(remainingOpponents), opponent)
                                cycles[unassignedWeek] = 0
                                unassignedWeek = lastAssignedWeek
                                lastAssignedWeek = -1
                                for i in range(unassignedWeek - 1, -1, -1):
                                    if allSchedules[currentTeam][i] > currentTeam:
                                        lastAssignedWeek = i
                                        break
                                continue

                        cycles[unassignedWeek] += 1

                        # this failsafe is redundant
                        for c in cycles:
                            if c > self.__numberTeams:
                                return []

                        availableOpponents = remainingOpponents.copy()

                        # this failsafe is redundant
                        if len(remainingOpponents) != len(list(set(remainingOpponents))):
                            return []

                        if len(availableOpponents) > 2:
                            opponentFound = False
                            while len(availableOpponents) > 0:
                                opponent = availableOpponents.pop(0)
                                opponentBusy = False
                                for team, schedule in enumerate(allSchedules):
                                    if team != currentTeam:
                                        if schedule[unassignedWeek] == opponent:
                                            opponentBusy = True
                                            break
                                if not opponentBusy:
                                    allSchedules[currentTeam][unassignedWeek] = opponent
                                    allSchedules[opponent][unassignedWeek] = currentTeam
                                    remainingOpponents.remove(opponent)
                                    lastAssignedWeek = unassignedWeek
                                    unassignedWeek += 1
                                    opponentFound = True
                                    break
                            if not opponentFound:
                                if lastAssignedWeek == -1:
                                    # the current row is given up with its current predecessors
                                    failed = True
                                    break
                                else:
                                    # step back and move previously assigned opponet to the tail of the queue
                                    opponent = allSchedules[currentTeam][lastAssignedWeek]
                                    allSchedules[opponent][lastAssignedWeek] = -1
                                    remainingOpponents.insert(len(remainingOpponents), opponent)
                                    cycles[unassignedWeek] = 0
                                    unassignedWeek = lastAssignedWeek
                                    lastAssignedWeek = -1
                                    for i in range(unassignedWeek - 1, -1, -1):
                                        if allSchedules[currentTeam][i] > currentTeam:
                                            lastAssignedWeek = i
                                            break
                        elif len(availableOpponents) == 2:
                            # last two we try and swap once
                            opponentBusy = False
                            for team, schedule in enumerate(allSchedules):
                                if team != currentTeam:
                                    if schedule[unassignedWeek] == availableOpponents[0]:
                                        opponentBusy = True
                                        break
                            if opponentBusy:
                                if lastAssignedWeek == -1:
                                    # the current row is given up with its current predecessors
                                    failed = True
                                    break
                                # step back and move previously assigned opponet to the tail of the queue
                                opponent = allSchedules[currentTeam][lastAssignedWeek]
                                allSchedules[opponent][lastAssignedWeek] = -1
                                remainingOpponents.insert(len(remainingOpponents), opponent)
                                cycles[unassignedWeek] = 0
                                unassignedWeek = lastAssignedWeek
                                lastAssignedWeek = -1
                                for i in range(unassignedWeek - 1, -1, -1):
                                    if allSchedules[currentTeam][i] > currentTeam:
                                        lastAssignedWeek = i
                                        break
                            else:
                                opponent = availableOpponents.pop(0)
                                allSchedules[currentTeam][unassignedWeek] = opponent
                                allSchedules[opponent][unassignedWeek] = currentTeam
                                remainingOpponents.remove(opponent)
                                lastAssignedWeek = unassignedWeek
                                unassignedWeek += 1
                        else:
                            # last team we just check
                            opponent = availableOpponents[0]
                            opponentBusy = False
                            for team, schedule in enumerate(allSchedules):
                                if team != currentTeam:
                                    if schedule[unassignedWeek] == opponent:
                                        opponentBusy = True
                                        break
                            if opponentBusy:
                                if lastAssignedWeek == -1:
                                    # the current row is given up with its current predecessors
                                    failed = True
                                    break
                                # step back and move previously assigned opponet to the tail of the queue
                                opponent = allSchedules[currentTeam][lastAssignedWeek]
                                allSchedules[opponent][lastAssignedWeek] = -1
                                remainingOpponents.insert(len(remainingOpponents), opponent)
                                cycles[unassignedWeek] += 0
                                unassignedWeek = lastAssignedWeek
                                lastAssignedWeek = -1
                                for i in range(unassignedWeek - 1, -1, -1):
                                    if allSchedules[currentTeam][i] > currentTeam:
                                        lastAssignedWeek = i
                                        break
                            else:
                                allSchedules[currentTeam][unassignedWeek] = opponent
                                allSchedules[opponent][unassignedWeek] = currentTeam
                                break
                if failed:
                    break
                currentTeam += 1
            if not failed:
                break
        self.__schedule = allSchedules.copy()

    # saveGame saves a game
    def saveGame(self):
        if self.valid:
            filename = input("Please give me the save name (enter for default)? ")
            if filename == "":
                filename = "default.save"
            saveData = {
                "week": self.__currentWeek,
                "teams": self.__teams,
                "calendar": self.__schedule,
                "relegationZone": self.__relegationZone,
                "spare": self.__fakeTeam
            }
            outfile = open(filename, 'wb')
            pickle.dump(saveData, outfile)
            outfile.close()
        return self.valid

    # return a ordered lost of teams representing the standings
    def __orderStandings(self):
        if not self.valid:
            return ""
        teamsWeight = {}
        zeros = 0
        for i in range(len(self.__teams)):
            team = self.__teams[i].data()
            teamsWeight[i] = team["PT"] + team["GD"] / 100 + team["GF"] / 1000 - team["GA"] / 1000000
            if teamsWeight[i] == 0:
                zeros += 1
        if len(self.__teams) == zeros:
            teamsWeight = {}
            for i in range(len(self.__teams)):
                teamsWeight[i] = self.__teams[i].name
            reverse = False
        else:
            reverse = True
        teamsWeight = sorted(teamsWeight.items(), key=lambda x: x[1], reverse=reverse)
        orderedTeams = []
        orderedTeamsIds = []
        weight: tuple
        for weight in teamsWeight:
            orderedTeams.append(self.__teams[weight[0]].data())
            orderedTeamsIds.append(weight[0])
        return orderedTeams, orderedTeamsIds

    # return a string with the current tabulated standings
    def orderStanding(self):
        orderedTeams, _ = self.__orderStandings()
        header = orderedTeams[0].keys()
        rows = [x.values() for x in orderedTeams]
        return tabulate.tabulate(rows, header)

    # execute a match day returning the results in a string
    def matchDay(self):
        if self.valid:
            halfSeason = len(self.__schedule[0])
            if self.__currentWeek >= 2 * halfSeason:
                return ""
            playingTeams = []
            matchResults = []
            for team in range(len(self.__schedule)):
                if team not in playingTeams:
                    if self.__currentWeek < halfSeason:
                        msg1 = ""
                        if team == self.__fakeTeam:
                            msg0 = self.__teams[self.__schedule[team][self.__currentWeek]].name + " rests"
                        elif self.__schedule[team][self.__currentWeek] == self.__fakeTeam:
                            msg0 = self.__teams[team].name + " rests"
                        else:
                            homeTeam = team
                            awayTeam = self.__schedule[team][self.__currentWeek]
                            msg0 = self.__teams[homeTeam].name + " vs " + self.__teams[awayTeam].name
                            result = Simulator.playMatch(self.__teams[homeTeam], self.__teams[awayTeam])
                            msg1 = str(result[0]) + " - " + str(result[1])
                            self.__teams[homeTeam] = result[2]
                            self.__teams[awayTeam] = result[3]
                        playingTeams.append(self.__schedule[team][self.__currentWeek])
                        matchResults.append([msg0, msg1])
                    else:
                        msg1 = ""
                        if team == self.__fakeTeam:
                            msg0 = self.__teams[self.__schedule[team][self.__currentWeek - halfSeason]].name + " rests "
                        elif self.__schedule[team][self.__currentWeek - halfSeason] == self.__fakeTeam:
                            msg0 = self.__teams[team].name + " rests"
                        else:
                            homeTeam = self.__schedule[team][self.__currentWeek - halfSeason]
                            awayTeam = team
                            msg0 = self.__teams[homeTeam].name + " vs " + self.__teams[awayTeam].name
                            result = Simulator.playMatch(self.__teams[homeTeam], self.__teams[awayTeam])
                            msg1 = str(result[0]) + " - " + str(result[1])
                            self.__teams[homeTeam] = result[2]
                            self.__teams[awayTeam] = result[3]
                        playingTeams.append(self.__schedule[team][self.__currentWeek - halfSeason])
                        matchResults.append([msg0, msg1])
                    playingTeams.append(team)
            self.__currentWeek += 1
            header = ["WEEK " + str(self.__currentWeek), "RESULTS"]
            rows = [x for x in matchResults]
            return tabulate.tabulate(rows, header)
        else:
            return ""

    # adjust team data for the next season
    def prepareNewSeason(self):
        for i in range(len(self.__teams)):
            self.__teams[i].reset()
        random.shuffle(self.__teams)
        self.__currentWeek = 0

    # replace relegated teams with promoted teams. If not enough promoted teams are given
    #  it leave the relegated team in
    def promoted(self, teams):
        _, orderedTeamsIds = self.__orderStandings()
        for i in range(self.__relegationZone):
            teamNumber = orderedTeamsIds[-1 - i]
            if len(teams) > 0:
                newTeam = teams.pop()
                self.__teams[teamNumber].name = newTeam
            else:
                break

    def relegationZone(self):
        return self.__relegationZone

    def teamNumber(self):
        return self.__numberTeams

    def teams(self):
        return [x.name for x in self.__teams]

