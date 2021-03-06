from game.league import League
from cligaming.teamUserInput import promotion_and_relegation
from support.diskstore import SaveFile
import cligaming.teamUserInput as ti


class FFM:
    """
    Teh Fantasy Football Manager game class
    """

    def __init__(self):
        """
        setting up the basic game variables
        """
        self.save_file = SaveFile("saves.dat")
        self.league = League([])

    def new(self):
        """
        creates a new game
        :return: False in case it fails
        """
        while True:
            command = input("(E)xisting, (R)andomize or (C)ustom league?  ").lower()
            if command == 'e':
                league_name, relegation_zone, teams = ti.existing_league()
                break
            elif command == 'r':
                league_name, relegation_zone, teams = ti.random_teams()
                break
            elif command == 'c':
                league_name, relegation_zone, teams = ti.fully_custom_l_eague()
                break

        self.league = League(team=league_name, teams=teams, relegation_zone=relegation_zone)
        return self.league.valid

    def load(self):
        """
        load a saved game
        """
        saves = ', '.join(self.save_file.stateList())
        print(f'Available saved games: {saves}')
        save_game_name = input("Provide the save game name (enter for \'Autosave\')? ")
        if save_game_name == "":
            save_game_name = 'Autosave'
        saved_game = self.save_file.read_state(save_game_name)
        if not saved_game:
            return False
        self.league.restore(saved_game)
        return True

    def play_round(self):
        """
        plays a game round or complete season
        """
        print(f'\nWelcome to league {self.league.league_name}\n\n{self.league.order_standing(True)}\n')

        season_completed = False
        while not season_completed:
            command = ""
            while command != "F" and command != "C" and command != "Q":
                command = input("(F)inalise season, (C)ontinue to a single game or (Q)uit? ").upper()
                if command != "F" and command != "C" and command != "Q":
                    print("!!! ERROR: please write a valid command !!!")
            if command == "C":
                match_day = self.league.match_day()
                if match_day == "":
                    season_completed = True
                else:
                    print(f'\n{match_day}\n')
                if input("Do you want to see the standings (y for yes)? ").lower() == 'y':
                    print(f"\nCurrent standings are:\n\n{self.league.order_standing()}\n")
            elif command == "F":
                # finish to run the season
                show_matches = input("Do you want to see all results (y for yes)? ").lower()
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
        print(f"\nThe season has finished. The final standings are:\n\n{self.league.order_standing()}\n")
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
        if input("Do you want to save the game (y for yes or anything else for no)? ").lower() == "y":
            save_game_name = input(f'Please give me the save name (enter for \'Autosave\')? ')
            if save_game_name == "":
                save_game_name = f"Autosave"
            else:
                save_game_name.strip().replace(" ", "_")
            self.save_file.write_state(save_game_name, self.league.data())
        print("\nThanks for playing!")

