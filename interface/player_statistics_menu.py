#!/usr/bin/env python3
"""
Player Statistics Menu Interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

UI layer for player statistics and analytics operations.
"""

from interface.cli_interface import CLIInterface
from interface.constants import PLAYER_STATS_MENU
from service.player_statistics_service import PlayerStatisticsService


class PlayerStatisticsMenu:
    """Interface for player statistics menu operations."""
    
    def __init__(self, stats_manager, player_manager, tournament_manager):
        self.cli = CLIInterface()
        self.player_statistics_service = PlayerStatisticsService(stats_manager, player_manager, tournament_manager)
    
    def show(self):
        """Display statistics management menu."""
        while True:
            try:
                choice = self.cli.display_menu_and_select(
                    PLAYER_STATS_MENU, 
                    "📊 PLAYER STATISTICS & LEADERBOARDS"
                )
                
                if choice == -1:  # User interrupted (Ctrl+C)
                    return
                
                if choice == len(PLAYER_STATS_MENU) - 1:  # Back to Main Menu
                    break
                
                # Delegate to service layer
                self._handle_choice(choice)
                
            except Exception as e:
                print(f"\nAn error occurred: {e}")
                input("Press Enter to continue...")
    
    def _handle_choice(self, choice):
        """Handle menu choice by calling appropriate service method."""
        if choice == 0:  # Career Statistics Leaders
            self.player_statistics_service.show_career_leaders()
            input("\nPress Enter to continue...")
        elif choice == 1:  # Tournament Statistics Leaders
            self.player_statistics_service.show_tournament_leaders()
            input("\nPress Enter to continue...")
        elif choice == 2:  # Individual Player Analysis
            self.player_statistics_service.show_individual_analysis()
            input("\nPress Enter to continue...")
        elif choice == 3:  # Tournament History
            self.player_statistics_service.show_tournament_history()
            input("\nPress Enter to continue...")
        elif choice == 4:  # Player Performance Comparison
            self.player_statistics_service.show_performance_comparison()
            input("\nPress Enter to continue...")
        elif choice == 5:  # Export Statistics
            self.player_statistics_service.export_statistics()
            input("\nPress Enter to continue...")