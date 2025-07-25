"""
Simplified Rich Terminal UI Interface for Fantasy Football Manager

This module provides a simpler, more stable version of the Rich UI that avoids
complex layouts and focuses on reliable display.
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.align import Align
from rich import box
from datetime import datetime
import time
from typing import List, Dict, Optional, Tuple

from core.entities.team import Team
from core.entities.league import League


class SimpleRichInterface:
    """Simplified Rich interface that avoids complex layouts."""
    
    def __init__(self, theme="auto"):
        self.console = Console()
        self.theme = theme  # "light", "dark", or "auto"
        self._colors = self._get_color_scheme()
    
    def _get_color_scheme(self):
        """Get color scheme based on terminal background."""
        if self.theme == "light":
            return {
                # Light background colors (white/light terminals)
                "primary": "blue",
                "secondary": "purple",
                "win": "green",
                "draw": "orange1", 
                "loss": "red",
                "text": "black",
                "numbers": "black",  # For MP, GF, GA, GD, Pts
                "highlight_bg": "blue",
                "highlight_text": "white",
                "champions": "bold green",
                "europa": "bold blue", 
                "relegation": "bold red",
                "your_team": "bold white on red"  # Much more visible - white text on red background
            }
        else:
            return {
                # Dark background colors (black/dark terminals)
                "primary": "cyan",
                "secondary": "magenta", 
                "win": "bright_green",
                "draw": "bright_yellow",
                "loss": "bright_red",
                "text": "white",
                "numbers": "white",  # For MP, GF, GA, GD, Pts
                "highlight_bg": "yellow",
                "highlight_text": "black",
                "champions": "bold bright_green",
                "europa": "bold bright_cyan",
                "relegation": "bold bright_red",
                "your_team": "bold black on bright_yellow"  # Keep existing for dark theme
            }
        
    def display_title_screen(self, user_name: str, version: str):
        """Display the enhanced title screen."""
        title_text = f"""
