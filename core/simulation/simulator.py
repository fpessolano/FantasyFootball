"""
Match Simulation Engine

This module provides enhanced football match simulation using ELO-based probability calculations
for realistic match outcomes. The simulation considers:

1. Team ELO ratings with home advantage
2. Team form and injury modifiers  
3. Realistic score distributions based on match outcome
4. Proper draw probability calculations

Match Flow:
1. Calculate team winning probabilities using ELO ratings
2. Determine match outcome (home win/draw/away win) using weighted probabilities
3. Generate realistic score based on outcome and team strengths
4. Update team ELO ratings based on result and goal difference

Match Modifiers (for future use):
- 60 for World Cup finals
- 50 for continental championship finals and major intercontinental tournaments  
- 40 for World Cup and continental qualifiers and major tournaments
- 30 for all other tournaments
- 20 for friendly matches
"""

import random
from core.entities.team import Team


class MatchType:
    """
    Constants for match types
    Currently not used
    """

    def __init__(self):
        pass

    @classmethod
    def world_cup_final(cls):
        return 60

    @classmethod
    def finals(cls):
        return 50

    @classmethod
    def major_tournaments(cls):
        return 40

    @classmethod
    def minor_division(cls):
        return 30

    @classmethod
    def friendly(cls):
        return 20


def match_result(home_win_probability, away_win_probability):
    """
    Enhanced match result calculation using ELO-based probabilities
    """
    # Calculate draw probability based on team strength similarity
    strength_diff = abs(home_win_probability - away_win_probability)
    draw_probability = 0.25 * (1 - strength_diff)
    
    # Normalize probabilities
    total = home_win_probability + away_win_probability + draw_probability
    home_win_prob = home_win_probability / total
    away_win_prob = away_win_probability / total
    draw_prob = draw_probability / total
    
    # Determine match outcome first
    outcome_roll = random.random()
    if outcome_roll < home_win_prob:
        # Home win - more realistic scoring
        base_home_goals = random.choice([1, 1, 2, 2, 2, 3, 3, 4])  # Favor 1-2 goals
        base_away_goals = max(0, base_home_goals - random.choice([1, 1, 1, 2, 2, 3]))  # Usually 1-2 goal difference
    elif outcome_roll < home_win_prob + draw_prob:
        # Draw - more 0-0, 1-1 draws
        draw_score = random.choice([0, 0, 1, 1, 1, 2, 2, 3])  # Favor low-scoring draws
        base_home_goals = base_away_goals = draw_score
    else:
        # Away win - more realistic scoring
        base_away_goals = random.choice([1, 1, 2, 2, 2, 3, 3, 4])  # Favor 1-2 goals
        base_home_goals = max(0, base_away_goals - random.choice([1, 1, 1, 2, 2, 3]))  # Usually 1-2 goal difference
    
    # Add some variance based on team strengths
    home_goals = base_home_goals
    away_goals = base_away_goals
    
    # Reduced chance for extra goals (more realistic)
    if random.random() < home_win_probability * 0.15:  # Reduced from 0.3 to 0.15
        home_goals += 1
    if random.random() < away_win_probability * 0.15:  # Reduced from 0.3 to 0.15
        away_goals += 1
    
    # Ensure realistic scores (cap at 5 goals)
    home_goals = min(home_goals, 5)  # Reduced from 7 to 5
    away_goals = min(away_goals, 5)  # Reduced from 7 to 5
    
    return home_goals, away_goals


def play_match(home_team: Team, away_team: Team, match_modifier=40, home_offset=50):
    """
    Main match simulation function that orchestrates the complete match process.
    
    This function:
    1. Calculates win probabilities for both teams using ELO ratings
    2. Simulates the match result using enhanced probability-based algorithm
    3. Updates both teams' ELO ratings based on the result
    4. Records match statistics for both teams
    
    Args:
        home_team (Team): The home team object
        away_team (Team): The away team object  
        match_modifier (int): ELO adjustment factor (default 40 for league matches)
        home_offset (int): Home advantage bonus to ELO (default 50)
        
    Returns:
        tuple: (home_goals, away_goals) - The final match score
        
    The ELO rating system ensures that:
    - Strong teams beating weak teams gain few points
    - Weak teams beating strong teams gain many points
    - Large victories provide additional ELO bonuses
    - Team form and injury factors influence probabilities
    """
    home_winning_probability = Team.winning_probability(home_team, away_team, home_offset)
    away_wining_probability = Team.winning_probability(away_team, home_team, 0)
    home_goals, away_goals = match_result(home_winning_probability, away_wining_probability)
    home_team.new_rating(match_modifier, home_goals - away_goals, home_winning_probability)
    away_team.new_rating(match_modifier, away_goals - home_goals, away_wining_probability)
    home_team.add_match(home_goals, away_goals)
    away_team.add_match(away_goals, home_goals)
    return home_goals, away_goals
