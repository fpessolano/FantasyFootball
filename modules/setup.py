import random


def defineRoster(numberTeams):
    teams = []
    teamNames = []
    print("Please provide the teams names:")
    numTeam = 0
    while len(teamNames) < numberTeams:
        msg = "team " + str(numTeam) + " name? "
        name = input(msg)
        if name == "":
            print("!!! Error: empty names are not allowed !!!")
            continue
        numTeam += 1
        teamNames.append(name)
        if len(teamNames) == len(set(teamNames)) or len(teamNames) == 1:
            teams.append({
                "NAME": name.strip(),
                "MP": 0,
                "W": 0,
                "D": 0,
                "L": 0,
                "GF": 0,
                "GA": 0,
                "GD": 0,
                "PT": 0,
            })
        else:
            print("Team already present")
            teamNames = list(set(teamNames))
    random.shuffle(teams)
    return teams


def updateRoster(teams, relegationZone):
    roster = []
    if relegationZone > 0:
        currentTeams = [x["NAME"] for x in teams]
        print("The following teams have relegated:")
        for i in range(relegationZone):
            print("\tPlace", len(teams) - i, ":", teams[len(teams) - 1 - i]["NAME"])
        if input("Do you want to replace them (yes or anything else for no)? ").lower() == "y":
            print("Name the team that have been promoted:")
            for i in range(relegationZone):
                accepted = False
                while not accepted:
                    msg = "\tNew team " + str(i + 1) + " name? "
                    newName = input(msg)
                    if newName not in currentTeams:
                        teams[len(teams) - 1 - i]["NAME"] = newName
                        accepted = True
                    else:
                        print("Team already present or being relegated")
    for team in teams:
        roster.append({
            "NAME": team["NAME"],
            "MP": 0,
            "W": 0,
            "D": 0,
            "L": 0,
            "GF": 0,
            "GA": 0,
            "GD": 0,
            "PT": 0,
        })
    random.shuffle(roster)
    return roster


def calendarCorrectness(cal):
    if len(cal) == 0:
        return False
    ok = True
    cal = definecalendar(16, 100000)
    for team in cal:
        if len(team) != len(set(team)):
            ok = False
            break
    ts = [[cal[j][i] for j in range(len(cal))] for i in range(len(cal[0]))]
    for team in cal:
        if len(team) != len(set(team)):
            ok = False
            break
    return ok

# above 16 teams brute force repetition does not work, we need to use step backs also
def definecalendar(numberTeams, maximumTries):
    allSchedules = []
    while True:
        if maximumTries <= 0:
            break
        maximumTries -= 1
        success = True
        allSchedules = [[-1 for x in range(numberTeams - 1)] for x in range(numberTeams)]
        currentTeam = 0
        while currentTeam < numberTeams:
            remainingOpponents = [x for x in range(numberTeams) if x > currentTeam]
            random.shuffle(remainingOpponents)
            if currentTeam == 0:
                allSchedules[currentTeam] = remainingOpponents
                for day, opponent in enumerate(allSchedules[currentTeam]):
                    allSchedules[opponent][day] = currentTeam
            else:
                try:
                    lastTwoSwapped = False
                    while True:
                        unassignedDay = allSchedules[currentTeam].index(-1)
                        availableOpponents = remainingOpponents.copy()
                        if len(availableOpponents) > 2:
                            found = False
                            while len(availableOpponents) > 0:
                                opponent = availableOpponents.pop(0)
                                # print(opponent, availableOpponents)
                                busy = False
                                for team, schedule in enumerate(allSchedules):
                                    if team != currentTeam:
                                        if schedule[unassignedDay] == opponent:
                                            busy = True
                                            break
                                if not busy:
                                    allSchedules[currentTeam][unassignedDay] = opponent
                                    allSchedules[opponent][unassignedDay] = currentTeam
                                    remainingOpponents.remove(opponent)
                                    found = True
                                    break
                            if not found:
                                success = False
                                break
                        elif len(availableOpponents) == 2:
                            # last two we try and swap once
                            busy = False
                            for team, schedule in enumerate(allSchedules):
                                if team != currentTeam:
                                    if schedule[unassignedDay] == availableOpponents[0]:
                                        busy = True
                                        break
                            if busy:
                                tmp = remainingOpponents[0]
                                remainingOpponents[0] = remainingOpponents[1]
                                remainingOpponents[1] = tmp
                                if not lastTwoSwapped:
                                    lastTwoSwapped = True
                                else:
                                    success = False
                                    break
                            else:
                                opponent = availableOpponents.pop(0)
                                allSchedules[currentTeam][unassignedDay] = opponent
                                allSchedules[opponent][unassignedDay] = currentTeam
                                remainingOpponents.remove(opponent)
                        else:
                            # last team we just check
                            opponent = availableOpponents[0]
                            busy = False
                            for team, schedule in enumerate(allSchedules):
                                if team != currentTeam:
                                    if schedule[unassignedDay] == opponent:
                                        busy = True
                                        break
                            if busy:
                                success = False
                            else:
                                allSchedules[currentTeam][unassignedDay] = opponent
                                allSchedules[opponent][unassignedDay] = currentTeam
                            break
                except:
                    pass
            if not success:
                break
            currentTeam += 1
        if success:
            break
        else:
            allSchedules = []
    return allSchedules
