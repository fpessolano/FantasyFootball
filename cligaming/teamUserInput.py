import random
import sys

from tabulate import tabulate

from game.team import Team
from game.gamestats import FootballStatistics


# TODO add stars
def fullyCustomLeague():
    """
    generates a full custom league
    :return:  number of teams to be relegates and list of teamNames
    """
    validInput = False
    numberTeams = 0
    relegationZone = 0
    leagueName = input('What is the name of new competition? ')
    leagueName.replace('_', " ").strip()
    while not validInput:
        try:
            numberTeams = input("How many teams? ")
            numberTeams = int(numberTeams)
            relegationZone = input("How many teams relegate? ")
            relegationZone = int(relegationZone)
            if numberTeams > 0 and numberTeams > relegationZone:
                validInput = True
            else:
                print(f'!!! ERROR: {numberTeams} and {relegationZone} are not valid values\n')
        except:
            print("!!! ERROR: please write valid numbers !!!")
    print()
    # user inout all team names
    teams = []
    names = []
    print("Please provide the teams names.")
    for i in range(numberTeams):
        name = input(f'  team {i + 1} name? ').lower().title().strip()
        while name == "" or name in names:
            print("!!! Error: a name must be unique and not empty !!!")
            name = input(f'  team {i + 1} name? ').lower().title()
        try:
            stars = float(input(f'  numbers of stars for team {name} (0 to 5)? '))
            names.append(name)
            teams.append(Team(name=name, elo=1000+200*stars))
        except:
            print('Number of stars is not valid')
    Team.calculateStars(teams)
    return leagueName, relegationZone, teams


def existingLeague(skipTeams=False):
    """
    generates a league from an existing one
    :return:  number of teams to be relegates and list of teams
    """
    stats = FootballStatistics()
    availableLeagues = []
    for country in stats.countries():
        for league in stats.leagues(country):
            teamsInLeague = stats.teams(country, league)
            if len(teamsInLeague) > 10:
                availableLeagues.append({
                    'country': country,
                    'league': league,
                    'teams': teamsInLeague
                })
    if not skipTeams:
        print('Available leagues:\n')
        [print(f'({i}) {availableLeagues[i]["country"]}-{availableLeagues[i]["league"]}') for i in
         range(len(availableLeagues))]
    try:
        selected = int(input('\nWhich league di you want to play? '))
        while selected < 0 or selected > len(availableLeagues) - 1:
            print(f'League number {selected} is not available!')
            selected = int(input('\nWhich league di you want to play? '))
        teamsList = [Team(name=x, elo=availableLeagues[selected]['teams'][x]['Elo']) for x in
                     availableLeagues[selected]['teams']]
        leagueName = f'{availableLeagues[selected]["country"]}-{availableLeagues[selected]["league"]}'
        teamsList = customise(teamsList)
        return leagueName, stats.relegation(availableLeagues[selected]['country']), teamsList
    except:
        print(f'Please type a valid number!')
        return existingLeague(True)


def randomTeams():
    """
    generates a random league from exiting teams
    :return:  number of teams to be relegates and list of teams
    """
    validInput = False
    numberTeams = 0
    relegationZone = 0
    top100 = False
    leagueName = input('What is the name of new competition? ')
    leagueName.replace('_', " ").strip()
    while not validInput:
        try:
            numberTeams = input("How many teams? ")
            numberTeams = int(numberTeams)
            relegationZone = input("How many teams relegate? ")
            relegationZone = int(relegationZone)
            if numberTeams > 0 and numberTeams > relegationZone:
                validInput = True
            else:
                print(f'!!! ERROR: {numberTeams} must be positive and greater than {relegationZone}\n')
                continue
            top100 = input('Do you want random teams only from the best 100 (y for yes)? ').lower() == 'y'
        except:
            print("!!! ERROR: please write valid numbers !!!")
    print()
    if top100:
        teams = [Team(name=y['Club'], elo=y['Elo']) for _, y in FootballStatistics().getTopTeams().items()]
    else:
        teams = [Team(name=y['Club'], elo=y['Elo']) for y in FootballStatistics().getTeams()]
    random.shuffle(teams)
    teams = customise(teams[:numberTeams])
    return leagueName, relegationZone, teams


def customise(teams):
    headers = ['ID', 'Team', 'Stars']
    names = printTeamList(headers, teams)
    print()
    if input('Do you want to replace a team (y for yes)? ').lower() == 'y':
        art = 'the'
        while True:
            try:
                ids = input(f'Provide the id of {art} team to be replaced or c to continue? ').lower()
                if ids == 'c':
                    break
                else:
                    teamId = int(ids)
                    newName = input('Please provide the new team name? ')
                    if names in names:
                        print('The name cannot be used, because it is already present or has been removed.')
                        continue
                    try:
                        stars = float(input(f'Please provide the numbers of stars for team {newName} (0 to 5)? '))
                        names.append(newName)
                        teams[teamId].name = newName
                        teams[teamId].eloFromStars(stars, True)
                        print()
                        names = printTeamList(headers, teams, False)
                        print()
                    except:
                        print('Number of stars is not valid')
            except:
                print('Invalid id/command')

    return teams


def printTeamList(headers, teams, calculateStars=True):
    if calculateStars:
        Team.calculateStars(teams)
    table = []
    names = []
    for i in range(len(teams)):
        table.append([i, teams[i].name, teams[i].stars])
        names.append(teams[i].name)
    print(tabulate(table, headers=headers))
    return names


def promotionAndRelegation(league):
    promotedTeams = []
    if input(
            f'The last {league.relegationZone()}'
            f' teams have relegated. Do you want to replace them (y for yes)? ').lower() == 'y':
        currentTeams = league.teams()
        numberTeams = league.teamNumber()
        for i in range(league.relegationZone()):
            accepted = False
            while not accepted:
                newName = input(f'  New team for position {numberTeams - i}/{numberTeams}? ').title()
                if newName not in currentTeams and newName != '':
                    try:
                        stars = float(input(f'  Please provide the ideal numbers of stars'
                                            f' for team {newName} (0 to 5)? '))
                        currentTeams.append(newName)
                        newTeam = Team(name=newName)
                        newTeam.eloFromStars(stars, True)
                        promotedTeams.append(newTeam)
                        accepted = True
                    except:
                        print('Number of stars is not valid')
                else:
                    print("!!! ERROR: please provide another name")
    return promotedTeams


if __name__ == '__main__':
    # ln, rz, teams = randomTeams()
    # ln, rz, teams = fullyCustomLeague()
    ln, rz, teams = existingLeague()
    # existingLeague()
    # [print(x.name, x.elo) for x in teams]
    # print(ln, rz)
    customise(teams)
