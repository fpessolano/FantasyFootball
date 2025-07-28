
import json
import random
from enum import Enum
from typing import List, Dict


# ---------- Models ----------

class Position(Enum):
    GK = "GK"
    CB = "CB"
    SW = "SW"
    LB = "LB"
    RB = "RB"
    CM = "CM"
    DM = "DM"
    WB = "WB"
    LWB = "LWB"
    RWB = "RWB"
    AM = "AM"
    LM = "LM"
    RM = "RM"
    ST = "ST"
    LW = "LW"
    RW = "RW"


class Player:
    def __init__(self, name: str, position: Position,
                 goalkeeping: int, defending: int, passing: int,
                 dribbling: int, shooting: int, physical: int):
        self.name = name
        self.position = position
        self.goalkeeping = goalkeeping
        self.defending = defending
        self.passing = passing
        self.dribbling = dribbling
        self.shooting = shooting
        self.physical = physical

    def to_dict(self):
        return {
            "name": self.name,
            "position": self.position.name,
            "goalkeeping": self.goalkeeping,
            "defending": self.defending,
            "passing": self.passing,
            "dribbling": self.dribbling,
            "shooting": self.shooting,
            "physical": self.physical
        }


class Team:
    def __init__(self, name: str, players: List[Player]):
        self.name = name
        self.players = players

    def compute_team_ratings(self) -> Dict[str, float]:
        total = {
            "keeping": 0,
            "defence": 0,
            "midfield": 0,
            "attack": 0,
            "left_flow": 0,
            "right_flow": 0,
            "center_flow": 0,
        }
        for p in self.players:
            total["keeping"] += p.goalkeeping if p.position == Position.GK else 0
            total["defence"] += p.defending
            total["midfield"] += p.passing + p.physical
            total["attack"] += p.shooting + p.dribbling
            if p.position in (Position.LB, Position.LM, Position.LW, Position.LWB):
                total["left_flow"] += p.passing
            if p.position in (Position.RB, Position.RM, Position.RW, Position.RWB):
                total["right_flow"] += p.passing
            if p.position in (Position.CM, Position.AM, Position.DM, Position.ST, Position.SW):
                total["center_flow"] += p.passing
        count = len(self.players) or 1
        return {k: v / count for k, v in total.items()}


# ---------- Logic ----------

def main():
    player_file = input("Enter player file [players.json]: ") or "players.json"
    try:
        with open(player_file, "r") as f:
            raw_players = json.load(f)
        players = [Player(
            name=p["name"],
            position=Position[p["position"]],
            goalkeeping=p["goalkeeping"],
            defending=p["defending"],
            passing=p["passing"],
            dribbling=p["dribbling"],
            shooting=p["shooting"],
            physical=p["physical"]
        ) for p in raw_players]
    except Exception as e:
        print(f"Failed to load players: {e}")
        return

    print(f"Loaded {len(players)} players.")
    team_name = input("Enter team name: ")

    selected_players = []
    used_indices = set()

    while len(selected_players) < 11:
        print(f"\nSelected {len(selected_players)} players.")
        print("Available positions: ", ', '.join(p.name for p in Position))
        pos_input = input("Enter exact position (e.g., GK, CB, CM): ").strip().upper()
        if pos_input not in Position.__members__:
            print("Invalid position. Try again.")
            continue
        pos = Position[pos_input]

        candidates = [p for i, p in enumerate(players)
                      if p.position == pos and i not in used_indices]

        if not candidates:
            print(f"No available players for position {pos.name}")
            continue

        chosen = random.choice(candidates)
        selected_players.append(chosen)
        used_indices.add(players.index(chosen))
        print(f"✔️ Added {chosen.name} ({chosen.position.name})")

    gks = [p for p in selected_players if p.position == Position.GK]
    if len(gks) != 1:
        print("\n⚠️ Invalid team: you must have exactly 1 goalkeeper.")
        return

    team = Team(name=team_name, players=selected_players)
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
        "formation": "Custom",
        "players": [p.to_dict() for p in team.players]
    })

    with open(out_file, "w") as f:
        json.dump(all_teams, f, indent=2)
    print(f"✅ Team '{team.name}' saved to {out_file}")


if __name__ == "__main__":
    main()
