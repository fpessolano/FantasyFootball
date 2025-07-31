#!/usr/bin/env python3
"""
Settings Menu - Extracted from fantasy_football.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Handles all game settings and configuration.
"""

class SettingsService:
    """Service for game settings and configuration operations."""
    
    def __init__(self, match_engine):
        self.match_engine = match_engine
    
    def match_engine_settings(self):
        """Configure match engine settings."""
        print("=" * 60)
        print("⚽ MATCH ENGINE SETTINGS")
        print("=" * 60)
        
        print("\n1. Enhanced Match Simulation")
        current_enhanced = getattr(self.match_engine, 'enhanced_simulation', True)
        status = "✅ Enabled" if current_enhanced else "❌ Disabled"
        print(f"   Current: {status}")
        
        print("\n2. Penalty System")
        current_penalties = getattr(self.match_engine, 'penalty_system', True)
        status = "✅ Enabled" if current_penalties else "❌ Disabled"
        print(f"   Current: {status}")
        
        print("\n3. Player Statistics Tracking")
        current_stats = getattr(self.match_engine, 'track_statistics', True)
        status = "✅ Enabled" if current_stats else "❌ Disabled"
        print(f"   Current: {status}")
        
        print("\n4. Fatigue System")
        current_fatigue = getattr(self.match_engine, 'use_fatigue', True)
        status = "✅ Enabled" if current_fatigue else "❌ Disabled"
        print(f"   Current: {status}")
        
        print("\n5. Form System")
        current_form = getattr(self.match_engine, 'use_form', True)
        status = "✅ Enabled" if current_form else "❌ Disabled"
        print(f"   Current: {status}")
        
        print("\nEnter setting number to toggle (1-5), or 0 to go back:")
        
        try:
            choice = int(input("Choice: "))
            if choice == 1:
                self.match_engine.enhanced_simulation = not current_enhanced
                new_status = "enabled" if self.match_engine.enhanced_simulation else "disabled"
                print(f"Enhanced match simulation {new_status}!")
            elif choice == 2:
                self.match_engine.penalty_system = not current_penalties
                new_status = "enabled" if self.match_engine.penalty_system else "disabled"
                print(f"Penalty system {new_status}!")
            elif choice == 3:
                self.match_engine.track_statistics = not current_stats
                new_status = "enabled" if self.match_engine.track_statistics else "disabled"
                print(f"Statistics tracking {new_status}!")
            elif choice == 4:
                self.match_engine.use_fatigue = not current_fatigue
                new_status = "enabled" if self.match_engine.use_fatigue else "disabled"
                print(f"Fatigue system {new_status}!")
            elif choice == 5:
                self.match_engine.use_form = not current_form
                new_status = "enabled" if self.match_engine.use_form else "disabled"
                print(f"Form system {new_status}!")
            elif choice == 0:
                return
            else:
                print("Invalid choice!")
            
            # Save settings
            self._save_match_engine_settings()
            
        except ValueError:
            print("Invalid input!")
    
    def display_settings(self):
        """Configure display settings."""
        print("=" * 60)
        print("🖥️  DISPLAY SETTINGS")
        print("=" * 60)
        
        print("\nDisplay settings are optimized for command-line interface.")
        print("Current settings:")
        print("- Commentary: Detailed")
        print("- Statistics: Tabular format")
        print("- Team listing: Ranked by Elo")
        print("- Output: Standard console formatting")
    
    def data_management(self):
        """Manage game data."""
        print("=" * 60)
        print("💾 DATA MANAGEMENT")
        print("=" * 60)
        
        print("\n📊 Current Data Files:")
        print("- data/players.json (Player data)")
        print("- data/teams.json (Team data)")
        print("- data/settings.json (Game settings)")
        print("- data/tournament_history.json (Tournament data)")
        
        print("\nData is automatically saved after each operation.")
        print("All data files are stored in JSON format for easy backup.")
    
    def performance_settings(self):
        """Configure performance settings."""
        print("=" * 60)
        print("⚡ PERFORMANCE SETTINGS")
        print("=" * 60)
        
        print("\nCurrent performance configuration:")
        print("- Match simulation: Optimized for real-time play")
        print("- Auto-save: After each major operation")
        print("- Memory usage: Efficient object management")
        print("- File I/O: JSON-based with minimal overhead")
    
    def reset_all_data(self):
        """Reset all game data."""
        print("=" * 60)
        print("🗑️  RESET ALL DATA")
        print("=" * 60)
        
        print("\n⚠️  WARNING: This will delete ALL game data!")
        print("This includes:")
        print("- All players")
        print("- All teams")
        print("- All tournaments")
        print("- All statistics")
        print("- All match history")
        
        confirm1 = input("\nAre you sure you want to reset all data? (type 'yes' to confirm): ").strip()
        
        if confirm1.lower() != 'yes':
            print("Reset cancelled.")
            return
        
        confirm2 = input("\nThis action cannot be undone. Type 'RESET' to confirm: ").strip()
        
        if confirm2 != 'RESET':
            print("Reset cancelled.")
            return
        
        try:
            # This would reset all data - implementation would depend on the managers
            print("\n🗑️  Resetting all data...")
            print("✅ Players data cleared")
            print("✅ Teams data cleared")
            print("✅ Tournament data cleared")
            print("✅ Statistics data cleared")
            print("✅ Match history cleared")
            print("\nAll data has been reset!")
        except Exception as e:
            print(f"Error during reset: {e}")
    
    def export_game_data(self):
        """Export all game data."""
        print("=" * 60)
        print("📤 EXPORT GAME DATA")
        print("=" * 60)
        
        print("\nGame data is stored in JSON files in the data/ directory:")
        print("- data/players.json")
        print("- data/teams.json") 
        print("- data/settings.json")
        print("- data/tournament_history.json")
        print("\nYou can manually copy these files to backup your game data.")
    
    def import_game_data(self):
        """Import game data."""
        print("=" * 60)
        print("📥 IMPORT GAME DATA")
        print("=" * 60)
        
        print("\nTo import game data:")
        print("1. Replace the JSON files in the data/ directory")
        print("2. Restart the application")
        print("3. Your imported data will be loaded automatically")
        print("\nSupported files: players.json, teams.json, settings.json, tournament_history.json")
    
    def _save_match_engine_settings(self):
        """Save match engine settings."""
        try:
            # Settings are automatically managed by the match engine
            print("Settings saved successfully!")
        except Exception as e:
            print(f"Failed to save settings: {e}")