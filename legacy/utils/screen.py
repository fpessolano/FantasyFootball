from os import system, name
from termcolor import colored
import sys

def clear():
    """Clear the terminal screen in a cross-platform way"""
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')
    # Fallback for some terminals
    print('\033[H\033[J', end='')
    sys.stdout.flush()

def highlight_table_row(table, row_number, color="green", format=["bold"]):
  """
  Given a tabulated string it highlights a given row
  :param table: The table string to highlight
  :param row_number: Row to be highlighted (0-based, excluding header)
  :param color: Highlight color (green for win, red for loss, yellow for draw)
  :param format: A termcolor list formatting the highlighted row
  :return: Table with highlighted row
  """
  complete_table = ""
  lines = table.split('\n')
  
  for ids, line in enumerate(lines):
    if ids == row_number + 2:  # +2 to account for header and separator
      complete_table += colored(line, color, attrs=format)
    else:
      complete_table += line
    
    # Add newline except for last line
    if ids < len(lines) - 1:
      complete_table += '\n'
      
  return complete_table


def print_colored_message(message, color="white", attrs=None):
  """Print a colored message to the terminal"""
  if attrs is None:
    attrs = []
  print(colored(message, color, attrs=attrs))


def format_team_name(team_name, is_user_team=False):
  """Format team name with special highlighting for user's team"""
  if is_user_team:
    return colored(team_name, "cyan", attrs=["bold"])
  return team_name