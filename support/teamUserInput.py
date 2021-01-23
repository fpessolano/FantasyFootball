import pprint
import random

from support.gamestats import FootballStatistics


def fullyCustomLeague():
    """
    generates a full custom league
    :return:  number of teams to be relegates and list of teamNames
    """
    validInput = False
    numberTeams = 0
    relegationZone = 0
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
    teamNames = []
    print("Please provide the teams names.")
    for i in range(numberTeams):
        name = input(f'  team {i + 1} name? ').lower().title().strip()
        while name == "" or name in teamNames:
            print("!!! Error: a name must be unique and not empty !!!")
            name = input(f'  team {i + 1} name? ').lower().title()
        teamNames.append(name)
    return relegationZone, teamNames


# TODO needs that fullyCustomLeague also returns teams and not names
#  there fore League class needs to be modified first
def existingLeague(skipTeams=False):
    """
    generates a league from an existing one
    :return:  number of teams to be relegates and list of teamNames
    """
    stats = FootballStatistics()
    availableLeagues = []
    for country in stats.countries():
        for league in stats.leagues(country):
            teams = stats.teams(country, league)
            if len(teams) > 10:
                availableLeagues.append({
                    'country': country,
                    'league': league,
                    'teams': teams
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
        # todo here, show list of teams tabulated, ask if proceed or modify a team
        return availableLeagues[selected]["teams"]
    except:
        print(f'Please type a valid number!')
        return existingLeague(True)


# TODO needs that fullyCustomLeague also returns teams and not names
#  there fore League class needs to be modified first
def randomTeams():
    """
    generates a random league from exiting teams
    :return:  number of teams to be relegates and list of teamNames
    """
    validInput = False
    numberTeams = 0
    relegationZone = 0
    top100 = False
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
        teams = [y for _,y in FootballStatistics().getTopTeams().items()]
    else:
        teams = FootballStatistics().getTeams()
    random.shuffle(teams)
    return teams[:numberTeams]

# TODO everything
def customise(teams):
    return teams

if __name__ == '__main__':
    pprint.pp(randomTeams())

