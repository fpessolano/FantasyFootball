#!/usr/bin/env python3
"""
Fantasy Football Manager - Simplified
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Main application entry point using CLI interface for the main menu only.
"""

import sys
import signal
import os
import random
from typing import Optional, List

from interface.cli_interface import CLIInterface
from interface.constants import MAIN_MENU
from interface.player_menu import PlayerMenu
from interface.team_menu import TeamMenu
from interface.match_menu import MatchMenu
from interface.tournament_menu import TournamentMenu
from interface.player_statistics_menu import PlayerStatisticsMenu
from interface.team_statistics_menu import TeamStatisticsMenu
from interface.settings_menu import SettingsMenu
from core.models import Position, TacticalStyle
from core.managers.player_manager import PlayerManager
from core.managers.team_manager import TeamManager
from core.engines.match_engine import MatchEngine
from core.managers.tournament_manager import TournamentManager
from core.engines.statistics_engine import PlayerStatisticsManager


class FantasyFootballManager:
    """Simplified Fantasy Football Manager with main menu only."""
    
    def __init__(self):
        self.cli = CLIInterface()
        self.running = True
        self.player_manager = PlayerManager()
        self.team_manager = TeamManager()
        self.match_engine = MatchEngine()
        self.tournament_manager = TournamentManager(self.team_manager, self.player_manager)
        self.stats_manager = PlayerStatisticsManager()
        # Set up signal handler for graceful Ctrl+C
        signal.signal(signal.SIGINT, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Handle Ctrl+C signal gracefully."""
        print("\n\nGracefully exiting Fantasy Football Manager...")
        print("Thank you for playing!")
        quit()
    
    def run(self):
        """Main application loop."""
        print("Starting Fantasy Football Manager...")
        
        while self.running:
            try:
                # Display main menu and get user choice
                choice = self.cli.display_menu_and_select(
                    MAIN_MENU, 
                    "FANTASY FOOTBALL MANAGER v2.3.1"
                )
                
                # Handle user choice
                self.handle_main_menu_choice(choice, MAIN_MENU)
            except Exception as e:
                print(f"\nAn error occurred: {e}")
                input("Press Enter to continue...")
    
    def handle_main_menu_choice(self, choice_index: int, options: list):
        """Handle the main menu choice."""
        
        if choice_index == -1:  # User interrupted (Ctrl+C) - CLI already handled exit
            return
            
        if choice_index == len(options) - 1:  # Exit option
            print("Thank you for playing Fantasy Football Manager!")
            self.running = False
            return
        
        # Route to appropriate menu
        match choice_index:
            case 0:  # Player Management
                player_menu = PlayerMenu(self.player_manager)
                player_menu.show()
            case 1:  # Team Management
                team_menu = TeamMenu(self.team_manager, self.player_manager)
                team_menu.show()
            case 2:  # Match Mode
                match_menu = MatchMenu(self.team_manager, self.player_manager, self.match_engine)
                match_menu.show()
            case 3:  # Tournament Mode
                tournament_menu = TournamentMenu(self.tournament_manager, self.team_manager, self.player_manager)
                tournament_menu.show()
            case 4:  # Player Statistics & Leaderboards
                player_stats_menu = PlayerStatisticsMenu(self.stats_manager, self.player_manager, self.tournament_manager)
                player_stats_menu.show()
            case 5:  # Team Statistics & Leaderboards
                team_stats_menu = TeamStatisticsMenu(self.team_manager, self.tournament_manager)
                team_stats_menu.show()
            case 6:  # Settings
                settings_menu = SettingsMenu(self.match_engine)
                settings_menu.show()
            case _:
                print(f"\nOption Not Available {options[choice_index]}")
                input("Press Enter to continue...")


def main():
    """Entry point for the application."""
    app = FantasyFootballManager()
    app.run()


if __name__ == "__main__":
    main()