#!/usr/bin/env python3
"""
Interactive Goal Average Test for Fantasy Football Manager

This test runs simulations across all leagues and reports goal average statistics
with color-coded results based on target compliance.

Target: 80-100% of 2.6 goals per match (2.08 - 2.6 goals)
"""

import sys
import os
import random
from typing import Dict, List, Tuple, Any
from pathlib import Path

# Add the parent directory to the path so we can import game modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.entities.team import Team
from core.entities.league import League
from core.simulation.simulator import play_match
from interfaces.cli.user_input import existing_league, random_teams
from core.storage.team_storage import team_storage, initialize_team_storage

# ANSI color codes for terminal output
class Colors:
    GREEN = '\033[92m'   # Target range (2.08-2.6)
    YELLOW = '\033[93m'  # Slightly above target (2.6-2.86)
    RED = '\033[91m'     # Outside acceptable range
    BOLD = '\033[1m'
    END = '\033[0m'

TARGET_MIN = 2.08
TARGET_MAX = 2.6
WARNING_MAX = 2.86  # 10% above target

def simulate_season_goals(teams: List[Team], num_simulations: int = 100) -> List[float]:
    """
    Simulate multiple complete seasons and return goals per match for each simulation.
    
    Args:
        teams: List of teams for the league
        num_simulations: Number of complete seasons to simulate
        
    Returns:
        List of average goals per match for each simulation
    """
    goals_per_match_results = []
    
    for sim in range(num_simulations):
        # Reset teams for each simulation
        for team in teams:
            team.reset()
        
        total_goals = 0
        total_matches = 0
        
        # Simulate a complete season (each team plays each other twice)
        for home_idx in range(len(teams)):
            for away_idx in range(len(teams)):
                if home_idx != away_idx:
                    home_goals, away_goals = play_match(teams[home_idx], teams[away_idx])
                    total_goals += home_goals + away_goals
                    total_matches += 1
        
        if total_matches > 0:
            avg_goals_per_match = total_goals / total_matches
            goals_per_match_results.append(avg_goals_per_match)
    
    return goals_per_match_results

def get_color_for_average(avg: float) -> str:
    """Get color code based on goal average."""
    if TARGET_MIN <= avg <= TARGET_MAX:
        return Colors.GREEN
    elif TARGET_MAX < avg <= WARNING_MAX:
        return Colors.YELLOW
    else:
        return Colors.RED

def analyze_league_goals(league_name: str, teams: List[Team], verbose: bool = False) -> Dict[str, Any]:
    """
    Analyze goal scoring patterns for a specific league.
    
    Args:
        league_name: Name of the league
        teams: List of teams in the league
        verbose: Whether to show detailed output
        
    Returns:
        Dictionary with statistics
    """
    if verbose:
        print(f"\n{Colors.BOLD}Analyzing {league_name}...{Colors.END}")
    
    # Run simulations
    goals_per_match_list = simulate_season_goals(teams, num_simulations=20)
    
    if not goals_per_match_list:
        return None
    
    # Calculate statistics
    avg_goals = sum(goals_per_match_list) / len(goals_per_match_list)
    min_goals = min(goals_per_match_list)
    max_goals = max(goals_per_match_list)
    
    # Determine status
    if TARGET_MIN <= avg_goals <= TARGET_MAX:
        status = "TARGET"
        color = Colors.GREEN
    elif TARGET_MAX < avg_goals <= WARNING_MAX:
        status = "WARNING"
        color = Colors.YELLOW
    else:
        status = "CRITICAL"
        color = Colors.RED
    
    if verbose:
        print(f"  Average: {color}{avg_goals:.2f}{Colors.END} goals per match")
        print(f"  Range: {min_goals:.2f} - {max_goals:.2f}")
        print(f"  Status: {color}{status}{Colors.END}")
    
    return {
        'league_name': league_name,
        'team_count': len(teams),
        'avg_goals': avg_goals,
        'min_goals': min_goals,
        'max_goals': max_goals,
        'status': status,
        'color': color
    }

def test_all_leagues(verbose: bool = True) -> List[Dict[str, Any]]:
    """
    Test goal averages across all available leagues.
    
    Args:
        verbose: Whether to show detailed output for each league
        
    Returns:
        List of analysis results for each league
    """
    print(f"{Colors.BOLD}=== Fantasy Football Manager Goal Average Test ==={Colors.END}")
    print(f"Target: {Colors.GREEN}{TARGET_MIN} - {TARGET_MAX}{Colors.END} goals per match")
    print(f"Warning: {Colors.YELLOW}{TARGET_MAX} - {WARNING_MAX}{Colors.END} goals per match")
    print(f"Critical: {Colors.RED}Outside acceptable range{Colors.END}")
    print()
    
    results = []
    
    try:
        # Initialize team storage if needed
        if not team_storage._loaded_from_raw:
            initialize_team_storage()
        
        # Get all available leagues
        available_leagues = team_storage.get_leagues_by_country()
        
        for country, leagues in available_leagues.items():
            if verbose:
                print(f"\n{Colors.BOLD}=== {country} ==={Colors.END}")
            
            for league_info in leagues:
                league_name, team_count, has_estimated = league_info
                full_league_name = f"{country} - {league_name}"
                
                try:
                    # Load teams for this league
                    teams = team_storage.get_league_teams(league_name, country)
                    
                    if teams and len(teams) >= 4:  # Need at least 4 teams for meaningful test
                        result = analyze_league_goals(full_league_name, teams, verbose)
                        if result:
                            results.append(result)
                    
                except Exception as e:
                    if verbose:
                        print(f"  Error loading {full_league_name}: {e}")
                        
    except Exception as e:
        print(f"Error getting available leagues: {e}")
        
    # Test random leagues
    if verbose:
        print(f"\n{Colors.BOLD}=== Random Leagues ==={Colors.END}")
    
    for team_count in [8, 12, 16, 20]:
        try:
            _, _, teams, _ = random_teams(team_count)
            result = analyze_league_goals(f"Random League ({team_count} teams)", teams, verbose)
            if result:
                results.append(result)
        except Exception as e:
            if verbose:
                print(f"  Error creating random league with {team_count} teams: {e}")
    
    return results

