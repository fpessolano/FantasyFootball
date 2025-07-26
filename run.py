#!/usr/bin/env python3
"""
run.py: Fantasy Football Manager launcher

Entry point for the Fantasy Football Manager with Rich terminal interface.
"""

from interfaces.cli.rich_game_cli import RichFFM
from rich.console import Console

__version__ = "0.9.1"


def main():
    """Main entry point for Rich UI version."""
    console = Console()
    
    # Clear screen at startup
    console.clear()
    
    # Get user name
    console.print("[bold cyan]Welcome to Fantasy Football Manager![/bold cyan]\n")
    user_name = input("What is your name? ")
    user_name_with_underscores = user_name.replace(" ", "_")
    
    # Ask about terminal background
    console.print("\n[bold]Terminal Background Detection[/bold]")
    console.print("To optimize colors for readability:")
    console.print("  [bold]L[/bold] - Light background (white/light terminal)")
    console.print("  [bold]D[/bold] - Dark background (black/dark terminal)")
    
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
    
    # Clear and start game
    console.clear()
    
    # Create and start the game with theme
    game = RichFFM(user_name, __version__, theme)
    
    try:
        game.start()
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Game interrupted by user.[/yellow]")
        console.print("[bold green]Thanks for playing Fantasy Football Manager![/bold green]")
    except Exception as e:
        console.print(f"\n[red]An error occurred: {e}[/red]")
        console.print("[yellow]Please report this issue if it persists.[/yellow]")


if __name__ == "__main__":
    main()