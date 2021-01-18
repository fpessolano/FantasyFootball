import math
import random

# defineRoster creates a team roster for a league composed by numberTeams teams
import sys
import traceback


def defineRoster(numberTeams):
    teams = []
    teamNames = []
    print("Please provide the teams names:")
    numTeam = 0
    while len(teamNames) < numberTeams:
        msg = "team " + str(numTeam + 1) + " name? "
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


# updateRosterupdate the roster of the league with relegation (if necessary)
# it also cleans all statistics and reshuffle the teams
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


# calendarCorrectness verifies that the calendar contains no errors
def calendarCorrectness(cal):
    if len(cal) == 0:
        return False
    ok = True
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


# calculate the initial reference calendar for the given number of teams
# it tries to solve the problem for a limited number of tries (maximumTries) before giving up
# above 16 teams brute force repetition does not work, we need to use step backs also

# definecalendarV1 does not use step back and restart at every error
def definecalendarV1(numberTeams, maximumTries=-1):
    if maximumTries == -1:
        maximumTries = 2 ** round(math.log(numberTeams, 2))+1
    allSchedules = []
    while True:
        if maximumTries <= 0:
            break
        maximumTries -= 1
        success = False
        allSchedules = [[-1 for x in range(numberTeams - 1)] for x in range(numberTeams)]
        currentTeam = 0
        while currentTeam < numberTeams:
            remainingOpponents = [x for x in range(numberTeams) if x > currentTeam]
            random.shuffle(remainingOpponents)
            if currentTeam == 0:
                allSchedules[currentTeam] = remainingOpponents
                for week, opponent in enumerate(allSchedules[currentTeam]):
                    allSchedules[opponent][week] = currentTeam
            else:
                try:
                    lastTwoSwapped = False
                    while True:
                        unassignedWeek = allSchedules[currentTeam].index(-1)
                        availableOpponents = remainingOpponents.copy()
                        if len(availableOpponents) > 2:
                            found = False
                            while len(availableOpponents) > 0:
                                opponent = availableOpponents.pop(0)
                                busy = False
                                for team, schedule in enumerate(allSchedules):
                                    if team != currentTeam:
                                        if schedule[unassignedWeek] == opponent:
                                            busy = True
                                            break
                                if not busy:
                                    allSchedules[currentTeam][unassignedWeek] = opponent
                                    allSchedules[opponent][unassignedWeek] = currentTeam
                                    remainingOpponents.remove(opponent)
                                    found = True
                                    break
                            if not found:
                                success = True
                                break
                        elif len(availableOpponents) == 2:
                            # last two we try and swap once
                            busy = False
                            for team, schedule in enumerate(allSchedules):
                                if team != currentTeam:
                                    if schedule[unassignedWeek] == availableOpponents[0]:
                                        busy = True
                                        break
                            if busy:
                                tmp = remainingOpponents[0]
                                remainingOpponents[0] = remainingOpponents[1]
                                remainingOpponents[1] = tmp
                                if not lastTwoSwapped:
                                    lastTwoSwapped = True
                                else:
                                    success = True
                                    break
                            else:
                                opponent = availableOpponents.pop(0)
                                allSchedules[currentTeam][unassignedWeek] = opponent
                                allSchedules[opponent][unassignedWeek] = currentTeam
                                remainingOpponents.remove(opponent)
                        else:
                            # last team we just check
                            opponent = availableOpponents[0]
                            busy = False
                            for team, schedule in enumerate(allSchedules):
                                if team != currentTeam:
                                    if schedule[unassignedWeek] == opponent:
                                        busy = True
                                        break
                            if busy:
                                success = True
                            else:
                                allSchedules[currentTeam][unassignedWeek] = opponent
                                allSchedules[opponent][unassignedWeek] = currentTeam
                            break
                except:
                    pass
            if success:
                break
            currentTeam += 1
        if not success:
            break
        else:
            allSchedules = []
    return allSchedules


