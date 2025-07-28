# Fantasy Football Manager v2.0

A comprehensive football simulation system with player management, team building, and match simulation capabilities.

## Features

- **Player Management**: Create and manage players with detailed attributes
- **Team Building**: Build teams manually or automatically with formation support
- **Single & Multiple Match Simulation**: Play one match, series between same teams, or multiple matches with random teams
- **Enhanced UI**: Clean, menu-driven interface with screen clearing and emojis
- **Streak/Momentum System**: Teams on winning/losing streaks get performance bonuses/penalties
- **Elo Rating System**: Track team performance over time with live updates
- **Tournament Support**: Run round-robin tournaments
- **Detailed Statistics**: Match events, possession, shots, and comprehensive analysis

## Quick Start

### Running the Application

```bash
python3 fantasy_football.py
```

### Demo Mode

For a quick demonstration of the system:

```bash
python3 demo.py
```

### Test the System

To verify everything is working:

```bash
python3 test_system.py
```

### Streak System Demo

To see the momentum/streak effects in action:

```bash
python3 test_streak_demo.py
```

### Enhanced Features Test

To test all enhanced features:

```bash
python3 test_enhanced_app.py
```

### Enhanced Streak System Test

To test the improved streak display and screen clearing:

```bash
python3 test_enhanced_streak.py
```

### Multiple Matches with Random Teams Test

To test the multiple matches feature with random teams:

```bash
python3 test_multiple_random_teams.py
```

### First Time Setup

1. **Generate Players**: Go to Player Management → Generate Player Pool
2. **Create Teams**: Go to Team Management → Create Random/Manual Team
3. **Single Match**: Select "Play Single Match" for one game
4. **Multiple Matches**: Select "Play Multiple Matches" to see streak effects develop
5. **Multiple Matches (Random Teams)**: Select "Play Multiple Matches (Random Teams)" to see streak effects with randomly generated teams

### Quick Play

Select "Quick Play" from the main menu for an instant match with randomly generated teams.

### Menu Navigation

- **Screen clearing** between all menu transitions and after match prompts
- **Visual streak indicators**: 🔥 (hot streak), ❄️ (cold streak), ⚪ (no streak)
- **Enhanced momentum display** with BOOST/PENALTY labels when active
- **Streak threshold notifications** when teams enter hot/cold streaks
- **Improved match progression** with clear before/after comparisons
- Pause between actions to review results

## System Architecture

### Core Modules

- **models.py**: Core data models (Player, Team, Position, TacticalStyle)
- **player_manager.py**: Player creation and management
- **team_manager.py**: Team creation and management
- **match_engine.py**: Match simulation engine
- **fantasy_football.py**: Main application

### Data Storage

- **players.json**: Stores all player data
- **teams.json**: Stores all team data

## Player Attributes

Each player has six core attributes (0-100 scale):

- **Goalkeeping**: Only relevant for goalkeepers
- **Defending**: Defensive ability
- **Passing**: Passing accuracy and vision
- **Dribbling**: Ball control and dribbling
- **Shooting**: Shooting accuracy and power
- **Physical**: Strength, speed, and stamina

## Positions

The system supports 16 different positions:

### Goalkeepers
- GK (Goalkeeper)

### Defenders
- CB (Center Back)
- SW (Sweeper/Libero)
- LB (Left Back)
- RB (Right Back)

### Midfielders
- DM (Defensive Midfielder)
- CM (Central Midfielder)
- AM (Attacking Midfielder)
- LM (Left Midfielder)
- RM (Right Midfielder)
- WB (Wing Back)
- LWB (Left Wing Back)
- RWB (Right Wing Back)

### Forwards
- ST (Striker)
- LW (Left Winger)
- RW (Right Winger)

## Formations

Pre-configured formations include:

- **4-4-2**: Classic balanced formation
- **4-3-3**: Attacking formation with wingers
- **3-5-2**: Midfield-heavy formation
- **4-2-3-1**: Modern formation with double pivot
- **5-3-2**: Defensive formation

You can also create custom formations with any combination of 11 players.

## Tactical Styles

Teams can adopt different tactical approaches:

