import tabulate
from modules.matchday import *
from modules.setup import *
from modules.support import *

if __name__ == '__main__':
    numberTeams = 0
    relegationZone = 0
    calendar = []
    spare = False
    startWeek = 0
    teams = []
    print("Welcome to Football Manager Matteo 2021")
    print("Version 0.1\n")
    command = ""
    while command != "n" and command != "l":
        command = input("(N)ew game or (L)oad game? ").lower()
        if command != "n" and command != "l":
            print("!!! ERROR: please write a valid command !!!")
    if command == "l":
        filename = input("Provide the save game name (enter for default)? ")
        if filename == "":
            filename = "default.save"
        startWeek, teams, calendar, relegationZone, spare = loadGame(filename)
        if startWeek > (len(teams) - 1) * 2 or \
                len(teams) != len(calendar) and not spare or \
                len(teams) != (len(calendar)-1) and spare or \
                relegationZone > len(teams):
            print("Save file is corrupted. Exiting game")
            quit()
        startWeek += 1
        numberTeams = len(teams)
    else:
        valid = False
        while not valid or numberTeams > 16:
            try:
                numberTeams = input("How many teams? ")
                numberTeams = int(numberTeams)
                relegationZone = input("How many teams relegate? ")
                relegationZone = int(relegationZone)
                if numberTeams > 0:
                    valid = True
            except:
                print("!!! ERROR: please write valid numbers !!!")
                pass
        nt = numberTeams
        if numberTeams % 2 == 1:
            numberTeams += 1
            spare = True
        calendar = definecalendar(numberTeams, 100000)
        while not calendarCorrectness(calendar):
            print("Failed to create a calendar, sorry")
            again = input("Should i try again? ").lower()
            if again != "y":
                print("bye bye\n")
                quit()
            else:
                calendar = definecalendar(numberTeams, 100000)
        teams = defineRoster(nt)
    while True:
        print("\nCurrent division")
        orderStanding(teams)
        command = ""
        while command != "F" and command!="C":
            command = input("(F)ull season or (C)ontinue to a single game? ").upper()
            if command != "F" and command != "C":
                print("!!! ERROR: please write a valid command !!!")
        for week in range(startWeek, 2 * (numberTeams - 1)):
            print()
            if not matchDay(week + 1, calendar, teams, spare):
                print("error")
                quit()
            # standings = orderStanding(teams)
            if command != "F":
                command = input("(F)inish season, (C)ontinue, (S)tandings or (Q)uit? ").upper()
                while command != "C" and command != "F":
                    if command != "S" and command != "Q":
                        print("Invalid Command")
                    elif command == "Q":
                        if input("Do you want to save the game (yes or anything else for no)? ").lower() == "y":
                            saveGame(week, teams, calendar, relegationZone, spare)
                        print("Thanks for playing")
                        quit()
                    elif command == "S":
                        print()
                        orderStanding(teams)
                    print()
                    command = input("(F)inish season, (C)ontinue, (S)tandings or (Q)uit? ").upper()
        print("\nThe season has finished. The final standings are:")
        orderedTeams = orderStanding(teams)
        startWeek = 0
        teams = updateRoster(orderedTeams, relegationZone)
        again = input("\nPlay again with the same teams (y/n)? ").lower()
        if again != "y":
            if input("Do you want to save the game (y for yes or anything else for no)? ").lower() == "y":
                saveGame(-1, teams, calendar, relegationZone, spare)
            print("\nThanks for playing!")
            quit()
        print()
