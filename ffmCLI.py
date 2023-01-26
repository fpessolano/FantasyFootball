"""
ffmCLI.py: command line game
"""

from cligaming.ffm import FFM
from support.screen_utils import clear

# TODO save crashes ...


def play_game(user_id=""):
    clear()
    if not user_id:
      print("Welcome to FantasyManager")
    else:
      print("Welcome", user_id, "to FantasyManager")
    print("Version 0.3.1_nighly\n")

    game = FFM(user_id)

    command = ""
    while True:
        if user_id:
          while command != "n" and command != "l":
              command = input("(N)ew game or (L)oad game? ").lower()
              if command != "n" and command != "l":
                  print("!!! ERROR: please write a valid command !!!")
        else:
          command = "n"
        if command == "l":
            if game.load():
                break
            else:
                print("Failed to load the saved game")
                command = ""
        else:
            while not game.new():
                print("Failed to create league.", end=' ')
                try_again = input("Try again (y for yes)? ").lower()
                if try_again != 'y':
                    print("Bye Bye!")
                    quit()
            break

    while True:
        if not game.play_round():
            break

        if input("\nPlay again with the same teams (y/n)? ").lower() != "y":
            game.save_end()
            break


if __name__ == '__main__':
    play_game()
