#!/usr/bin/env python3
"""
Match Menu Interface
~~~~~~~~~~~~~~~~~~~

UI layer for match playing operations.
"""

from interface.cli_interface import CLIInterface
from interface.constants import MATCH_MENU
from service.match_service import MatchService


class MatchMenu:
    """Interface for match menu operations."""
    
    def __init__(self, team_manager, player_manager, match_engine):
        self.cli = CLIInterface()
        self.match_service = MatchService(team_manager, player_manager, match_engine)
    
    def show(self):
        """Display match management menu."""
        while True:
            try:
                choice = self.cli.display_menu_and_select(
                    MATCH_MENU, 
                    "⚽ MATCH MODE"
                )
                
                if choice == -1:  # User interrupted (Ctrl+C)
                    return
                
                if choice == len(MATCH_MENU) - 1:  # Back to Main Menu
                    break
                
                # Delegate to service layer
                self._handle_choice(choice)
                
            except Exception as e:
                print(f"\nAn error occurred: {e}")
                input("Press Enter to continue...")
    
    def _handle_choice(self, choice):
        """Handle menu choice by calling appropriate service method."""
        match choice:
            case 0:  # Play Single Match
                home_team, away_team = self.match_service.select_teams(random_selection=False, create_teams=False)
                if home_team and away_team:
                    self.match_service.run_matches(home_team, away_team, num_matches=1, match_title="SINGLE MATCH")
                input("\nPress Enter to continue...")
                
            case 1:  # Play Multiple Matches
                home_team, away_team = self.match_service.select_teams(random_selection=False, create_teams=False)
                if home_team and away_team:
                    try:
                        num_matches = int(input("\nHow many matches to simulate? [5]: ") or "5")
                        if num_matches > 1:
                            self.match_service.run_matches(home_team, away_team, num_matches=num_matches, match_title="MULTIPLE MATCHES")
                        else:
                            print("Number of matches must greater than 1!")
                    except ValueError:
                        print("Invalid number!")
                input("\nPress Enter to continue...")
                
            case 2:  # Play Random Match
                home_team, away_team = self.match_service.select_teams(random_selection=True, create_teams=False)
                if home_team and away_team:
                    self.match_service.run_matches(home_team, away_team, num_matches=1, match_title="RANDOM MATCH")
                input("\nPress Enter to continue...")
                
            case 3:  # Play Multiple Random Matches
                home_team, away_team = self.match_service.select_teams(random_selection=False, create_teams=True)
                if home_team and away_team:
                    try:
                        num_matches = int(input("\nHow many matches to simulate? [5]: ") or "5")
                        if num_matches > 1:
                            self.match_service.run_matches(home_team, away_team, num_matches=num_matches, match_title="MULTIPLE MATCHES WITH NEW TEAMS")
                        else:
                            print("Number of matches must greater than 1!")
                    except ValueError:
                        print("Invalid number!")
                input("\nPress Enter to continue...")