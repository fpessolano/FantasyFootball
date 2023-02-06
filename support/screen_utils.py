from os import system, name
from termcolor import colored

def clear():

    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

def highlight_table_row(table, row_number, color="green", format=["bold"]):
  """
  given a tabulated string it highlights a given row
  :param row number: row to be highlighted
  "param color: highlight color
  :param format: a termcolor list formatting the highlighted row
  """
  complete_table =""
  for ids, line in enumerate(table.split('\n')):
    if ids == row_number+2:
      complete_table += colored(line, color, attrs=format) + '\n'
    else:
      complete_table += line + '\n'
  return complete_table