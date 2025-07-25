"""
Rich Terminal UI Interface for Fantasy Football Manager

This module provides enhanced terminal UI using the Rich library for
beautiful tables, progress bars, and interactive displays.
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.text import Text
from rich.align import Align
from rich import box
from datetime import datetime
import time
from typing import List, Dict, Optional, Tuple

from core.entities.team import Team
from core.entities.league import League


class RichInterface:
    """Enhanced terminal interface using Rich library."""
    
    def __init__(self):
        self.console = Console()
        
    def display_title_screen(self, user_name: str, version: str):
        """Display the enhanced title screen."""
        title_text = """
[bold cyan]
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
[/bold cyan]
        """
        
        welcome_panel = Panel(
            Align.center(
                f"{title_text}\n\n[bold green]Welcome {user_name}![/bold green]\n[blue]Version {version}[/blue]"
            ),
            box=box.DOUBLE,
            style="cyan",
            width=60
        )
        
        self.console.print("\n")
        self.console.print(welcome_panel, justify="center")
        self.console.print("\n")
        
    def display_main_menu(self) -> str:
        """Display the main menu with rich formatting."""
        menu_table = Table(show_header=False, box=None, padding=(0, 2))
        menu_table.add_column("Option", style="cyan", no_wrap=True)
        menu_table.add_column("Description", style="white")
        
        menu_table.add_row("[bold cyan]new[/bold cyan]", "Start a new game")
        menu_table.add_row("[bold cyan]load[/bold cyan]", "Load a saved game")
        menu_table.add_row("[bold cyan]help[/bold cyan]", "Show help information")
        menu_table.add_row("[bold cyan]exit[/bold cyan]", "Exit the game")
        
        self.console.print(Panel(menu_table, title="[bold]Main Menu[/bold]", box=box.ROUNDED))
        
        return input("\nType your command: ").strip().lower()
        
    def display_league_table(self, league: League, highlight_team: Optional[int] = None):
        """Display a beautiful league table with team standings."""
        teams = league.order_list()
        
        # Create the table
        table = Table(
            title=f"[bold]{league.league_name} - Season {league.season}[/bold]",
            show_header=True,
            header_style="bold magenta",
            box=box.HEAVY_EDGE,
            title_style="bold cyan",
            caption=f"Match Day {league.current_match_day()}"
        )
        
        # Add columns
        table.add_column("Pos", style="cyan", no_wrap=True, width=4, justify="center")
        table.add_column("Team", style="white", no_wrap=False, width=20)
        table.add_column("MP", justify="center", width=4)
        table.add_column("W", justify="center", style="green", width=4)
        table.add_column("D", justify="center", style="yellow", width=4)
        table.add_column("L", justify="center", style="red", width=4)
        table.add_column("GF", justify="center", width=4)
        table.add_column("GA", justify="center", width=4)
        table.add_column("GD", justify="center", width=4)
        table.add_column("Pts", justify="center", style="bold", width=4)
        table.add_column("Form", justify="center", width=12)
        
        # Add rows
        for i, team_idx in enumerate(teams):
            team = league.get_team_by_index(team_idx)
            pos = i + 1
            
            # Determine row style
            row_style = None
            if highlight_team is not None and team_idx == highlight_team:
                row_style = "bold yellow on blue"
            elif pos <= 4:  # Champions League spots
                row_style = "green"
            elif pos <= 6:  # Europa League spots
                row_style = "cyan"
            elif pos > len(teams) - league.relegation_zone():  # Relegation zone
                row_style = "red"
                
            # Get form (last 5 matches)
            form = self._get_team_form(team)
            
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
                form,
                style=row_style
            )
            
        self.console.print("\n")
        self.console.print(table)
        self.console.print("\n")
        
    def display_match_day_overview(self, league: League, match_day_fixtures: List[Tuple[int, int]], 
                                  my_team: Optional[int] = None):
        """Display match day overview with fixtures."""
        self.console.clear()
        
        # Header
        header = Panel(
            Align.center(
                f"[bold cyan]MATCH DAY {league.current_match_day()}[/bold cyan]\n"
                f"[white]{datetime.now().strftime('%A, %B %d')}[/white]"
            ),
            box=box.DOUBLE,
            style="cyan"
        )
        self.console.print(header)
        self.console.print("\n")
        
        # Fixtures table
        fixtures_table = Table(
            title="[bold]Today's Fixtures[/bold]",
            show_header=True,
            header_style="bold cyan",
            box=box.ROUNDED
        )
        
        fixtures_table.add_column("Home", style="white", no_wrap=True, width=25)
        fixtures_table.add_column("Time", justify="center", style="cyan", width=7)
        fixtures_table.add_column("Away", style="white", no_wrap=True, width=25)
        
        # Add fixtures
        for i, (home_idx, away_idx) in enumerate(match_day_fixtures):
            home_team = league.get_team_by_index(home_idx)
            away_team = league.get_team_by_index(away_idx)
            
            # Highlight user's team match
            home_style = "bold yellow" if my_team == home_idx else "white"
            away_style = "bold yellow" if my_team == away_idx else "white"
            
            time_slot = f"{15 + i*2:02d}:00"  # Stagger kick-off times
            
            home_text = f"{'⭐ ' if my_team == home_idx else ''}{home_team.name}"
            away_text = f"{away_team.name}{' ⭐' if my_team == away_idx else ''}"
            
            fixtures_table.add_row(
                home_text,
                time_slot,
                away_text,
                style="on blue" if my_team in [home_idx, away_idx] else None
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
        
    def simulate_match_with_live_view(self, home_team: Team, away_team: Team, 
                                    home_score: int, away_score: int,
                                    goal_events: List[Dict]) -> None:
        """Display live match simulation with events."""
        match_layout = Layout()
        match_layout.split_column(
            Layout(name="header", size=3),
            Layout(name="score", size=3),
            Layout(name="events", size=10),
            Layout(name="stats", size=8),
            Layout(name="controls", size=3)
        )
        
        # Simulate match progression
        with Live(match_layout, refresh_per_second=1, console=self.console):
            for minute in range(0, 91):
                # Update header
                match_layout["header"].update(
                    Panel(f"[bold]{home_team.name} vs {away_team.name}[/bold]", 
                          style="cyan", box=box.DOUBLE)
                )
                
                # Update score
                current_home_score = sum(1 for e in goal_events if e['team'] == 'home' and e['minute'] <= minute)
                current_away_score = sum(1 for e in goal_events if e['team'] == 'away' and e['minute'] <= minute)
                
                score_text = f"[bold size=large]{current_home_score} - {current_away_score}[/bold]  ⏱️ {minute}'"
                match_layout["score"].update(
                    Align.center(Panel(score_text, box=box.HEAVY))
                )
                
                # Update events
                events_text = "[bold]⚽ Goal Events:[/bold]\n"
                for event in goal_events:
                    if event['minute'] <= minute:
                        icon = "⚽" if event['type'] == 'goal' else "🟥"
                        team_name = home_team.name if event['team'] == 'home' else away_team.name
                        events_text += f"  {event['minute']}' {icon} {event['player']} ({team_name})\n"
                        
                match_layout["events"].update(Panel(events_text, box=box.ROUNDED))
                
                # Update stats
                stats_table = Table(show_header=True, box=box.SIMPLE)
                stats_table.add_column("", style="cyan")
                stats_table.add_column(home_team.name, justify="center")
                stats_table.add_column(away_team.name, justify="center")
                
                # Mock stats that update during the match
                possession_home = 48 + (minute % 10) - 5
                possession_away = 100 - possession_home
                
                stats_table.add_row("Possession", f"{possession_home}%", f"{possession_away}%")
                stats_table.add_row("Shots", str(5 + minute // 15), str(4 + minute // 18))
                stats_table.add_row("On Target", str(2 + minute // 25), str(2 + minute // 30))
                stats_table.add_row("Corners", str(minute // 20), str(minute // 25))
                
                match_layout["stats"].update(Panel(stats_table, title="[bold]Match Stats[/bold]"))
                
                # Update controls
                controls_text = "⏸️  [Space] Pause  ⏩ [F] Fast Forward  ⏭️ [S] Skip to End"
                match_layout["controls"].update(Panel(controls_text, style="dim"))
                
                time.sleep(0.05)  # Fast simulation
                
    def display_match_results_summary(self, results: List[Dict]):
        """Display a summary of match results."""
        results_table = Table(
            title="[bold]Match Results[/bold]",
            show_header=True,
            header_style="bold cyan",
            box=box.ROUNDED
        )
        
        results_table.add_column("Home", style="white", no_wrap=True)
        results_table.add_column("Score", justify="center", style="bold")
        results_table.add_column("Away", style="white", no_wrap=True)
        results_table.add_column("Key Events", style="dim")
        
        for result in results:
            score_style = "green" if result['home_score'] > result['away_score'] else \
                         "red" if result['home_score'] < result['away_score'] else "yellow"
            
            score_text = f"{result['home_score']} - {result['away_score']}"
            
            # Create key events summary
            events = []
            if result.get('goals'):
                events.append(f"⚽ {len(result['goals'])} goals")
            if result.get('red_cards'):
                events.append(f"🟥 {result['red_cards']} red cards")
                
            events_text = ", ".join(events) if events else "No major events"
            
            results_table.add_row(
                result['home_team'],
                score_text,
                result['away_team'],
                events_text,
                style="on blue" if result.get('user_team') else None
            )
            
        self.console.print("\n")
        self.console.print(results_table)
        self.console.print("\n")
        
    def display_season_progress(self, league: League, my_team_idx: Optional[int] = None):
        """Display season progress with statistics."""
        if my_team_idx is not None:
            my_team = league.get_team_by_index(my_team_idx)
            teams_sorted = league.order_list()
            position = teams_sorted.index(my_team_idx) + 1
            
            # Progress bar for season
            total_matches = (league.team_number() - 1) * 2  # Home and away
            played_matches = league.current_match_day() - 1
            
            with Progress() as progress:
                task = progress.add_task(
                    "[cyan]Season Progress", 
                    total=total_matches,
                    completed=played_matches
                )
                
                # Quick stats panel
                stats_text = (
                    f"[bold]⚡ Quick Stats:[/bold]\n"
                    f"- Current Position: [bold]{position}[/bold]\n"
                    f"- Form: {self._get_team_form(my_team)}\n"
                    f"- Points: [bold]{my_team.points()}[/bold]\n"
                    f"- Goal Difference: [bold]{my_team.goals_for - my_team.goals_against:+d}[/bold]"
                )
                
                self.console.print(Panel(stats_text, title=f"[bold]{my_team.name}[/bold]", 
                                       box=box.ROUNDED))
                
    def _get_team_form(self, team: Team, last_n: int = 5) -> str:
        """Get team's recent form as a string of W/D/L indicators."""
        # This would need to be implemented with actual match history
        # For now, return a mock form string
        import random
        form_chars = ['[green]W[/green]', '[yellow]D[/yellow]', '[red]L[/red]']
        return ' '.join(random.choices(form_chars, k=min(last_n, team.matches_played)))
        
    def show_loading(self, message: str = "Loading..."):
        """Display a loading spinner."""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description=message, total=None)
            time.sleep(1)  # Simulate loading