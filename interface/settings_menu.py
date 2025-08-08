#!/usr/bin/env python3
"""
Settings Menu Interface
~~~~~~~~~~~~~~~~~~~~~~~

UI layer for game settings and configuration.
"""

from interface.cli_interface import CLIInterface
from interface.constants import SETTINGS_MENU
from service.settings_service import SettingsService


class SettingsMenu:
    """Interface for settings menu operations."""
    
    def __init__(self, match_engine):
        self.cli = CLIInterface()
        self.settings_service = SettingsService(match_engine)
    
    def show(self):
        """Display settings management menu."""
        while True:
            try:
                choice = self.cli.display_menu_and_select(
                    SETTINGS_MENU, 
                    "⚙️  GAME SETTINGS"
                )
                
                if choice == -1:  # User interrupted (Ctrl+C)
                    return
                
                if choice == len(SETTINGS_MENU) - 1:  # Back to Main Menu
                    break
                
                # Delegate to service layer
                self._handle_choice(choice)
                
            except Exception as e:
                print(f"\nAn error occurred: {e}")
                input("Press Enter to continue...")
    
    def _handle_choice(self, choice):
        """Handle menu choice by calling appropriate service method."""
        match choice:
            case 0:  # Match Engine Settings
                self.settings_service.match_engine_settings()
                input("\nPress Enter to continue...")
            case 1:  # Display Settings
                self.settings_service.display_settings()
                input("\nPress Enter to continue...")
            case 2:  # Data Management
                self.settings_service.data_management()
                input("\nPress Enter to continue...")
            case 3:  # Performance Settings
                self.settings_service.performance_settings()
                input("\nPress Enter to continue...")
            case 4:  # Reset All Data
                self.settings_service.reset_all_data()
                input("\nPress Enter to continue...")
            case 5:  # Export Game Data
                self.settings_service.export_game_data()
                input("\nPress Enter to continue...")
            case 6:  # Import Game Data
                self.settings_service.import_game_data()
                input("\nPress Enter to continue...")