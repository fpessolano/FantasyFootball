import csv
import sys

from support.diskstore import SaveFile


class FootballStatistics:
    """
    retrieve official team data (when needed) from online sources
    currently supporting elo ratings data from clubelo.com
    """

    def __init__(self, codefile='countrycodes.csv', datafile='leagues.dat', elo_csv = 'elo.csv'):
        """
        Initialise the instance reading the leagues data and updating the data file if a file called elo.csv is present
        """

        newData = {}
        countryCodes = {}
        self.__relegationZones = {}
        with open(codefile, 'r') as file:
            Lines = file.readlines()
        for line in Lines:
            code, country, relegationZone = line.strip().split(',')
            countryCodes[code.strip()] = country.strip().title()
            try:
                if relegationZone != '-1':
                    self.__relegationZones[country.strip().title()] = int(relegationZone)
            except:
                pass
        self.__datafile = SaveFile(datafile)
        self.__data = self.__datafile.readState('__leagues')
        if not self.__data:
            self.__data = {}
        try:
            # read the new data and merge it (not in this block)
            with open(elo_csv, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row:
                        team = dict(row)
                        if team['Club'] and team['Country'] in countryCodes:
                            country = countryCodes[team['Country']]
                            try:
                                if team['Rank'] == 'None':
                                    rank = -1
                                else:
                                    rank = int(team['Rank'])
                                record = {
                                    'Rank': rank,
                                    'Elo': float(team['Elo'])
                                }
                                if country in newData:
                                    try:
                                        newData[country][team['Level']][team['Club']] = record
                                    except:
                                        newData[country][team['Level']] = {team['Club']: record}
                                else:
                                    newData[country] = {}
                                    newData[country][team['Level']] = {team['Club']: record}
                            except:
                                print('error')
                                pass
        except:
            # no updated data is available
            pass
        if len(newData) > 0:
            for country in newData:
                try:
                    _ = self.__data[country]
                except:
                    self.__data[country] = {}
                for level in newData[country]:
                    try:
                        _ = self.__data[country][level]
                    except:
                        self.__data[country][level] = {}
                    for team in newData[country][level]:
                        self.__data[country][level][team] = newData[country][level][team]
            self.__datafile.writeState('__leagues', self.__data)

    def countries(self):
        return self.__data.keys()

    def leagues(self, country):
        try:
            return self.__data[country].keys()
        except:
            return None

    def teams(self, country, level):
        try:
            return self.__data[country][level]
        except:
            return None

    def relegation(self, country):
        try:
            return self.__relegationZones[country]
        except:
            return 0

    def getTeams(self, lvl=10, elo=0):
        teams = []
        for country in self.__data:
            for level in self.__data[country]:
                for team in self.__data[country][level]:
                    try:
                        if int(level) <= lvl and self.__data[country][level][team]['Elo'] > elo:
                            teamStat = {
                                'Club': team,
                                'Rank': self.__data[country][level][team]['Rank'],
                                'Elo': self.__data[country][level][team]['Elo']
                            }
                            teams.append(teamStat)
                    except:
                        pass
        return teams

    def getTopTeams(self, top=1, bottom=100):
        teams = {}
        if top < 1:
            top = 1
        for country in self.__data:
            for level in self.__data[country]:
                for team in self.__data[country][level]:
                    try:
                        if self.__data[country][level][team]['Rank'] != -1 and self.__data[country][level][team][
                            'Rank'] <= bottom and self.__data[country][level][team]['Rank'] >= top:
                            teamStat = {
                                'Club': team,
                                'Rank': self.__data[country][level][team]['Rank'],
                                'Elo': self.__data[country][level][team]['Elo']
                            }
                            teams[self.__data[country][level][team]['Rank']] = teamStat
                    except:
                        pass
        return {k: v for k, v in sorted(teams.items(), key=lambda item: item[0])}
