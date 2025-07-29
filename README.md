# Fantasy Football Manager v2.2 - Tournament Edition

A comprehensive football simulation system with realistic performance bounds, player management, team building, and advanced match simulation capabilities.

## 🎯 **Key Features**

### **Enhanced Realism**
- **Realistic Performance Bounds**: Prevents unrealistic performance scaling (60-rated players can't perform at 95+ levels)
- **Elite Player Consistency**: Better players show more consistent performance (based on real football research)
- **Sigmoid Performance Curves**: Smooth scaling prevents harsh performance cutoffs
- **Research-Based Bounds**: Elite players 2.7x more consistent than average players

### **Core Systems**
- **Player Management**: Create and manage players with 16 detailed attributes including mental and physical traits
- **Team Building**: Build teams with formations, tactical styles, and strategic depth
- **Advanced Match Engine**: Realistic match simulation with fatigue, form, momentum, and pressure effects
- **Performance Tracking**: Dynamic fatigue, stamina, form, and confidence systems
- **Elo Rating System**: Track team performance over time with live updates

### **Gameplay Features**
- **Single & Multiple Match Simulation**: Play individual matches or series with streak effects
- **Tournament Mode**: Knockout-style tournaments with bracket progression and penalty shootouts
- **Team Modification**: Edit existing teams with formation-aware position assignments
- **Momentum/Streak System**: Teams on winning/losing streaks get performance bonuses/penalties
- **Quick Play**: Instant match with randomly generated teams
- **Detailed Statistics**: Match events, possession, shots, fatigue impact, and momentum tracking

## 🚀 **Quick Start**

### **Running the Game**
```bash
python3 fantasy_football.py
```

### **First Time Setup**
1. **Generate Players**: Go to Player Management → Generate Player Pool (recommended: 50+ players)
2. **Create Teams**: Go to Team Management → Create Random/Manual Team  
3. **Play Matches**: Select \"Play Single Match\" or \"Quick Play\" for instant action

### **Recommended Workflow**
1. Generate 50-80 players for a good player pool
2. Create 4-6 teams with different formations and styles
3. Play multiple matches to see streak effects and Elo progression
4. Use \"Play Multiple Matches (Random Teams)\" to see performance systems in action

## 📊 **System Architecture**

### **Core Application Files**
- **`fantasy_football.py`**: Main application with clean UI and all game modes
- **`match_engine.py`**: Advanced match simulation with performance tracking
- **`models.py`**: Core data models (Player, Team, Position, TacticalStyle) with realistic bounds
- **`player_manager.py`**: Player creation, management, and migration support
- **`team_manager.py`**: Team creation, formations, and Elo management
- **`tournament_manager.py`**: Tournament bracket generation and match management
- **`performance_system.py`**: Multi-layered performance management (fatigue, form, momentum, pressure)

### **Data Storage**
- **`players.json`**: Persistent player database with full attribute storage
- **`teams.json`**: Team database with formations, styles, and Elo ratings

## 👤 **Player System**

### **Core Attributes (0-100)**
- **Goalkeeping**: Shot-stopping ability (only relevant for goalkeepers)
- **Defending**: Defensive positioning, tackling, marking
- **Passing**: Passing accuracy, vision, distribution
- **Dribbling**: Ball control, close control, skill moves
- **Shooting**: Finishing, shot power, accuracy
- **Physical**: Strength, speed, stamina, jumping

### **Extended Attributes (0-100)**
- **Natural Fitness**: Base stamina and recovery rate
- **Work Rate**: How quickly player gets tired during matches
- **Pressure Handling**: Performance under high-stakes situations
- **Concentration**: Maintains performance when fatigued
- **Determination**: Resistance to negative momentum
- **Composure**: Performance in crucial moments
- **Leadership**: Influence on team momentum

### **Personality & Form**
- **Temperament**: COOL_HEADED, PASSIONATE, CONSISTENT, VOLATILE
- **Age**: Affects consistency and recovery (18-35 range)
- **Form System**: Dynamic 1-10 rating based on recent performances
- **Confidence**: 0-100 scale affecting performance modifiers

## ⚽ **Team System**

### **Formations**
Pre-configured formations include:
- **4-4-2**: Classic balanced formation
- **4-3-3**: Attacking formation with wingers  
- **3-5-2**: Midfield-heavy formation
- **4-2-3-1**: Modern formation with double pivot
- **5-3-2**: Defensive formation
- **Custom**: Build your own 11-player formation

### **Tactical Styles**
- **BALANCED**: No modifications (default)
- **ATTACKING**: +20% attack, -10% defense
- **DEFENSIVE**: -20% attack, +20% defense  
- **WIDE**: +10% midfield (emphasizes wing play)
- **CENTRAL**: -10% midfield (emphasizes central play)

### **Performance Tracking**
- **Elo Ratings**: Dynamic team strength ratings (start at 1500)
- **Streak System**: Win/loss streaks affect performance (±15% maximum)
- **Team Momentum**: Match events influence team performance (-100 to +100)

### **Team Modification System**
- **Formation-Aware Positions**: Shows where each player actually plays in the current formation
- **Position Assignment Display**: 
  - `Playing: CB` - Natural position matches formation role
  - `Playing: CM (Natural: AM)` - Player adapted to new tactical role
- **Smart Replacement Suggestions**: 
  - `✅` Perfect match for position
  - `⚠️` Compatible position (good adaptation)
  - `❌` Poor fit but available
- **Position Compatibility**: Understands realistic position changes (CB↔SW, LB↔LWB, CM↔DM↔AM)

## 🏆 **Tournament System**

### **Tournament Features**
- **Knockout Style**: Direct elimination tournament with bracket progression
- **Flexible Team Selection**:
  - Manual selection from existing teams
  - Random selection from existing teams
  - Create all new random teams
  - Mix existing and random teams
- **Automatic Bracket Generation**: Supports any number of teams (pads to power of 2)
- **Penalty Shootouts**: Realistic penalty simulation for drawn knockout matches
- **Live Tournament Progress**: Visual bracket with match results and advancement tracking

### **Tournament Flow**
1. **Create Tournament**: Name tournament and specify team count
2. **Team Selection**: Choose from 4 different team selection methods
3. **Bracket Generation**: Automatic knockout bracket with proper seeding
4. **Match Simulation**: Full match details with enhanced statistics
5. **Round Progression**: Clear round summaries and advancement notifications
6. **Tournament Completion**: Championship ceremony with final bracket display

### **Match Display in Tournaments**
- **Tournament Progress Bar**: Visual progress through rounds
- **Enhanced Match Stats**: Same detailed statistics as single matches
- **Team Attribution**: Clear event descriptions showing which team scored/received cards
- **Elo Updates**: Live rating changes after each match
- **Professional Presentation**: Clean screen management and staged tournament flow

## 🎮 **Match Engine**

### **Realistic Performance Bounds**
The new system ensures realistic performance scaling:

**Before (Unrealistic):**
- 60-rated player with perfect conditions: 95 performance (59% boost) ❌

**After (Realistic):**  
- 60-rated player with perfect conditions: ~72 performance (~20% boost) ✅

### **Performance Factors**
- **Form Modifier**: 0.9 to 1.15 (±12.5% max, down from ±20%)
- **Momentum Modifier**: ±12% maximum (down from ±15%)  
- **Pressure Modifier**: ±8% maximum (down from ±15%)
- **Consistency-Based Bounds**: Elite players more consistent than average players

### **Match Statistics**
- **Possession %**: Based on midfield strength and fatigue
- **Expected Goals (xG)**: Zone-based calculations with tactical modifiers
- **Shots & Accuracy**: Dynamic based on team ratings and fatigue
- **Match Events**: Goals, cards, substitutions with detailed tracking
- **Fatigue Impact**: Real-time stamina tracking affects performance

### **Disciplinary System**
- **Yellow Cards**: Performance penalty (-8 momentum), tracked per match
- **Red Cards**: Two types with full implementation:
  - **Direct Red Card**: Immediate sending off (-25 momentum)
  - **Second Yellow**: Automatic red card after 2 yellows
- **Numerical Disadvantage**: Teams with red cards play with reduced players:
  - **10 players**: 15% performance penalty
  - **9 players**: 30% performance penalty
  - **8 players**: 45% performance penalty
  - **7 players**: 60% performance penalty
  - **<7 players**: Match abandoned, opposition awarded 3-0 victory
- **Individual Impact**: Sent-off player's attributes completely removed from team calculations
- **Match Reset**: All cards cleared between matches - players available for next game

### **Elite vs Average Consistency**
Based on football research:
- **Elite players (85+)**: ±8-15% performance variation
- **Average players (60-69)**: ±20-25% performance variation  
- **Poor players (<60)**: -25%/+15% performance variation

## 📋 **Game Modes**

### **Player Management**
- **View All Players**: Browse by position with top performers
- **Create Random Player**: Generate position-appropriate players
- **Create Manual Player**: Full control over attributes and traits
- **Generate Player Pool**: Bulk creation ensuring positional balance
- **Search Players**: Find players by name
- **View Top Players**: Rankings by overall rating

### **Team Management**  
- **View All Teams**: Elo rankings with formations and styles
- **Create Random Team**: Automatic team building with best available players
- **Create Manual Team**: Choose formation, style, and individual players
- **View Team Details**: Comprehensive team analysis
- **Delete Team**: Remove teams from database

### **Match Simulation**
- **Play Single Match**: One-off match with detailed statistics
- **Play Multiple Matches**: Series between same teams showing streak development
  - **Detailed Mode (≤5 matches)**: Full match analysis with events, statistics, and momentum tracking
  - **Fast Mode (>5 matches)**: Progress indicator with comprehensive final summary
- **Play Multiple Matches (Random Teams)**: Generated teams with performance progression
- **Quick Play**: Instant match with random teams
- **View Rankings**: Current Elo standings

### **Settings**
- **Toggle Momentum**: Enable/disable streak effects
- **Toggle Detailed Simulation**: Choose simulation depth
- **Reset All Data**: Clean slate for new campaigns
- **View System Info**: Database statistics and feature overview

## 🧪 **Testing & Verification**

### **Verification Scripts**
- **`quick_verify.py`**: Quick test of realistic bounds
- **`test_realistic_bounds.py`**: Comprehensive testing suite
- **`demo_realistic_bounds.py`**: Before/after performance comparison

### **Sample Test Results**
```
🧪 Testing 60-rated player with perfect conditions
Base Overall Rating: 60.0
Effective Overall: 71.8
Performance Boost: +19.7%
✅ PASS: Within realistic bounds (max 75.0)
```

## 📈 **Performance Research**

The realistic bounds system is based on actual football research:
- **Elite consistency**: 9.2% coefficient of variation between matches
- **Average consistency**: 24.8% coefficient of variation  
- **Performance hierarchy**: Elite players maintain superiority while allowing tactical depth
- **Sigmoid curves**: Natural performance scaling prevents exploitation

## 🎯 **Tips for Success**

### **Team Building**
- **Balance is Key**: Don't focus only on attack or defense
- **Formation Matters**: Choose formations that suit your player strengths  
- **Tactical Styles**: Match your style to your team's attributes
- **Squad Depth**: Keep multiple players for each position

### **Performance Management**
- **Monitor Fatigue**: Tired players perform poorly and get cards
- **Build Momentum**: Winning streaks provide significant boosts
- **Pressure Situations**: High-pressure matches favor composed players
- **Consistency Advantage**: Elite players are more reliable than average players with good form

### **Strategic Depth**
- **Elite vs Average**: A consistent 85-rated player often outperforms a volatile 75-rated player
- **Temperament Matters**: CONSISTENT players more reliable, VOLATILE players more unpredictable
- **Age Curves**: Peak consistency at 27-30, younger players more erratic
- **Mental Attributes**: Concentration, composure, and determination affect consistency

## 🔧 **Technical Details**

### **System Requirements**
- Python 3.7+ 
- No external dependencies (uses only standard library)
- Cross-platform (Windows, macOS, Linux)

### **File Structure**
```
fantasy_football/
├── fantasy_football.py      # Main application
├── models.py               # Core data models  
├── performance_system.py   # Performance management
├── match_engine.py         # Match simulation
├── player_manager.py       # Player operations
├── team_manager.py         # Team operations
├── players.json           # Player database
├── teams.json            # Team database
└── README.md             # This file
```

### **Data Migration**
The system automatically migrates legacy player data to the new extended format with realistic bounds. No manual intervention required.

## 🆕 **Version 2.1 Changes**

### **Major Improvements**
- ✅ **Realistic Performance Bounds**: Research-based performance scaling
- ✅ **Elite Player Consistency**: Better players show less variation  
- ✅ **Sigmoid Performance Curves**: Smooth, natural scaling
- ✅ **Consistency-Based Bounds**: Different limits for different player tiers
- ✅ **Cleaned Codebase**: Removed duplicate/legacy files

### **Performance System Overhaul**
- Form modifier: 0.8-1.2 → 0.9-1.15 (more realistic)
- Momentum modifier: ±15% → ±12% (capped)
- Pressure modifier: ±15% → ±8% (more subtle)
- Master bounds: Prevents any player from exceeding realistic performance

### **Bug Fixes**
- Fixed unrealistic performance scaling
- Improved consistency calculations
- Better age-based attribute adjustment
- Enhanced temperament effects

## 🔮 **Future Enhancements**

Potential improvements for future versions:
- **Transfer System**: Player trading between teams
- **Season Mode**: Full league campaigns with fixtures
- **Player Development**: Attribute growth/decline over time
- **Injuries**: Temporary player unavailability
- **Financial Management**: Budgets and salaries
- **Custom Leagues**: User-created competitions
- **Advanced Analytics**: Detailed performance metrics

---

**Fantasy Football Manager v2.1** - Where tactical depth meets realistic performance! 🏆
