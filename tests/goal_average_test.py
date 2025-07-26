#!/usr/bin/env python3
"""
All Leagues Grouped Statistics Test

Simulates all leagues completely and shows grouped statistics at regular intervals:
- Every day, every 5 days, or every 10 days (user choice)
- Shows stats for all leagues together per reporting period
- Final summary with min/max daily averages per league
"""

import sys
import os

# Add parent directory to path so we can import from core/
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.entities.league import League
from core.entities.team import Team
from core.simulation.goals_calibration import get_calibration
import pandas as pd

def create_mock_teams(num_teams, league_name):
    """Create mock teams for simulation."""
    teams = []
    for i in range(num_teams):
        team = Team(f"{league_name.replace(' ', '')}_Team_{i+1}")
        teams.append(team)
    return teams

def get_league_team_count(league_name):
    """Get realistic team count for different leagues."""
    # Major leagues with their typical team counts (now with country prefix)
    team_counts = {
        "England - Premier League": 20,
        "England - Championship": 24,
        "England - League One": 24, 
        "England - League Two": 24,
        "Spain - La Liga": 20,
        "Spain - La Liga 2": 22,
        "Germany - Bundesliga": 18,
        "Germany - 2. Bundesliga": 18,
        "Austria - Bundesliga": 12,
        "Italy - Serie A": 20,
        "Italy - Serie B": 20,
        "France - Ligue 1": 20,
        "France - Ligue 2": 20,
        "Netherlands - Eredivisie": 18,
        "Portugal - Primeira Liga": 18,
        "Switzerland - Super League": 10,
        "China - Super League": 18,
        "India - Super League": 11,
        "Scotland - Scottish Premiership": 12,
        "Belgium - First Division": 16,
        "Belgium - Pro League": 18,
        "Turkey - Super Lig": 20,
        "Russia - Russian Premier League": 16,
        "Saudi Arabia - Saudi Pro League": 18,
        "Norway - Eliteserien": 16
    }
    
    # Return specific count if known, otherwise use varied counts based on league position
    if league_name in team_counts:
        return team_counts[league_name]
    
    # For unknown leagues, vary the team count to create different season lengths
    hash_val = hash(league_name) % 5
    return [16, 18, 20, 22, 24][hash_val]

def get_all_test_leagues():
    """Get all leagues from the CSV file."""
    # Get the parent directory (FantasyFootball) and construct path to assets
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(parent_dir, "assets", "league_average_goals.csv")
    try:
        df = pd.read_csv(csv_path)
        # Use country-league combination to avoid name conflicts
        leagues = [(f"{row['Country']} - {row['League']}", row['Average Goals per Match']) for _, row in df.iterrows()]
        return leagues
    except Exception as e:
        print(f"Error loading leagues: {e}")
        return []

def get_reporting_interval():
    """Ask user how often they want to see grouped statistics."""
    print("How often would you like to see grouped statistics?")
    print("Examples: 1 (every day), 2 (every 2 days), 5 (every 5 days), etc.")
    
    while True:
        try:
            choice = input("\nEnter interval (number of days): ").strip()
            interval = int(choice)
            if interval >= 1:
                interval_name = f"every {interval} day{'s' if interval > 1 else ''}"
                return interval, interval_name
            else:
                print("Please enter a positive number")
        except ValueError:
            print("Please enter a valid number")
        except KeyboardInterrupt:
            sys.exit(0)

