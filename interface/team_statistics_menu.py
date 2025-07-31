#!/usr/bin/env python3
"""
Team Statistics Menu Interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

UI layer for team statistics and analytics operations.
"""

from interface.cli_interface import CLIInterface
from interface.constants import TEAM_STATS_MENU
from service.team_statistics_service import TeamStatisticsService


class TeamStatisticsMenu:
    """Interface for team statistics menu operations."""
    
    def __init__(self, team_manager, tournament_manager):
        self.cli = CLIInterface()
        self.team_statistics_service = TeamStatisticsService(team_manager, tournament_manager)
    
    def show(self):
        """Display team statistics management menu."""
        while True:
            try:
                choice = self.cli.display_menu_and_select(
                    TEAM_STATS_MENU, 
                    "📊 TEAM STATISTICS & LEADERBOARDS"
                )
                
                if choice == -1:  # User interrupted (Ctrl+C)
                    return
                
                if choice == len(TEAM_STATS_MENU) - 1:  # Back to Main Menu
                    break
                
                # Delegate to service layer
                self._handle_choice(choice)
                
            except Exception as e:
                print(f"\nAn error occurred: {e}")
                input("Press Enter to continue...")
    
    def _handle_choice(self, choice):
        """Handle menu choice by calling appropriate service method."""
        if choice == 0:  # Tournament History
            self.team_statistics_service.show_tournament_history()
            input("\nPress Enter to continue...")
        elif choice == 1:  # Overall Ranking
            self.team_statistics_service.show_overall_ranking()
            input("\nPress Enter to continue...")