#!/usr/bin/env python3
"""
Random Leagues Grouped Statistics Test

Creates 10 random leagues with different team counts and simulates complete seasons:
- Shows stats for all random leagues together per reporting period
- Final summary with min/max daily averages per league
- Tests goal calibration for random leagues with real teams
"""

import sys
import os
import random

# Add parent directory to path so we can import from core/
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.entities.league import League
from core.entities.team import Team
from core.storage.team_storage import team_storage
from core.simulation.goals_calibration import get_calibration


def create_random_league(league_name: str, num_teams: int, top100_only: bool = False):
    """Create a random league similar to the user_input.py logic."""
    
    # Use optimized team storage if available
    if team_storage._loaded_from_raw:
        if top100_only:
            # Get top teams by rating
            teams = team_storage.get_random_teams(num_teams, min_rating=85, max_rating=100)
            if len(teams) < num_teams:
                teams.extend(team_storage.get_random_teams(num_teams - len(teams), min_rating=75, max_rating=84))
        else:
            teams = team_storage.get_random_teams(num_teams)
    else:
        # Fallback - this shouldn't happen in our setup but keeping for completeness
        from core.storage.football_statistics import FootballStatistics
        if top100_only:
            teams = [
                Team(name=y['Club'], elo=y['Elo'])
                for _, y in FootballStatistics().get_top_teams().items()
            ]
        else:
            teams = [
                Team(name=y['Club'], elo=y['Elo'])
                for y in FootballStatistics().get_teams()
            ]
        random.shuffle(teams)
        teams = teams[:num_teams]
    
    # Create the league
    league = League(
        league_name=league_name,
        teams=teams,
        my_team=None,  # No user team for testing
        relegation_zone=2,
        is_random_league=True  # This is the key flag!
    )
    
    return league


def get_expected_average_for_random_league(teams):
    """Get expected goal average based on weighted average of team origins."""
    calibration = get_calibration()
    league_counts = {}  # Count teams per league
    league_averages = {}  # Store league averages
    unknown_teams = 0
    
    # Count teams from each league
    for team in teams:
        original_avg = calibration.get_team_league_average(team.name)
        if original_avg:
            # Find which league this average belongs to (reverse lookup)
            league_name = None
            for league, avg in calibration.goals_data.items():
                if abs(avg - original_avg) < 0.01:  # Match within small tolerance
                    league_name = league
                    break
            
            if league_name:
                league_counts[league_name] = league_counts.get(league_name, 0) + 1
                league_averages[league_name] = original_avg
        else:
            unknown_teams += 1
    
    if league_counts:
        # Calculate weighted average
        total_weight = sum(league_counts.values())
        weighted_sum = sum(count * league_averages[league] for league, count in league_counts.items())
        weighted_average = weighted_sum / total_weight
        
        # If there are unknown teams, blend with default (2.7)
        if unknown_teams > 0:
            total_teams = len(teams)
            known_weight = total_weight / total_teams
            unknown_weight = unknown_teams / total_teams
            final_average = (weighted_average * known_weight) + (2.7 * unknown_weight)
            return final_average
        else:
            return weighted_average
    else:
        # All teams unknown - use default calibration
        return 2.7


