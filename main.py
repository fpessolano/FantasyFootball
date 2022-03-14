"""
main.py: game mode selector
"""

import ffmCLI

print("Thanks for playing Fantasy Manager.\nCurrently only CLI is possible")
user_name = input("What is your user name (enter to skip)? ")
ffmCLI.play_game(user_name)
