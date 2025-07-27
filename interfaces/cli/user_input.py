import random
import signal
import sys
from utils import screen as su

from tabulate import tabulate

from core.entities.team import Team
from stats.gamestats import FootballStatistics
from core.storage.team_storage import team_storage


def _setup_signal_handler():
    """Setup signal handler for graceful exit in user input functions."""
    def signal_handler(sig, frame):
        from rich.console import Console
        console = Console()
        
        console.print('\n\n[bold yellow]⚠️  Ctrl+C detected![/bold yellow]')
        console.print('[bold cyan]🔄 Exiting Fantasy Football Manager...[/bold cyan]')
        console.print('[blue]👋 Thanks for playing![/blue]')
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)


def fully_custom_league():
  """
    generates a full custom league
    :return:  league name, 0 (no relegation), list of team Names and my team name
    """
  _setup_signal_handler()
  valid_input = False
  number_teams = 0
  league_name = input('What is the name of new competition? ')
  league_name.replace('_', " ").strip()
  while not valid_input:
    try:
      number_teams = input("How many teams? ")
      number_teams = int(number_teams)
      if number_teams > 0:
        valid_input = True
      else:
        print(f'!!! ERROR: {number_teams} must be positive\n')
    except ValueError:
      print("!!! ERROR: please write valid numbers !!!")
  print()
  # user input all team names
  teams = []
  names = []
  print("Please provide the teams names.")
  for i in range(number_teams):
    name = input(f'  team {i + 1} name? ').lower().title().strip()
    while name == "" or name in names:
      print("!!! Error: a name must be unique and not empty !!!")
      name = input(f'  team {i + 1} name? ').lower().title()
    try:
      stars = float(input(f'  numbers of stars for team {name} (0 to 5)? '))
      names.append(name)
      teams.append(Team(name=name, elo=1000 + 200 * stars))
    except ValueError:
      print('Number of stars is not valid')
  Team.calculate_stars(teams)
  my_team = select_my_team(teams)
  return league_name, 0, teams, my_team  # No relegation


def existing_league(skip_teams=False):
  """
    generates a league from an existing one
    :return:  league name, number of teams to be relegates,list of team Names and my team name
    """
  _setup_signal_handler()
  
  # Check if optimized team storage is available
  if team_storage._loaded_from_raw:
    result = _select_country_then_league(skip_teams)
    if result is None:
      return None  # User chose to go back
    return result
  else:
    # Fallback to original system
    stats = FootballStatistics()
    available_leagues = []
    for country in stats.countries():
      for league in stats.leagues(country):
        teams_in_league = stats.teams(country, league)
        if len(teams_in_league) > 10:
          available_leagues.append({
            'country': country,
            'league': league,
            'teams': teams_in_league
          })
    print('Available leagues:\n')
    [
      print(
        f'({i}) {available_leagues[i]["country"]}-{available_leagues[i]["league"]}'
      ) for i in range(len(available_leagues))
    ]
    print(f'\n({len(available_leagues)}) ← Back to main menu')
    
    while True:
      try:
        selected = int(input('\nWhich league do you want to play? '))
        
        # Check for back option
        if selected == len(available_leagues):
          return None  # Signal to go back
        
        # Validate selection
        if selected < 0 or selected >= len(available_leagues):
          print(f'❌ Invalid selection! Please choose a number between 0 and {len(available_leagues)}')
          continue
        
        teams_list = [
          Team(name=x, elo=available_leagues[selected]['teams'][x]['Elo'])
          for x in available_leagues[selected]['teams']
        ]
        league_name = f'{available_leagues[selected]["country"]}-{available_leagues[selected]["league"]}'
        teams_list = customise(teams_list)
        my_team = select_my_team(teams_list)
        return league_name, 0, teams_list, my_team  # No relegation
      except ValueError:
        print('❌ Please enter a valid number!')
        continue


def random_teams(number_teams=None):
  """
    generates a random league from existing teams
    :return:  league name, 0 (no relegation), list of team Names and my team name
    """
  _setup_signal_handler()
  valid_input = False
  top100 = False
  
  # Allow calling with predefined number of teams (for testing)
  if number_teams is None:
    league_name = input('What is the name of new competition? ')
    league_name.replace('_', " ").strip()
    while not valid_input:
      try:
        number_teams = input("How many teams? ")
        number_teams = int(number_teams)
        if number_teams > 0:
          valid_input = True
        else:
          print(f'!!! ERROR: {number_teams} must be positive\n')
          continue
        top100 = input(
          'Do you want random teams only from the best 100 (y for yes)? ').lower(
          ) == 'y'
      except ValueError:
        print("!!! ERROR: please write valid numbers !!!")
  else:
    league_name = f"Random League ({number_teams} teams)"
    valid_input = True
  print()
  
  # Use optimized team storage if available
  if team_storage._loaded_from_raw:
    if top100:
      # Get top teams by rating
      teams = team_storage.get_random_teams(number_teams, min_rating=85, max_rating=100)
      if len(teams) < number_teams:
        teams.extend(team_storage.get_random_teams(number_teams - len(teams), min_rating=75, max_rating=84))
    else:
      teams = team_storage.get_random_teams(number_teams)
  else:
    # Fallback to original system
    if top100:
      teams = [
        Team(name=y['Club'], elo=y['Elo'])
        for _, y in FootballStatistics().get_top_teams().items()
      ]
    else:
      teams = [
        Team(name=y['Club'], elo=y['Elo'])
        for y in FootballStatistics().get_teams()
      ]
    random.shuffle(teams)
    teams = teams[:number_teams]
  
  teams_list = customise(teams)
  my_team = select_my_team(teams_list)
  return league_name, 0, teams_list, my_team  # No relegation


