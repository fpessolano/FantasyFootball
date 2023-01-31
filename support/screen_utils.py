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
  complete_table =""
  for ids, line in enumerate(table.split('\n')):
    if ids == row_number+2:
      complete_table += colored(line, color, attrs=format) + '\n'
    else:
      complete_table += line + '\n'
  return complete_table