[bold {self._colors['primary']}]
     ______          _                    
    |  ____|        | |                   
    | |__ __ _ _ __ | |_ __ _ ___ _   _   
    |  __/ _` | '_ \\| __/ _` / __| | | |  
    | | | (_| | | | | || (_| \\__ \\ |_| |  
    |_|  \\__,_|_| |_|\\__\\__,_|___/\\__, |  
    |  \\/  |                       __/ |  
    | \\  / | __ _ _ __   __ _  __ |___/_ _ __
    | |\\/| |/ _` | '_ \\ / _` |/ _` |/ _ \\ '__|
    | |  | | (_| | | | | (_| | (_| |  __/ |
    |_|  |_|\\__,_|_| |_|\\__,_|\\__, |\\___|_|
                                __/ |      
                               |___/       
[/bold {self._colors['primary']}]
        """
        
        self.console.print("\n")
        
        self.console.print(Panel(
            Align.center(
                f"{title_text}\n\n[bold {self._colors['win']}]Welcome {user_name}![/bold {self._colors['win']}]\n[{self._colors['secondary']}]Version {version}[/{self._colors['secondary']}]"
            ),
            box=box.DOUBLE,
            style=self._colors["primary"],
            width=60
        ), justify="center")
        self.console.print("\n")
        
    def display_main_menu(self) -> str:
        """Display the main menu with rich formatting."""
        menu_table = Table(show_header=False, box=None, padding=(0, 2))
        menu_table.add_column("Option", style=self._colors["primary"], no_wrap=True)
        menu_table.add_column("Description", style=self._colors["text"])
        
        menu_table.add_row(f"[bold {self._colors['primary']}]new[/bold {self._colors['primary']}]", "Start a new game")
        menu_table.add_row(f"[bold {self._colors['primary']}]load[/bold {self._colors['primary']}]", "Load a saved game")
        menu_table.add_row(f"[bold {self._colors['primary']}]help[/bold {self._colors['primary']}]", "Show help information")
        menu_table.add_row(f"[bold {self._colors['primary']}]exit[/bold {self._colors['primary']}]", "Exit the game")
        
        self.console.print(Panel(menu_table, title=f"[bold {self._colors['text']}]Main Menu[/bold {self._colors['text']}]", box=box.ROUNDED))
        
        return input("\nType your command: ").strip().lower()
        
    def display_league_table(self, league: League, highlight_team: Optional[int] = None):
        """Display a beautiful league table with team standings."""
        teams = league.order_list()
        
        # Calculate optimal team name column width
        max_team_name_length = 0
        for team_idx in teams:
            team = league.get_team_by_index(team_idx)
            if team:
                max_team_name_length = max(max_team_name_length, len(team.name))
        
        # Set team column width with minimum and padding
        team_column_width = max(15, max_team_name_length + 2)
        
        # Create the table
        table = Table(
            title=f"[bold]{league.league_name} - Season {league.season}[/bold]",
            show_header=True,
            header_style="bold magenta",
            box=box.HEAVY_EDGE,
            title_style="bold cyan",
            caption=f"Match Day {league.current_match_day()}"
        )
        
        # Add columns with theme-appropriate colors
        table.add_column("Pos", style=self._colors["primary"], no_wrap=True, width=4, justify="center")
        table.add_column("Team", style=self._colors["text"], no_wrap=False, width=team_column_width)
        table.add_column("MP", justify="center", style=self._colors["numbers"], width=4)
        table.add_column("W", justify="center", style=self._colors["win"], width=4)
        table.add_column("D", justify="center", style=self._colors["draw"], width=4)
        table.add_column("L", justify="center", style=self._colors["loss"], width=4)
        table.add_column("GF", justify="center", style=self._colors["numbers"], width=4)
        table.add_column("GA", justify="center", style=self._colors["numbers"], width=4)
        table.add_column("GD", justify="center", style=self._colors["numbers"], width=4)
        table.add_column("Pts", justify="center", style=f"bold {self._colors['numbers']}", width=4)
        
        # Add rows
        for i, team_idx in enumerate(teams):
            team = league.get_team_by_index(team_idx)
            pos = i + 1
            
            # Skip invalid teams
            if team is None:
                continue
            
            # Determine row style based on theme
            row_style = None
            if highlight_team is not None and team_idx == highlight_team:
                row_style = self._colors["your_team"]
            elif pos <= 4:  # Champions League spots
                row_style = self._colors["champions"]
            elif pos <= 6:  # Europa League spots
                row_style = self._colors["europa"]
            elif pos > len(teams) - league.relegation_zone():  # Relegation zone
                row_style = self._colors["relegation"]
                
            table.add_row(
                str(pos),
                team.name,
                str(team.matches_played),
                str(team.won),
                str(team.drawn),
                str(team.lost),
                str(team.goals_for),
                str(team.goals_against),
                f"{team.goals_for - team.goals_against:+d}",
                str(team.points()),
                style=row_style
            )
            
        self.console.print("\n")
        self.console.print(table)
        self.console.print("\n")
        
    def display_match_day_overview(self, league: League, match_day_fixtures: List[Tuple[int, int]], 
                                  my_team: Optional[int] = None):
        """Display match day overview with fixtures."""
        self.console.clear()
        
        # Calculate optimal column widths based on team names
        max_team_name_length = 0
        for home_idx, away_idx in match_day_fixtures:
            home_team = league.get_team_by_index(home_idx)
            away_team = league.get_team_by_index(away_idx)
            if home_team and away_team:
                max_team_name_length = max(max_team_name_length, len(home_team.name), len(away_team.name))
        
        # Set column width with minimum and padding
        team_column_width = max(20, max_team_name_length + 2)
        
        # Header  
        self.console.print(Panel(
            Align.center(
                f"[bold cyan]MATCH DAY {league.current_match_day()}[/bold cyan]\n"
                f"[white]{datetime.now().strftime('%A, %B %d')}[/white]"
            ),
            box=box.DOUBLE,
            style="cyan"
        ))
        self.console.print("\n")
        
        # Fixtures table
        fixtures_table = Table(
            title="[bold]Today's Fixtures[/bold]",
            show_header=True,
            header_style="bold cyan",
            box=box.ROUNDED
        )
        
        fixtures_table.add_column("Home", style="white", no_wrap=True, width=team_column_width)
        fixtures_table.add_column("vs", justify="center", style="cyan", width=4)
        fixtures_table.add_column("Away", style="white", no_wrap=True, width=team_column_width)
        
        # Add fixtures
        for i, (home_idx, away_idx) in enumerate(match_day_fixtures):
            home_team = league.get_team_by_index(home_idx)
            away_team = league.get_team_by_index(away_idx)
            
            # Skip fixture if teams are invalid
            if home_team is None or away_team is None:
                continue
            
            # Highlight user's team match with same colors as league table
            my_team_idx = league.get_my_team_index()
            row_style = None
            if my_team_idx is not None and my_team_idx in [home_idx, away_idx]:
                row_style = self._colors["your_team"]
            
            fixtures_table.add_row(
                home_team.name,
                "vs",
                away_team.name,
                style=row_style
            )
            
        self.console.print(fixtures_table)
        self.console.print("\n")
        
        # Options
        options_text = (
            "[bold cyan][S][/bold cyan]imulate All  "
            "[bold cyan][W][/bold cyan]atch All  "
            "[bold cyan][F][/bold cyan]ollow Your Team  "
            "[bold cyan][C][/bold cyan]hoose Matches"
        )
        self.console.print(Panel(options_text, box=box.SIMPLE))
        
    def simulate_all_matches_live(self, fixtures: List[Tuple[int, int]], league: League, follow_your_team: bool = False) -> List[Dict]:
        """Display all matches updating simultaneously."""
        self.console.clear()
        
        # Different headers for different modes  
        my_team_idx = league.get_my_team_index()
        if follow_your_team and my_team_idx is not None:
            my_team = league.get_team_by_index(my_team_idx)
            if my_team is not None:
                header_text = f"[bold {self._colors['primary']}]FOLLOWING {my_team.name.upper()}[/bold {self._colors['primary']}]"
            else:
                header_text = f"[bold {self._colors['primary']}]LIVE MATCH TRACKER[/bold {self._colors['primary']}]"
        else:
            header_text = f"[bold {self._colors['primary']}]LIVE MATCH TRACKER[/bold {self._colors['primary']}]"
        
        self.console.print(Panel(
            header_text,
            box=box.DOUBLE,
            style=self._colors["primary"]
        ))
        self.console.print("\n")
        
        # Simulate all matches simultaneously with real-time updates
        results = []
        all_match_events = []
        
        # Generate all match results and events upfront
        for home_idx, away_idx in fixtures:
            home_score, away_score = league.simulate_match(home_idx, away_idx)
            goal_events = self._generate_goal_events(home_score, away_score)
            
            all_match_events.append({
                'home_idx': home_idx,
                'away_idx': away_idx,
                'home_score': home_score,
                'away_score': away_score,
                'goal_events': goal_events
            })
            
            home_team = league.get_team_by_index(home_idx)
            away_team = league.get_team_by_index(away_idx)
            
            results.append({
                'home_team': home_team.name if home_team else f"Team {home_idx}",
                'away_team': away_team.name if away_team else f"Team {away_idx}",
                'home_score': home_score,
                'away_score': away_score,
                'user_team': my_team_idx is not None and (home_idx == my_team_idx or away_idx == my_team_idx)
            })
        
        # Show simultaneous progression
        self._simulate_all_matches_simultaneous(all_match_events, league, follow_your_team)
        
        self.console.print(f"\n[bold {self._colors['primary']}]All matches completed![/bold {self._colors['primary']}]")
        return results
        
    def display_match_results_summary(self, results: List[Dict]):
        """Display a summary of match results with theme colors."""
        results_table = Table(
            title=f"[bold {self._colors['primary']}]Match Results[/bold {self._colors['primary']}]",
            show_header=True,
            header_style=f"bold {self._colors['primary']}",
            box=box.ROUNDED
        )
        
        results_table.add_column("Home", style=self._colors["text"], no_wrap=True)
        results_table.add_column("Score", justify="center", style=f"bold {self._colors['text']}")
        results_table.add_column("Away", style=self._colors["text"], no_wrap=True)
        
        for result in results:
            score_text = f"{result['home_score']}-{result['away_score']}"
            
            # Highlight user's team matches
            row_style = self._colors["your_team"] if result.get('user_team') else None
            
            results_table.add_row(
                result['home_team'],
                score_text,
                result['away_team'],
                style=row_style
            )
            
        self.console.print("\n")
        self.console.print(results_table)
        self.console.print("\n")
        
    def display_season_progress(self, league: League, my_team_idx: Optional[int] = None):
        """Display season progress with statistics."""
        if my_team_idx is not None:
            my_team = league.get_team_by_index(my_team_idx)
            if my_team is not None:
                teams_sorted = league.order_list()
                position = teams_sorted.index(my_team_idx) + 1
                
                # Progress info
                total_matches = (league.team_number() - 1) * 2  # Home and away
                played_matches = league.current_match_day() - 1
                
                progress_text = f"Season Progress: {played_matches}/{total_matches} matches"
                
                # Quick stats panel
                stats_text = (
                    f"[bold]⚡ Quick Stats:[/bold]\n"
                    f"- Current Position: [bold]{position}[/bold]\n"
                    f"- Points: [bold]{my_team.points()}[/bold]\n"
                    f"- Goal Difference: [bold]{my_team.goals_for - my_team.goals_against:+d}[/bold]\n"
                    f"- {progress_text}"
                )
                
                self.console.print(Panel(stats_text, title=f"[bold]{my_team.name}[/bold]", 
                                       box=box.ROUNDED))
        
    def show_loading(self, message: str = "Loading..."):
        """Display a loading message."""
        self.console.print(f"[dim]{message}[/dim]")
        time.sleep(0.5)
    
    def get_help_text(self) -> str:
        """Get theme-aware help text."""
        return f"""
[bold {self._colors['primary']}]Fantasy Football Manager - Help[/bold {self._colors['primary']}]

[bold {self._colors['text']}]Commands:[/bold {self._colors['text']}]
  [{self._colors['primary']}]new[/{self._colors['primary']}]   - Start a new game
  [{self._colors['primary']}]load[/{self._colors['primary']}]  - Load a saved game  
  [{self._colors['primary']}]help[/{self._colors['primary']}]  - Show this help message
  [{self._colors['primary']}]exit[/{self._colors['primary']}]  - Exit the game

[bold {self._colors['text']}]Game Types:[/bold {self._colors['text']}]
  [{self._colors['primary']}](E)xisting[/{self._colors['primary']}] - Play with real world leagues
  [{self._colors['primary']}](R)andom[/{self._colors['primary']}]   - Generate random teams
  [{self._colors['primary']}](C)ustom[/{self._colors['primary']}]   - Create your own league

[bold {self._colors['text']}]During Play:[/bold {self._colors['text']}]
  [{self._colors['primary']}](S)imulate All[/{self._colors['primary']}]     - Quick simulation of all matches
  [{self._colors['primary']}](W)atch All[/{self._colors['primary']}]        - Watch all matches with details
  [{self._colors['primary']}](F)ollow Your Team[/{self._colors['primary']}] - Only watch your team's matches
  [{self._colors['primary']}](V)iew Table[/{self._colors['primary']}]       - Show current standings
  [{self._colors['primary']}](Q)uit[/{self._colors['primary']}]             - Save and exit current game
        """
    
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
                'type': 'goal'
            })
            
        # Generate away goals
        for i in range(away_score):
            events.append({
                'minute': minutes_available.pop(),
                'team': 'away',
                'type': 'goal'
            })
            
        # Sort by minute
        events.sort(key=lambda x: x['minute'])
        
        return events
    
    def _simulate_all_matches_simultaneous(self, all_match_events: List[Dict], league: League, follow_your_team: bool = False):
        """Simulate all matches simultaneously with real-time updates."""
        
        # Get user's team index once
        my_team_idx = league.get_my_team_index()
        
        # Calculate optimal column widths based on team names
        max_team_name_length = 0
        for match in all_match_events:
            home_team = league.get_team_by_index(match['home_idx'])
            away_team = league.get_team_by_index(match['away_idx'])
            if home_team and away_team:
                match_text_length = len(f"{home_team.name} vs {away_team.name}")
                max_team_name_length = max(max_team_name_length, match_text_length)
        
        # Set minimum width and add some padding
        match_column_width = max(35, max_team_name_length + 2)
        other_match_column_width = max(30, max_team_name_length)
        
        # Collect all unique minutes from all matches
        all_minutes = set([0, 90])  # Always show start and end
        for match in all_match_events:
            for event in match['goal_events']:
                all_minutes.add(event['minute'])
        
        # Add some regular intervals
        all_minutes.update([15, 30, 45, 60, 75])
        minutes_to_show = sorted(all_minutes)
        
        for minute in minutes_to_show:
            # Create table for current minute
            matches_table = Table(
                show_header=True,
                header_style=f"bold {self._colors['primary']}",
                box=box.ROUNDED
            )
            
            if follow_your_team and my_team_idx is not None:
                # Show only your team's match prominently
                matches_table.add_column("Your Match", style=self._colors["text"], width=match_column_width)
                matches_table.add_column("Time", justify="center", style=self._colors["primary"], width=8)
                matches_table.add_column("Score", justify="center", style=f"bold {self._colors['text']}", width=10)
                
                # Find and display only your team's match
                user_match_found = False
                for match in all_match_events:
                    if match['home_idx'] == my_team_idx or match['away_idx'] == my_team_idx:
                        home_team = league.get_team_by_index(match['home_idx'])
                        away_team = league.get_team_by_index(match['away_idx'])
                        
                        if home_team is not None and away_team is not None:
                            # Calculate current score at this minute
                            current_home = sum(1 for e in match['goal_events'] if e['team'] == 'home' and e['minute'] <= minute)
                            current_away = sum(1 for e in match['goal_events'] if e['team'] == 'away' and e['minute'] <= minute)
                            
                            match_name = f"{home_team.name} vs {away_team.name}"
                            score_text = f"{current_home}-{current_away}" if minute > 0 else "-"
                            
                            matches_table.add_row(match_name, score_text, style=self._colors["your_team"])
                            user_match_found = True
                        break
                
                # If no user match found, show message
                if not user_match_found:
                    matches_table.add_row("No team match found", "--", "--", style="dim")
                        
                # Show other matches in a separate table with dimmed colors
                other_table = Table(
                    title="[dim]Other Matches[/dim]",
                    show_header=True,
                    header_style="dim",
                    box=box.SIMPLE
                )
                other_table.add_column("Match", style="dim", width=other_match_column_width)
                other_table.add_column("Time", justify="center", style="dim", width=6)
                other_table.add_column("Score", justify="center", style="dim", width=8)
                
                # Add other matches to the table
                for match in all_match_events:
                    if my_team_idx is None or (match['home_idx'] != my_team_idx and match['away_idx'] != my_team_idx):
                        home_team = league.get_team_by_index(match['home_idx'])
                        away_team = league.get_team_by_index(match['away_idx'])
                        
                        if home_team is not None and away_team is not None:
                            current_home = sum(1 for e in match['goal_events'] if e['team'] == 'home' and e['minute'] <= minute)
                            current_away = sum(1 for e in match['goal_events'] if e['team'] == 'away' and e['minute'] <= minute)
                            
                            match_name = f"{home_team.name} vs {away_team.name}"
                            score_text = f"{current_home}-{current_away}" if minute > 0 else "-"
                            
                            other_table.add_row(match_name, score_text)
                        
            else:
                # Show all matches equally
                matches_table.add_column("Match", style=self._colors["text"], width=match_column_width)
                matches_table.add_column("Score", justify="center", style=f"bold {self._colors['text']}", width=10)
                
                for match in all_match_events:
                    home_team = league.get_team_by_index(match['home_idx'])
                    away_team = league.get_team_by_index(match['away_idx'])
                    
                    if home_team is not None and away_team is not None:
                        # Calculate current score at this minute
                        current_home = sum(1 for e in match['goal_events'] if e['team'] == 'home' and e['minute'] <= minute)
                        current_away = sum(1 for e in match['goal_events'] if e['team'] == 'away' and e['minute'] <= minute)
                        
                        match_name = f"{home_team.name} vs {away_team.name}"
                        score_text = f"{current_home}-{current_away}" if minute > 0 else "-"
                        
                        user_match = my_team_idx is not None and (match['home_idx'] == my_team_idx or match['away_idx'] == my_team_idx)
                        style = self._colors["your_team"] if user_match else None
                        
                        matches_table.add_row(match_name, score_text, style=style)
            
            # Clear and show updated display
            self.console.clear()
            
            if follow_your_team and my_team_idx is not None:
                my_team = league.get_team_by_index(my_team_idx)
                if my_team is not None:
                    header_text = f"[bold {self._colors['primary']}]FOLLOWING {my_team.name.upper()}[/bold {self._colors['primary']}]"
                else:
                    header_text = f"[bold {self._colors['primary']}]LIVE MATCH TRACKER[/bold {self._colors['primary']}]"
            else:
                header_text = f"[bold {self._colors['primary']}]LIVE MATCH TRACKER[/bold {self._colors['primary']}]"
            
            self.console.print(Panel(
                header_text,
                box=box.DOUBLE,
                style=self._colors["primary"]
            ))
            
            # Show global match clock
            clock_text = f"🕐 {minute}'"
            if minute == 0:
                clock_text = "🕐 Kick-off"
            elif minute >= 90:
                clock_text = "🕐 Full-time"
            
            self.console.print(f"\n{clock_text}\n", style=f"bold {self._colors['primary']}", justify="center")
            self.console.print(matches_table)
            
            if follow_your_team and 'other_table' in locals() and other_table.row_count > 0:
                self.console.print("\n")
                self.console.print(other_table)
            
            # Show goal alerts for this minute
            goals_this_minute = []
            for match in all_match_events:
                for event in match['goal_events']:
                    if event['minute'] == minute:
                        if event['team'] == 'home':
                            scoring_team = league.get_team_by_index(match['home_idx'])
                        else:
                            scoring_team = league.get_team_by_index(match['away_idx'])
                        
                        if scoring_team is not None:
                            team_name = scoring_team.name
                            
                            # Special highlight for user's team goals
                            if my_team_idx is not None and (match['home_idx'] == my_team_idx or match['away_idx'] == my_team_idx):
                                goals_this_minute.append(f"⚽ [bold {self._colors['primary']}]GOAL! {team_name} scores at {minute}'![/bold {self._colors['primary']}]")
                            else:
                                goals_this_minute.append(f"⚽ {team_name} scores at {minute}'")
            
            if goals_this_minute:
                self.console.print("")
                for goal in goals_this_minute:
                    self.console.print(goal)
            
            # Pause for effect
            if minute < 90:
                time.sleep(1.2 if goals_this_minute else 0.6)
            else:
                time.sleep(1.5)