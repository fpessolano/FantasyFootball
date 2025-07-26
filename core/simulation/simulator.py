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
from core.simulation.goals_calibration import get_calibration


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


def match_result(home_win_probability, away_win_probability, league_name=None, league_instance=None):
    """
    Enhanced match result calculation using ELO-based probabilities
    with league-specific goal calibration.
    """
    # Get calibration data if league is specified
    calibration = get_calibration() if league_name else None
    target_avg = calibration.get_league_average(league_name) if calibration and league_name else 2.75
    
    # Apply rolling average calibration if league instance is available
    rolling_avg_adjustment = 1.0
    if league_instance and calibration and league_name:
        current_avg = league_instance.get_season_average_goals()
        match_count = league_instance.get_season_match_count()
        
        # Only apply adjustment after a few matches to get meaningful average
        if match_count >= 5:
            if current_avg > target_avg:
                # Current average is too high, reduce goals slightly
                rolling_avg_adjustment = max(0.7, target_avg / current_avg)
            elif current_avg < target_avg * 0.9:
                # Current average is significantly low, increase goals slightly
                rolling_avg_adjustment = min(1.3, (target_avg * 0.95) / current_avg)
    
    # Calculate draw probability based on team strength similarity - Increased draws for lower scoring
    strength_diff = abs(home_win_probability - away_win_probability)
    if league_name and calibration:
        if target_avg < 2.6:
            draw_multiplier = 0.35  # More draws in low-scoring leagues
        elif target_avg < 2.9:
            draw_multiplier = 0.30
        else:
            draw_multiplier = 0.25
    else:
        draw_multiplier = 0.28
    
    draw_probability = draw_multiplier * (1 - strength_diff)
    
    # Normalize probabilities
    total = home_win_probability + away_win_probability + draw_probability
    home_win_prob = home_win_probability / total
    away_win_prob = away_win_probability / total
    draw_prob = draw_probability / total
    
    # Conservative goal distributions targeting 80-100% of league averages
    if league_name and calibration:
        # Define base distributions for different average goal ranges - conservative approach
        if target_avg < 2.5:  # Very low scoring leagues
            home_win_goals = [1, 1, 1, 2, 2]
            away_loss_goals = [0, 0, 1, 1]
            draw_scores = [0, 1, 1, 1]
        elif target_avg < 2.7:  # Low scoring leagues
            home_win_goals = [1, 1, 1, 2, 2]
            away_loss_goals = [0, 0, 1, 1]
            draw_scores = [1, 1, 1, 1]
        elif target_avg < 2.9:  # Medium scoring leagues
            home_win_goals = [1, 1, 2, 2, 2]
            away_loss_goals = [0, 1, 1, 1]
            draw_scores = [1, 1, 1, 1]
        elif target_avg < 3.1:  # Medium-high scoring leagues
            home_win_goals = [1, 1, 2, 2, 2]
            away_loss_goals = [0, 1, 1, 1]
            draw_scores = [1, 1, 1, 2]
        else:  # High scoring leagues (3.1+) - slightly increased for very high targets
            home_win_goals = [1, 2, 2, 2, 3]
            away_loss_goals = [0, 1, 1, 1, 1]
            draw_scores = [1, 1, 2, 2]
    else:
        # Default distributions - balanced
        home_win_goals = [1, 1, 2, 2, 2, 2]
        away_loss_goals = [0, 1, 1, 1, 1]
        draw_scores = [1, 1, 1, 1, 2]
    
    # Determine match outcome first
    outcome_roll = random.random()
    if outcome_roll < home_win_prob:
        # Home win - use league-adjusted scoring
        base_home_goals = random.choice(home_win_goals)
        base_away_goals = random.choice(away_loss_goals)
        # Ensure home team wins
        if base_away_goals >= base_home_goals:
            base_home_goals = base_away_goals + 1
    elif outcome_roll < home_win_prob + draw_prob:
        # Draw - use league-adjusted draw scores
        draw_score = random.choice(draw_scores)
        base_home_goals = base_away_goals = draw_score
    else:
        # Away win - use league-adjusted scoring
        base_away_goals = random.choice(home_win_goals)
        base_home_goals = random.choice(away_loss_goals)
        # Ensure away team wins
        if base_home_goals >= base_away_goals:
            base_away_goals = base_home_goals + 1
    
    # Add some variance based on team strengths
    home_goals = base_home_goals
    away_goals = base_away_goals
    
    # Conservative extra goal probability targeting 80-100% of targets
    if league_name and calibration:
        # Reduced extra goal chances to avoid overshooting targets
        if target_avg < 2.5:
            base_extra_goal_chance = 0.02  # Very conservative for low scoring leagues
        elif target_avg < 2.8:
            base_extra_goal_chance = 0.03  # Conservative for low scoring leagues
        elif target_avg < 3.1:
            base_extra_goal_chance = 0.04  # Moderate for medium-high scoring leagues
        else:
            base_extra_goal_chance = 0.06  # Slight increase for very high-scoring leagues
        
        # Apply rolling average adjustment
        extra_goal_chance = base_extra_goal_chance * rolling_avg_adjustment
    else:
        extra_goal_chance = 0.04  # Balanced default
        
    # Very conservative chance for extra goals
    if random.random() < home_win_probability * extra_goal_chance:
        home_goals += 1
    if random.random() < away_win_probability * extra_goal_chance:
        away_goals += 1
    
    # Ensure realistic scores (cap at 4 goals for most leagues)
    max_goals = 5 if target_avg > 3.0 else 4
    home_goals = min(home_goals, max_goals)
    away_goals = min(away_goals, max_goals)
    
    return home_goals, away_goals


def play_match(home_team: Team, away_team: Team, match_modifier=40, home_offset=50, league_name=None, is_random_league=False, league_instance=None):
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
    
    # For random leagues, determine effective league based on teams
    effective_league = league_name
    if is_random_league and league_name:
        calibration = get_calibration()
        # Get the average for each team's original league
        home_avg = calibration.get_team_league_average(home_team.name)
        away_avg = calibration.get_team_league_average(away_team.name)
        
        # Use the lower average for more defensive matches
        if home_avg is not None and away_avg is not None:
            lower_avg = min(home_avg, away_avg)
            # Find the closest matching league
            for league, avg in calibration.goals_data.items():
                if abs(avg - lower_avg) < 0.1:
                    effective_league = league
                    break
        
    home_goals, away_goals = match_result(home_winning_probability, away_wining_probability, effective_league, league_instance)
    home_team.new_rating(match_modifier, home_goals - away_goals, home_winning_probability)
    away_team.new_rating(match_modifier, away_goals - home_goals, away_wining_probability)
    home_team.add_match(home_goals, away_goals)
    away_team.add_match(away_goals, home_goals)
    return home_goals, away_goals
