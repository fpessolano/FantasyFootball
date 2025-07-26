import random
import tabulate

from core.simulation import simulator as game_simulator
from core.entities.team import Team
from utils.database import SaveFile
from utils.screen import highlight_table_row
from core.simulation import scheduling as sc

# TODO: using disk based file saving, concurrent access an issue. 

class League:
    """
    Optimized League class with dictionary-based team storage for O(1) lookups.
    
    Key improvements:
    - Teams stored in dictionary by name for O(1) access
    - Maintains backwards compatibility with index-based operations
    - Enhanced for regular internet data updates
    """
    def __init__(self,
                 teams,
                 league_name='My League',
                 my_team=None,
                 relegation_zone=0,
                 season=1,
                 schedule_recovery_params=[5, 1, 3],
                 is_random_league=False):
        """
        initialises a new instance
        :param league_name: league name
        :param relegation_zone: how many teams are relegated
        :param teams: the league team objects
        :param schedule_recovery_params: regulates the usage of saved generated schedules
        """

        self.league_name = league_name
        self.season = season
        self.is_random_league = is_random_league
        
        # Goal tracking for calibration
        self.__season_total_goals = 0
        self.__season_total_matches = 0
        if my_team is not None:
          self.my_team = teams[my_team].name
        else:
          self.my_team = None
        self.my_team_position = 0
        self.__result_color = "green"
        self.__berger_schedule = []
        self.__calendar = []
        self.__state_file = SaveFile('data.dat')
        self.completed = False  # Track if season is complete
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
        
        # Optimized team storage
        self.__teams = {}  # Dictionary for O(1) lookups by name
        self.__team_order = []  # List to maintain order for matches (index-based compatibility)
        
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
            # Populate teams with optimized storage
            for i, team in enumerate(teams):
                self.__teams[team.name] = team
                self.__team_order.append(team.name)
            random.shuffle(self.__team_order)

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

    def get_team_by_name(self, name: str) -> Team:
        """Get team by name - O(1) lookup."""
        return self.__teams.get(name)
    
    def get_team_by_index(self, index: int) -> Team:
        """Get team by index - for backwards compatibility."""
        if 0 <= index < len(self.__team_order):
            team_name = self.__team_order[index]
            return self.__teams[team_name]
        return None

    def data(self):
        """
        returns the league data in a readable DICT
        :return: a dict of all league data
        """
        # Convert teams back to list format for save compatibility
        teams_list = [self.__teams[name] for name in self.__team_order]
        
        return {
            "week": self.__current_week,
            "teams": teams_list,
            "calendar": self.__berger_schedule,
            "relegationZone": self.__relegation_zone,
            "spare": self.__fakeTeam,
            "name": self.league_name,
            "season": self.season,
            "myteam": self.my_team,
            "is_random_league": self.is_random_league,
            "season_total_goals": self.__season_total_goals,
            "season_total_matches": self.__season_total_matches
        }

    def __order_standings(self, showStars=False):
        """
        Generate the standings based on the points and goal stats - OPTIMIZED
        :return: a ordered list
        """

        if not self.valid:
            return "", []
        
        teams_weight = {}
        zeros = 0
        
        # Use team names for sorting instead of indices
        for i, team_name in enumerate(self.__team_order):
            team = self.__teams[team_name]
            team_data = team.data()
            teams_weight[i] = team_data["PT"] + team_data["GD"] / 100 + team_data[
                "GF"] / 1000 - team_data["GA"] / 1000000
            if teams_weight[i] == 0:
                zeros += 1
                
        if len(self.__team_order) == zeros:
            teams_weight = {}
            for i, team_name in enumerate(self.__team_order):
                teams_weight[i] = team_name
            reverse = False
        else:
            reverse = True
            
        teams_weight = sorted(teams_weight.items(),
                              key=lambda x: x[1],
                              reverse=reverse)
        ordered_teams = []
        ordered_teams_ids = []
        
        for weight in teams_weight:
            team_index = weight[0]
            team_name = self.__team_order[team_index]
            team = self.__teams[team_name]
            ordered_teams.append(team.data(showStars))
            ordered_teams_ids.append(team_index)

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
        Execute a match day with all matches and rested teams - OPTIMIZED
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
        """Process a single match - OPTIMIZED for dictionary access."""
        if self.__fakeTeam in match:
            return 
            
        # Get teams by index (backwards compatible)
        team1 = self.get_team_by_index(match[0])
        team2 = self.get_team_by_index(match[1])
        
        if not team1 or not team2:
            return
            
        msg0 = team1.name + " vs " + team2.name
        result = game_simulator.play_match(team1, team2, league_name=self.league_name, is_random_league=self.is_random_league, league_instance=self)
        msg1 = str(result[0]) + " - " + str(result[1])
        match_results.append([msg0, msg1])
        
        # Track goals for rolling average
        self.add_match_goals(result[0], result[1])
        
        # Determine result color for user's team
        if team1.name == self.my_team:
          if result[0] == result[1]:
            self.__result_color = "yellow"
          elif result[0] < result[1]:
            self.__result_color = "red"
        elif team2.name == self.my_team:
          if result[0] == result[1]:
            self.__result_color = "yellow"
          elif result[0] > result[1]:
            self.__result_color = "red"
        return 

    def prepare_new_season(self):
        """
        adjusts team data for the next season - OPTIMIZED
        """
        # Increment season
        self.season += 1
        self.completed = False
        self.__current_week = 0
        
        # Reset season goal tracking
        self.reset_season_stats()
        
        # Reset all teams
        for team in self.__teams.values():
            team.reset()
            
        # Calculate stars for all teams
        teams_list = list(self.__teams.values())
        Team.calculate_stars(teams_list)
        
        # Shuffle team order
        random.shuffle(self.__team_order)
        self.__current_week = 0

    def promoted(self, new_teams):
        """
        replaces relegated teams with promoted teams - OPTIMIZED
        :param new_teams: the promoted teams
        """
        _, ordered_teams_ids = self.__order_standings()
        
        for i in range(self.__relegation_zone):
            team_index = ordered_teams_ids[-1 - i]
            if len(new_teams) > 0:
                # Remove old team
                old_team_name = self.__team_order[team_index]
                del self.__teams[old_team_name]
                
                # Add new team
                new_team = new_teams.pop()
                self.__teams[new_team.name] = new_team
                self.__team_order[team_index] = new_team.name
            else:
                break

    def relegation_zone(self):
        return self.__relegation_zone

    def team_number(self):
        return self.__number_teams

    def teams(self):
        """Return list of team names."""
        return [self.__teams[name].name for name in self.__team_order]

    def restore(self, savedState):
        """
        restore the league from the provided data - OPTIMIZED
        :param savedState: dict containing all necessary league data
        """
        self.__current_week = savedState["week"]
        self.__berger_schedule = savedState["calendar"]
        self.__calendar = sc.generate_calendar(self.__berger_schedule)
        self.__relegation_zone = savedState["relegationZone"]
        self.__fakeTeam = savedState["spare"]
        self.league_name = savedState["name"]
        self.season = savedState.get("season", 1)  # Default to 1 if not present
        self.my_team = savedState["myteam"]
        self.is_random_league = savedState.get("is_random_league", False)  # Default to False for old saves
        
        # Restore goal tracking stats
        self.__season_total_goals = savedState.get("season_total_goals", 0)
        self.__season_total_matches = savedState.get("season_total_matches", 0)

        # Restore teams with optimized storage
        self.__teams = {}
        self.__team_order = []
        
        for i, team_data in enumerate(savedState["teams"]):
            team = Team(full_definition=team_data)
            self.__teams[team.name] = team
            self.__team_order.append(team.name)

        self.__number_teams = len(self.__teams)
        self.valid = (self.__number_teams > 2) and (self.__number_teams > self.__relegation_zone) and \
                        sc.calendar_valid(self.__berger_schedule)
    
    def order_list(self) -> list:
        """Get ordered list of team indices by standings."""
        _, ordered_teams_ids = self.__order_standings()
        return ordered_teams_ids
    
    def current_match_day(self) -> int:
        """Get the current match day number."""
        return self.__current_week + 1
    
    def get_current_fixtures(self) -> list:
        """Get fixtures for the current match day."""
        if self.__current_week >= len(self.__calendar):
            return []
        return self.__calendar[self.__current_week]
    
    def advance_match_day(self):
        """Advance to the next match day."""
        self.__current_week += 1
        if self.__current_week >= len(self.__calendar):
            self.completed = True
    
    def simulate_match(self, home_idx: int, away_idx: int) -> tuple:
        """
        Simulate a match between two teams.
        
        Args:
            home_idx: Index of home team
            away_idx: Index of away team
            
        Returns:
            Tuple of (home_score, away_score)
        """
        # Skip if fake team is involved (odd number of teams)
        if self.__fakeTeam in [home_idx, away_idx]:
            return (0, 0)
            
        # Use existing match simulation logic
        home_team = self.get_team_by_index(home_idx)
        away_team = self.get_team_by_index(away_idx)
        
        # Check if teams are valid before simulation
        if home_team is None or away_team is None:
            # Return default score if teams are invalid
            return (0, 0)
        
        # Run the simulation with league context
        home_score, away_score = game_simulator.play_match(home_team, away_team, league_name=self.league_name, is_random_league=self.is_random_league, league_instance=self)
        
        # Track goals for rolling average
        self.add_match_goals(home_score, away_score)
        
        return home_score, away_score
    
    def get_my_team_index(self) -> int:
        """Get the index of the user's team."""
        if self.my_team is None:
            return None
        
        for i, team_name in enumerate(self.__team_order):
            if team_name == self.my_team:
                return i
        return None
    
    def add_match_goals(self, home_goals: int, away_goals: int):
        """Track goals for rolling average calculation."""
        self.__season_total_goals += home_goals + away_goals
        self.__season_total_matches += 1
    
    def get_season_average_goals(self) -> float:
        """Get current season rolling average goals per match."""
        if self.__season_total_matches == 0:
            return 0.0
        return self.__season_total_goals / self.__season_total_matches
    
    def get_season_match_count(self) -> int:
        """Get number of matches played this season."""
        return self.__season_total_matches
    
    def reset_season_stats(self):
        """Reset season goal tracking stats."""
        self.__season_total_goals = 0
        self.__season_total_matches = 0
