"""
run.py: Fantasy Football Manager with Rich UI

Main entry point for the Fantasy Football Manager using Rich terminal UI.
"""

from interfaces.cli.rich_game_cli import RichFFM
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
import json
import os
import signal
import sys

__version__ = "1.0.0"

def load_user_preferences():
    """Load user preferences from previous session."""
    prefs_file = os.path.join("saves_json", "user_preferences.json")
    try:
        if os.path.exists(prefs_file):
            with open(prefs_file, 'r') as f:
                return json.load(f)
    except Exception:
        pass
    return None

def save_user_preferences(user_name, theme):
    """Save user preferences for next session."""
    prefs_file = os.path.join("saves_json", "user_preferences.json")
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(prefs_file), exist_ok=True)
        
        preferences = {
            "user_name": user_name,
            "theme": theme,
            "last_used": __version__
        }
        
        with open(prefs_file, 'w') as f:
            json.dump(preferences, f, indent=2)
    except Exception:
        pass  # Silently fail if we can't save preferences

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully with immediate exit."""
    from rich.console import Console
    console = Console()
    
    console.print('\n\n[bold yellow]⚠️  Ctrl+C detected![/bold yellow]')
    console.print('[bold cyan]🔄 Exiting Fantasy Football Manager...[/bold cyan]')
    console.print('[green]📁 Your progress has been automatically saved.[/green]')
    console.print('[blue]👋 Thanks for playing![/blue]')
    sys.exit(0)

def main():
    """Main entry point."""
    # Set up graceful exit handling
    signal.signal(signal.SIGINT, signal_handler)
    
    # Clear screen at startup
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Initialize Rich console
    console = Console()
    
    # Try to load previous preferences
    previous_prefs = load_user_preferences()
    
    # Get user name with Rich formatting
    if previous_prefs:
        console.print(Panel(
            f"[bold cyan]Welcome Back![/bold cyan]\n\n"
            f"Previous user: [bold]{previous_prefs['user_name']}[/bold]\n"
            f"Theme: [bold]{previous_prefs['theme']}[/bold]",
            title="[bold]User Setup[/bold]",
            box=box.ROUNDED
        ), justify="center")
        
        user_name = input(f"\nWhat is your name? (Enter for '{previous_prefs['user_name']}'): ").strip()
        if not user_name:
            user_name = previous_prefs['user_name']
            theme = previous_prefs['theme']
            console.print(f"\n[green]Welcome back {user_name}! Using {theme} theme from last session.[/green]")
            user_name_with_underscores = user_name.replace(" ", "_")
            
            # Save preferences again to update last_used
            save_user_preferences(user_name, theme)
            
            # Create and start the game with Rich UI
            game = RichFFM(user_name_with_underscores, __version__, theme)
            game.start()
            return
    else:
        console.print(Panel(
            "[bold cyan]Welcome to Fantasy Football Manager![/bold cyan]\n\n"
            "Let's set up your profile",
            title="[bold]First Time Setup[/bold]",
            box=box.ROUNDED
        ), justify="center")
        
        user_name = input("\nWhat is your name? ").strip()
        if not user_name:
            user_name = "Player"
    
    user_name_with_underscores = user_name.replace(" ", "_")
    
    # Ask about terminal background with Rich formatting
    console.print("\n")
    theme_table = Table(show_header=True, header_style="bold cyan", box=box.ROUNDED)
    theme_table.add_column("Option", style="bold cyan", width=8, justify="center")
    theme_table.add_column("Description", style="white")
    
    theme_table.add_row("L", "Light background (white/light terminal)")
    theme_table.add_row("D", "Dark background (black/dark terminal)")
    
    console.print(Panel(
        theme_table,
        title="[bold]Terminal Background for Maximum Contrast[/bold]",
        box=box.ROUNDED
    ), justify="center")
    
    while True:
        theme_choice = input("\nIs your terminal background Light or Dark? (L/D): ").upper().strip()
        if theme_choice in ['L', 'LIGHT']:
            theme = "light"
            break
        elif theme_choice in ['D', 'DARK']:
            theme = "dark"
            break
        else:
            console.print("[red]Please enter L for Light or D for Dark[/red]")
    
    # Save preferences for next session
    save_user_preferences(user_name, theme)
    
    # Create and start the game with Rich UI
    game = RichFFM(user_name_with_underscores, __version__, theme)
    game.start()


if __name__ == "__main__":
    main()