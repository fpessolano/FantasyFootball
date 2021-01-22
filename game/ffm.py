from game.league import League
from support.diskstore import SaveFile
from support.teamUserInput import fullyCustomLeague


class FFM:
    """
    Teh Fantasy Football Manager game class
    """

    def __init__(self):
        """
        setting up the basic game variables
        """
        self.saveFile = SaveFile("saves.dat")
        self.league = League()

    def new(self):
        """
        creates a new game
        :return: False in case it fails
        """
        leagueName = input('What is the name of new competition? ')
        leagueName.replace('_', " ").strip()

        relegationZone, teamNames = fullyCustomLeague()

        self.league = League(name=leagueName, teamNames=teamNames, relegationZone=relegationZone)
        return self.league.valid

    def load(self):
        """
        load a saved game
        """
        saves = ', '.join(self.saveFile.stateList())
        print(f'Available saved games: {saves}')
        saveGameName = input("Provide the save game name (enter for \'Autosave\')? ")
        if saveGameName == "":
            saveGameName = 'Autosave'
        savedGame = self.saveFile.readState(saveGameName)
        if not savedGame:
            return False
        self.league.restore(savedGame)
        return True

    def playRound(self):
        """
        plays a game round or complete season
        """
        print(f'\nWelcome to league {self.league.leagueName}\n\n{self.league.orderStanding()}\n')

        seasonCompleted = False
        while not seasonCompleted:
            command = ""
            while command != "F" and command != "C" and command != "Q":
                command = input("(F)inalise season, (C)ontinue to a single game or (Q)uit? ").upper()
                if command != "F" and command != "C" and command != "Q":
                    print("!!! ERROR: please write a valid command !!!")
            if command == "C":
                matchDay = self.league.matchDay()
                if matchDay == "":
                    seasonCompleted = True
                else:
                    print(f'\n{matchDay}\n')
                if input("Do you want to see the standings (y for yes)? ").lower() == 'y':
                    print(f"\nCurrent standings are:\n\n{self.league.orderStanding()}\n")
            elif command == "F":
                # finish to run the season
                showMatches = input("Do you want to see all results (y for yes)? ").lower()
                matchDay = self.league.matchDay()
                while matchDay != "":
                    if showMatches == 'y':
                        print(f'\n{matchDay}')
                    matchDay = self.league.matchDay()
                seasonCompleted = True
                print()
            else:
                self.saveEnd()
                quit()
        print(f"\nThe season has finished. The final standings are:\n\n{self.league.orderStanding()}\n")
        if self.league.relegationZone() > 0:
            if input(
                    f'The last {self.league.relegationZone()}'
                    f' teams have relegated. Do you want to replace them (y for yes)? ').lower() == 'y':
                currentTeams = self.league.teams()
                promotedTeams = []
                numberTeams = self.league.teamNumber()
                for i in range(self.league.relegationZone()):
                    accepted = False
                    while not accepted:
                        newName = input(f'  New team for position {numberTeams - i}/{numberTeams}? ').title()
                        if newName not in currentTeams and newName != '':
                            promotedTeams.append(newName)
                            accepted = True
                        else:
                            print("!!! ERROR: please provide another name")
                self.league.promoted(promotedTeams)
        self.league.prepareNewSeason()

    def saveEnd(self):
        """
        ends the game
        """
        if input("Do you want to save the game (y for yes or anything else for no)? ").lower() == "y":
            saveGameName = input(f'Please give me the save name (enter for \'Autosave\')? ')
            if saveGameName == "":
                saveGameName = f"Autosave"
            else:
                saveGameName.strip().replace(" ", "_")
            self.saveFile.writeState(saveGameName, self.league.data())
        print("\nThanks for playing!")
