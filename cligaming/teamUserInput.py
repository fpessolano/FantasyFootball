import random
# import sys

from tabulate import tabulate

from game.team import Team
from game.gamestats import FootballStatistics

# TODO support for fractional stars
def fully_custom_league():
    """
    generates a full custom league
    :return:  number of teams to be relegates and list of teamNames
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
        except:
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
            stars = float(
                input(f'  numbers of stars for team {name} (0 to 5)? '))
            names.append(name)
            teams.append(Team(name=name, elo=1000 + 200 * stars))
        except:
            print('Number of stars is not valid')
    Team.calculate_stars(teams)
    return league_name, relegation_zone, teams


def existing_league(skip_teams=False):
    """
    generates a league from an existing one
    :return:  number of teams to be relegates and list of teams
    """

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
        selected = int(input('\nWhich league di you want to play? '))
        while selected < 0 or selected > len(available_leagues) - 1:
            print(f'League number {selected} is not available!')
            selected = int(input('\nWhich league di you want to play? '))
        teams_list = [
            Team(name=x, elo=available_leagues[selected]['teams'][x]['Elo'])
            for x in available_leagues[selected]['teams']
        ]
        league_name = f'{available_leagues[selected]["country"]}-{available_leagues[selected]["league"]}'
        teams_list = customise(teams_list)
        return league_name, stats.relegation(
            available_leagues[selected]['country']), teams_list
    except:
        print('Please type a valid number!')
        return existing_league(True)


def random_teams():
    """
    generates a random league from exiting teams
    :return:  number of teams to be relegates and list of teams
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
                'Do you want random teams only from the best 100 (y for yes)? '
            ).lower() == 'y'
        except:
            print("!!! ERROR: please write valid numbers !!!")
    print()
    if top100:
        teams = [
            Team(name=y['Club'], elo=y['Elo']) for _, y in FootballStatistics().get_top_teams().items()
        ]
    else:
        teams = [
            Team(name=y['Club'], elo=y['Elo']) for y in FootballStatistics().get_teams()
        ]
    random.shuffle(teams)
    teams = customise(teams[:number_teams])
    return league_name, relegation_zone, teams


def customise(teams):
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
                    except:
                        print('Number of stars is not valid')
            except:
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
    if input(
            f'The last {league.relegation_zone()}'
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
                            input(
                                f'  Please provide the ideal numbers of stars'
                                f' for team {new_name} (0 to 5)? '))
                        current_teams.append(new_name)
                        new_team = Team(name=new_name)
                        new_team.elo_from_stars(stars, True)
                        promoted_teams.append(new_team)
                        accepted = True
                    except:
                        print('Number of stars is not valid')
                else:
                    print("!!! ERROR: please provide another name")
    return promoted_teams


if __name__ == '__main__':
    # ln, rz, teams = randomTeams()
    # ln, rz, teams = fullyCustomLeague()
    ln, rz, teams = existing_league()
    # existingLeague()
    # [print(x.name, x.elo) for x in teams]
    # print(ln, rz)
    customise(teams)
