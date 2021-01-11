import random

# finalScore determines the final match result
# currently it is purely random based
def finalScore():
    maxShots = random.randint(0, 10)
    homeAttacks = random.randint(0, maxShots)
    awayAttacks = random.randint(0, maxShots)
    homeGoals = 0
    awayGoals = 0
    for _ in range(homeAttacks):
        if random.randint(0, 10) > random.randint(0, 10):
            homeGoals += 1
    for _ in range(awayAttacks):
        if random.randint(0, 10) > random.randint(0, 10):
            awayGoals += 1
    return homeGoals, awayGoals

# matchResult takes care of updating all stats based on the match result
def matchResult(home, away):
    # homeGoals = random.randint(0, 5)
    # awayGoals = random.randint(0, 5)
    homeGoals, awayGoals = finalScore()
    home["GF"] += homeGoals
    home["GA"] += awayGoals
    home["GD"] += (homeGoals - awayGoals)
    away["GF"] += awayGoals
    away["GA"] += homeGoals
    away["GD"] += (awayGoals - homeGoals)
    home["MP"] += 1
    away["MP"] += 1
    if homeGoals > awayGoals:
        home["W"] += 1
        away["L"] += 1
        home["PT"] += 3
    elif homeGoals == awayGoals:
        away["D"] += 1
        home["D"] += 1
        away["PT"] += 1
        home["PT"] += 1
    else:
        away["W"] += 1
        home["L"] += 1
        away["PT"] += 3
        # away team wins
    return [homeGoals, awayGoals, home, away]

# matchDay sets the correct match or rest day for every team for a given season week
def matchDay(week, calendar, teams, spare):
    if calendar == None or teams == None:
        print(1)
        return False
    if len(calendar) == 1:
        print(2)
        return False
    if (not spare and len(calendar) != len(teams)) or (spare and len(calendar) != (len(teams) + 1)):
        print(3)
        return False
    halfSeason = len(calendar[0])
    if week > 2 * halfSeason:
        return False
    rested = -1
    if spare:
        rested = len(calendar) - 1
    print("Week " + str(week) + " match results:")
    playingTeams = []
    for team in range(len(calendar)):
        if team not in playingTeams:
            if week <= halfSeason:
                if team == rested:
                    print("\t" + teams[calendar[team][week - 1]]["NAME"] + " rests ")
                elif calendar[team][week - 1] == rested:
                    print("\t" + teams[team]["NAME"] + " rests ")
                else:
                    homeTeam = team
                    awayTeam = calendar[team][week - 1]
                    print("\t" + teams[homeTeam]["NAME"] + " vs " + teams[awayTeam]["NAME"], end=" ")
                    result = matchResult(teams[homeTeam], teams[awayTeam])
                    print(result[0], "-", result[1])
                    teams[homeTeam] = result[2]
                    teams[awayTeam] = result[3]
                playingTeams.append(calendar[team][week - 1])
            else:
                if team == rested:
                    print("\t" + teams[calendar[team][week - halfSeason - 1]]["NAME"] + " rests ")
                elif calendar[team][week - halfSeason - 1] == rested:
                    print("\t" + teams[team]["NAME"] + " rests ")
                else:
                    homeTeam = calendar[team][week - halfSeason - 1]
                    awayTeam = team
                    print("\t" + teams[homeTeam]["NAME"] + " vs " + teams[awayTeam]["NAME"], end=" ")
                    result = matchResult(teams[homeTeam], teams[awayTeam])
                    print(result[0], "-", result[1])
                    teams[homeTeam] = result[2]
                    teams[awayTeam] = result[3]
                playingTeams.append(calendar[team][week - halfSeason - 1])
            playingTeams.append(team)
    print()
    return True