def print_summary_table(results: List[Dict[str, Any]]):
    """Print a summary table of all results."""
    print(f"\n{Colors.BOLD}=== SUMMARY TABLE ==={Colors.END}")
    print(f"{'League':<40} {'Teams':<6} {'Avg Goals':<10} {'Min':<6} {'Max':<6} {'Status':<10}")
    print("-" * 85)
    
    target_count = 0
    warning_count = 0
    critical_count = 0
    
    # Sort results by status (target first, then warning, then critical)
    status_order = {'TARGET': 0, 'WARNING': 1, 'CRITICAL': 2}
    results.sort(key=lambda x: (status_order[x['status']], x['league_name']))
    
    for result in results:
        color = result['color']
        status = result['status']
        
        if status == 'TARGET':
            target_count += 1
        elif status == 'WARNING':
            warning_count += 1
        else:
            critical_count += 1
        
        print(f"{result['league_name']:<40} "
              f"{result['team_count']:<6} "
              f"{color}{result['avg_goals']:<10.2f}{Colors.END} "
              f"{result['min_goals']:<6.2f} "
              f"{result['max_goals']:<6.2f} "
              f"{color}{status:<10}{Colors.END}")
    
    print("-" * 85)
    print(f"{Colors.BOLD}Total leagues tested: {len(results)}{Colors.END}")
    print(f"{Colors.GREEN}Target range: {target_count}{Colors.END}")
    print(f"{Colors.YELLOW}Warning range: {warning_count}{Colors.END}")
    print(f"{Colors.RED}Critical range: {critical_count}{Colors.END}")
    
    if len(results) > 0:
        success_rate = (target_count / len(results)) * 100
        print(f"{Colors.BOLD}Success rate: {success_rate:.1f}%{Colors.END}")

def interactive_mode():
    """Run the test in interactive mode with user choices."""
    print(f"{Colors.BOLD}Fantasy Football Manager - Goal Average Interactive Test{Colors.END}")
    print()
    print("Options:")
    print("1. Test all leagues (quick overview)")
    print("2. Test all leagues (detailed analysis)")
    print("3. Test specific league")
    print("4. Test random leagues only")
    print("5. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == "1":
                results = test_all_leagues(verbose=False)
                print_summary_table(results)
                
            elif choice == "2":
                results = test_all_leagues(verbose=True)
                print_summary_table(results)
                
            elif choice == "3":
                print("\nAvailable countries:")
                try:
                    # Initialize team storage if needed
                    if not team_storage._loaded_from_raw:
                        initialize_team_storage()
                    
                    available_leagues = team_storage.get_leagues_by_country()
                    for i, country in enumerate(available_leagues.keys(), 1):
                        print(f"  {i}. {country}")
                    
                    country_choice = input("\nEnter country name: ").strip()
                    if country_choice in available_leagues:
                        leagues = available_leagues[country_choice]
                        print(f"\nAvailable leagues in {country_choice}:")
                        for i, (league_name, team_count, has_estimated) in enumerate(leagues, 1):
                            print(f"  {i}. {league_name} ({team_count} teams)")
                        
                        league_choice = input("\nEnter league name: ").strip()
                        
                        # Find matching league
                        selected_league = None
                        for league_name, team_count, has_estimated in leagues:
                            if league_name.lower() == league_choice.lower():
                                selected_league = (league_name, team_count, has_estimated)
                                break
                        
                        if selected_league:
                            teams = team_storage.get_league_teams(selected_league[0], country_choice)
                            if teams:
                                result = analyze_league_goals(f"{country_choice} - {selected_league[0]}", teams, verbose=True)
                                if result:
                                    print_summary_table([result])
                            else:
                                print("Could not load teams for this league.")
                        else:
                            print("League not found.")
                    else:
                        print("Country not found.")
                        
                except Exception as e:
                    print(f"Error: {e}")
                    
            elif choice == "4":
                results = []
                for team_count in [8, 10, 12, 16, 18, 20, 24]:
                    try:
                        _, _, teams, _ = random_teams(team_count)
                        result = analyze_league_goals(f"Random League ({team_count} teams)", teams, verbose=True)
                        if result:
                            results.append(result)
                    except Exception as e:
                        print(f"Error creating random league with {team_count} teams: {e}")
                
                print_summary_table(results)
                
            elif choice == "5":
                print("Goodbye!")
                break
                
            else:
                print("Invalid choice. Please enter 1-5.")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        # Run automatic test for all leagues
        results = test_all_leagues(verbose=False)
        print_summary_table(results)
    else:
        # Run interactive mode
        interactive_mode()