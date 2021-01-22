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
