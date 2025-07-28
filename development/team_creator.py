
"""
team_creator.py (Improved Role Display)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This version presents all matching candidates and their actual positions
clearly during team assembly. It avoids using the same player twice and
ensures the user is selecting from players within the correct role group.
"""

import json
from team_model import Player, Team, Position

ROLE_BUCKETS = {
    "GK": [Position.GK],
    "Deep Defender": [Position.CB, Position.SW, Position.LB, Position.RB],
    "Libero-like": [Position.SW, Position.CB, Position.DM],
    "Midfielder": [Position.CM, Position.DM, Position.WB],
    "Attacking Midfielder": [Position.AM, Position.LM, Position.RM],
    "Attacker": [Position.ST, Position.LW, Position.RW],
}

def load_players(filename: str) -> list[Player]:
    with open(filename, "r") as f:
        raw_players = json.load(f)
    return [Player(
        name=p["name"],
        position=Position[p["position"]],
        goalkeeping=p["goalkeeping"],
        defending=p["defending"],
        passing=p["passing"],
        dribbling=p["dribbling"],
        shooting=p["shooting"],
        physical=p["physical"]
    ) for p in raw_players]

def main():
    player_file = input("Enter player file [players.json]: ") or "players.json"
    try:
        players = load_players(player_file)
    except Exception as e:
        print(f"Failed to load players: {e}")
        return

    print(f"Loaded {len(players)} players.")
    team_name = input("Enter team name: ")

    selected_players = []
    used_indices = set()

    while len(selected_players) < 11:
        print(f"\nSelected {len(selected_players)} players. Pick role type for next player:")
        for i, role in enumerate(ROLE_BUCKETS.keys(), 1):
            print(f"[{i}] {role}")
        try:
            role_choice = int(input("Select role: "))
            role = list(ROLE_BUCKETS.keys())[role_choice - 1]
        except Exception:
            print("Invalid role. Try again.")
            continue

        allowed_positions = ROLE_BUCKETS[role]
        candidates = [p for i, p in enumerate(players)
                      if p.position in allowed_positions and i not in used_indices]
        if not candidates:
            print(f"No available players for role {role}")
            continue

        print(f"\nAvailable {role} candidates (showing actual positions):")
        for i, p in enumerate(candidates):
            print(f"[{i + 1}] {p.name} — {p.position.name} | G:{p.goalkeeping} D:{p.defending} P:{p.passing} "
                  f"Dr:{p.dribbling} S:{p.shooting} Ph:{p.physical}")
        try:
            index = int(input("Choose player number: "))
            if 1 <= index <= len(candidates):
                chosen = candidates[index - 1]
                selected_players.append(chosen)
                used_indices.add(players.index(chosen))
            else:
                print("Invalid number.")
        except Exception:
            print("Invalid input.")

    gks = [p for p in selected_players if p.position == Position.GK]
    if len(gks) != 1:
        print("\n⚠️ Invalid team: you must have exactly 1 goalkeeper.")
        return

    team = Team(name=team_name, formation="Custom", players=selected_players)
    ratings = team.compute_team_ratings()
    print(f"\nTeam Ratings for {team_name}:")
    for key, val in ratings.items():
        print(f"  {key}: {val:.2f}")

    save = input("Save this team to file? [Y/n]: ").strip().lower()
    if save in ("n", "no"):
        return

    out_file = input("Save to which file? [teams.json]: ") or "teams.json"
    try:
        with open(out_file, "r") as f:
            all_teams = json.load(f)
    except Exception:
        all_teams = []

    all_teams.append({
        "name": team.name,
        "formation": team.formation,
        "players": [
            {
                "name": p.name,
                "position": p.position.name,
                "goalkeeping": p.goalkeeping,
                "defending": p.defending,
                "passing": p.passing,
                "dribbling": p.dribbling,
                "shooting": p.shooting,
                "physical": p.physical,
            }
            for p in team.players
        ]
    })

    with open(out_file, "w") as f:
        json.dump(all_teams, f, indent=2)
    print(f"✅ Team '{team.name}' saved to {out_file}")

if __name__ == "__main__":
    main()
