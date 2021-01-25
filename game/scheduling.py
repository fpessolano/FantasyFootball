def calendarValid(cal):
    """
    calendarCorrectness verifies that the calendar contains no errors
    :param cal: schedule
    :return: true if schedule is valid
    """
    if len(cal) == 0:
        return False
    ok = True
    for team in cal:
        if len(team) != len(set(team)):
            ok = False
            break
    ts = [[cal[j][i] for j in range(len(cal))] for i in range(len(cal[0]))]
    for team in ts:
        if len(team) != len(set(team)):
            ok = False
            break
    return ok


def bergerTableSchedule(number):
    """
    Generate a schedule using Berger tables
    :param number: number of partecipating teams
    :return: schedule array and a flag indicating if a team was added (in case the original number was odd)
    """
    if number < 2:
        return [], False
    bergerTable = []
    addedOne = False
    if number % 2 != 0:
        number += 1
        addedOne = True
    # generate Bergen table
    for i in range(0, number - 1):
        row = []
        offset = 0
        for j in range(1, number):
            # value = (i + j) % number + int((i + j) / number)
            value = (i + j) % number + ((i + j) // number)
            row.append(value)
        bergerTable.append(row)
    # unroll table
    schedule = [[0 for _ in range(number - 1)] for _ in range(number)]
    for team in range(0, number - 1):
        for opponent in range(0, number - 1):
            if team == opponent:
                schedule[team][bergerTable[team][opponent] - 1] = number - 1
                schedule[number - 1][bergerTable[team][opponent] - 1] = team
            else:
                schedule[team][bergerTable[team][opponent] - 1] = opponent
    return schedule, addedOne


if __name__ == '__main__':
    print(bergerTableSchedule(15))
