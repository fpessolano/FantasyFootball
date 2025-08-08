#!/usr/bin/env python3
"""
Player Menu Interface
~~~~~~~~~~~~~~~~~~~~

UI layer for player management operations.
"""

from interface.cli_interface import CLIInterface
from interface.constants import PLAYER_MENU
from service.player_service import PlayerService


class PlayerMenu:
    """Interface for player menu operations."""
    
    def __init__(self, player_manager):
        self.cli = CLIInterface()
        self.player_service = PlayerService(player_manager)
    
    def show(self):
        """Display player management menu."""
        while True:
            try:
                choice = self.cli.display_menu_and_select(
                    PLAYER_MENU, 
                    "PLAYER MANAGEMENT"
                )
                
                if choice == -1:  # User interrupted (Ctrl+C)
                    return
                
                if choice == len(PLAYER_MENU) - 1:  # Back to Main Menu
                    break
                
                # Delegate to service layer
                self._handle_choice(choice)
                
            except Exception as e:
                print(f"\nAn error occurred: {e}")
                input("Press Enter to continue...")
    
    def _handle_choice(self, choice):
        """Handle menu choice by calling appropriate service method."""
        # if choice == 0:  # View All Players
        #     self.player_service.view_all_players()
        #     input("\nPress Enter to continue...")
        # elif choice == 1:  # Create Random Player
        #     self.player_service.create_random_player()
        #     input("\nPress Enter to continue...")
        # elif choice == 2:  # Create Manual Player
        #     self.player_service.create_manual_player()
        #     input("\nPress Enter to continue...")
        # elif choice == 3:  # Generate Player Pool
        #     self.player_service.generate_player_pool()
        #     input("\nPress Enter to continue...")
        # elif choice == 4:  # Search Players
        #     self.player_service.search_players()
        #     input("\nPress Enter to continue...")
        # elif choice == 5:  # View Top Players
        #     self.player_service.view_top_players()
        #     input("\nPress Enter to continue...")

        match choice:
            case 0:  # Create Random Player
                self.player_service.create_random_player()
                input("\nPress Enter to continue...")
            case 1:  # Create Manual Player
                self.player_service.create_manual_player()
                input("\nPress Enter to continue...")
            case 2:  # Generate Player Pool
                self.player_service.generate_player_pool()
                input("\nPress Enter to continue...")
            case 3:  # Search Players
                self.player_service.search_players()
                input("\nPress Enter to continue...")
            case 4:  # View Top Players
                self.player_service.view_top_players()
                input("\nPress Enter to continue...")