def initialize_random_leagues():
    """Initialize 10 random leagues with different team counts."""
    print("🔧 Initializing team storage...")
    
    # Initialize team storage
    from core.storage.team_storage import initialize_team_storage
    try:
        initialize_team_storage()
        print("   ✅ Team storage initialized successfully")
    except Exception as e:
        print(f"   ❌ Failed to initialize team storage: {e}")
        return []
    
    all_leagues = []
    
    # Create 10 random leagues with different team counts (6-20 teams)
    team_counts = [6, 8, 10, 12, 14, 16, 18, 20, 22, 24]
    
    print(f"\n🏟️  Creating {len(team_counts)} random leagues...")
    
    for i, num_teams in enumerate(team_counts):
        league_name = f"League_{num_teams:02d}"
        print(f"   Creating {league_name} with {num_teams} teams...", end=" ")
        
        # Alternate between regular random and top100 teams
        top100_only = (i % 3 == 0)  # Every 3rd league uses top100 teams
        
        try:
            league = create_random_league(league_name, num_teams, top100_only)
            
            if league.valid:
                # Get teams for analysis
                teams = [league.get_team_by_index(j) for j in range(league.team_number())]
                teams = [t for t in teams if t is not None]
                
                # Calculate expected match days (double round-robin)
                expected_match_days = (num_teams - 1) * 2
                
                # Get expected average
                expected_avg = get_expected_average_for_random_league(teams)
                
                all_leagues.append({
                    'name': league_name,
                    'league': league,
                    'num_teams': num_teams,
                    'expected_match_days': expected_match_days,
                    'target': expected_avg,
                    'daily_averages': [],
                    'rolling_averages': [],
                    'completed': False,
                    'teams': teams,
                    'top100': top100_only
                })
                print("✅")
            else:
                print("❌ Invalid league")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n✅ Successfully initialized {len(all_leagues)} random leagues")
    
    # Show league details
    print(f"\n📋 RANDOM LEAGUE DETAILS:")
    total_expected_days = 0
    for league_data in all_leagues:
        expected = league_data['expected_match_days']
        total_expected_days = max(total_expected_days, expected)
        league_type = "Elite" if league_data['top100'] else "Mixed"
        print(f"   • {league_data['name']}: {league_data['num_teams']} teams, {expected} match days, {league_type}, Target: {league_data['target']:.2f}")
    
    print(f"\n🏁 Longest season: {total_expected_days} match days")
    
    return all_leagues


def show_progress_report(all_leagues, match_day, reporting_interval):
    """Show progress report for all leagues together."""
    if match_day % reporting_interval != 0:
        return
    
    # Clear screen
    import os
    os.system('clear' if os.name == 'posix' else 'cls')
    
    print(f"📊 PROGRESS REPORT - MATCH DAY {match_day}")
    print("-" * 120)
    
    # Prepare table data
    table_data = []
    total_goals = 0
    total_matches = 0
    
    for league_data in all_leagues:
        if league_data['daily_averages']:
            current_avg = league_data['daily_averages'][-1]
            rolling_avg = league_data['rolling_averages'][-1] if league_data['rolling_averages'] else 0
            status = "✓" if league_data['completed'] else "→"
            
            # Get match stats for this league
            league_matches = len(league_data['daily_averages'])
            league_goals = sum(league_data['daily_averages']) * league_matches  # Approximate
            
            total_goals += league_goals
            total_matches += league_matches
            
            table_data.append({
                'League': league_data['name'],
                'Teams': league_data['num_teams'],
                'Type': "Elite" if league_data['top100'] else "Mixed",
                'Target': f"{league_data['target']:.2f}",
                'Current': f"{current_avg:.2f}",
                'Rolling': f"{rolling_avg:.2f}",
                'Status': status
            })
    
    if table_data:
        # Print header
        print(f"{'League':<12} {'Teams':<6} {'Type':<6} {'Target':<7} {'Current':<8} {'Rolling':<8} {'Status':<7}")
        print("-" * 120)
        
        # Print data
        for league_data in all_leagues:
            if league_data['daily_averages']:
                current_avg = league_data['daily_averages'][-1]
                rolling_avg = league_data['rolling_averages'][-1] if league_data['rolling_averages'] else 0
                target = league_data['target']
                
                # Add status symbol based on rolling average vs target (same logic as original)
                if rolling_avg <= target:
                    status_symbol = "🟢"  # Fine - at or below target
                elif rolling_avg <= target * 1.1:
                    status_symbol = "🟡"  # Okayish - within 10% above target
                else:
                    status_symbol = "🔴"  # Issues - more than 10% above target
                
                # Truncate league name if too long and add completion indicator
                league_name = league_data['name']
                if league_data['completed']:
                    if len(league_name) > 7:
                        league_name = league_name[:7] + "(✓)"
                    else:
                        league_name = f"{league_name} (✓)"
                
                # Ensure consistent width
                league_name = league_name[:12]
                league_type = "Elite" if league_data['top100'] else "Mixed"
                
                print(f"{league_name:<12} "
                      f"{league_data['num_teams']:<6} "
                      f"{league_type:<6} "
                      f"{target:<7.2f} "
                      f"{current_avg:<8.2f} "
                      f"{rolling_avg:<8.2f} "
                      f"{status_symbol:<7}")
        
        # Count active vs completed leagues
        active_count = sum(1 for l in all_leagues if not l['completed'])
        completed_count = sum(1 for l in all_leagues if l['completed'])
        
        print(f"\n📊 MATCH DAY {match_day} STATUS:")
        print(f"   • Active leagues: {active_count}")
        print(f"   • Completed leagues: {completed_count}")
        print(f"   • Total leagues: {len(all_leagues)}")
        
        # Pause before continuing
        input("\nPress Enter to continue simulation...")


