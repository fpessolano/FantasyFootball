"""
main.py: game launcher
"""

import ffmCLI
import os

user_name = os.environ['REPL_OWNER']
version = "0.4.1_nightly"

ffmCLI.play_game(user_name, version)
