
import json
import random
from enum import Enum
from typing import List


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


class TacticalStyle(Enum):
    BALANCED = "BALANCED"
    DEFENSIVE = "DEFENSIVE"
    ATTACKING = "ATTACKING"


class Player:
    def __init__(self, name, position, goalkeeping, defending, passing, dribbling, shooting, physical):
        self.name = name
        self.position = Position[position]
        self.goalkeeping = goalkeeping
        self.defending = defending
        self.passing = passing
        self.dribbling = dribbling
        self.shooting = shooting
        self.physical = physical


class Team:
    def __init__(self, name, players, style):
        self.name = name
        self.players = players
        self.style = style
        self.streak = 0

    def compute_strength(self):
        gk = sum(p.goalkeeping for p in self.players if p.position == Position.GK)
        defense = sum(p.defending for p in self.players)
        midfield = sum(p.passing + p.physical for p in self.players)
        attack = sum(p.shooting + p.dribbling for p in self.players)

        if self.style == TacticalStyle.ATTACKING:
            attack *= 1.1
        elif self.style == TacticalStyle.DEFENSIVE:
            defense *= 1.1

        return gk * 0.1 + defense * 0.3 + midfield * 0.3 + attack * 0.3

    def adjust_for_streak(self, enabled):
        if not enabled:
            return 1.0
        streak_bonus = min(max(self.streak, -5), 5)
        return 1 + 0.03 * streak_bonus

    def summary(self):
        print(f"\n📋 {self.name} ({self.style.name})")
        for p in self.players:
            print(f" - {p.name:20} {p.position.name:3} G:{p.goalkeeping} D:{p.defending} P:{p.passing} "
                  f"Dr:{p.dribbling} S:{p.shooting} Ph:{p.physical}")
        print(f"Total strength: {self.compute_strength():.2f}")


def load_team_from_file(filename, team_name, style):
    with open(filename, "r") as f:
        teams = json.load(f)

    for team in teams:
        if team["name"].lower() == team_name.lower():
            players = [Player(**{**p, "position": p["position"]}) for p in team["players"]]
            return Team(name=team["name"], players=players, style=style)
    raise ValueError(f"Team {team_name} not found in {filename}")


def simulate_match(team1, team2, momentum=True):
    strength1 = team1.compute_strength() * team1.adjust_for_streak(momentum)
    strength2 = team2.compute_strength() * team2.adjust_for_streak(momentum)

    lambda1 = max(0.5, strength1 / (strength1 + strength2) * 3)
    lambda2 = max(0.5, strength2 / (strength1 + strength2) * 3)

    goals1 = random.poisson(lambda1) if hasattr(random, "poisson") else int(random.gauss(lambda1, 1))
    goals2 = random.poisson(lambda2) if hasattr(random, "poisson") else int(random.gauss(lambda2, 1))

    goals1 = max(0, goals1)
    goals2 = max(0, goals2)

    if goals1 > goals2:
        team1.streak += 1
        team2.streak = min(team2.streak - 1, 0)
    elif goals2 > goals1:
        team2.streak += 1
        team1.streak = min(team1.streak - 1, 0)

    return goals1, goals2


def get_team(label):
    from_input = input(f"Load {label} team from file? [Y/n]: ").strip().lower()
    if from_input in ("n", "no"):
        print("Team creation from scratch not implemented.")
        exit(1)
    filename = input("Enter team file [teams.json]: ") or "teams.json"
    name = input(f"Enter {label} team name: ")
    style_input = input("Tactical style (e.g. BALANCED, DEFENSIVE, ATTACKING): ").strip().upper()
    try:
        style = TacticalStyle[style_input]
    except KeyError:
        print("Invalid tactical style.")
        exit(1)
    return load_team_from_file(filename, name, style)


def main():
    match_count = input("How many matches to simulate? [100]: ")
    try:
        n_matches = int(match_count) if match_count.strip() else 100
    except ValueError:
        print("Invalid number.")
        return

    momentum = input("Enable streak (momentum) effect? [Y/n]: ").strip().lower() not in ("n", "no")

    home_team = get_team("home")
    away_team = get_team("away")

    home_team.summary()
    away_team.summary()

    home_wins = draws = away_wins = 0
    total_goals = 0

    for _ in range(n_matches):
        g1, g2 = simulate_match(home_team, away_team, momentum=momentum)
        total_goals += g1 + g2
        if g1 > g2:
            home_wins += 1
        elif g2 > g1:
            away_wins += 1
        else:
            draws += 1

    print(f"\n📊 Results after {n_matches} matches:")
    print(f"{home_team.name} wins: {home_wins}")
    print(f"{away_team.name} wins: {away_wins}")
    print(f"Draws: {draws}")
    print(f"Average total goals per match: {total_goals / n_matches:.2f}")


if __name__ == "__main__":
    main()