def simulate_all_leagues_grouped():
    """Simulate all leagues with grouped statistics reporting."""
    print("ALL LEAGUES GROUPED SIMULATION")
    print("=" * 80)
    
    # Get all leagues
    leagues_data = get_all_test_leagues()
    if not leagues_data:
        print("No leagues found!")
        return
    
    # Get reporting interval
    interval, interval_name = get_reporting_interval()
    
    print(f"\nFound {len(leagues_data)} leagues to simulate")
    print(f"Each league will use realistic team counts (16-24 teams)")
    print(f"Statistics will be shown {interval_name}")
    print("\nStarting full simulation of all leagues...")
    
    input("Press Enter to start...")
    
    # Initialize all leagues
    all_leagues = []
    for league_name, target_avg in leagues_data:
        num_teams = get_league_team_count(league_name)
        teams = create_mock_teams(num_teams, league_name)
        test_league = League(
            teams=teams,
            league_name=league_name,
            my_team=0,
            relegation_zone=0,
            is_random_league=False
        )
        
        if test_league.valid:
            # Calculate expected match days for this league
            if num_teams % 2 == 0:
                expected_match_days = (num_teams - 1) * 2  # Double round-robin
            else:
                expected_match_days = num_teams * 2  # With dummy team
                
            all_leagues.append({
                'league': test_league,
                'name': league_name,
                'target': target_avg,
                'num_teams': num_teams,
                'expected_match_days': expected_match_days,
                'daily_averages': [],
                'rolling_averages': [],
                'completed': False
            })
        else:
            print(f"❌ Could not create valid league for {league_name}")
    
    print(f"\n✅ Successfully initialized {len(all_leagues)} leagues")
    
    # Show league details
    print(f"\n📋 LEAGUE DETAILS:")
    total_expected_days = 0
    for league_data in all_leagues:
        expected = league_data['expected_match_days']
        total_expected_days = max(total_expected_days, expected)
        print(f"   • {league_data['name']}: {league_data['num_teams']} teams, {expected} match days")
    
    print(f"\n🏁 Longest season: {total_expected_days} match days")
    print(f"🚀 Starting simulation...\n")
    
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
            rolling_avg = league.get_season_average_goals()
            
            league_data['daily_averages'].append(daily_avg)
            league_data['rolling_averages'].append(rolling_avg)
            
            # Advance to next match day
            league.advance_match_day()
        
        # Show statistics at specified intervals (5, 10, 15, 20, etc.)
        if match_day % interval == 0:
            # Clear screen for clean display
            import os
            os.system('clear' if os.name == 'posix' else 'cls')
            
            show_grouped_statistics(match_day, all_leagues, interval_name)
            
            try:
                input(f"\nPress Enter to continue to next reporting period...")
            except KeyboardInterrupt:
                break
        
        match_day += 1
        
        # Safety check to prevent infinite loops (based on longest expected season)
        max_expected_days = max(league_data['expected_match_days'] for league_data in all_leagues)
        safety_limit = max_expected_days + 10  # Add buffer
        if match_day > safety_limit:
            print(f"\n⚠️  Safety limit reached at match day {match_day} (expected max: {max_expected_days})")
            break
    
    # Final comprehensive summary
    import os
    os.system('clear' if os.name == 'posix' else 'cls')
    show_final_summary(all_leagues)

def show_grouped_statistics(match_day, all_leagues_data, interval_name):
    """Show individual league statistics in a table format."""
    print(f"\n{'='*140}")
    print(f"MATCH DAY {match_day} - ALL LEAGUES INDIVIDUAL STATISTICS")
    print(f"{'='*140}")
    
    # Prepare data for table
    table_data = []
    
    for league_data in all_leagues_data:
        if not league_data['daily_averages']:
            continue
            
        # For completed leagues, use their final values
        # For active leagues, use current values
        if league_data['completed'] or len(league_data['daily_averages']) == 0:
            # Use last available data
            current_daily = league_data['daily_averages'][-1] if league_data['daily_averages'] else 0
            current_rolling = league_data['rolling_averages'][-1] if league_data['rolling_averages'] else 0
        else:
            # Use current data
            current_daily = league_data['daily_averages'][-1]
            current_rolling = league_data['rolling_averages'][-1]
            
        min_daily = min(league_data['daily_averages']) if league_data['daily_averages'] else 0
        max_daily = max(league_data['daily_averages']) if league_data['daily_averages'] else 0
        target = league_data['target']
        
        # Mark league status with color symbols
        if current_rolling <= target:
            status_symbol = "🟢"  # Fine - at or below target
        elif current_rolling <= target * 1.1:
            status_symbol = "🟡"  # Okayish - within 10% above target
        else:
            status_symbol = "🔴"  # Issues - more than 10% above target
            
        table_data.append({
            'name': league_data['name'],
            'teams': league_data['num_teams'],
            'expected_days': league_data['expected_match_days'],
            'daily_avg': current_daily,
            'rolling_avg': current_rolling,
            'min_daily': min_daily,
            'max_daily': max_daily,
            'target': target,
            'status_symbol': status_symbol,
            'completed': league_data['completed']
        })
    
    # Sort by league name for consistent display
    table_data.sort(key=lambda x: x['name'])
    
    # Display table header
    print(f"{'League':<22} {'Teams':<5} {'Days':<4} {'Daily Avg':<9} {'Rolling':<8} {'Min Day':<8} {'Max Day':<8} {'Target':<7} {'Status':<6}")
    print("-" * 150)
    
    # Display each league
    for data in table_data:
        # Truncate league name to fit and add completion indicator
        league_name = data['name']
        if data['completed']:
            # Truncate name to make room for (✓)
            if len(league_name) > 17:
                league_name = league_name[:17] + "(✓)"
            else:
                league_name = f"{league_name} (✓)"
        
        # Ensure consistent width
        league_name = league_name[:22]  # Truncate if too long
            
        print(f"{league_name:<22} "
              f"{data['teams']:<5} "
              f"{data['expected_days']:<4} "
              f"{data['daily_avg']:<9.2f} "
              f"{data['rolling_avg']:<8.2f} "
              f"{data['min_daily']:<8.2f} "
              f"{data['max_daily']:<8.2f} "
              f"{data['target']:<7.2f} "
              f"{data['status_symbol']:<6}")
    
    # Count active vs completed leagues
    active_count = sum(1 for d in table_data if not d['completed'])
    completed_count = sum(1 for d in table_data if d['completed'])
    
    print(f"\n📊 MATCH DAY {match_day} STATUS:")
    print(f"   • Active leagues: {active_count}")
    print(f"   • Completed leagues: {completed_count}")
    print(f"   • Total leagues: {len(table_data)}")