def show_final_summary(all_leagues):
    """Show final comprehensive summary for all random leagues."""
    # Clear screen before final summary
    import os
    os.system('clear' if os.name == 'posix' else 'cls')
    
    print(f"{'='*130}")
    print("FINAL COMPREHENSIVE SUMMARY - ALL RANDOM LEAGUES")
    print(f"{'='*130}")
    
    results = []
    for league_data in all_leagues:
        if league_data['daily_averages']:
            season_avg = sum(league_data['daily_averages']) / len(league_data['daily_averages'])
            min_daily = min(league_data['daily_averages'])
            max_daily = max(league_data['daily_averages'])
            final_rolling = league_data['rolling_averages'][-1] if league_data['rolling_averages'] else 0
            
            results.append({
                'league': league_data['name'],
                'teams': league_data['num_teams'],
                'type': "Elite" if league_data['top100'] else "Mixed",
                'target': league_data['target'],
                'season_avg': season_avg,
                'final_rolling': final_rolling,
                'min_daily': min_daily,
                'max_daily': max_daily,
                'daily_span': max_daily - min_daily,
                'accuracy': abs(final_rolling - league_data['target'])
            })
    
    if not results:
        print("No data to display.")
        return
    
    # Sort by team count for better display
    results.sort(key=lambda x: x['teams'])
    
    # Print detailed table
    print(f"{'League':<12} {'Teams':<6} {'Type':<6} {'Target':<7} {'Season':<7} {'Rolling':<8} {'Min':<6} {'Max':<6} {'Span':<6} {'Accuracy':<9} {'Status':<6}")
    print("-" * 130)
    
    total_accuracy = 0
    for r in results:
        # Add status symbol based on final rolling average (same logic as original)
        if r['final_rolling'] <= r['target']:
            status_symbol = "🟢"  # Fine - at or below target
        elif r['final_rolling'] <= r['target'] * 1.1:
            status_symbol = "🟡"  # Okayish - within 10% above target
        else:
            status_symbol = "🔴"  # Issues - more than 10% above target
        
        # Truncate league name if too long to maintain alignment
        league_name = r['league']
        if len(league_name) > 11:
            league_name = league_name[:8] + "..."
            
        print(f"{league_name:<12} {r['teams']:<6} {r['type']:<6} {r['target']:<7.2f} {r['season_avg']:<7.2f} {r['final_rolling']:<8.2f} {r['min_daily']:<6.2f} {r['max_daily']:<6.2f} {r['daily_span']:<6.2f} {r['accuracy']:<9.2f} {status_symbol:<6}")
        total_accuracy += r['accuracy']
    
    print("-" * 130)
    
    # Summary statistics
    avg_accuracy = total_accuracy / len(results)
    season_averages = [r['season_avg'] for r in results]
    rolling_averages = [r['final_rolling'] for r in results]
    targets = [r['target'] for r in results]
    
    print(f"\n📈 SUMMARY STATISTICS:")
    print(f"   • Total random leagues: {len(results)}")
    print(f"   • Average accuracy: {avg_accuracy:.3f} goals/match")
    print(f"   • Season averages range: {min(season_averages):.2f} - {max(season_averages):.2f}")
    print(f"   • Rolling averages range: {min(rolling_averages):.2f} - {max(rolling_averages):.2f}")
    print(f"   • Target range: {min(targets):.2f} - {max(targets):.2f}")
    
    # Performance assessment
    excellent = sum(1 for r in results if r['accuracy'] <= 0.15)
    good = sum(1 for r in results if 0.15 < r['accuracy'] <= 0.30)
    acceptable = sum(1 for r in results if 0.30 < r['accuracy'] <= 0.50)
    
    print(f"\n🎯 PERFORMANCE BREAKDOWN:")
    print(f"   • Excellent (≤0.15): {excellent}/{len(results)} leagues")
    print(f"   • Good (0.15-0.30): {good}/{len(results)} leagues")
    print(f"   • Acceptable (0.30-0.50): {acceptable}/{len(results)} leagues")
    
    if avg_accuracy <= 0.30:
        print(f"\n🎉 OVERALL ASSESSMENT: Excellent calibration for random leagues!")
    elif avg_accuracy <= 0.50:
        print(f"\n✅ OVERALL ASSESSMENT: Good calibration for random leagues.")
    else:
        print(f"\n⚠️  OVERALL ASSESSMENT: Calibration needs improvement.")


