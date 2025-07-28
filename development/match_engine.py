"""
Match Engine
~~~~~~~~~~~~

Module for simulating matches between teams.
"""

import random
from typing import Tuple, List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
from models import Team, Position, TacticalStyle


@dataclass
class MatchEvent:
    """Represents an event during a match."""
    minute: int
    event_type: str  # "goal", "yellow_card", "red_card", "substitution"
    team: str
    player: str
    description: str


@dataclass
class MatchResult:
    """Complete match result with statistics."""
    home_team: str
    away_team: str
    home_score: int
    away_score: int
    events: List[MatchEvent]
    stats: Dict[str, Dict[str, float]]  # Team -> stat type -> value
    date: datetime


class MatchEngine:
    """Engine for simulating football matches."""
    
    def __init__(self, use_momentum: bool = True, detailed_sim: bool = True):
        self.use_momentum = use_momentum
        self.detailed_sim = detailed_sim
    
    def simulate_match(self, home_team: Team, away_team: Team) -> MatchResult:
        """
        Simulate a match between two teams.
        
        Args:
            home_team: Home team
            away_team: Away team
        
        Returns:
            MatchResult with score and statistics
        """
        # Calculate expected goals
        home_xg = self._calculate_expected_goals(home_team, away_team, is_home=True)
        away_xg = self._calculate_expected_goals(away_team, home_team, is_home=False)
        
        # Apply momentum if enabled
        if self.use_momentum:
            home_xg *= home_team.adjust_for_streak()
            away_xg *= away_team.adjust_for_streak()
        
        # Generate actual goals
        home_goals = self._generate_goals(home_xg)
        away_goals = self._generate_goals(away_xg)
        
        # Generate match events if detailed simulation is enabled
        events = []
        if self.detailed_sim:
            events = self._generate_match_events(
                home_team, away_team, home_goals, away_goals
            )
        
        # Calculate match statistics
        stats = self._calculate_match_stats(home_team, away_team, home_xg, away_xg)
        
        return MatchResult(
            home_team=home_team.name,
            away_team=away_team.name,
            home_score=home_goals,
            away_score=away_goals,
            events=events,
            stats=stats,
            date=datetime.now()
        )
    
    def _calculate_expected_goals(self, team: Team, opponent: Team, is_home: bool) -> float:
        """Calculate expected goals for a team."""
        # Get team ratings
        team_ratings = team.compute_team_ratings()
        opp_ratings = opponent.compute_team_ratings()
        
        # Apply tactical style multipliers
        att_mult, def_mult, mid_mult = team.style.multipliers()
        opp_att_mult, opp_def_mult, opp_mid_mult = opponent.style.multipliers()
        
        # Calculate zone contributions
        zones = [
            ("left_flow", team_ratings["left_flow"] * mid_mult, 
             opp_ratings["left_flow"] * opp_mid_mult),
            ("center_flow", team_ratings["center_flow"] * mid_mult, 
             opp_ratings["center_flow"] * opp_mid_mult),
            ("right_flow", team_ratings["right_flow"] * mid_mult, 
             opp_ratings["right_flow"] * opp_mid_mult)
        ]
        
        expected_goals = 0.0
        base_factor = 1.2 if is_home else 1.0  # Home advantage
        
        for zone_name, our_flow, their_flow in zones:
            # Midfield control in this zone
            total_flow = our_flow + their_flow
            if total_flow > 0:
                mid_control = our_flow / total_flow
            else:
                mid_control = 0.5
            
            # Attack vs defence
            our_attack = team_ratings["attack"] * att_mult
            their_defence = opp_ratings["defence"] * opp_def_mult
            
            if (our_attack + their_defence) > 0:
                attack_success = our_attack / (our_attack + their_defence)
            else:
                attack_success = 0.5
            
            # Zone contribution to expected goals
            expected_goals += base_factor * mid_control * attack_success
        
        return expected_goals
    
    def _generate_goals(self, expected_goals: float) -> int:
        """Generate actual goals from expected goals using Poisson distribution."""
        if expected_goals <= 0:
            return 0
        
        # Proper Poisson distribution implementation
        import math
        
        # Knuth's algorithm for Poisson distribution
        L = math.exp(-expected_goals)
        k = 0
        p = 1.0
        
        while p > L:
            k += 1
            p *= random.random()
        
        return k - 1
    
    def _generate_match_events(self, home_team: Team, away_team: Team, 
                             home_goals: int, away_goals: int) -> List[MatchEvent]:
        """Generate detailed match events."""
        events = []
        
        # Generate goal events
        for i in range(home_goals):
            minute = random.randint(1, 90)
            # Pick a likely scorer (attackers and midfielders more likely)
            scorers = [p for p in home_team.players 
                      if p.position in [Position.ST, Position.LW, Position.RW, 
                                      Position.AM, Position.CM, Position.LM, Position.RM]]
            if not scorers:
                scorers = home_team.players
            
            scorer = random.choice(scorers)
            events.append(MatchEvent(
                minute=minute,
                event_type="goal",
                team=home_team.name,
                player=scorer.name,
                description=f"{scorer.name} scores for {home_team.name}!"
            ))
        
        for i in range(away_goals):
            minute = random.randint(1, 90)
            scorers = [p for p in away_team.players 
                      if p.position in [Position.ST, Position.LW, Position.RW, 
                                      Position.AM, Position.CM, Position.LM, Position.RM]]
            if not scorers:
                scorers = away_team.players
            
            scorer = random.choice(scorers)
            events.append(MatchEvent(
                minute=minute,
                event_type="goal",
                team=away_team.name,
                player=scorer.name,
                description=f"{scorer.name} scores for {away_team.name}!"
            ))
        
        # Sort events by minute
        events.sort(key=lambda e: e.minute)
        
        return events
    
    def _calculate_match_stats(self, home_team: Team, away_team: Team,
                             home_xg: float, away_xg: float) -> Dict[str, Dict[str, float]]:
        """Calculate match statistics."""
        home_ratings = home_team.compute_team_ratings()
        away_ratings = away_team.compute_team_ratings()
        
        # Calculate possession based on midfield strength
        total_mid = home_ratings["midfield"] + away_ratings["midfield"]
        home_possession = (home_ratings["midfield"] / total_mid * 100) if total_mid > 0 else 50
        
        # Calculate shots based on attack ratings
        home_shots = 8 + (home_ratings["attack"] - away_ratings["defence"]) / 10
        away_shots = 8 + (away_ratings["attack"] - home_ratings["defence"]) / 10
        
        # Ensure positive values
        home_shots = max(3, home_shots)
        away_shots = max(3, away_shots)
        
        return {
            home_team.name: {
                "possession": home_possession,
                "expected_goals": home_xg,
                "shots": home_shots,
                "shots_on_target": home_shots * 0.35,
                "pass_accuracy": 70 + (home_ratings["midfield"] / 40)
            },
            away_team.name: {
                "possession": 100 - home_possession,
                "expected_goals": away_xg,
                "shots": away_shots,
                "shots_on_target": away_shots * 0.35,
                "pass_accuracy": 70 + (away_ratings["midfield"] / 40)
            }
        }
    
    def simulate_tournament(self, teams: List[Team], rounds: int = 1) -> List[MatchResult]:
        """
        Simulate a round-robin tournament.
        
        Args:
            teams: List of teams to participate
            rounds: Number of times each team plays each other
        
        Returns:
            List of all match results
        """
        results = []
        
        for round_num in range(rounds):
            # Generate all pairings
            for i in range(len(teams)):
                for j in range(i + 1, len(teams)):
                    # Alternate home/away based on round
                    if round_num % 2 == 0:
                        home, away = teams[i], teams[j]
                    else:
                        home, away = teams[j], teams[i]
                    
                    result = self.simulate_match(home, away)
                    results.append(result)
                    
                    # Update streaks
                    if result.home_score > result.away_score:
                        home.streak_count = max(1, home.streak_count + 1)
                        away.streak_count = min(-1, away.streak_count - 1)
                    elif result.away_score > result.home_score:
                        home.streak_count = min(-1, home.streak_count - 1)
                        away.streak_count = max(1, away.streak_count + 1)
                    else:
                        home.streak_count = 0
                        away.streak_count = 0
        
        return results
    
    def display_match_result(self, result: MatchResult) -> None:
        """Display a match result in a formatted way."""
        print("\n" + "="*60)
        print(f"MATCH RESULT: {result.home_team} vs {result.away_team}")
        print(f"Date: {result.date.strftime('%Y-%m-%d %H:%M')}")
        print("="*60)
        
        # Score
        print(f"\nFINAL SCORE: {result.home_team} {result.home_score} - "
              f"{result.away_score} {result.away_team}")
        
        # Events
        if result.events:
            print("\nMATCH EVENTS:")
            for event in result.events:
                print(f"{event.minute}' - {event.description}")
        
        # Statistics
        print("\nMATCH STATISTICS:")
        print(f"{'Stat':<20} {result.home_team:<15} {result.away_team:<15}")
        print("-" * 50)
        
        home_stats = result.stats[result.home_team]
        away_stats = result.stats[result.away_team]
        
        print(f"{'Possession':<20} {home_stats['possession']:<15.1f}% "
              f"{away_stats['possession']:<15.1f}%")
        print(f"{'Expected Goals':<20} {home_stats['expected_goals']:<15.2f} "
              f"{away_stats['expected_goals']:<15.2f}")
        print(f"{'Shots':<20} {home_stats['shots']:<15.0f} "
              f"{away_stats['shots']:<15.0f}")
        print(f"{'Shots on Target':<20} {home_stats['shots_on_target']:<15.0f} "
              f"{away_stats['shots_on_target']:<15.0f}")
        print(f"{'Pass Accuracy':<20} {home_stats['pass_accuracy']:<15.1f}% "
              f"{away_stats['pass_accuracy']:<15.1f}%")
        
        print("="*60)