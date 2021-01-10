def orderStanding(teams):
    teamsWeigth = {i: teams[i]["PT"] + teams[i]["GD"] / 100 + teams[i]["GF"] / 1000 + teams[i]["GA"] / 1000000 for i in
                   range(len(teams))}
    teamsWeigth = sorted(teamsWeigth.items(), key=lambda x: x[1], reverse=True)
    orderedTeams = []
    for i in teamsWeigth:
        orderedTeams.append(teams[i[0]])
    return orderedTeams

# TODO
def load():
    return


# TODO
def save():
    return