# definecalendarV1 uses step-back for a single team
def definecalendarV2(numberTeams, maximumTries=-1):
    if maximumTries == -1:
        maximumTries = 200 * (round(math.log(numberTeams, 2))+1)
    allSchedules = []
    while True:
        # check the number of tries
        if maximumTries < 0:
            return []
        maximumTries -= 1
        failed = False
        allSchedules = [[-1 for _ in range(numberTeams - 1)] for _ in range(numberTeams)]
        currentTeam = 0
        while currentTeam < numberTeams:
            remainingOpponents = [x for x in range(numberTeams) if x > currentTeam]
            random.shuffle(remainingOpponents)
            if currentTeam == 0:
                allSchedules[currentTeam] = remainingOpponents
                for week, opponent in enumerate(allSchedules[currentTeam]):
                    allSchedules[opponent][week] = currentTeam
            else:
                lastAssignedWeek = -1
                unassignedWeek = 0
                # cycles is used to check on the cycle permutations
                cycles = [0 for _ in range(numberTeams - 1)]

                while unassignedWeek + 1 < numberTeams:
                    # we skip assignments that are from previous rows
                    if allSchedules[currentTeam][unassignedWeek] < currentTeam and \
                            allSchedules[currentTeam][unassignedWeek] != -1:
                        unassignedWeek += 1
                        continue

                    # checks if the number of iterations has covered all possible permutations
                    if cycles[unassignedWeek] > numberTeams - 1 - unassignedWeek:
                        if lastAssignedWeek == -1:
                            # the current row is given up with its current predecessors
                            failed = True
                            break
                        else:
                            opponent = allSchedules[currentTeam][lastAssignedWeek]
                            allSchedules[opponent][lastAssignedWeek] = -1
                            remainingOpponents.insert(len(remainingOpponents), opponent)
                            cycles[unassignedWeek] = 0
                            unassignedWeek = lastAssignedWeek
                            lastAssignedWeek = -1
                            for i in range(unassignedWeek - 1, -1, -1):
                                if allSchedules[currentTeam][i] > currentTeam:
                                    lastAssignedWeek = i
                                    break
                            continue

                    cycles[unassignedWeek] += 1

                    # this failsafe is redundant
                    for c in cycles:
                        if c > numberTeams:
                            return []

                    availableOpponents = remainingOpponents.copy()

                    # this failsafe is redundant
                    if len(remainingOpponents) != len(list(set(remainingOpponents))):
                        return []

                    if len(availableOpponents) > 2:
                        opponentFound = False
                        while len(availableOpponents) > 0:
                            opponent = availableOpponents.pop(0)
                            opponentBusy = False
                            for team, schedule in enumerate(allSchedules):
                                if team != currentTeam:
                                    if schedule[unassignedWeek] == opponent:
                                        opponentBusy = True
                                        break
                            if not opponentBusy:
                                allSchedules[currentTeam][unassignedWeek] = opponent
                                allSchedules[opponent][unassignedWeek] = currentTeam
                                remainingOpponents.remove(opponent)
                                lastAssignedWeek = unassignedWeek
                                unassignedWeek += 1
                                opponentFound = True
                                break
                        if not opponentFound:
                            if lastAssignedWeek == -1:
                                # the current row is given up with its current predecessors
                                failed = True
                                break
                            else:
                                # step back and move previously assigned opponet to the tail of the queue
                                opponent = allSchedules[currentTeam][lastAssignedWeek]
                                allSchedules[opponent][lastAssignedWeek] = -1
                                remainingOpponents.insert(len(remainingOpponents), opponent)
                                cycles[unassignedWeek] = 0
                                unassignedWeek = lastAssignedWeek
                                lastAssignedWeek = -1
                                for i in range(unassignedWeek - 1, -1, -1):
                                    if allSchedules[currentTeam][i] > currentTeam:
                                        lastAssignedWeek = i
                                        break
                    elif len(availableOpponents) == 2:
                        # last two we try and swap once
                        opponentBusy = False
                        for team, schedule in enumerate(allSchedules):
                            if team != currentTeam:
                                if schedule[unassignedWeek] == availableOpponents[0]:
                                    opponentBusy = True
                                    break
                        if opponentBusy:
                            if lastAssignedWeek == -1:
                                # the current row is given up with its current predecessors
                                failed = True
                                break
                            # step back and move previously assigned opponet to the tail of the queue
                            opponent = allSchedules[currentTeam][lastAssignedWeek]
                            allSchedules[opponent][lastAssignedWeek] = -1
                            remainingOpponents.insert(len(remainingOpponents), opponent)
                            cycles[unassignedWeek] = 0
                            unassignedWeek = lastAssignedWeek
                            lastAssignedWeek = -1
                            for i in range(unassignedWeek - 1, -1, -1):
                                if allSchedules[currentTeam][i] > currentTeam:
                                    lastAssignedWeek = i
                                    break
                        else:
                            opponent = availableOpponents.pop(0)
                            allSchedules[currentTeam][unassignedWeek] = opponent
                            allSchedules[opponent][unassignedWeek] = currentTeam
                            remainingOpponents.remove(opponent)
                            lastAssignedWeek = unassignedWeek
                            unassignedWeek += 1
                    else:
                        # last team we just check
                        opponent = availableOpponents[0]
                        opponentBusy = False
                        for team, schedule in enumerate(allSchedules):
                            if team != currentTeam:
                                if schedule[unassignedWeek] == opponent:
                                    opponentBusy = True
                                    break
                        if opponentBusy:
                            if lastAssignedWeek == -1:
                                # the current row is given up with its current predecessors
                                failed = True
                                break
                            # step back and move previously assigned opponet to the tail of the queue
                            opponent = allSchedules[currentTeam][lastAssignedWeek]
                            allSchedules[opponent][lastAssignedWeek] = -1
                            remainingOpponents.insert(len(remainingOpponents), opponent)
                            cycles[unassignedWeek] += 0
                            unassignedWeek = lastAssignedWeek
                            lastAssignedWeek = -1
                            for i in range(unassignedWeek - 1, -1, -1):
                                if allSchedules[currentTeam][i] > currentTeam:
                                    lastAssignedWeek = i
                                    break
                        else:
                            allSchedules[currentTeam][unassignedWeek] = opponent
                            allSchedules[opponent][unassignedWeek] = currentTeam
                            # redundant
                            # unassignedWeek += 1
                            break
            if failed:
                break
            currentTeam += 1
        if not failed:
            break
        else:
            allSchedules = []
    return allSchedules
