#!/usr/bin/env python3
"""
Tournament Menu Interface
~~~~~~~~~~~~~~~~~~~~~~~~~

UI layer for tournament management operations.
"""

from interface.cli_interface import CLIInterface
from interface.constants import TOURNAMENT_MENU
from service.tournament_service import TournamentService


class TournamentMenu:
    """Interface for tournament menu operations."""
    
    def __init__(self, tournament_manager, team_manager, player_manager):
        self.cli = CLIInterface()
        self.tournament_service = TournamentService(tournament_manager, team_manager, player_manager)
    
    def show(self):
        """Display tournament management menu."""
        while True:
            try:
                choice = self.cli.display_menu_and_select(
                    TOURNAMENT_MENU, 
                    "🏆 TOURNAMENT MODE"
                )
                
                if choice == -1:  # User interrupted (Ctrl+C)
                    return
                
                if choice == len(TOURNAMENT_MENU) - 1:  # Back to Main Menu
                    break
                
                # Delegate to service layer
                self._handle_choice(choice)
                
            except Exception as e:
                print(f"\nAn error occurred: {e}")
                input("Press Enter to continue...")
    
    def _handle_choice(self, choice):
        """Handle menu choice by calling appropriate service method."""
        if choice == 0:  # Create New Tournament
            self.tournament_service.create_tournament()
            input("\nPress Enter to continue...")
        elif choice == 1:  # Continue Existing Tournament
            self.tournament_service.continue_tournament()
            input("\nPress Enter to continue...")
        elif choice == 2:  # View Tournament Bracket
            self.tournament_service.view_tournament_bracket()
            input("\nPress Enter to continue...")
        elif choice == 3:  # Show Tournament List
            self.tournament_service.show_tournament_list()
            input("\nPress Enter to continue...")
        elif choice == 4:  # Rename Tournament
            self.tournament_service.rename_tournament()
            input("\nPress Enter to continue...")
        elif choice == 5:  # Delete Tournament
            self.tournament_service.delete_tournament()
            input("\nPress Enter to continue...")