- **BALANCED**: No modifications to team attributes
- **ATTACKING**: +20% attack, -10% defense
- **DEFENSIVE**: -20% attack, +20% defense
- **WIDE**: +10% midfield (emphasizes wing play)
- **CENTRAL**: -10% midfield (emphasizes central play)

## Match Engine

The match engine uses sophisticated calculations:

### Expected Goals (xG)
- Based on team ratings and tactical styles
- Zone-based calculations (left, center, right)
- Home advantage bonus

### Momentum System
- Teams on winning streaks get performance bonuses
- Losing streaks decrease performance
- Can be toggled on/off in settings

### Match Statistics
- Possession percentage
- Expected goals
- Shots and shots on target
- Pass accuracy
- Match events (goals with scorers)

## Elo Rating System

- Teams start with 1500 Elo rating
- Ratings update after each match
- K-factor of 20 (adjustable)
- Momentum affects rating changes

## Creating Players

### Random Players
1. Go to Player Management
2. Select "Create Random Player"
3. Choose position (or random)
4. Optionally provide name prefix

### Manual Players
1. Go to Player Management
2. Select "Create Manual Player"
3. Enter name and attributes

### Bulk Generation
1. Go to Player Management
2. Select "Generate Player Pool"
3. Enter number of players
4. System ensures at least 2 players per position

## Creating Teams

### Random Teams
1. Go to Team Management
2. Select "Create Random Team"
3. Enter team name
4. System automatically:
   - Selects formation
   - Picks best available players
   - Assigns tactical style

### Manual Teams
1. Go to Team Management
2. Select "Create Manual Team"
3. Choose formation or custom
4. Select tactical style
5. Pick players for each position

## Playing Matches

### Single Match
1. Select "Play Single Match" from main menu
2. Choose home and away teams
3. View detailed match result
4. Elo ratings update automatically

### Multiple Matches (Same Teams)
1. Select "Play Multiple Matches" from main menu
2. Choose two teams
3. Set number of matches to simulate
4. Watch streak effects develop over time
5. View comprehensive series summary

### Multiple Matches (Random Teams)
1. Select "Play Multiple Matches (Random Teams)" from main menu
2. Choose number of matches to simulate
3. System creates two random teams once
4. Watch the same teams play multiple times to see:
   - Streak effects developing over time
   - Elo rating changes
   - Momentum boosts and penalties
   - Performance consistency patterns

### Tournament Mode
Use the match_engine's `simulate_tournament` method to run round-robin tournaments.

## Tips

- **Balance is Key**: Don't focus only on attack or defense
- **Formations Matter**: Choose formations that suit your players
- **Tactical Styles**: Match your style to your team's strengths
- **Squad Depth**: Keep multiple players for each position
- **Momentum**: Teams on winning streaks perform better

## Advanced Usage

### Custom Formations

```python
from models import Team, Position
from team_manager import TeamManager

# Create custom formation
my_formation = {
    Position.GK: 1,
    Position.CB: 2,
    Position.DM: 1,
    Position.CM: 3,
    Position.AM: 2,
    Position.ST: 2
}
```

### Batch Simulations

```python
from match_engine import MatchEngine

engine = MatchEngine()
results = engine.simulate_tournament(teams, rounds=2)
```

## File Structure

```
development/
├── fantasy_football.py    # Main application
├── models.py             # Core data models
├── player_manager.py     # Player management
├── team_manager.py       # Team management
├── match_engine.py       # Match simulation
├── players.json          # Player database
├── teams.json           # Team database
└── README.md            # This file
```

## Troubleshooting

### Not enough players for position
- Generate more players using Player Pool
- Some positions can substitute (e.g., WB can play LB/RB)

### Teams not balanced
- Check team ratings in Team Details
- Adjust tactical style to compensate
- Consider rebuilding with different players

### Unrealistic scores
- Toggle detailed simulation for more realistic results
- Adjust team strengths by editing players
- Check if momentum system is affecting results

## Future Enhancements

Potential improvements:
- Player transfers between teams
- Season mode with fixtures
- Player development over time
- Injuries and suspensions
- Financial management
- Custom leagues and cups