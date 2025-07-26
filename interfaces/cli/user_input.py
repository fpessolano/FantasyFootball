import random
from utils import screen as su

from tabulate import tabulate

from core.entities.team import Team
from stats.gamestats import FootballStatistics
from core.storage.team_storage import team_storage


# TODO support for fractional stars
def fully_custom_league():
  """
    generates a full custom league
    :return:  league name, number of teams to be relegates,list of team Names and my team name
    """
  valid_input = False
  number_teams = 0
  relegation_zone = 0
  league_name = input('What is the name of new competition? ')
  league_name.replace('_', " ").strip()
  while not valid_input:
    try:
      number_teams = input("How many teams? ")
      number_teams = int(number_teams)
      relegation_zone = input("How many teams relegate? ")
      relegation_zone = int(relegation_zone)
      if number_teams > 0 and number_teams > relegation_zone:
        valid_input = True
      else:
        print(
          f'!!! ERROR: {number_teams} and {relegation_zone} are not valid values\n'
        )
    except ValueError:
      print("!!! ERROR: please write valid numbers !!!")
  print()
  # user inout all team names
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
  return league_name, relegation_zone, teams, my_team


def existing_league(skip_teams=False):
  """
    generates a league from an existing one
    :return:  league name, number of teams to be relegates,list of team Names and my team name
    """
  
  # Check if optimized team storage is available
  if team_storage._loaded_from_raw:
    return _select_country_then_league(skip_teams)
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
    if not skip_teams:
      print('Available leagues:\n')
      [
        print(
          f'({i}) {available_leagues[i]["country"]}-{available_leagues[i]["league"]}'
        ) for i in range(len(available_leagues))
      ]
    try:
      selected = int(input('\nWhich league do you want to play? '))
      while selected < 0 or selected > len(available_leagues) - 1:
        print(f'League number {selected} is not available!')
        selected = int(input('\nWhich league do you want to play? '))
      teams_list = [
        Team(name=x, elo=available_leagues[selected]['teams'][x]['Elo'])
        for x in available_leagues[selected]['teams']
      ]
      league_name = f'{available_leagues[selected]["country"]}-{available_leagues[selected]["league"]}'
      teams_list = customise(teams_list)
      my_team = select_my_team(teams_list)
      return league_name, stats.relegation(
        available_leagues[selected]['country']), teams_list, my_team
    except (ValueError, IndexError) as e:
      print('Please type a valid number!')
      return existing_league(True)


def random_teams():
  """
    generates a random league from exiting teams
    :return:  league name, number of teams to be relegates,list of team Names and my team name
    """
  valid_input = False
  number_teams = 0
  relegation_zone = 0
  top100 = False
  league_name = input('What is the name of new competition? ')
  league_name.replace('_', " ").strip()
  while not valid_input:
    try:
      number_teams = input("How many teams? ")
      number_teams = int(number_teams)
      relegation_zone = input("How many teams relegate? ")
      relegation_zone = int(relegation_zone)
      if number_teams > 0 and number_teams > relegation_zone:
        valid_input = True
      else:
        print(
          f'!!! ERROR: {number_teams} must be positive and greater than {relegation_zone}\n'
        )
        continue
      top100 = input(
        'Do you want random teams only from the best 100 (y for yes)? ').lower(
        ) == 'y'
    except ValueError:
      print("!!! ERROR: please write valid numbers !!!")
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
  return league_name, relegation_zone, teams_list, my_team


def select_my_team(teams):
  """
    Selects the player terms
    :return: the player team id
    """
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


def promotion_and_relegation(league):
  promoted_teams = []
  if input(f'The last {league.relegation_zone()}'
           f' teams have relegated. Do you want to replace them (y for yes)? '
           ).lower() == 'y':
    current_teams = league.teams()
    number_teams = league.team_number()
    for i in range(league.relegation_zone()):
      accepted = False
      while not accepted:
        new_name = input(
          f'  New team for position {number_teams - i}/{number_teams}? '
        ).title()
        if new_name not in current_teams and new_name != '':
          try:
            stars = float(
              input(f'  Please provide the ideal numbers of stars'
                    f' for team {new_name} (0 to 5)? '))
            current_teams.append(new_name)
            new_team = Team(name=new_name)
            new_team.elo_from_stars(stars, True)
            promoted_teams.append(new_team)
            accepted = True
          except ValueError:
            print('Number of stars is not valid')
        else:
          print("!!! ERROR: please provide another name")
  return promoted_teams


def _select_country_then_league(skip_teams=False):
  """
  Two-step selection: first country, then league within that country.
  
  Args:
    skip_teams: If True, skip the display (used for retries)
    
  Returns:
    tuple: (league_display_name, relegation_zone, teams_list, my_team)
  """
  leagues_by_country = team_storage.get_leagues_by_country()
  
  # Step 1: Select Country
  while True:
    # Always clear screen and show choices
    su.clear()
    print('Select a country:\n')
      
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
    print()
    
    try:
      # Get country selection
      country_choice = int(input('Select country number: '))
      if 0 <= country_choice < len(countries):
        selected_country = countries[country_choice]
        available_leagues = leagues_by_country[selected_country]
        break
      else:
        print(f'Country number {country_choice} is not available!')
        input('Press Enter to try again...')
        continue
        
    except (ValueError, IndexError):
      print('Please type a valid number!')
      input('Press Enter to try again...')
      continue
  
  # Step 2: Select League within chosen country (if more than one)
  if len(available_leagues) == 1:
    # Only one league - auto-select it
    league_name, team_count, has_estimated = available_leagues[0]
    print(f'\nAuto-selected: {selected_country} - {league_name} ({team_count} teams)')
    input('Press Enter to continue...')
  else:
    # Multiple leagues - let user choose
    while True:
      su.clear()
      print(f'{selected_country} - Select a league:\n')
      
      for i, (league_name, team_count, has_estimated) in enumerate(available_leagues):
        print(f'({i}) {league_name} ({team_count} teams)')
      
      print(f'(b) Back to country selection')
      print()
      
      try:
        choice = input('Select league number (or "b" for back): ').strip().lower()
        
        if choice == 'b':
          return _select_country_then_league()  # Go back to country selection
        
        league_choice = int(choice)
        if 0 <= league_choice < len(available_leagues):
          league_name, team_count, has_estimated = available_leagues[league_choice]
          break
        else:
          print(f'League number {league_choice} is not available!')
          input('Press Enter to try again...')
          continue
          
      except (ValueError, IndexError):
        print('Please type a valid number or "b" for back!')
        input('Press Enter to try again...')
        continue
  
  teams_list = team_storage.get_league_teams(league_name, selected_country)
  league_display_name = f'{selected_country}-{league_name}'
  
  teams_list = customise(teams_list)
  my_team = select_my_team(teams_list)
  return league_display_name, 3, teams_list, my_team  # Default relegation zone


if __name__ == '__main__':
  # ln, rz, teams = randomTeams()
  # ln, rz, teams = fullyCustomLeague()
  ln, rz, teams = existing_league()
  # existingLeague()
  # [print(x.name, x.elo) for x in teams]
  # print(ln, rz)
  customise(teams)
