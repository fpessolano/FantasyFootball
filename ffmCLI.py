"""
ffmCLI.py: command line game
"""

from cligaming.ffm import FFM
from termcolor import colored
from support.screen_utils import clear

"""
This is he main loop of the game.
The used name is required to save and load games, but it is not necessary for playing.
"""


def startScreen(user_id="", version=""):
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
*     | | | (_| | | | | || (_| \__ \ |_| |           * 
*     |_|  \__,_|_| |_|\__\__,_|___/\__, |           *
*     |  \/  |                       __/ |           *
*     | \  / | __ _ _ __   __ _  __ |___/_ _ __      *
*     | |\/| |/ _` | '_ \ / _` |/ _` |/ _ \ '__|     *
*     | |  | | (_| | | | | (_| | (_| |  __/ |        *
*     |_|  |_|\__,_|_| |_|\__,_|\__, |\___|_|        *
*                                __/ |               *
*                               |___/                *
*                                                    *""")
  print("*" + f'Version {version_colored}'.center(61) + "*")
  print("""*                                                    *
******************************************************
  """)


def play_game(user_id="", version=""):

  startScreen(user_id, version)
  game = FFM(user_id)

  command = ""
  while True:
    if user_id:
      while command != "n" and command != "l":
        command = input("             (N)ew game or (L)oad game? ").lower()
        if command != "n" and command != "l":
          print("!!! ERROR: please write a valid command !!!")
    else:
      command = "n"

    clear()
    print()
    
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
