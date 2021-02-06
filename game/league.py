import random

import tabulate

import game.simulator as elo
from game.team import Team
from support.diskstore import SaveFile
import game.scheduling as sc


class League:
    """
    Object that define a league including all teams, calendar, and all related methods
    """

    def __init__(self, teams, team='My League', relegationZone=0):
        """
        initialises a new instance
        :param team: league name
        :param relegationZone: how many teams are relegated
        :param teams: the league team names
        """

        self.leagueName = team
        self.__schedule = []
        self.__stateFile = SaveFile('data.dat')
        if not teams:
            self.valid = False
            return
        numberTeams = len(teams)
        if (numberTeams < 2) or (numberTeams < relegationZone):
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
        minimumSet = 5
        if self.__numberTeams > 16:
            minimumSet = 1
        elif self.__numberTeams > 10:
            minimumSet = 3
        if not self.__readSchedule(minimumSet):
            # self.__generateScheduleStepwise()
            self.__schedule, _ = sc.bergerTableSchedule(self.__numberTeams)
            self.__saveSchedule()
        self.valid = sc.calendarValid(self.__schedule)
        if self.valid:
            # the league is populated with teams
            for team in teams:
                self.__teams.append(team)

    def restore(self, savedState):
        """
        restore the league from the provided data
        :param savedState: dict containing all necessary league data
        """
        self.__currentWeek = savedState["week"]
        self.__teams = savedState["teams"]
        self.__schedule = savedState["calendar"]
        self.__relegationZone = savedState["relegationZone"]
        self.__fakeTeam = savedState["spare"]
        self.leagueName = savedState["name"]
        self.__numberTeams = len(self.__teams)
        self.valid = (self.__numberTeams > 2) and (self.__numberTeams > self.__relegationZone) and \
                     sc.calendarValid(self.__schedule)

    def __readSchedule(self, minimumSet=5):
        """
        Read schedule from ones previously stored
        :param minimumSet: if not 0 it will expect a 'randomize' number of schedules to pick one at random or fails
        :return: a valid true if a valid schedule has been found and set
        """

        savedSchedules = self.__stateFile.readState(str(self.__numberTeams))
        if not savedSchedules:
            return False
        elif len(savedSchedules) < minimumSet:
            return False
        else:
            random.shuffle(savedSchedules)
            self.__schedule = savedSchedules[0]
            return True

    def __saveSchedule(self):
        """
        Save a new schedule to file
        """

        savedSchedules = self.__stateFile.readState(str(self.__numberTeams))
        if not savedSchedules:
            savedSchedules = []
        skip = False
        rows, cols = len(self.__schedule), len(self.__schedule[0])
        for el in savedSchedules:
            skip = all([self.__schedule[i][j] == el[i][j] for j in range(cols) for i in range(rows)])
            if skip:
                print('skip')
                break
        if not skip:
            savedSchedules.append(self.__schedule)
        self.__stateFile.writeState(str(self.__numberTeams), savedSchedules)

    def data(self):
        """
        returns the league data in a readable DICT
        :return: a dict of all league data
        """

        return {
            "week": self.__currentWeek,
            "teams": self.__teams,
            "calendar": self.__schedule,
            "relegationZone": self.__relegationZone,
            "spare": self.__fakeTeam,
            "name": self.leagueName
        }

    def __orderStandings(self, showStars=False):
        """
        Generate the standings based on the points and goal stats
        :return: a ordered list
        """

        if not self.valid:
            return "", []
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
            orderedTeams.append(self.__teams[weight[0]].data(showStars))
            orderedTeamsIds.append(weight[0])
        return orderedTeams, orderedTeamsIds

    def orderStanding(self, showStars=False):
        """
        convert an ordered list of teams representing the standings into a tabulated string
        :return:  a string with the tabulated standings
        """

        orderedTeams, _ = self.__orderStandings(showStars)
        header = ['Position']
        header += orderedTeams[0].keys()
        rows = [x.values() for x in orderedTeams]
        for i in range(len(rows)):
            rows[i] = [i + 1] + list(rows[i])
        return tabulate.tabulate(rows, header)

    def matchDay(self):
        """
        Execute a match day with all matches and rested teams
        :return: a tabulated string with all match results
        """

        if self.valid:
            halfSeason = len(self.__schedule[0])
            if self.__currentWeek >= 2 * halfSeason:
                return ""
            playingTeams = []
            matchResults = []
            for team in range(len(self.__schedule)):
                if team not in playingTeams:
                    if self.__currentWeek < halfSeason:
                        self._singleMatch(0, matchResults, playingTeams, team)
                    else:
                        self._singleMatch(halfSeason, matchResults, playingTeams, team)
                    playingTeams.append(team)
            self.__currentWeek += 1
            header = ["WEEK " + str(self.__currentWeek), "RESULTS"]
            rows = [x for x in matchResults]
            return tabulate.tabulate(rows, header)
        else:
            return ""

    def _singleMatch(self, offset, matchResults, playingTeams, team):
        msg1 = ""
        if team == self.__fakeTeam:
            msg0 = self.__teams[self.__schedule[team][self.__currentWeek - offset]].name + " rests "
        elif self.__schedule[team][self.__currentWeek - offset] == self.__fakeTeam:
            msg0 = self.__teams[team].name + " rests"
        else:
            if offset == 0:
                homeTeam = team
                awayTeam = self.__schedule[team][self.__currentWeek]
            else:
                homeTeam = self.__schedule[team][self.__currentWeek - offset]
                awayTeam = team
            msg0 = self.__teams[homeTeam].name + " vs " + self.__teams[awayTeam].name
            # result = Simulator.playMatch(self.__teams[homeTeam], self.__teams[awayTeam])
            result = elo.playMatch(self.__teams[homeTeam], self.__teams[awayTeam])
            msg1 = str(result[0]) + " - " + str(result[1])
            # self.__teams[homeTeam] = result[2]
            # self.__teams[awayTeam] = result[3]
        playingTeams.append(self.__schedule[team][self.__currentWeek - offset])
        matchResults.append([msg0, msg1])

    def prepareNewSeason(self):
        """
        adjusts team data for the next season
        """

        for i in range(len(self.__teams)):
            self.__teams[i].reset()
        Team.calculateStars(self.__teams)
        random.shuffle(self.__teams)
        self.__currentWeek = 0

    def promoted(self, teams):
        """
        replaces relegated teams with promoted teams. If not enough promoted teams are given
        it leave the relegated team in
        :param teams: the promoted teams
        """

        _, orderedTeamsIds = self.__orderStandings()
        for i in range(self.__relegationZone):
            teamNumber = orderedTeamsIds[-1 - i]
            if len(teams) > 0:
                newTeam = teams.pop()
                # self.__teams[teamNumber].name = newTeam
                self.__teams[teamNumber] = newTeam
            else:
                break

    def relegationZone(self):
        return self.__relegationZone

    def teamNumber(self):
        return self.__numberTeams

    def teams(self):
        return [x.name for x in self.__teams]
