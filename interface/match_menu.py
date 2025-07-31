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
        if choice == 0:  # Play Single Match
            self.match_service.play_single_match()
            input("\nPress Enter to continue...")
        elif choice == 1:  # Play Multiple Matches
            self.match_service.play_multiple_matches()
            input("\nPress Enter to continue...")
        elif choice == 2:  # Play Multiple Matches (Random Teams)
            self.match_service.play_multiple_random_matches()
            input("\nPress Enter to continue...")
        elif choice == 3:  # Quick Play (Random Teams)
            self.match_service.quick_play()
            input("\nPress Enter to continue...")