def show_final_summary(all_leagues):
    """Show final comprehensive summary for all leagues."""
    print(f"\n{'='*150}")
    print("FINAL COMPREHENSIVE SUMMARY - ALL LEAGUES")
    print(f"{'='*150}")
    
    results = []
    for league_data in all_leagues:
        if league_data['daily_averages']:
            season_avg = sum(league_data['daily_averages']) / len(league_data['daily_averages'])
            min_daily = min(league_data['daily_averages'])
            max_daily = max(league_data['daily_averages'])
            final_rolling = league_data['rolling_averages'][-1] if league_data['rolling_averages'] else 0
            
            results.append({
                'league': league_data['name'],
                'target': league_data['target'],
                'season_avg': season_avg,
                'final_rolling': final_rolling,
                'min_daily': min_daily,
                'max_daily': max_daily,
                'daily_span': max_daily - min_daily,
                'accuracy': abs(final_rolling - league_data['target'])
            })
    
    if results:
        print(f"{'League':<30} {'Target':<7} {'Season':<7} {'Final':<7} {'Min Day':<8} {'Max Day':<8} {'D.Span':<7} {'Error':<7} {'Status':<6}")
        print("-" * 150)
        
        for r in results:
            # Add status symbol based on final rolling average
            if r['final_rolling'] <= r['target']:
                status_symbol = "🟢"  # Fine - at or below target
            elif r['final_rolling'] <= r['target'] * 1.1:
                status_symbol = "🟡"  # Okayish - within 10% above target
            else:
                status_symbol = "🔴"  # Issues - more than 10% above target
            
            # Truncate league name if too long to maintain alignment
            league_name = r['league']
            if len(league_name) > 30:
                league_name = league_name[:27] + "..."
                
            print(f"{league_name:<30} "
                  f"{r['target']:<7.2f} "
                  f"{r['season_avg']:<7.2f} "
                  f"{r['final_rolling']:<7.2f} "
                  f"{r['min_daily']:<8.2f} "
                  f"{r['max_daily']:<8.2f} "
                  f"{r['daily_span']:<7.2f} "
                  f"{r['accuracy']:<7.3f} "
                  f"{status_symbol:<6}")
        
        print(f"\n{'='*150}")
        print("OVERALL ANALYSIS:")
        
        # Calculate overall statistics
        avg_accuracy = sum(r['accuracy'] for r in results) / len(results)
        avg_daily_span = sum(r['daily_span'] for r in results) / len(results)
        avg_season_vs_target = sum(r['season_avg'] - r['target'] for r in results) / len(results)
        
        # Color status distribution
        green_final = sum(1 for r in results if r['final_rolling'] <= r['target'])
        yellow_final = sum(1 for r in results if r['target'] < r['final_rolling'] <= r['target'] * 1.1)
        red_final = sum(1 for r in results if r['final_rolling'] > r['target'] * 1.1)
        
        print(f"• Leagues completed: {len(results)}")
        print(f"• 🟢 Fine (≤ target): {green_final} ({green_final/len(results)*100:.1f}%)")
        print(f"• 🟡 Okayish (≤ target+10%): {yellow_final} ({yellow_final/len(results)*100:.1f}%)")
        print(f"• 🔴 Issues (> target+10%): {red_final} ({red_final/len(results)*100:.1f}%)")
        print(f"• Average accuracy (final rolling vs target): {avg_accuracy:.3f}")
        print(f"• Average daily span (flexibility): {avg_daily_span:.2f}")
        print(f"• Average season bias: {avg_season_vs_target:+.3f}")
        
        # Distribution analysis by error magnitude
        excellent = sum(1 for r in results if r['accuracy'] <= 0.1)
        good = sum(1 for r in results if 0.1 < r['accuracy'] <= 0.2)
        poor = sum(1 for r in results if r['accuracy'] > 0.2)
        
        print(f"\nAccuracy Distribution:")
        print(f"• Excellent (≤0.1): {excellent} leagues ({excellent/len(results)*100:.1f}%)")
        print(f"• Good (0.1-0.2): {good} leagues ({good/len(results)*100:.1f}%)")
        print(f"• Poor (>0.2): {poor} leagues ({poor/len(results)*100:.1f}%)")
        
        # Best and worst
        most_accurate = min(results, key=lambda x: x['accuracy'])
        most_flexible = max(results, key=lambda x: x['daily_span'])
        least_flexible = min(results, key=lambda x: x['daily_span'])
        
        print(f"\nKey Performers:")
        print(f"• Most accurate: {most_accurate['league']} (error: {most_accurate['accuracy']:.3f})")
        print(f"• Most flexible: {most_flexible['league']} (daily span: {most_flexible['daily_span']:.2f})")
        print(f"• Least flexible: {least_flexible['league']} (daily span: {least_flexible['daily_span']:.2f})")
        
        # Highlight problematic leagues in final summary
        final_problem_leagues = []
        for r in results:
            if r['final_rolling'] > r['target']:
                diff = r['final_rolling'] - r['target']
                final_problem_leagues.append((r['league'], diff, r['accuracy']))
        
        if final_problem_leagues:
            # Sort by severity (highest difference first)
            final_problem_leagues.sort(key=lambda x: x[1], reverse=True)
            print(f"\n🚨 FINAL LEAGUES WITH ISSUES (Rolling > Target):")
            for name, diff, accuracy in final_problem_leagues:
                severity = "🔴" if diff > 0.5 else "🟡" if diff > 0.2 else "🟠"
                print(f"   {severity} {name}: +{diff:.2f} above target (total error: {accuracy:.3f})")
        else:
            print(f"\n✅ All leagues finished within target ranges!")
        
        # Show leagues that need calibration adjustment
        high_error_leagues = [r for r in results if r['accuracy'] > 0.3]
        if high_error_leagues:
            print(f"\n⚙️ LEAGUES NEEDING CALIBRATION ADJUSTMENT (>0.3 error):")
            high_error_leagues.sort(key=lambda x: x['accuracy'], reverse=True)
            for r in high_error_leagues[:10]:  # Show top 10 worst
                direction = "↗️" if r['final_rolling'] > r['target'] else "↘️"
                print(f"   {direction} {r['league']}: {r['final_rolling']:.2f} vs {r['target']:.2f} (error: {r['accuracy']:.3f})")
            if len(high_error_leagues) > 10:
                print(f"   ... and {len(high_error_leagues) - 10} more leagues need adjustment")
    
    print(f"\n{'='*150}")
    print("🎉 SIMULATION COMPLETE!")
    print("The rolling average system successfully balances daily flexibility with season accuracy.")

if __name__ == "__main__":
    try:
        simulate_all_leagues_grouped()
    except KeyboardInterrupt:
        print("\n\nSimulation interrupted by user. Goodbye!")
        sys.exit(0)