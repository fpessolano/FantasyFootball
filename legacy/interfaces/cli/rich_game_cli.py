"""
Enhanced Game CLI using Rich Terminal UI

This module provides an enhanced command-line interface for the Fantasy Football Manager
using the Rich library for beautiful terminal output.
"""

from typing import Optional, List, Tuple, Dict
import time
import signal
import sys

from core.entities.league import League
from interfaces.cli.rich_interface_simple import SimpleRichInterface
import interfaces.cli.user_input as ti
from utils.save_system import SaveGameManager
from core.storage.team_storage import initialize_team_storage
from core.storage.data_updater import check_and_update_data
import json
import os


class RichFFM:
    """Enhanced Fantasy Football Manager game class with Rich UI."""
    
    def __init__(self, user_id: str, version: str = "1.0.0", theme: str = "dark"):
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
            self.save_manager = SaveGameManager(user_id)
        else:
            self.save_manager = None
            
        self.league = League([])
        self.last_loaded_save = None  # Track last loaded save name
        self.current_league_save_name = None  # Track current league for save naming
        
        # Set up signal handler for graceful exit during game
        signal.signal(signal.SIGINT, self._signal_handler)
        
        # Initialize team storage and check for updates
        self._initialize_team_storage()
        self._check_weekly_updates()
        
    def _signal_handler(self, sig, frame):
        """Handle Ctrl+C gracefully with auto-save."""
        self.ui.console.print('\n\n[bold yellow]⚠️  Ctrl+C detected![/bold yellow]')
        self.ui.console.print('[bold cyan]🔄 Exiting Fantasy Football Manager...[/bold cyan]')
        
        # Auto-save current game if in progress
        if self.league.valid and self.save_manager:
            try:
                save_name = self.current_league_save_name or "Emergency_Autosave"
                description = f"Emergency save - {self.user_id} - Match Day {self.league.current_match_day()}"
                success = self.save_manager.save_game(save_name, self.league.data(), description)
                if success:
                    self.ui.console.print(f'[green]📁 Game auto-saved as "{save_name}"[/green]')
                else:
                    self.ui.console.print('[yellow]⚠️  Could not auto-save game[/yellow]')
            except Exception:
                self.ui.console.print('[yellow]⚠️  Could not auto-save game[/yellow]')
        
        self.ui.console.print('[blue]👋 Thanks for playing![/blue]')
        sys.exit(0)
        
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
        self.ui.console.clear()  # Clear screen at startup
        self.ui.display_title_screen(self.user_id, self.version)
        self._main_menu_loop()
        
    def _main_menu_loop(self):
        """Main menu loop with Rich UI."""
        while True:
            command = self.ui.display_main_menu()
            
            if command == "help":
                self._show_help()
                self.ui.console.clear()  # Clear after help
            elif command == "new":
                if self.new():
                    self._play_game_loop()
                self.ui.console.clear()  # Clear after game
            elif command == "load":
                if self.load():
                    self._play_game_loop()
                self.ui.console.clear()  # Clear after game
            elif command == "exit":
                self.ui.console.clear()
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
            self.ui.console.print("  [cyan](C)[/cyan]ustom   - Create your own league")
            self.ui.console.print("  [cyan](B)[/cyan]ack     - Return to main menu\n")
            
            command = input("Your choice: ").lower()
            
            if command == 'e':
                self.ui.show_loading("Loading real world leagues...")
                result = ti.existing_league()
                if result is None:
                    # User chose to go back
                    self.ui.console.clear()
                    continue
                league_name, relegation_zone, teams, my_team = result
                break
            elif command == 'r':
                self.ui.show_loading("Generating random teams...")
                league_name, relegation_zone, teams, my_team = ti.random_teams()
                break
            elif command == 'c':
                league_name, relegation_zone, teams, my_team = ti.fully_custom_league()
                break
            elif command == 'b':
                return False  # Go back to main menu
            else:
                self.ui.console.print("[red]Invalid choice. Please select E, R, C, or B.[/red]")
                
        self.league = League(
            league_name=league_name,
            teams=teams,
            my_team=my_team,
            relegation_zone=0  # No relegation
        )
        
        # Set the default save name for this new game
        if self.league.valid:
            # Clean league name for filename
            clean_league_name = league_name.replace(" ", "_").replace("-", "_")
            self.current_league_save_name = f"autosave_{clean_league_name}"
            self.last_loaded_save = None  # Reset since this is a new game
        
        return self.league.valid
        
    def load(self) -> bool:
        """Load a saved game with Rich UI."""
        if not self.save_manager:
            self.ui.console.print("[red]No save manager available for loading games.[/red]")
            return False
            
        saves = self.save_manager.list_saves()
        if not saves:
            self.ui.console.print("[yellow]No saved games found.[/yellow]")
            return False
            
        while True:
            self.ui.console.clear()
            self.ui.console.print("[bold cyan]Load Saved Game[/bold cyan]\n")
            
            # Display saves in a nice table with metadata
            from rich.table import Table
            
            saves_table = Table(show_header=True, header_style="bold cyan")
            saves_table.add_column("Index", style="bold cyan", width=6, justify="center")
            saves_table.add_column("Save Name", style=f"bold {self.ui._colors['primary']}")
            saves_table.add_column("Description", style=self.ui._colors["text"])
            saves_table.add_column("Date", style=self.ui._colors["accent1"])
            
            for i, save_info in enumerate(saves):
                # Parse timestamp for display
                timestamp = save_info.get('timestamp', 'Unknown')
                if timestamp != 'Unknown':
                    try:
                        from datetime import datetime
                        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        timestamp = dt.strftime('%Y-%m-%d %H:%M')
                    except:
                        pass
                
                saves_table.add_row(
                    str(i),
                    save_info['name'], 
                    save_info.get('description', 'No description'),
                    timestamp
                )
                
            self.ui.console.print(saves_table)
            self.ui.console.print("\n")
            
            # Show options
            self.ui.console.print("[bold]Options:[/bold]")
            self.ui.console.print("  [cyan]<index>[/cyan] or [cyan]<save_name>[/cyan] - Load a specific save")
            self.ui.console.print("  [cyan]delete <save_name>[/cyan] - Delete a specific save")
            self.ui.console.print("  [cyan]delete all[/cyan] - Delete all saves")
            self.ui.console.print("  [cyan]back[/cyan] - Return to main menu\n")
            
            command = input("Enter command: ").strip()
            
            if not command:
                self.ui.console.print("[yellow]Please enter a save name or command.[/yellow]")
                continue
            
            if command.lower() == "back":
                return False
            elif command.lower().startswith("delete "):
                save_to_delete = command[7:].strip()
                if save_to_delete.lower() == "all":
                    # Delete all saves
                    confirm = input("[bold red]Delete ALL saves? This cannot be undone! (type 'yes' to confirm): [/bold red]").strip()
                    if confirm.lower() == "yes":
                        deleted_count = 0
                        for save_info in saves:
                            if self.save_manager.delete_save(save_info['name']):
                                deleted_count += 1
                        self.ui.console.print(f"[green]Deleted {deleted_count} save(s).[/green]")
                        saves = self.save_manager.list_saves()  # Refresh list
                        if not saves:
                            self.ui.console.print("[yellow]No saved games remaining.[/yellow]")
                            time.sleep(2)
                            return False
                    else:
                        self.ui.console.print("[yellow]Deletion cancelled.[/yellow]")
                else:
                    # Delete specific save
                    if self.save_manager.save_exists(save_to_delete):
                        confirm = input(f"Delete save '{save_to_delete}'? (y/n): ").strip().lower()
                        if confirm == 'y':
                            if self.save_manager.delete_save(save_to_delete):
                                self.ui.console.print(f"[green]Deleted save '{save_to_delete}'.[/green]")
                                saves = self.save_manager.list_saves()  # Refresh list
                                if not saves:
                                    self.ui.console.print("[yellow]No saved games remaining.[/yellow]")
                                    time.sleep(2)
                                    return False
                            else:
                                self.ui.console.print(f"[red]Failed to delete save '{save_to_delete}'.[/red]")
                        else:
                            self.ui.console.print("[yellow]Deletion cancelled.[/yellow]")
                    else:
                        self.ui.console.print(f"[red]Save '{save_to_delete}' not found.[/red]")
                time.sleep(1)
                continue
            else:
                # Check if command is an index number
                try:
                    index = int(command)
                    if 0 <= index < len(saves):
                        save_game_name = saves[index]['name']
                    else:
                        self.ui.console.print(f"[red]Invalid index {index}. Please choose 0-{len(saves)-1}[/red]")
                        time.sleep(2)
                        continue
                except ValueError:
                    # Not a number, treat as save name
                    save_game_name = command
                
                # Try to load the save
                self.ui.show_loading(f"Loading {save_game_name}...")
                
                saved_game = self.save_manager.load_game(save_game_name)
                if not saved_game:
                    self.ui.console.print(f"[red]Could not load save game '{save_game_name}'[/red]")
                    time.sleep(2)
                    continue
                    
                try:
                    self.league.restore(saved_game)
                    self.last_loaded_save = save_game_name  # Remember the loaded save name
                    self.ui.console.print(f"[green]Successfully loaded {save_game_name}![/green]")
                    time.sleep(1)
                    return True
                except Exception as e:
                    self.ui.console.print(f"[red]Unexpected error loading game: {e}[/red]")
                    time.sleep(2)
                    continue
            
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
            
        # Show all simulation options in one menu
        while True:
            self.ui.console.print("\n[bold]Match Day Options:[/bold]")
            self.ui.console.print("  [cyan](S)[/cyan]imulate Next Match Day - Live animation with results")
            self.ui.console.print("  [cyan](Q)[/cyan]uick Results - Simulate next match day without animation")
            self.ui.console.print("  [cyan](A)[/cyan]ll Season - Simulate entire season with ranking evolution")
            self.ui.console.print("  [cyan](E)[/cyan]xit - Save and quit game\n")
            
            command = input("Your choice: ").upper()
            
            if command == "S":
                # Simulate next match day with animation
                fixtures = self.league.get_current_fixtures()
                if fixtures:
                    self._simulate_matches(fixtures, show_summary=True)
                    self.league.advance_match_day()
                else:
                    self.league.completed = True
                break
            elif command == "Q":
                # Quick simulate next match day without animation
                fixtures = self.league.get_current_fixtures()
                if fixtures:
                    self._simulate_matches(fixtures, show_summary=False)
                    self.league.advance_match_day()
                else:
                    self.league.completed = True
                break
            elif command == "A":
                # Simulate entire season
                self._simulate_to_end()
                break
            elif command == "E":
                self._save_and_exit()
                return False
            else:
                self.ui.console.print("[red]Invalid choice![/red]")
                
        return True
        
        
    def _simulate_matches(self, fixtures: List[Tuple[int, int]], show_summary: bool = True):
        """Simulate matches with optional summary display."""
        if show_summary:
            # Use live display for visible simulation
            results = self.ui.simulate_all_matches_live(fixtures, self.league)
            input("\nPress Enter to continue...")
        else:
            # Quick simulation - clear screen and show results but no animation
            self.ui.console.clear()
            results = []
            for home_idx, away_idx in fixtures:
                home_score, away_score = self.league.simulate_match(home_idx, away_idx)
                home_team = self.league.get_team_by_index(home_idx)
                away_team = self.league.get_team_by_index(away_idx)
                
                if home_team and away_team:
                    my_team_idx = self.league.get_my_team_index()
                    results.append({
                        'home_team': home_team.name,
                        'away_team': away_team.name,
                        'home_score': home_score,
                        'away_score': away_score,
                        'user_team': my_team_idx is not None and (home_idx == my_team_idx or away_idx == my_team_idx)
                    })
            
            # Display results quickly
            self.ui.display_match_results_summary(results)
            input("\nPress Enter to continue...")
            
        
    def _simulate_to_end(self):
        """Simulate to the end of the season showing ranking evolution."""
        from rich.table import Table
        from rich import box
        
        remaining_days = (self.league.team_number() - 1) * 2 - self.league.current_match_day() + 1
        
        self.ui.console.clear()
        self.ui.console.print(f"\n[bold {self.ui._colors['primary']}]Simulating Season to Completion...[/bold {self.ui._colors['primary']}]\n")
        
        my_team_idx = self.league.get_my_team_index()
        
        for day in range(remaining_days):
            fixtures = self.league.get_current_fixtures()
            if not fixtures:
                break
            
            # Simulate all matches for this day
            user_match_info = None
            for home_idx, away_idx in fixtures:
                home_score, away_score = self.league.simulate_match(home_idx, away_idx)
                
                # Check if this is the user's match
                if my_team_idx is not None and (home_idx == my_team_idx or away_idx == my_team_idx):
                    home_team = self.league.get_team_by_index(home_idx)
                    away_team = self.league.get_team_by_index(away_idx)
                    if home_team and away_team:
                        user_match_info = {
                            'home': home_team.name,
                            'away': away_team.name,
                            'home_score': home_score,
                            'away_score': away_score
                        }
            
            # Clear and show updated standings
            self.ui.console.clear()
            
            # Print Match Day header centered
            header_text = f"[bold {self.ui._colors['primary']}]Match Day {self.league.current_match_day()} Results[/bold {self.ui._colors['primary']}]"
            self.ui.console.print(header_text, justify="center")
            
            # Show user's match result centered below the header
            if user_match_info:
                match_table = Table(
                    show_header=False,
                    box=box.HEAVY,
                    style=self.ui._colors["your_team"],
                    width=60  # Fixed width for consistent centering
                )
                match_table.add_column("Match", style=f"bold {self.ui._colors['your_team']}", width=40)
                match_table.add_column("Score", justify="center", style=f"bold {self.ui._colors['your_team']}", width=20)
                
                match_text = f"{user_match_info['home']} vs {user_match_info['away']}"
                score_text = f"{user_match_info['home_score']}-{user_match_info['away_score']}"
                match_table.add_row(match_text, score_text)
                
                self.ui.console.print("\n")
                self.ui.console.print(match_table, justify="center")
            
            self.ui.console.print("\n")
            
            # Show league table
            self.ui.display_league_table(self.league, my_team_idx)
            
            self.league.advance_match_day()
            time.sleep(0.8)  # Pause to show each match day
            
        self.league.completed = True
        
        # Show final standings
        self.ui.console.clear()
        self.ui.console.print(f"\n[bold {self.ui._colors['win']}]Season Complete - Final Standings[/bold {self.ui._colors['win']}]\n")
        self.ui.display_league_table(self.league, my_team_idx)
        
        input("\nPress Enter to continue...")
        
    def _display_season_results(self, all_results):
        """Display comprehensive season results."""
        from rich.table import Table
        from rich import box
        
        self.ui.console.print(f"\n[bold {self.ui._colors['primary']}]SEASON RESULTS SUMMARY[/bold {self.ui._colors['primary']}]\n")
        
        # Show user's matches
        my_team_idx = self.league.get_my_team_index()
        if my_team_idx is not None:
            my_team = self.league.get_team_by_index(my_team_idx)
            if my_team:
                user_results = [r for r in all_results if r['user_match']]
                
                if user_results:
                    user_table = Table(
                        title=f"[bold {self.ui._colors['your_team']}]{my_team.name} - Season Results[/bold {self.ui._colors['your_team']}]",
                        show_header=True,
                        header_style=f"bold {self.ui._colors['primary']}",
                        box=box.ROUNDED
                    )
                    
                    user_table.add_column("MD", justify="center", style=self.ui._colors["numbers"], width=3)
                    user_table.add_column("Match", style=self.ui._colors["text"])
                    user_table.add_column("Score", justify="center", style=f"bold {self.ui._colors['text']}", width=8)
                    user_table.add_column("Result", justify="center", width=6)
                    
                    wins = draws = losses = 0
                    
                    for result in user_results[-10:]:  # Show last 10 matches
                        if result['home_team'] == my_team.name:
                            opponent = result['away_team']
                            score = f"{result['home_score']}-{result['away_score']}"
                            if result['home_score'] > result['away_score']:
                                result_text = f"[{self.ui._colors['win']}]W[/{self.ui._colors['win']}]"
                                wins += 1
                            elif result['home_score'] == result['away_score']:
                                result_text = f"[{self.ui._colors['draw']}]D[/{self.ui._colors['draw']}]"
                                draws += 1
                            else:
                                result_text = f"[{self.ui._colors['loss']}]L[/{self.ui._colors['loss']}]"
                                losses += 1
                        else:
                            opponent = result['home_team']
                            score = f"{result['away_score']}-{result['home_score']}"
                            if result['away_score'] > result['home_score']:
                                result_text = f"[{self.ui._colors['win']}]W[/{self.ui._colors['win']}]"
                                wins += 1
                            elif result['away_score'] == result['home_score']:
                                result_text = f"[{self.ui._colors['draw']}]D[/{self.ui._colors['draw']}]"
                                draws += 1
                            else:
                                result_text = f"[{self.ui._colors['loss']}]L[/{self.ui._colors['loss']}]"
                                losses += 1
                        
                        user_table.add_row(
                            str(result['match_day']),
                            f"vs {opponent}",
                            score,
                            result_text
                        )
                    
                    self.ui.console.print(user_table)
                    self.ui.console.print(f"\n[{self.ui._colors['text']}]Season Record: [{self.ui._colors['win']}]{wins}W[/{self.ui._colors['win']}] [{self.ui._colors['draw']}]{draws}D[/{self.ui._colors['draw']}] [{self.ui._colors['loss']}]{losses}L[/{self.ui._colors['loss']}][/{self.ui._colors['text']}]")
        
        input("\nPress Enter to continue...")
        time.sleep(0.5)
        
    def _handle_season_end(self) -> bool:
        """Handle end of season (no relegation system)."""
        self.ui.console.clear()
        self.ui.console.print("[bold cyan]Season Complete![/bold cyan]\n")
        
        # Show final standings
        my_team_idx = self.league.get_my_team_index()
        self.ui.display_league_table(self.league, my_team_idx)
        
        # No relegation/promotion - just prepare new season
        self.league.prepare_new_season()
        
        # Ask if player wants to continue
        continue_playing = input("\nContinue to next season? (y/n): ").lower() == 'y'
        
        if continue_playing:
            self.ui.console.print("\n[green]Starting new season...[/green]")
            time.sleep(1)
            
        return continue_playing
        
    def _save_and_exit(self):
        """Save the game and exit."""
        if not self.save_manager:
            self.ui.console.print("\n[yellow]No save functionality available.[/yellow]")
            return
            
        save_choice = input("\nSave the game? (y/n): ").lower()
        
        if save_choice == 'y':
            # Suggest the last loaded save name if available, otherwise use current league save name
            if self.last_loaded_save:
                default_name = self.last_loaded_save
            elif self.current_league_save_name:
                default_name = self.current_league_save_name
            else:
                default_name = "Autosave"
            
            save_name = input(f"Save name (Enter for '{default_name}'): ").strip()
            if not save_name:
                save_name = default_name
            
            description = input("Save description (optional): ").strip()
            if not description:
                my_team = self.league.get_my_team_index()
                if my_team is not None:
                    my_team_name = self.league.get_team_by_index(my_team).name
                    description = f"{my_team_name} - Match Day {self.league.current_match_day()}"
                else:
                    description = f"Season save - Match Day {self.league.current_match_day()}"
                
            self.ui.show_loading(f"Saving as '{save_name}'...")
            success = self.save_manager.save_game(save_name, self.league.data(), description)
            
            if success:
                self.ui.console.print(f"[green]Game saved as '{save_name}'![/green]")
            else:
                self.ui.console.print(f"[red]Failed to save game![/red]")
            
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