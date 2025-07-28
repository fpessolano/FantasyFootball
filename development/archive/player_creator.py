
import json
import random
from enum import Enum


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
    def __init__(self, name, position, goalkeeping, defending, passing, dribbling, shooting, physical):
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


def generate_random_player(position: Position) -> Player:
    def stat():
        return random.randint(30, 100)

    return Player(
        name=f"{position.name}_{random.randint(1000, 9999)}",
        position=position,
        goalkeeping=stat() if position == Position.GK else 0,
        defending=stat(),
        passing=stat(),
        dribbling=stat(),
        shooting=stat(),
        physical=stat()
    )


def main():
    filename = input("Enter file to save players [players.json]: ") or "players.json"

    try:
        with open(filename, "r") as f:
            existing = json.load(f)
    except FileNotFoundError:
        existing = []

    try:
        count = int(input("How many players to generate (min 2 per position)? "))
        if count < len(Position) * 2:
            raise ValueError("Too few players for full coverage.")
    except Exception as e:
        print(f"Invalid input: {e}")
        return

    positions = list(Position)
    players = []

    # Step 1: ensure 2 per position
    for pos in positions:
        players.append(generate_random_player(pos))
        players.append(generate_random_player(pos))

    # Step 2: fill remainder randomly
    while len(players) < count:
        pos = random.choice(positions)
        players.append(generate_random_player(pos))

    all_players = existing + [p.to_dict() for p in players]

    with open(filename, "w") as f:
        json.dump(all_players, f, indent=2)

    print(f"✅ Generated {len(players)} new players (total in file: {len(all_players)})")


if __name__ == "__main__":
    main()
