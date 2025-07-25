"""
Enhanced Game CLI using Rich Terminal UI

This module provides an enhanced command-line interface for the Fantasy Football Manager
using the Rich library for beautiful terminal output.
"""

from typing import Optional, List, Tuple, Dict
import time

from core.entities.league import League
from interfaces.cli.rich_interface_simple import SimpleRichInterface
from interfaces.cli.user_input import promotion_and_relegation
import interfaces.cli.user_input as ti
from utils.shelve_db_store import GameData
from core.storage.team_storage import initialize_team_storage
from core.storage.data_updater import check_and_update_data
import json
import os


class RichFFM:
    """Enhanced Fantasy Football Manager game class with Rich UI."""
    
    def __init__(self, user_id: str, version: str = "0.9.0", theme: str = "dark"):
        """
        Initialize the game with Rich UI support.
        
        Args:
            user_id: User identifier for save/load operations
            version: Game version for display
            theme: Color theme ("light" or "dark")
        """
        self.user_id = user_id
        self.version = version
        self.ui = SimpleRichInterface(theme)
        
        if user_id:
            self.user_data = GameData(user_id)
        else:
            self.user_data = None
            
        self.league = League([])
        
        # Initialize team storage and check for updates
        self._initialize_team_storage()
        self._check_weekly_updates()
        
    def _initialize_team_storage(self):
        """Initialize the optimized team storage system if raw data is available."""
        try:
            success = initialize_team_storage()
        except Exception:
            pass
            
    def _check_weekly_updates(self):
        """Check for and perform weekly team rating updates."""
        try:
            update_performed = check_and_update_data(show_progress=False)
            if update_performed:
                self.ui.console.print("📈 Team ratings have been updated with latest data", style="green")
        except Exception:
            pass
            
    def start(self):
        """Start the game with Rich UI."""
        self.ui.display_title_screen(self.user_id, self.version)
        self._main_menu_loop()
        
    def _main_menu_loop(self):
        """Main menu loop with Rich UI."""
        while True:
            command = self.ui.display_main_menu()
            
            if command == "help":
                self._show_help()
            elif command == "new":
                if self.new():
                    self._play_game_loop()
            elif command == "load":
                if self.load():
                    self._play_game_loop()
            elif command == "exit":
                self.ui.console.print("\n[bold green]Thanks for playing Fantasy Football Manager![/bold green]")
                break
            else:
                self.ui.console.print("[red]Unknown command. Type 'help' for available commands.[/red]")
                
    def _show_help(self):
        """Display help information with Rich formatting."""
        self.ui.console.clear()
        
        help_text = self.ui.get_help_text()
        
        self.ui.console.print(help_text)
        input("\nPress Enter to continue...")
        self.ui.console.clear()
        self.ui.display_title_screen(self.user_id, self.version)
        
    def new(self) -> bool:
        """Create a new game with Rich UI enhancements."""
        self.ui.console.clear()
        self.ui.console.print("[bold cyan]Starting New Game[/bold cyan]\n")
        
        while True:
            self.ui.console.print("[bold]Choose game type:[/bold]")
            self.ui.console.print("  [cyan](E)[/cyan]xisting - Play with real world leagues")
            self.ui.console.print("  [cyan](R)[/cyan]andom   - Generate random teams")
            self.ui.console.print("  [cyan](C)[/cyan]ustom   - Create your own league\n")
            
            command = input("Your choice: ").lower()
            
            if command == 'e':
                self.ui.show_loading("Loading real world leagues...")
                league_name, relegation_zone, teams, my_team = ti.existing_league()
                break
            elif command == 'r':
                self.ui.show_loading("Generating random teams...")
                league_name, relegation_zone, teams, my_team = ti.random_teams()
                break
            elif command == 'c':
                league_name, relegation_zone, teams, my_team = ti.fully_custom_league()
                break
            else:
                self.ui.console.print("[red]Invalid choice. Please select E, R, or C.[/red]")
                
        self.league = League(
            league_name=league_name,
            teams=teams,
            my_team=my_team,
            relegation_zone=relegation_zone
        )
        
        return self.league.valid
        
    def load(self) -> bool:
        """Load a saved game with Rich UI."""
        if not self.user_data:
            self.ui.console.print("[red]No user data available for loading games.[/red]")
            return False
            
        saves = self.user_data.saved_game_list()
        if not saves:
            self.ui.console.print("[yellow]No saved games found.[/yellow]")
            return False
            
        self.ui.console.clear()
        self.ui.console.print("[bold cyan]Load Saved Game[/bold cyan]\n")
        
        # Display saves in a nice table
        from rich.table import Table
        
        saves_table = Table(show_header=True, header_style="bold cyan")
        saves_table.add_column("Save Name", style="white")
        saves_table.add_column("League", style="green")
        saves_table.add_column("Season", style="yellow")
        
        for save_name in saves:
            # For now, just show the save name
            # In future, could load metadata about each save
            saves_table.add_row(save_name, "N/A", "N/A")
            
        self.ui.console.print(saves_table)
        self.ui.console.print("\n")
        
        save_game_name = input("Enter save game name (or press Enter for 'Autosave'): ").strip()
        if not save_game_name:
            save_game_name = "Autosave"
            
        self.ui.show_loading(f"Loading {save_game_name}...")
        
        saved_game = self.user_data.read_game(save_game_name)
        if not saved_game:
            self.ui.console.print(f"[red]Could not load save game '{save_game_name}'[/red]")
            return False
            
        try:
            saved_game = json.loads(saved_game)
            self.league.restore(saved_game)
            self.ui.console.print(f"[green]Successfully loaded {save_game_name}![/green]")
            time.sleep(1)
            return True
        except json.JSONDecodeError as e:
            self.ui.console.print(f"[red]Failed to parse saved game: {e}[/red]")
            return False
        except Exception as e:
            self.ui.console.print(f"[red]Unexpected error loading game: {e}[/red]")
            return False
            
    def _play_game_loop(self):
        """Main game loop with Rich UI enhancements."""
        while True:
            continue_playing = self._play_round()
            if not continue_playing:
                break
                
    def _play_round(self) -> bool:
        """Play a game round with enhanced UI."""
        # Clear screen for clean display
        self.ui.console.clear()
        
        # Display current standings
        my_team_idx = self.league.get_my_team_index()
        self.ui.display_league_table(self.league, my_team_idx)
        
        if self.league.completed:
            return self._handle_season_end()
            
        # Show match day options
        while True:
            self.ui.console.print("\n[bold]Options:[/bold]")
            self.ui.console.print("  [cyan](C)[/cyan]ontinue - Play next match day")
            self.ui.console.print("  [cyan](S)[/cyan]imulate - Quick simulate to end of season")
            self.ui.console.print("  [cyan](V)[/cyan]iew - View detailed standings")
            self.ui.console.print("  [cyan](Q)[/cyan]uit - Save and exit\n")
            
            command = input("Your choice: ").upper()
            
            if command == "C":
                self._play_match_day()
                break
            elif command == "S":
                self._simulate_to_end()
                break
            elif command == "V":
                my_team_idx = self.league.get_my_team_index()
                self.ui.display_league_table(self.league, my_team_idx)
            elif command == "Q":
                self._save_and_exit()
                return False
            else:
                self.ui.console.print("[red]Invalid choice![/red]")
                
        return True
        
    def _play_match_day(self):
        """Play a single match day with match viewing options."""
        fixtures = self.league.get_current_fixtures()
        if not fixtures:
            self.league.completed = True
            return
            
        # Display match day overview
        my_team_idx = self.league.get_my_team_index()
        self.ui.display_match_day_overview(self.league, fixtures, my_team_idx)
        
        command = input("\nYour choice: ").upper()
        
        if command == "S":
            # Simulate all matches quickly
            self._simulate_matches(fixtures, show_summary=True)
        elif command == "W":
            # Watch all matches
            self._watch_all_matches(fixtures)
        elif command == "F":
            # Follow only your team
            self._follow_your_team(fixtures)
        elif command == "C":
            # Choose specific matches
            self._choose_matches_to_watch(fixtures)
        else:
            # Default: simulate all
            self._simulate_matches(fixtures, show_summary=True)
            
        # Advance to next match day
        self.league.advance_match_day()
        
    def _simulate_matches(self, fixtures: List[Tuple[int, int]], show_summary: bool = True):
        """Simulate matches with optional summary display."""
        if show_summary:
            # Use live display for visible simulation
            results = self.ui.simulate_all_matches_live(fixtures, self.league)
            input("\nPress Enter to continue...")
        else:
            # Silent simulation for season end
            for home_idx, away_idx in fixtures:
                self.league.simulate_match(home_idx, away_idx)
            
    def _watch_all_matches(self, fixtures: List[Tuple[int, int]]):
        """Watch all matches with live updating table."""
        # Use the new live match tracker
        results = self.ui.simulate_all_matches_live(fixtures, self.league)
        input("\nPress Enter to continue...")
            
    def _follow_your_team(self, fixtures: List[Tuple[int, int]]):
        """Follow your team with highlighted display."""
        my_team_idx = self.league.get_my_team_index()
        if my_team_idx is None:
            self.ui.console.print("[yellow]No user team selected. Showing all matches instead.[/yellow]")
            time.sleep(2)
            results = self.ui.simulate_all_matches_live(fixtures, self.league, follow_your_team=False)
        else:
            results = self.ui.simulate_all_matches_live(fixtures, self.league, follow_your_team=True)
        input("\nPress Enter to continue...")
        
    def _choose_matches_to_watch(self, fixtures: List[Tuple[int, int]]):
        """Let user choose which matches to watch."""
        # This would be implemented with a selection interface
        # For now, just simulate all
        self._simulate_matches(fixtures, show_summary=True)
        
    def _simulate_to_end(self):
        """Simulate to the end of the season with simple progress."""
        remaining_days = (self.league.team_number() - 1) * 2 - self.league.current_match_day() + 1
        
        self.ui.console.print("\n[bold cyan]Simulating to end of season...[/bold cyan]\n")
        
        for day in range(remaining_days):
            fixtures = self.league.get_current_fixtures()
            if not fixtures:
                break
                
            self.ui.console.print(f"[dim]Match Day {self.league.current_match_day()}...[/dim]", end="\r")
            self._simulate_matches(fixtures, show_summary=False)
            self.league.advance_match_day()
            time.sleep(0.1)  # Brief pause for visual effect
            
        self.league.completed = True
        self.ui.console.print("\n[green]Season simulation complete![/green]")
        time.sleep(1)
        
    def _handle_season_end(self) -> bool:
        """Handle end of season with promotion/relegation."""
        self.ui.console.clear()
        self.ui.console.print("[bold cyan]Season Complete![/bold cyan]\n")
        
        # Show final standings
        my_team_idx = self.league.get_my_team_index()
        self.ui.display_league_table(self.league, my_team_idx)
        
        # Handle promotion/relegation
        if self.league.relegation_zone() > 0:
            promoted_teams = promotion_and_relegation(self.league)
            if len(promoted_teams) > 0:
                self.league.promoted(promoted_teams)
                
        # Prepare new season
        self.league.prepare_new_season()
        
        # Ask if player wants to continue
        continue_playing = input("\nContinue to next season? (y/n): ").lower() == 'y'
        
        if continue_playing:
            self.ui.console.print("\n[green]Starting new season...[/green]")
            time.sleep(1)
            
        return continue_playing
        
    def _save_and_exit(self):
        """Save the game and exit."""
        if not self.user_data:
            self.ui.console.print("\n[yellow]No save functionality available.[/yellow]")
            return
            
        save_choice = input("\nSave the game? (y/n): ").lower()
        
        if save_choice == 'y':
            save_name = input("Save name (Enter for 'Autosave'): ").strip()
            if not save_name:
                save_name = "Autosave"
                
            self.ui.show_loading(f"Saving as '{save_name}'...")
            self.user_data.save_game(save_name, self.league.data())
            self.ui.console.print(f"[green]Game saved as '{save_name}'![/green]")
            
        self.ui.console.print("\n[bold green]Thanks for playing![/bold green]")
        
    def _generate_goal_events(self, home_score: int, away_score: int) -> List[Dict]:
        """Generate mock goal events for match simulation."""
        import random
        
        events = []
        minutes_available = list(range(1, 91))
        random.shuffle(minutes_available)
        
        # Generate home goals
        for i in range(home_score):
            events.append({
                'minute': minutes_available.pop(),
                'team': 'home',
                'type': 'goal',
                'player': f'Player {random.randint(1, 11)}'
            })
            
        # Generate away goals
        for i in range(away_score):
            events.append({
                'minute': minutes_available.pop(),
                'team': 'away',
                'type': 'goal',
                'player': f'Player {random.randint(1, 11)}'
            })
            
        # Sort by minute
        events.sort(key=lambda x: x['minute'])
        
        return events