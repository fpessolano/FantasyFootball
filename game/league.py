import random
import tabulate

import game.simulator as game_simulator
from game.team import Team
from support.diskstore import SaveFile
from support.screen_utils import highlight_table_row
import game.scheduling as sc

# TODO: using disk based file saving, concurrent access an issue. 

class League:
    """
    Object that define a league including all teams, calendar, and all related methods
    """
    def __init__(self,
                 teams,
                 league_name='My League',
                 my_team=None,
                 relegation_zone=0,
                 schedule_recovery_params=[5, 1, 3]):
        """
        initialises a new instance
        :param league_name: league name
        :param relegation_zone: how many teams are relegated
        :param teams: the league team names
        :param schedule_recovery_params: regulates the usage of saved generated schedules
        """

        self.league_name = league_name
        if my_team:
          self.my_team = teams[my_team].name
        else:
          self.my_team = None
        self.my_team_position = 0
        self.__result_color = "green"
        self.__berger_schedule = []
        self.__calendar = []
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
        
        minimum_set = schedule_recovery_params[0]
        if self.__number_teams > 16:
            minimum_set = schedule_recovery_params[1]
        elif self.__number_teams > 10:
            minimum_set = schedule_recovery_params[2]
        if not self.__read_berger_schedule(minimum_set):
            self.__berger_schedule, _ = sc.berger_table_schedule(
                self.__number_teams)
            self.__save_schedule()
        self.__calendar = sc.generate_calendar(self.__berger_schedule)
        self.valid = sc.calendar_valid(self.__berger_schedule)
        if self.valid:
            # the league is populated with teams
            for team in teams:
                self.__teams.append(team)
            random.shuffle(self.__teams)

    def __read_berger_schedule(self, minimum_set=5):
        """
        Read schedule from ones previously stored
        :param minimum_set: if not 0 it will expect a 'randomize' number of schedules to pick one at random or fails
        :return: a valid true if a valid schedule has been found and set
        """

        saved_schedules = self.__state_file.read_state(str(
            self.__number_teams))
        if not saved_schedules:
            return False
        elif len(saved_schedules) < minimum_set:
            return False
        else:
            random.shuffle(saved_schedules)
            self.__berger_schedule = saved_schedules[0]
            return True

    def __save_schedule(self):
        """
        Save a new schedule to file
        """

        saved_schedules = self.__state_file.read_state(str(
            self.__number_teams))
        if not saved_schedules:
            saved_schedules = []
        skip = False
        rows, cols = len(self.__berger_schedule), len(
            self.__berger_schedule[0])
        for el in saved_schedules:
            skip = all([
                self.__berger_schedule[i][j] == el[i][j] for j in range(cols)
                for i in range(rows)
            ])
            if skip:
                print('skip')
                break
        if not skip:
            saved_schedules.append(self.__berger_schedule)
        self.__state_file.write_state(str(self.__number_teams),
                                      saved_schedules)

    def data(self):
        """
        returns the league data in a readable DICT
        :return: a dict of all league data
        """

        return {
            "week": self.__current_week,
            "teams": self.__teams,
            "calendar": self.__berger_schedule,
            "relegationZone": self.__relegation_zone,
            "spare": self.__fakeTeam,
            "name": self.league_name,
            "myteam": self.my_team
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
            teams_weight[i] = team["PT"] + team["GD"] / 100 + team[
                "GF"] / 1000 - team["GA"] / 1000000
            if teams_weight[i] == 0:
                zeros += 1
        if len(self.__teams) == zeros:
            teams_weight = {}
            for i in range(len(self.__teams)):
                teams_weight[i] = self.__teams[i].name
            reverse = False
        else:
            reverse = True
        teams_weight = sorted(teams_weight.items(),
                              key=lambda x: x[1],
                              reverse=reverse)
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
            if rows[i][1] == self.my_team:
             self.my_team_position = rows[i][0]
        table = tabulate.tabulate(rows, header)
        table = highlight_table_row(table, self.my_team_position-1)
        return table

    def match_day(self):
        """
        Execute a match day with all matches and rested teams
        :return: a tabulated string with all match results
        """

        if self.valid:
            half_season = len(self.__berger_schedule[0])
            if self.__current_week >= 2 * half_season:
                return ""
            match_results = []
            self.__result_color = "green"
            for match in self.__calendar[self.__current_week]:
                self._single_match(match_results, match)
            self.__current_week += 1
            header = ["WEEK " + str(self.__current_week), "RESULTS"]
            rows = [x for x in match_results]
            highlight_row = -1
            for ids, row in enumerate(rows):
              if self.my_team in row[0]:
                highlight_row = ids
                break
            table = tabulate.tabulate(rows, header)
            if highlight_row >= 0:

              table = highlight_table_row(table=table, row_number=highlight_row, color=self.__result_color)
            return table
        else:
            return ""

    def _single_match(self, match_results, match):
        if self.__fakeTeam in match:
            return 
        msg0 = self.__teams[match[0]].name + " vs " + self.__teams[
            match[1]].name
        result = game_simulator.play_match(self.__teams[match[0]], self.__teams[match[1]])
        msg1 = str(result[0]) + " - " + str(result[1])
        match_results.append([msg0, msg1])
        if self.__teams[match[0]].name == self.my_team:
          if result[0] == result[1]:
            self.__result_color = "yellow"
          elif result[0] < result[1]:
            self.__result_color = "red"
        elif self.__teams[match[1]].name == self.my_team:
          if result[0] == result[1]:
            self.__result_color = "yellow"
          elif result[0] > result[1]:
            self.__result_color = "red"
        return 

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
                self.__teams[team_number] = new_team
            else:
                break

    def relegation_zone(self):
        return self.__relegation_zone

    def team_number(self):
        return self.__number_teams

    def teams(self):
        return [x.name for x in self.__teams]

    def restore(self, savedState):
        """
        restore the league from the provided data
        :param savedState: dict containing all necessary league data
        """

        self.__current_week = savedState["week"]
        self.__berger_schedule = savedState["calendar"]
        self.__calendar = sc.generate_calendar(self.__berger_schedule)
        self.__relegation_zone = savedState["relegationZone"]
        self.__fakeTeam = savedState["spare"]
        self.league_name = savedState["name"]
        self.my_team = savedState["myteam"]

        self.__teams = []
        for team in savedState["teams"]:
            self.__teams.append(Team(full_definition=team))

        self.__number_teams = len(self.__teams)
        self.valid = (self.__number_teams > 2) and (self.__number_teams > self.__relegation_zone) and \
                        sc.calendar_valid(self.__berger_schedule)