def select_my_team(teams):
  """
    Selects the player terms
    :return: the player team id
    """
  _setup_signal_handler()
  su.clear()
  headers = ['ID', 'Team', 'Stars']
  names = print_team_list(headers, teams)
  print()
  while True:
    my_team = int(input('Select your team (type the id)? '))
    if my_team < len(names):
      input(f'Your team is {names[my_team]}. Press enter to continue.')
      su.clear()  # Clear screen after team selection
      return my_team
    else:
      print('Please select an existing team')


def customise(teams):
  """
    Allows thwe players to replace teams with custom ones
    :return: all teams
    """
  _setup_signal_handler()
  su.clear()
  headers = ['ID', 'Team', 'Stars']
  names = print_team_list(headers, teams)
  print()
  if input('Do you want to replace a team (y for yes)? ').lower() == 'y':
    art = 'the'
    while True:
      try:
        ids = input(
          f'Provide the id of {art} team to be replaced or c to continue? '
        ).lower()
        if ids == 'c':
          break
        else:
          team_id = int(ids)
          new_name = input('Please provide the new team name? ')
          if names in names:
            print(
              'The name cannot be used, because it is already present or has been removed.'
            )
            continue
          try:
            stars = float(
              input(
                f'Please provide the numbers of stars for team {new_name} (0 to 5)? '
              ))
            names.append(new_name)
            teams[team_id].name = new_name
            teams[team_id].elo_from_stars(stars, True)
            print()
            names = print_team_list(headers, teams, False)
            print()
          except ValueError:
            print('Number of stars is not valid')
      except (ValueError, IndexError):
        print('Invalid id/command')

  return teams


def print_team_list(headers, teams, calculate_stars=True):
  if calculate_stars:
    Team.calculate_stars(teams)
  table = []
  names = []
  for i in range(len(teams)):
    table.append([i, teams[i].name, teams[i].stars])
    names.append(teams[i].name)
  print(tabulate(table, headers=headers))
  return names


def _select_country_then_league(skip_teams=False):
  """
  Two-step selection: first country, then league within that country.
  
  Args:
    skip_teams: If True, skip the display (used for retries)
    
  Returns:
    tuple: (league_display_name, relegation_zone, teams_list, my_team) or None if user backs out
  """
  _setup_signal_handler()
  # Clear screen for clean league selection interface
  su.clear()
  
  leagues_by_country = team_storage.get_leagues_by_country()
  
  # Step 1: Select Country
  print('🌍 Select a country:\n')
    
  countries = list(leagues_by_country.keys())
  
  # Display countries in columns for better readability
  cols = 3
  for i in range(0, len(countries), cols):
    row_countries = countries[i:i+cols]
    for j, country in enumerate(row_countries):
      league_count = len(leagues_by_country[country])
      if league_count == 1:
        league_text = f"{league_count} league "
      else:
        league_text = f"{league_count} leagues"
      print(f'({i+j:2d}) {country:<20} ({league_text})', end='  ')
    print()  # New line after each row
  
  print(f'\n({len(countries)}) ← Back to main menu')
  print()
  
  while True:
    try:
      # Get country selection
      country_choice = int(input('Select country number: '))
      
      # Check for back option
      if country_choice == len(countries):
        return None  # Signal to go back
      
      # Validate selection
      if country_choice < 0 or country_choice >= len(countries):
        print(f'❌ Invalid selection! Please choose a number between 0 and {len(countries)}')
        continue
      
      selected_country = countries[country_choice]
      available_leagues = leagues_by_country[selected_country]
      break
      
    except ValueError:
      print('❌ Please enter a valid number!')
      continue
  
  # Check if country has only one league
  if len(available_leagues) == 1:
    # Skip league selection and go directly to team selection
    league_name, team_count, has_estimated = available_leagues[0]
    print(f'\n✅ Loading {selected_country} - {league_name}...')
    teams_list = team_storage.get_league_teams(league_name, selected_country)
    league_display_name = f'{selected_country}-{league_name}'
    
    teams_list = customise(teams_list)
    my_team = select_my_team(teams_list)
    return league_display_name, 0, teams_list, my_team  # No relegation
  
  # Step 2: Select League within chosen country (only if multiple leagues)
  su.clear()
  print(f'{selected_country} - Select a league:\n')
  
  for i, (league_name, team_count, has_estimated) in enumerate(available_leagues):
    print(f'({i}) {league_name} ({team_count} teams)')
  
  print(f'\n({len(available_leagues)}) ← Back to country selection')
  print()
  
  while True:
    try:
      # Get league selection
      league_choice = int(input('Select league number: '))
      
      # Check for back option
      if league_choice == len(available_leagues):
        return _select_country_then_league()  # Go back to country selection
      
      # Validate selection
      if league_choice < 0 or league_choice >= len(available_leagues):
        print(f'❌ Invalid selection! Please choose a number between 0 and {len(available_leagues)}')
        continue
      
      league_name, team_count, has_estimated = available_leagues[league_choice]
      teams_list = team_storage.get_league_teams(league_name, selected_country)
      league_display_name = f'{selected_country}-{league_name}'
      
      teams_list = customise(teams_list)
      my_team = select_my_team(teams_list)
      return league_display_name, 0, teams_list, my_team  # No relegation
      
    except ValueError:
      print('❌ Please enter a valid number!')
      continue


if __name__ == '__main__':
  ln, rz, teams = existing_league()
  customise(teams)