def main():
    print("🧪 RANDOM LEAGUES GOAL AVERAGE TEST SUITE")
    print("=" * 60)
    
    # Get user preference for reporting interval
    print("Select reporting frequency:")
    print("1. Every match day (detailed)")
    print("2. Every 5 match days (balanced)")
    print("3. Every 10 match days (summary)")
    
    while True:
        try:
            choice = input("Enter choice (1-3): ").strip()
            if choice == "1":
                reporting_interval = 1
                break
            elif choice == "2":
                reporting_interval = 5
                break
            elif choice == "3":
                reporting_interval = 10
                break
            else:
                print("Please enter 1, 2, or 3")
        except (ValueError, KeyboardInterrupt):
            print("Please enter 1, 2, or 3")
    
    print(f"📊 Reporting every {reporting_interval} match day(s)")
    
    # Initialize leagues
    all_leagues = initialize_random_leagues()
    
    if not all_leagues:
        print("❌ No valid leagues created. Exiting.")
        return
    
    print(f"\n🚀 Starting simulation...\n")
    
    # Simulate all leagues match day by match day
    match_day = 1
    
    while True:
        # Check if any leagues are still active
        active_leagues = [l for l in all_leagues if not l['completed']]
        if not active_leagues:
            break
            
        # Simulate this match day for all leagues that are still active
        for league_data in all_leagues:
            if league_data['completed']:
                continue
                
            league = league_data['league']
            fixtures = league.get_current_fixtures()
            
            if not fixtures:
                league_data['completed'] = True
                continue
            
            # Simulate all matches for this day
            daily_goals = 0
            daily_matches = 0
            
            for home_idx, away_idx in fixtures:
                home_goals, away_goals = league.simulate_match(home_idx, away_idx)
                daily_goals += home_goals + away_goals
                daily_matches += 1
            
            # Calculate averages
            daily_avg = daily_goals / daily_matches if daily_matches > 0 else 0
            league_data['daily_averages'].append(daily_avg)
            
            # Calculate rolling average (last 10 match days)
            recent_averages = league_data['daily_averages'][-10:]
            rolling_avg = sum(recent_averages) / len(recent_averages)
            league_data['rolling_averages'].append(rolling_avg)
            
            # Advance league to next match day
            league.advance_match_day()
        
        # Show progress report
        show_progress_report(all_leagues, match_day, reporting_interval)
        
        match_day += 1
    
    # Show final summary
    show_final_summary(all_leagues)


if __name__ == "__main__":
    main()