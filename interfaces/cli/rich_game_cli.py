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
from utils.json_save_system import GameData
from core.storage.team_storage import initialize_team_storage
from core.storage.data_updater import check_and_update_data
import json
import os


class RichFFM:
    """Enhanced Fantasy Football Manager game class with Rich UI."""
    
    def __init__(self, user_id: str, version: str = "0.9.1", theme: str = "dark"):
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
        self.current_save_name = None  # Track the currently loaded save name
        
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
            elif command == "delete":
                self._manage_saves()
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
        
        is_random_league = False
        
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
                is_random_league = True
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
            relegation_zone=relegation_zone,
            is_random_league=is_random_league
        )
        
        # Clear current save name for new games
        self.current_save_name = None
        
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
        saves_table.add_column("Save Name", style="bold white")
        saves_table.add_column("League", style="bold green")
        saves_table.add_column("Season", style="bold yellow")
        
        for save_name in saves:
            # Get save metadata from the new JSON system
            save_info = self.user_data.get_save_info(save_name)
            if save_info and 'progress_info' in save_info:
                progress = save_info['progress_info']
                league_name = progress.get('league_name', 'Unknown')
                season = str(progress.get('season', 1))
            else:
                league_name = "Unknown"
                season = "1"
            
            saves_table.add_row(save_name, league_name, season)
            
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
            self.current_save_name = save_game_name  # Remember the loaded save name
            self.ui.console.print(f"[green]Successfully loaded {save_game_name}![/green]")
            time.sleep(1)
            return True
        except json.JSONDecodeError as e:
            self.ui.console.print(f"[red]Failed to parse saved game: {e}[/red]")
            return False
        except Exception as e:
            self.ui.console.print(f"[red]Unexpected error loading game: {e}[/red]")
            return False
    
    def _manage_saves(self):
        """Manage saved games - delete individual saves or all saves."""
        if not self.user_data:
            self.ui.console.print("\n[red]No user data available for managing saves.[/red]")
            input("Press Enter to continue...")
            return
            
        saves = self.user_data.saved_game_list()
        if not saves:
            self.ui.console.print("\n[yellow]No saved games found.[/yellow]")
            input("Press Enter to continue...")
            return
            
        while True:
            self.ui.console.clear()
            self.ui.console.print("[bold cyan]Manage Saved Games[/bold cyan]\n")
            
            # Display saves in a table
            from rich.table import Table
            
            saves_table = Table(show_header=True, header_style="bold cyan")
            saves_table.add_column("#", style="bold white", width=3)
            saves_table.add_column("Save Name", style="bold white")
            saves_table.add_column("League", style="bold green")
            saves_table.add_column("Season", style="bold yellow")
            
            for i, save_name in enumerate(saves, 1):
                save_info = self.user_data.get_save_info(save_name)
                if save_info and 'progress_info' in save_info:
                    progress = save_info['progress_info']
                    league_name = progress.get('league_name', 'Unknown')
                    season = str(progress.get('season', 1))
                else:
                    league_name = "Unknown"
                    season = "1"
                
                saves_table.add_row(str(i), save_name, league_name, season)
                
            self.ui.console.print(saves_table)
            self.ui.console.print("\n[bold]Options:[/bold]")
            self.ui.console.print("  [cyan]1-{0}[/cyan] - Delete specific save".format(len(saves)))
            self.ui.console.print("  [cyan]all[/cyan] - Delete all saves")
            self.ui.console.print("  [cyan]back[/cyan] - Return to main menu\n")
            
            choice = input("Your choice: ").strip().lower()
            
            if choice == "back":
                break
            elif choice == "all":
                confirm = input(f"\n[bold red]Delete ALL {len(saves)} saved games? This cannot be undone! (type 'DELETE ALL' to confirm): ")
                if confirm == "DELETE ALL":
                    deleted_count = 0
                    for save_name in saves[:]:  # Copy list to avoid modification during iteration
                        if self.user_data.delete_saved_game(save_name):
                            deleted_count += 1
                    
                    if deleted_count > 0:
                        self.ui.console.print(f"\n[green]Successfully deleted {deleted_count} saved games![/green]")
                        saves = []  # Clear the list since all saves are deleted
                    else:
                        self.ui.console.print("\n[red]Failed to delete saved games.[/red]")
                    input("Press Enter to continue...")
                    if not saves:  # Exit if no saves left
                        break
                else:
                    self.ui.console.print("\n[yellow]Deletion cancelled.[/yellow]")
                    input("Press Enter to continue...")
            else:
                try:
                    save_index = int(choice) - 1
                    if 0 <= save_index < len(saves):
                        save_name = saves[save_index]
                        confirm = input(f"\nDelete '{save_name}'? (y/n): ").lower()
                        if confirm == 'y':
                            if self.user_data.delete_saved_game(save_name):
                                self.ui.console.print(f"\n[green]Successfully deleted '{save_name}'![/green]")
                                saves.remove(save_name)  # Remove from our local list
                                if not saves:  # Exit if no saves left
                                    input("Press Enter to continue...")
                                    break
                            else:
                                self.ui.console.print(f"\n[red]Failed to delete '{save_name}'.[/red]")
                            input("Press Enter to continue...")
                        else:
                            self.ui.console.print("\n[yellow]Deletion cancelled.[/yellow]")
                            input("Press Enter to continue...")
                    else:
                        self.ui.console.print(f"\n[red]Invalid choice. Please enter 1-{len(saves)}.[/red]")
                        input("Press Enter to continue...")
                except ValueError:
                    self.ui.console.print(f"\n[red]Invalid choice. Please enter 1-{len(saves)}, 'all', or 'back'.[/red]")
                    input("Press Enter to continue...")
            
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
            self.ui.console.print("  [cyan](Q)[/cyan]uit - Save and exit\n")
            
            command = input("Your choice: ").upper()
            
            if command == "C":
                self._play_match_day()
                break
            elif command == "S":
                self._simulate_to_end()
                break
            elif command == "Q":
                self._save_and_exit()
                return False
            else:
                self.ui.console.print("[red]Invalid choice. Please select C, S, or Q.[/red]")
                
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
            # Quick simulation - process matches and show results
            self.ui.console.clear()
            self.ui.console.print(f"[bold cyan]🎲 Simulating Match Day {self.league.current_match_day()}...[/bold cyan]\n")
            
            results = []
            my_team_idx = self.league.get_my_team_index()
            
            for home_idx, away_idx in fixtures:
                home_team = self.league.get_team_by_index(home_idx)
                away_team = self.league.get_team_by_index(away_idx)
                
                if home_team and away_team:
                    home_score, away_score = self.league.simulate_match(home_idx, away_idx)
                    
                    # Check if this match involves the user's team
                    is_user_match = my_team_idx is not None and (home_idx == my_team_idx or away_idx == my_team_idx)
                    
                    results.append({
                        'home_team': home_team.name,
                        'away_team': away_team.name, 
                        'home_score': home_score,
                        'away_score': away_score,
                        'user_team': is_user_match
                    })
            
            # Display results
            self.ui.display_match_results_summary(results)
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
        """Simulate to the end of the season with live table updates."""
        remaining_days = (self.league.team_number() - 1) * 2 - self.league.current_match_day() + 1
        my_team_idx = self.league.get_my_team_index()
        
        self.ui.console.print("\n[bold cyan]Simulating to end of season...[/bold cyan]\n")
        time.sleep(0.5)
        
        for day in range(remaining_days):
            fixtures = self.league.get_current_fixtures()
            if not fixtures:
                break
                
            current_match_day = self.league.current_match_day()
            
            # Find my team's match if any
            my_team_result = None
            if my_team_idx is not None:
                for home_idx, away_idx in fixtures:
                    if my_team_idx in [home_idx, away_idx]:
                        # We'll get the result after match_day() processes it
                        home_team = self.league.get_team_by_index(home_idx)
                        away_team = self.league.get_team_by_index(away_idx)
                        
                        # Skip if teams not found
                        if not home_team or not away_team:
                            continue
                            
                        my_team_result = {
                            'home': home_team.name,
                            'away': away_team.name,
                            'home_idx': home_idx,
                            'away_idx': away_idx,
                            'is_home': my_team_idx == home_idx
                        }
                        break
            
            # Process all matches for this day
            match_results = self.league.match_day()
            
            # Extract my team's score from results if they played
            if my_team_result and match_results:
                import re
                # Remove ANSI color codes
                clean_results = re.sub(r'\x1b\[[0-9;]*m', '', match_results)
                
                for result in clean_results.split('\n'):
                    if my_team_result['home'] in result and my_team_result['away'] in result:
                        # Extract score from result string (format: "Team1 vs Team2      2 - 1")
                        if ' - ' in result:
                            # Find the score pattern (number - number)
                            score_match = re.search(r'(\d+)\s*-\s*(\d+)', result)
                            if score_match:
                                my_team_result['home_score'] = int(score_match.group(1))
                                my_team_result['away_score'] = int(score_match.group(2))
            
            self.league.advance_match_day()
            
            # Update display for every match day
            self.ui.console.clear()
            self.ui.console.print(f"[bold cyan]Simulating Season - Match Day {current_match_day}/{(self.league.team_number() - 1) * 2}[/bold cyan]\n")
            
            # Show league table first
            self.ui.display_league_table(self.league, my_team_idx)
            
            # Show my team's result below the table if they played
            if my_team_idx is not None and my_team_result and 'home_score' in my_team_result:
                if my_team_result['is_home']:
                    result_text = f"[bold yellow]{my_team_result['home']}[/bold yellow] {my_team_result['home_score']} - {my_team_result['away_score']} {my_team_result['away']}"
                else:
                    result_text = f"{my_team_result['home']} {my_team_result['home_score']} - {my_team_result['away_score']} [bold yellow]{my_team_result['away']}[/bold yellow]"
                self.ui.console.print(f"\nYour Match: {result_text}")
            
            time.sleep(0.5)  # Half second pause for each match day
            
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
            # Check if relegation is actually possible (multiple leagues in country)
            if self._can_relegate():
                if self.league.is_random_league:
                    # For random leagues, offer to replace with random teams
                    promoted_teams = self._handle_random_league_relegation()
                else:
                    # For regular leagues, check if we can offer teams from same country
                    promoted_teams = self._handle_regular_league_relegation()
                
                if len(promoted_teams) > 0:
                    self.league.promoted(promoted_teams)
            else:
                self.ui.console.print("\n[yellow]Note: Relegation zone highlighted but no relegation occurs (only league in country).[/yellow]")
                input("Press Enter to continue...")
                
        # Prepare new season
        self.league.prepare_new_season()
        
        # Ask if player wants to continue
        continue_playing = input("\nContinue to next season? (y/n): ").lower() == 'y'
        
        if continue_playing:
            self.ui.console.print("\n[green]Starting new season...[/green]")
            time.sleep(1)
        else:
            # Clear screen before returning to main menu
            self.ui.console.clear()
            
        return continue_playing
        
    def _save_and_exit(self):
        """Save the game and exit."""
        if not self.user_data:
            self.ui.console.print("\n[yellow]No save functionality available.[/yellow]")
            return
            
        save_choice = input("\nSave the game? (y/n): ").lower()
        
        if save_choice == 'y':
            # Offer current save name if available, otherwise default to Autosave
            default_name = self.current_save_name if self.current_save_name else "Autosave"
            save_name = input(f"Save name (Enter for '{default_name}'): ").strip()
            if not save_name:
                save_name = default_name
                
            self.ui.show_loading(f"Saving as '{save_name}'...")
            self.user_data.save_game(save_name, self.league.data())
            self.ui.console.print(f"[green]Game saved as '{save_name}'![/green]")
            
        self.ui.console.print("\n[bold green]Thanks for playing![/bold green]")
    
    def _can_relegate(self) -> bool:
        """Check if relegation is possible for this league (i.e., multiple leagues in country)."""
        league_name = self.league.league_name
        if not league_name or '-' not in league_name:
            return True  # Default to allowing relegation if we can't determine
        
        # Extract country from league name (format: "Country - League")
        country = league_name.split(' - ')[0]
        
        # Check if team storage is available and get leagues by country
        from core.storage.team_storage import team_storage
        if team_storage._loaded_from_raw:
            leagues_by_country = team_storage.get_leagues_by_country()
            if country in leagues_by_country:
                return len(leagues_by_country[country]) > 1
        
        # Default to allowing relegation if we can't determine
        return True
    
    def _handle_random_league_relegation(self) -> list:
        """Handle relegation for random leagues by offering to replace with random teams."""
        from core.storage.team_storage import team_storage
        
        promoted_teams = []
        relegated_count = self.league.relegation_zone()
        
        replace_choice = input(f'\nThe last {relegated_count} teams have been relegated. '
                             f'Replace them with random teams? (y/n): ').lower()
        
        if replace_choice == 'y':
            # Ask for team quality preference
            quality_choice = input('Use elite teams only? (y/n): ').lower()
            use_elite = quality_choice == 'y'
            
            self.ui.console.print(f"\n[cyan]Generating {relegated_count} random replacement teams...[/cyan]")
            
            if team_storage._loaded_from_raw:
                # Get list of existing team names to avoid duplicates
                existing_team_names = set()
                for i in range(self.league.team_number()):
                    team = self.league.get_team_by_index(i)
                    if team:
                        existing_team_names.add(team.name)
                
                # Generate unique teams
                new_teams = []
                attempts = 0
                max_attempts = relegated_count * 10  # Prevent infinite loops
                
                while len(new_teams) < relegated_count and attempts < max_attempts:
                    if use_elite:
                        # Get elite teams
                        candidate_teams = team_storage.get_random_teams(relegated_count * 2, min_rating=85, max_rating=100)
                        if not candidate_teams:
                            # Fill with good teams if no elite teams available
                            candidate_teams = team_storage.get_random_teams(relegated_count * 2, min_rating=75, max_rating=84)
                    else:
                        # Get mixed quality teams
                        candidate_teams = team_storage.get_random_teams(relegated_count * 2)
                    
                    # Filter out existing teams and already selected teams
                    selected_names = {team.name for team in new_teams}
                    for team in candidate_teams:
                        if (team.name not in existing_team_names and 
                            team.name not in selected_names and 
                            len(new_teams) < relegated_count):
                            new_teams.append(team)
                    
                    attempts += 1
                
                # Add the new teams to promoted_teams list
                for team in new_teams:
                    promoted_teams.append(team)
                    self.ui.console.print(f"   • {team.name}")
                
                if promoted_teams:
                    self.ui.console.print(f"\n[green]Successfully added {len(promoted_teams)} unique random teams![/green]")
                    if len(promoted_teams) < relegated_count:
                        self.ui.console.print(f"[yellow]Warning: Only found {len(promoted_teams)} unique teams out of {relegated_count} requested.[/yellow]")
                else:
                    self.ui.console.print(f"\n[red]Failed to generate random teams.[/red]")
            else:
                self.ui.console.print(f"\n[red]Team storage not available for random team generation.[/red]")
            
            input("Press Enter to continue...")
        
        return promoted_teams
    
    def _handle_regular_league_relegation(self) -> list:
        """Handle relegation for regular leagues with option for random teams from same country."""
        from interfaces.cli.user_input import promotion_and_relegation
        from core.storage.team_storage import team_storage
        
        relegated_count = self.league.relegation_zone()
        league_name = self.league.league_name
        
        # Check if there are other leagues in the same country
        country = None
        other_leagues = []
        
        if league_name and '-' in league_name:
            country = league_name.split(' - ')[0]
            
            if team_storage._loaded_from_raw:
                leagues_by_country = team_storage.get_leagues_by_country()
                if country in leagues_by_country:
                    other_leagues = [league for league in leagues_by_country[country] 
                                   if f"{country} - {league}" != league_name]
        
        # Show relegation options
        self.ui.console.print(f"\n[yellow]The last {relegated_count} teams have been relegated.[/yellow]")
        
        if other_leagues:
            self.ui.console.print(f"\nReplacement options:")
            self.ui.console.print(f"1. Manual team entry (custom teams)")
            self.ui.console.print(f"2. Random teams from {country} leagues")
            self.ui.console.print(f"3. No replacement")
            
            choice = input("Select option (1-3): ").strip()
            
            if choice == "1":
                # Use original promotion/relegation function
                return promotion_and_relegation(self.league)
            elif choice == "2":
                # Generate random teams from same country
                return self._generate_random_teams_from_country(country, other_leagues, relegated_count)
            else:
                return []
        else:
            # No other leagues available, use original function
            return promotion_and_relegation(self.league)
    
    def _generate_random_teams_from_country(self, country: str, available_leagues: list, count: int) -> list:
        """Generate random teams from other leagues in the same country."""
        from core.storage.team_storage import team_storage
        
        promoted_teams = []
        
        self.ui.console.print(f"\n[cyan]Generating {count} random teams from {country} leagues...[/cyan]")
        
        # Get teams from all other leagues in the country
        all_available_teams = []
        for league_name in available_leagues:
            league_teams = team_storage.get_league_teams(league_name, country)
            if league_teams:
                all_available_teams.extend(league_teams)
        
        # Get list of existing team names to avoid duplicates
        existing_team_names = set()
        for i in range(self.league.team_number()):
            team = self.league.get_team_by_index(i)
            if team:
                existing_team_names.add(team.name)
        
        # Filter out teams that are already in the current league
        unique_available_teams = [team for team in all_available_teams 
                                if team.name not in existing_team_names]
        
        if unique_available_teams and len(unique_available_teams) >= count:
            # Randomly select teams
            import random
            selected_teams = random.sample(unique_available_teams, count)
            
            for team in selected_teams:
                promoted_teams.append(team)
                self.ui.console.print(f"   • {team.name}")
            
            self.ui.console.print(f"\n[green]Successfully added {len(promoted_teams)} unique teams from {country}![/green]")
        else:
            self.ui.console.print(f"\n[red]Not enough teams available in other {country} leagues.[/red]")
            self.ui.console.print(f"[yellow]Falling back to manual team entry...[/yellow]")
            # Fall back to manual entry
            from interfaces.cli.user_input import promotion_and_relegation
            return promotion_and_relegation(self.league)
        
        input("Press Enter to continue...")
        return promoted_teams
        
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