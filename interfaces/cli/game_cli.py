from core.entities.league import League
from interfaces.cli.user_input import promotion_and_relegation
import interfaces.cli.user_input as ti
from utils.screen import clear
from utils.shelve_db_store import GameData
from core.storage.team_storage import initialize_team_storage
from core.storage.data_updater import check_and_update_data
import json
import os


class FFM:
    """
    The Fantasy Football Manager game class
    """
    def __init__(self, user_id, version="0.7.1"):
        """
        setting up the basic game variables
        :param user_id: needed for save and load operations only
        :param version: game version for display
        """
        self.user_id = user_id
        self.version = version
        if user_id:
            self.user_data = GameData(user_id)
        else:
            self.user_data = None
        self.league = League([])
        
        # Initialize optimized team storage if raw data is available
        self._initialize_team_storage()
        
        # Check for weekly data updates
        self._check_weekly_updates()

    def new(self):
        """
        creates a new game
        :return: False in case it fails
        """
        while True:
            command = input(
                "(E)xisting, (R)andomize or (C)ustom league?  ").lower()
            if command == 'e':
                league_name, relegation_zone, teams, my_team = ti.existing_league()
                break
            elif command == 'r':
                league_name, relegation_zone, teams, my_team = ti.random_teams()
                break
            elif command == 'c':
                league_name, relegation_zone, teams, my_team = ti.fully_custom_league()
                break

        self.league = League(league_name=league_name,
                             teams=teams,
                             my_team=my_team,
                             relegation_zone=relegation_zone)
        return self.league.valid

    def load(self):
        """
        load a saved game
        """
        saves = ', '.join(self.user_data.saved_game_list())
        print(f'Available saved games: {saves}')
        save_game_name = input("Provide the save game name please (enter for \'Autosave\')? ")
        if save_game_name == "":
            saved_game = "Autosave"
            # return False
        saved_game = self.user_data.read_game(save_game_name)
        if not saved_game:
            return False
        try:
          saved_game = json.loads(saved_game)
        except json.JSONDecodeError as e:
          print(f"Failed to parse saved game: {e}")
          return False
        except Exception as e:
          print(f"Unexpected error loading game: {e}")
          return False
        self.league.restore(saved_game)
        return True

    def play_round(self):
        """
        plays a game round or complete season
        """
        clear()
        print(
            f'\nWelcome to league {self.league.league_name}\n\n{self.league.order_standing(True)}\n'
        )

        season_completed = False
        while not season_completed:
            command = ""
            while command != "F" and command != "C" and command != "Q":
                command = input(
                    "(F)inalise season, (C)ontinue to a single game or (Q)uit? "
                ).upper()
                clear()
                if command != "F" and command != "C" and command != "Q":
                    print("!!! ERROR: please write a valid command !!!")
            if command == "C":
                match_day = self.league.match_day()
                if match_day == "":
                    season_completed = True
                else:
                    print(f'\n{match_day}\n')
                print(
                    f"\nCurrent standings are:\n\n{self.league.order_standing()}\n"
                )
            elif command == "F":
                # finish to run the season
                show_matches = input(
                    "Do you want to see all results (y for yes)? ").lower()
                match_day = self.league.match_day()
                while match_day != "":
                    if show_matches == 'y':
                        print(f'\n{match_day}')
                    match_day = self.league.match_day()
                season_completed = True
                print()
            else:
                self.save_end()
                return False
        print(
            f"\nThe season has finished. The final standings are:\n\n{self.league.order_standing()}\n"
        )
        if self.league.relegation_zone() > 0:
            promoted_teams = promotion_and_relegation(self.league)
            if len(promoted_teams) > 0:
                self.league.promoted(promoted_teams)
        self.league.prepare_new_season()
        return True

    def save_end(self):
        """
        ends the game
        """
        if not self.user_data:
          print("\nThanks for playing!")
          return
        if input(
                "Do you want to save the game (y for yes or anything else for no)? "
        ).lower() == "y":
            save_game_name = input(
                "Please give me the save name (enter for \'Autosave\')? ")
            if save_game_name == "":
                save_game_name = "Autosave"
            else:
                save_game_name.strip().replace(" ", "_")
            self.user_data.save_game(save_game_name, self.league.data())
        print("\nThanks for playing!")

    def _initialize_team_storage(self):
        """Initialize the optimized team storage system if raw data is available."""
        try:
            # Use the correct path - initialize_team_storage has its own path resolution
            success = initialize_team_storage()
            # Silent initialization - no output messages during game startup
        except Exception as e:
            # Silent error handling - no output messages during game startup
            pass

    def _check_weekly_updates(self):
        """Check for and perform weekly team rating updates."""
        try:
            # Check if updates are needed (silently)
            update_performed = check_and_update_data(show_progress=False)
            
            # Only show message if update was actually performed
            if update_performed:
                print("📈 Team ratings have been updated with latest data")
                
        except Exception as e:
            # Silent error handling
            pass

    def new_game(self):
        """Create a new game - wrapper for new() method for consistency."""
        if self.new():
            self._play_game_loop()

    def load_game(self):
        """Load a saved game - wrapper for load() method for consistency."""
        if self.load():
            self._play_game_loop()
    
    def _play_game_loop(self):
        """Main game loop that continues across multiple seasons."""
        while True:
            continue_playing = self.play_round()
            if not continue_playing:
                # Player chose to quit or game ended
                break

    def _show_title_screen(self):
        """Display the game title screen."""
        from termcolor import colored
        user_id_colored = colored(self.user_id, "green")
        version_colored = colored(self.version, "blue")
        print("""
******************************************************
*                                                    *""")
        print("*" + f'Welcome {user_id_colored} to'.center(61) + "*")
        print("""*                                                    *
*                                                    *
*      ______          _                             *
*     |  ____|        | |                            *
*     | |__ __ _ _ __ | |_ __ _ ___ _   _            *
*     |  __/ _` | '_ \\| __/ _` / __| | | |           *
*     | | | (_| | | | | || (_| \\\\__ \\\\ |_| |           * 
*     |_|  \\\\__,_|_| |_|\\\\__\\\\__,_|___/\\\\__, |           *
*     |  \\/  |                       __/ |           *
*     | \\  / | __ _ _ __   __ _  __ |___/_ _ __      *
*     | |\\/| |/ _` | '_ \\ / _` |/ _` |/ _ \\ '__|     *
*     | |  | | (_| | | | | (_| | (_| |  __/ |        *
*     |_|  |_|\\\\__,_|_| |_|\\\\__,_|\\\\__, |\\\\___|_|        *
*                                __/ |               *
*                               |___/                *
*                                                    *""")
        print("*" + f'Version {version_colored}'.center(61) + "*")
        print("""*                                                    *
******************************************************
  """)

    def help(self):
        """Display help information."""
        clear()
        print("""
Fantasy Football Manager - Help

Commands:
  new   - Start a new game
  load  - Load a saved game  
  help  - Show this help message
  exit  - Exit the game

Game Types:
  (E)xisting - Play with real world leagues
  (R)andom   - Generate random teams
  (C)ustom   - Create your own league

During Play:
  (F)inalize - Simulate rest of season quickly
  (C)ontinue - Play one match day at a time
  (Q)uit     - Save and exit current game
""")
        input("Press Enter to continue...")
        clear()
        self._show_title_screen()
