"""
ffmCLI.py: command line game
"""

__author__ = "Francesco Pessolano"
__copyright__ = "2021"
__version__ = "0.5.0"

from cligaming.ffm import FFM
from support.screen_utils import clear


def play_game():
  clear()
  print("Welcome to FMM2021")
  print("Version 0.2.0\n")

  game = FFM()

  command = ""
  while True:
      while command != "n" and command != "l":
          command = input("(N)ew game or (L)oad game? ").lower()
          if command != "n" and command != "l":
              print("!!! ERROR: please write a valid command !!!")
      if command == "l":
          if game.load():
              break
          else:
              print('Failed to load the saved game')
              command = ""
      else:
          while not game.new():
              print('Failed to create league.', end=' ')
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
