from modules.league import League
from modules.savefile import SaveFile

def playGame():
    print("Welcome to FMM2021")
    print("Version 0.2.0\n")
    saveFile = SaveFile("saves.dat")
    command = ""
    failed = True
    league = League()  # redundant, used to avoid IDE nil checks
    while failed:
        while command != "n" and command != "l":
            command = input("(N)ew game or (L)oad game? ").lower()
            if command != "n" and command != "l":
                print("!!! ERROR: please write a valid command !!!")
        if command == "l":
            saves = ', '.join(saveFile.stateList())
            print(f'Available saved games: {saves}')
            saveGameName = input("Provide the save game name (enter for \'Autosave\')? ")
            if saveGameName == "":
                saveGameName = 'Autosave'
            league.restore(saveFile.readState(saveGameName))
        else:
            leagueName = input('What is the name of new competition? ')
            valid = False
            numberTeams = 0
            relegationZone = 0
            while not valid:
                try:
                    numberTeams = input("How many teams? ")
                    numberTeams = int(numberTeams)
                    relegationZone = input("How many teams relegate? ")
                    relegationZone = int(relegationZone)
                    if numberTeams > 0 and numberTeams > relegationZone:
                        valid = True
                    else:
                        print(f'!!! ERROR: {numberTeams} and {relegationZone} are not valid values\n')
                except:
                    print("!!! ERROR: please write valid numbers !!!")
            print()
            # user inout all team names
            teamNames = []
            print("Please provide the teams names.")
            for i in range(numberTeams):
                name = input(f'  team {i + 1} name? ').lower().title()
                while name == "" or name in teamNames:
                    print("!!! Error: a name must be unique and not empty !!!")
                    name = input(f'  team {i + 1} name? ').lower().title()
                teamNames.append(name)

            league = League(name=leagueName, teamNames=teamNames, relegationZone=relegationZone)
        if league.valid:
            failed = False
        else:
            print('Failed to create league.', end=' ')
            tryAgain = input("Try again (y for yes)? ").lower()
            if tryAgain != 'y':
                print("Bye Bye!")
                quit()
    while True:
        print(f'\nWelcome to league {league.leagueName}\n\n{league.orderStanding()}\n')
        seasonCompleted = False
        while not seasonCompleted:
            command = ""
            while command != "F" and command != "C" and command != "Q":
                command = input("(F)inalise season, (C)ontinue to a single game or (Q)uit? ").upper()
                if command != "F" and command != "C" and command != "Q":
                    print("!!! ERROR: please write a valid command !!!")
            if command == "C":
                matchDay = league.matchDay()
                if matchDay == "":
                    seasonCompleted = True
                else:
                    print(f'\n{matchDay}\n')
                if input("Do you want to see the standings (y for yes)? ").lower() == 'y':
                    print(f"\nCurrent standings are:\n\n{league.orderStanding()}\n")
            elif command == "F":
                # finish to run the season
                showMatches = input("Do you want to see all results (y for yes)? ").lower()
                matchDay = league.matchDay()
                while matchDay != "":
                    if showMatches == 'y':
                        print(f'\n{matchDay}')
                    matchDay = league.matchDay()
                seasonCompleted = True
                print()
            else:
                if input("Do you want to save the game (y for yes or anything else for no)? ").lower() == "y":
                    # league.saveGame()
                    saveGameName = input("Please give me the save name (enter for default)? ")
                    if saveGameName == "":
                        saveGameName = 'Autosave'
                    saveFile.writeState(saveGameName, league.data())
                quit()
        print(f"\nThe season has finished. The final standings are:\n\n{league.orderStanding()}\n")
        if league.relegationZone() > 0:
            if input(
                    f'The last {league.relegationZone()} teams have relegated. Do you want to replace them (y for yes)? ').lower() == 'y':
                currentTeams = league.teams()
                promotedTeams = []
                numberTeams = league.teamNumber()
                for i in range(league.relegationZone()):
                    accepted = False
                    while not accepted:
                        newName = input(f'  New team for position {numberTeams - i}/{numberTeams}? ').title()
                        if newName not in currentTeams and newName != '':
                            promotedTeams.append(newName)
                            accepted = True
                        else:
                            print("!!! ERROR: please provide another name")
                league.promoted(promotedTeams)
        league.prepareNewSeason()

        again = input("\nPlay again with the same teams (y/n)? ").lower()
        if again != "y":
            if input("Do you want to save the game (y for yes or anything else for no)? ").lower() == "y":
                saveGameName = input("Please give me the save name (enter for \'Autosave\')? ")
                if saveGameName == "":
                    saveGameName = f"Autosave {league.leagueName}"
                saveFile.writeState(saveGameName, league.data())
            print("\nThanks for playing!")
            quit()


if __name__ == '__main__':
    playGame()
