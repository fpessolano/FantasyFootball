"""
main.py: game launcher
"""

import ffmCLI
import os

version = "0.5.0_wip"

user_name = input("What is your name? ")
user_name_with_underscores = user_name.replace(" ", "_")
ffmCLI.play_game(user_name, version)
