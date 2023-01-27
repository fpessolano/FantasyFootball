import csv
import requests
import os
from datetime import date
import time

from support.diskstore import SaveFile

# TODO: automatic update based on age of stats (every week)


class FootballStatistics:
  """
    retrieve official team data (when needed) from online sources
    currently supporting elo ratings data from clubelo.com
    """

  def __init__(self,
               code_file='countrycodes.csv',
               data_file='leagues.dat',
               elo_csv='elo.csv',
               maximum_data_age_seconds=604800):
    """
        Initialise the instance reading the leagues data and updating the data file if a file called elo.csv is present
        """

    new_data = {}
    country_codes = {}
    self.__relegation_zones = {}

    data_age = (int(time.time()) - os.stat(data_file).st_mtime)
    get_new_data = data_age > maximum_data_age_seconds

    if get_new_data:
      url = 'http://api.clubelo.com/' + str(date.today())
      r = requests.get(url)
      with open(elo_csv, 'wb') as output_file:
        output_file.write(r.content)
      print("\nTeam statistics aligned with real life\n")

    with open(code_file, 'r') as file:
      Lines = file.readlines()
    for line in Lines:
      code, country, relegation_zone = line.strip().split(',')
      country_codes[code.strip()] = country.strip().title()
      try:
        if relegation_zone != '-1':
          self.__relegation_zones[country.strip().title()] = int(
            relegation_zone)
      except:
        pass
    self.__datafile = SaveFile(data_file)
    self.__data = self.__datafile.read_state('__leagues')
    if not self.__data:
      self.__data = {}
    try:
      # read the new data and merge it (not in this block)
      with open(elo_csv, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
          if row:
            team = dict(row)
            if team['Club'] and team['Country'] in country_codes:
              country = country_codes[team['Country']]
              try:
                if team['Rank'] == 'None':
                  rank = -1
                else:
                  rank = int(team['Rank'])
                record = {'Rank': rank, 'Elo': float(team['Elo'])}
                if country in new_data:
                  try:
                    new_data[country][team['Level']][team['Club']] = record
                  except:
                    new_data[country][team['Level']] = {team['Club']: record}
                else:
                  new_data[country] = {}
                  new_data[country][team['Level']] = {team['Club']: record}
              except:
                print('error')
                pass
    except:
      # no updated data is available
      pass
    if get_new_data:
      os.remove(elo_csv)
    if len(new_data) > 0:
      for country in new_data:
        self.__data[country] = {}
        for level in new_data[country]:
          try:
            _ = self.__data[country][level]
          except:
            self.__data[country][level] = {}
          for team in new_data[country][level]:
            self.__data[country][level][team] = new_data[country][level][team]
      self.__datafile.write_state('__leagues', self.__data)

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
      return self.__relegation_zones[country]
    except:
      return 0

  def get_teams(self, lvl=10, elo=0):
    teams = []
    for country in self.__data:
      for level in self.__data[country]:
        for team in self.__data[country][level]:
          try:
            if int(level
                   ) <= lvl and self.__data[country][level][team]['Elo'] > elo:
              teamStat = {
                'Club': team,
                'Rank': self.__data[country][level][team]['Rank'],
                'Elo': self.__data[country][level][team]['Elo']
              }
              teams.append(teamStat)
          except:
            pass
    return teams

  def get_top_teams(self, top=1, bottom=100):
    teams = {}
    if top < 1:
      top = 1
    for country in self.__data:
      for level in self.__data[country]:
        for team in self.__data[country][level]:
          try:
            if self.__data[country][level][team]['Rank'] != -1 and self.__data[
                country][level][team]['Rank'] <= bottom and self.__data[
                  country][level][team]['Rank'] >= top:
              teamStat = {
                'Club': team,
                'Rank': self.__data[country][level][team]['Rank'],
                'Elo': self.__data[country][level][team]['Elo']
              }
              teams[self.__data[country][level][team]['Rank']] = teamStat
          except:
            pass
    return {k: v for k, v in sorted(teams.items(), key=lambda item: item[0])}
