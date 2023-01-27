"""
main.py: game launcher
"""

import ffmCLI

print("Thanks for playing Fantasy Manager.\n")
user_name = input("What is your user name (enter to skip)? ")
ffmCLI.play_game(user_name)
