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

    def __init__(self, teams, team='My League', relegation_zone=0):
        """
        initialises a new instance
        :param team: league name
        :param relegation_zone: how many teams are relegated
        :param teams: the league team names
        """

        self.league_name = team
        self.__schedule = []
        self.__state_file = SaveFile('data.dat')
        if not teams:
            self.valid = False
            return
        number_teams = len(teams)
        if (number_teams < 2) or (number_teams < relegation_zone):
            self.valid = False
            return
        # number of teams is forced to be even internally for the schedule calculation
        if number_teams % 2 != 0:
            self.__fakeTeam = number_teams
            number_teams += 1
        else:
            self.__fakeTeam = -1
        self.__number_teams = number_teams
        self.__teams = []
        self.__relegation_zone = relegation_zone
        self.__current_week = 0
        minimum_set = 5
        if self.__number_teams > 16:
            minimum_set = 1
        elif self.__number_teams > 10:
            minimum_set = 3
        if not self.__read_schedule(minimum_set):
            # self.__generateScheduleStepwise()
            self.__schedule, _ = sc.berger_table_schedule(self.__number_teams)
            self.__save_schedule()
        self.valid = sc.calendar_valid(self.__schedule)
        if self.valid:
            # the league is populated with teams
            for team in teams:
                self.__teams.append(team)

    def restore(self, savedState):
        """
        restore the league from the provided data
        :param savedState: dict containing all necessary league data
        """
        self.__current_week = savedState["week"]
        self.__teams = savedState["teams"]
        self.__schedule = savedState["calendar"]
        self.__relegation_zone = savedState["relegationZone"]
        self.__fakeTeam = savedState["spare"]
        self.league_name = savedState["name"]
        self.__number_teams = len(self.__teams)
        self.valid = (self.__number_teams > 2) and (self.__number_teams > self.__relegation_zone) and \
                     sc.calendar_valid(self.__schedule)

    def __read_schedule(self, minimum_set=5):
        """
        Read schedule from ones previously stored
        :param minimum_set: if not 0 it will expect a 'randomize' number of schedules to pick one at random or fails
        :return: a valid true if a valid schedule has been found and set
        """

        saved_schedules = self.__state_file.read_state(str(self.__number_teams))
        if not saved_schedules:
            return False
        elif len(saved_schedules) < minimum_set:
            return False
        else:
            random.shuffle(saved_schedules)
            self.__schedule = saved_schedules[0]
            return True

    def __save_schedule(self):
        """
        Save a new schedule to file
        """

        saved_schedules = self.__state_file.read_state(str(self.__number_teams))
        if not saved_schedules:
            saved_schedules = []
        skip = False
        rows, cols = len(self.__schedule), len(self.__schedule[0])
        for el in saved_schedules:
            skip = all([self.__schedule[i][j] == el[i][j] for j in range(cols) for i in range(rows)])
            if skip:
                print('skip')
                break
        if not skip:
            saved_schedules.append(self.__schedule)
        self.__state_file.write_state(str(self.__number_teams), saved_schedules)

    def data(self):
        """
        returns the league data in a readable DICT
        :return: a dict of all league data
        """

        return {
            "week": self.__current_week,
            "teams": self.__teams,
            "calendar": self.__schedule,
            "relegationZone": self.__relegation_zone,
            "spare": self.__fakeTeam,
            "name": self.league_name
        }

    def __order_standings(self, showStars=False):
        """
        Generate the standings based on the points and goal stats
        :return: a ordered list
        """

        if not self.valid:
            return "", []
        teams_weight = {}
        zeros = 0
        for i in range(len(self.__teams)):
            team = self.__teams[i].data()
            teams_weight[i] = team["PT"] + team["GD"] / 100 + team["GF"] / 1000 - team["GA"] / 1000000
            if teams_weight[i] == 0:
                zeros += 1
        if len(self.__teams) == zeros:
            teams_weight = {}
            for i in range(len(self.__teams)):
                teams_weight[i] = self.__teams[i].name
            reverse = False
        else:
            reverse = True
        teams_weight = sorted(teams_weight.items(), key=lambda x: x[1], reverse=reverse)
        ordered_teams = []
        ordered_teams_ids = []
        weight: tuple
        for weight in teams_weight:
            ordered_teams.append(self.__teams[weight[0]].data(showStars))
            ordered_teams_ids.append(weight[0])
        return ordered_teams, ordered_teams_ids

    def order_standing(self, showStars=False):
        """
        convert an ordered list of teams representing the standings into a tabulated string
        :return:  a string with the tabulated standings
        """

        ordered_teams, _ = self.__order_standings(showStars)
        header = ['Position']
        header += ordered_teams[0].keys()
        rows = [x.values() for x in ordered_teams]
        for i in range(len(rows)):
            rows[i] = [i + 1] + list(rows[i])
        return tabulate.tabulate(rows, header)

    def match_day(self):
        """
        Execute a match day with all matches and rested teams
        :return: a tabulated string with all match results
        """

        if self.valid:
            half_season = len(self.__schedule[0])
            if self.__current_week >= 2 * half_season:
                return ""
            playing_teams = []
            match_results = []
            for team in range(len(self.__schedule)):
                if team not in playing_teams:
                    if self.__current_week < half_season:
                        self._single_match(0, match_results, playing_teams, team)
                    else:
                        self._single_match(half_season, match_results, playing_teams, team)
                    playing_teams.append(team)
            self.__current_week += 1
            header = ["WEEK " + str(self.__current_week), "RESULTS"]
            rows = [x for x in match_results]
            return tabulate.tabulate(rows, header)
        else:
            return ""

    def _single_match(self, offset, match_results, playing_teams, team):
        msg1 = ""
        if team == self.__fakeTeam:
            msg0 = self.__teams[self.__schedule[team][self.__current_week - offset]].name + " rests "
        elif self.__schedule[team][self.__current_week - offset] == self.__fakeTeam:
            msg0 = self.__teams[team].name + " rests"
        else:
            if offset == 0:
                home_team = team
                away_team = self.__schedule[team][self.__current_week]
            else:
                home_team = self.__schedule[team][self.__current_week - offset]
                away_team = team
            msg0 = self.__teams[home_team].name + " vs " + self.__teams[away_team].name
            # result = Simulator.playMatch(self.__teams[homeTeam], self.__teams[away_team])
            result = elo.play_match(self.__teams[home_team], self.__teams[away_team])
            msg1 = str(result[0]) + " - " + str(result[1])
            # self.__teams[homeTeam] = result[2]
            # self.__teams[away_team] = result[3]
        playing_teams.append(self.__schedule[team][self.__current_week - offset])
        match_results.append([msg0, msg1])

    def prepare_new_season(self):
        """
        adjusts team data for the next season
        """

        for i in range(len(self.__teams)):
            self.__teams[i].reset()
        Team.calculate_stars(self.__teams)
        random.shuffle(self.__teams)
        self.__current_week = 0

    def promoted(self, teams):
        """
        replaces relegated teams with promoted teams. If not enough promoted teams are given
        it leave the relegated team in
        :param teams: the promoted teams
        """

        _, ordered_teams_ids = self.__order_standings()
        for i in range(self.__relegation_zone):
            team_number = ordered_teams_ids[-1 - i]
            if len(teams) > 0:
                new_team = teams.pop()
                # self.__teams[team_number].name = new_team
                self.__teams[team_number] = new_team
            else:
                break

    def relegation_zone(self):
        return self.__relegation_zone

    def team_number(self):
        return self.__number_teams

    def teams(self):
        return [x.name for x in self.__teams]
