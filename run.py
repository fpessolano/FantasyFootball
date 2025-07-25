"""
run.py: New modular game launcher

Entry point for the Fantasy Football Manager using the new modular architecture.
"""

from interfaces.cli.game_cli import FFM
from utils.screen import clear
from termcolor import colored

__version__ = "0.7.1"


def start_screen(user_id="", version=""):
    """Display the game start screen."""
    user_id_colored = colored(user_id, "green")
    version_colored = colored(version, "blue")
    print("""
******************************************************
*                                                    *""")
    print("*" + f'Welcome {user_id_colored} to'.center(61) + "*")
    print("""*                                                    *
*                                                    *
*      ______          _                             *
*     |  ____|        | |                            *
*     | |__ __ _ _ __ | |_ __ _ ___ _   _            *
*     |  __/ _` | '_ \| __/ _` / __| | | |           *
*     | | | (_| | | | | || (_| \\__ \\ |_| |           * 
*     |_|  \\__,_|_| |_|\\__\\__,_|___/\\__, |           *
*     |  \/  |                       __/ |           *
*     | \  / | __ _ _ __   __ _  __ |___/_ _ __      *
*     | |\/| |/ _` | '_ \ / _` |/ _` |/ _ \ '__|     *
*     | |  | | (_| | | | | (_| | (_| |  __/ |        *
*     |_|  |_|\\__,_|_| |_|\\__,_|\\__, |\\___|_|        *
*                                __/ |               *
*                               |___/                *
*                                                    *""")
    print("*" + f'Version {version_colored}'.center(61) + "*")
    print("""*                                                    *
******************************************************
  """)


def play_game(user_id="", version=""):
    """Main game loop."""
    start_screen(user_id, version)
    game = FFM(user_id, version)

    command = ""
    while True:
        try:
            command = input("\nType your command (help, new, load, exit): ").strip().lower()
            
            if command == "help":
                game.help()
            elif command == "new":
                game.new_game()
            elif command == "load":
                game.load_game()
            elif command == "exit":
                print("Thanks for playing Fantasy Football Manager!")
                break
            else:
                print("Unknown command. Type 'help' for available commands.")
                
        except KeyboardInterrupt:
            print("\n\nThanks for playing Fantasy Football Manager!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Please try again or type 'exit' to quit.")


def main():
    """Main entry point."""
    # Clear screen at startup for clean presentation
    clear()

    user_name = input("What is your name? ")
    user_name_with_underscores = user_name.replace(" ", "_")

    # Clear screen after name input before starting game
    clear()

    play_game(user_name, __version__)


if __name__ == "__main__":
    main()