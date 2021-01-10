import tabulate
from modules.matchDay import *
from modules.setup import *
from modules.support import *

if __name__ == '__main__':
    print("Welcome to Football Manager Matteo 2021")
    print("Version 0.1\n")
    numberTeams = 0
    valid = False
    relegationZone = 0
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
    spare = False
    nt = numberTeams
    if numberTeams % 2 == 1:
        numberTeams += 1
        spare = True
    calendar = defineCalender(numberTeams, 100000)
    while not calenderCorrectness(calendar):
        print("Failed to create a calender, sorry")
        again = input("Should i try again? ").lower()
        if again != "y":
            print("bye bye\n")
            quit()
    teams = defineRoster(nt)
    while True:
        command = input("(F)ull season or (S)ingle game? ").upper()
        for day in range(2 * (numberTeams - 1)):
            print()
            if not matchDay(day + 1, calendar, teams, spare):
                print("error")
                quit()
            standings = orderStanding(teams)
            if command != "F":
                command = input("(F)inish season, (C)ontinue, (S)tandings or (Q)uit? ").upper()
                while command != "C" and command != "F":
                    if command != "S" and command != "Q":
                        print("Invalid Command")
                    elif command == "Q":
                        print("One day you will be able to save also")
                        print("Thanks for playing")
                        quit()
                    elif command == "S":
                        print()
                        header = standings[0].keys()
                        rows = [x.values() for x in standings]
                        print(tabulate.tabulate(rows, header))
                    print()
                    command = input("(F)inish season, (C)ontinue, (S)tandings or (Q)uit? ").upper()
        print("\nThe season has finished. The final standings are:\n")
        teams = orderStanding(teams)
        header = teams[0].keys()
        rows = [x.values() for x in teams]
        print(tabulate.tabulate(rows, header))
        again = input("\nPlay again with the same teams (y/n)? ").lower()
        if again != "y":
            print("\nThanks for playing!")
            quit()
        teams = updateRoster(teams,relegationZone)
        print()
