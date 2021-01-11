import tabulate
import pickle

# orderStanding prints the standings considering points, goald difference, goals made and goals conceived
def orderStanding(teams):
    print()
    teamsWeigth = {i: teams[i]["PT"] + teams[i]["GD"] / 100 + teams[i]["GF"] / 1000 - teams[i]["GA"] / 1000000 for i in
                   range(len(teams))}
    teamsWeigth = sorted(teamsWeigth.items(), key=lambda x: x[1], reverse=True)
    orderedTeams = []
    for i in teamsWeigth:
        orderedTeams.append(teams[i[0]])
    header = orderedTeams[0].keys()
    rows = [x.values() for x in orderedTeams]
    print(tabulate.tabulate(rows, header))
    print()
    return orderedTeams

# loadGame loads a saved game
def loadGame(filename):
    try:
        infile = open(filename, 'rb')
        savedState = pickle.load(infile)
        infile.close()
        return savedState["week"], savedState["teams"],savedState["calendar"],savedState["relegationZone"],savedState["spare"]
    except:
        return None, None, None, None

# saveGame saves a game
def saveGame(week, teams, calendar, relegationZone, spare):
    filename = input("Please give me the save name (enter for default)? ")
    if filename == "":
        filename = "default.save"
    saveData = {
        "week": week,
        "teams" : teams,
        "calendar" : calendar,
        "relegationZone": relegationZone,
        "spare": spare
    }
    outfile = open(filename, 'wb')
    pickle.dump(saveData, outfile)
    outfile.close()
    return
