#!/usr/bin/env python3
"""
Team Menu Interface
~~~~~~~~~~~~~~~~~~

UI layer for team management operations.
"""

from interface.cli_interface import CLIInterface
from interface.constants import TEAM_MENU
from service.team_service import TeamService


class TeamMenu:
    """Interface for team menu operations."""
    
    def __init__(self, team_manager, player_manager):
        self.cli = CLIInterface()
        self.team_service = TeamService(team_manager, player_manager)
    
    def show(self):
        """Display team management menu."""
        while True:
            try:
                choice = self.cli.display_menu_and_select(
                    TEAM_MENU, 
                    "TEAM MANAGEMENT"
                )
                
                if choice == -1:  # User interrupted (Ctrl+C)
                    return
                
                if choice == len(TEAM_MENU) - 1:  # Back to Main Menu
                    break
                
                # Delegate to service layer
                self._handle_choice(choice)
                
            except Exception as e:
                print(f"\nAn error occurred: {e}")
                input("Press Enter to continue...")
    
    def _handle_choice(self, choice):
        """Handle menu choice by calling appropriate service method."""
        match choice:
            case 0:  # View All Teams
                self.team_service.view_all_teams()
                input("\nPress Enter to continue...")
            case 1:  # Create Random Team
                self.team_service.create_random_team()
                input("\nPress Enter to continue...")
            case 2:  # Create Manual Team
                self.team_service.create_manual_team()
                input("\nPress Enter to continue...")
            case 3:  # Create National Team
                self.team_service.create_national_team()
                input("\nPress Enter to continue...")
            case 4:  # Create Mixed Nationality Team
                self.team_service.create_mixed_nationality_team()
                input("\nPress Enter to continue...")
            case 5:  # Create Continental Team
                self.team_service.create_continental_team()
                input("\nPress Enter to continue...")
            case 6:  # View Team Details
                self.team_service.view_team_details()
                input("\nPress Enter to continue...")
            case 7:  # Modify Team
                self.team_service.modify_team()
            case 8:  # Delete Team
                self.team_service.delete_team()
                input("\nPress Enter to continue...")
            case 9:  # Check Nationality Availability
                self.team_service.check_nationality_availability()
                input("\nPress Enter to continue...")