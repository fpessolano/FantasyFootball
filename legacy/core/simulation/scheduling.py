import random

def calendar_valid(cal):
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


def berger_table_schedule(number):
    """
    Generate a schedule using Berger tables
    :param number: number of participating teams
    :return: schedule array and a flag indicating if a team was added (in case the original number was odd)
    """
    if number < 2:
        return [], False
    berger_table = []
    added_one = False
    if number % 2 != 0:
        number += 1
        added_one = True
    # generate Bergen table
    for i in range(0, number - 1):
        row = []
        # offset = 0
        for j in range(1, number):
            # value = (i + j) % number + int((i + j) / number)
            value = (i + j) % number + ((i + j) // number)
            row.append(value)
        berger_table.append(row)
    # unroll table
    schedule = [[0 for _ in range(number - 1)] for _ in range(number)]
    for team in range(0, number - 1):
        for opponent in range(0, number - 1):
            if team == opponent:
                schedule[team][berger_table[team][opponent] - 1] = number - 1
                schedule[number - 1][berger_table[team][opponent] - 1] = team
            else:
                schedule[team][berger_table[team][opponent] - 1] = opponent
    return schedule, added_one


def generate_calendar(schedule):
    """
    Generate a true calendar from a berger schedule
    :param schedule: number of participating teams
    :return: true calendar
    """
    calendar = []
    calendar_return = []
    for day in range(len(schedule[0])):
        match_day = []
        match_day_return = []
        for team in range(len(schedule)):
            match = [team, schedule[team][day]]
            match_reversed =  [schedule[team][day], team]
            if match not in match_day and match_reversed not in match_day:
              if bool(random.getrandbits(1)):
                match_day.append(match)
                match_day_return.append(match_reversed)
              else:
                match_day.append(match_reversed)
                match_day_return.append(match)
        calendar.append(match_day)
        calendar_return.append(match_day_return)
    return calendar + calendar_return


if __name__ == '__main__':
    print(generate_calendar(berger_table_schedule(4)[0]))
