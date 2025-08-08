# Fantasy Football Manager v2.3.2

A comprehensive football simulation game featuring realistic international player management, team building, advanced match simulation with tournament modes, and comprehensive player statistics tracking.

## 🎮 **What is this?**

Fantasy Football Manager is a terminal-based football (soccer) simulation game where you:
- Create custom players with detailed attributes
- Build and manage teams with tactical formations  
- Simulate realistic matches with advanced statistics
- Run knockout tournaments with penalty shootouts
- Track comprehensive player and team statistics
- Manage tournament history with winners tracking

## 🚀 **Quick Start**

### **Installation**
```bash
# Install dependencies
pip install -r requirements.txt

# Or check dependencies manually
python dependency_checker.py
```

### **Run the Game**
```bash
python3 ffm.py
```

### **First Steps**
1. Generate a player pool (50+ recommended)
2. Create teams with different formations
3. Play matches or run tournaments
4. Watch your teams develop over time

## ⚽ **Key Features**

### **Player Management**
- **16 Detailed Attributes**: Physical, mental, and technical skills
- **International Players**: Authentic names from 28 countries with Latin alphabet
- **Realistic Performance**: Elite players more consistent than average
- **Player Development**: Form, fatigue, and confidence systems
- **Personality Types**: Cool-headed, passionate, consistent, volatile
- **Unique Players**: No duplicate players across teams

### **Team Building** 
- **10 Formation System**: 4-4-2, 4-3-3, 3-5-2, 4-2-3-1, 5-3-2, 3-4-3, 4-1-4-1, 4-5-1, 3-4-2-1, 4-1-2-1-2
- **Tactical Styles**: Attacking, defensive, balanced, wide, central
- **International Squads**: Teams with diverse, authentic player nationalities
- **Squad Management**: Formation-aware position assignments
- **Team Chemistry**: Momentum and streak effects

### **Match Simulation**
- **Realistic Match Engine**: Possession, shots, expected goals
- **Live Events**: Goals, cards, substitutions with detailed descriptions
- **Advanced Statistics**: Pass accuracy, team ratings, fatigue impact
- **Disciplinary System**: Yellow/red cards with numerical disadvantage

### **Tournament Mode**
- **Knockout Tournaments**: Direct elimination with bracket progression
- **Flexible Setup**: Choose teams manually or randomly generate
- **Penalty Shootouts**: Individual player mechanics with pressure effects
- **Professional Presentation**: Clean tournament flow and statistics

### **International Player System** ⭐ NEW
- **28 Nationalities**: American, British, French, German, Italian, Spanish, Brazilian, Polish, Dutch, Swedish, Norwegian, Danish, Finnish, Turkish, Indonesian, Filipino, Czech, Hungarian, Romanian, Croatian, Slovenian, Estonian, Latvian, Lithuanian, Slovak, Icelandic, Irish, Portuguese
- **Authentic Names**: Realistic names using Latin alphabet for readability
- **Cultural Diversity**: Each nationality has authentic naming patterns
- **Clean Names**: No titles or honorifics, professional football player names

### **Enhanced Penalty System**
- **Individual Player Skills**: Penalty takers vs goalkeepers
- **Realistic Success Rates**: 40-95% based on skill difference
- **Pressure Situations**: Sudden death penalties are harder
- **Detailed Outcomes**: Saves, misses, and goals with player names

### **Player Statistics System** ⭐ NEW v2.2.0
- **Career Statistics**: Comprehensive tracking of goals, assists, matches, cards
- **Tournament-Specific Stats**: Per-tournament performance tracking
- **Advanced Metrics**: Pass accuracy, shots on target, clean sheets, efficiency ratings
- **Leaderboards**: Top scorers, assist providers, most appearances, clean sheet leaders
- **Individual Player Analysis**: Detailed statistics view with career and tournament breakdowns

### **Tournament Management** ⭐ NEW v2.2.0
- **Tournament History**: Automatic tracking of completed tournaments with winners
- **Tournament Operations**: Rename and delete tournaments from centralized menu
- **Winner Tracking**: Every completed tournament shows its champion
- **Statistics Integration**: Tournament results automatically update player statistics
- **Data Management**: Clean separation of tournament history and player career stats

### **Enhanced Tournament Display** ⭐ NEW v2.2.1
- **Top Scorer Integration**: Tournament bracket display now shows top scorer information
- **Improved Statistics Reliability**: Fixed tournament statistics display issues
- **Real-time Data Loading**: Tournament lists always show current player statistics
- **Enhanced Data Management**: Improved "Reset All Data" to preserve players while clearing game data

### **Modular Architecture** ⭐ NEW v2.3.0
- **Clean Architecture**: Complete separation of interface, service, and core layers
- **Interface Layer**: Dedicated menu classes for each game feature
- **Service Layer**: Business logic separation for maintainable code
- **Core Managers**: Centralized game logic with proper dependency management
- **Modern Entry Point**: New `ffm.py` launcher with improved CLI interface

## 🏆 **Game Modes**

- **Single Match**: Quick one-off games
- **Multiple Matches**: Series between same teams
- **Random Matches**: Generated teams with performance tracking
- **Tournament Mode**: Knockout competitions with brackets and winner tracking
- **Quick Play**: Instant action with random teams
- **Statistics Analysis**: Comprehensive player and tournament statistics tracking

## 📊 **Performance Tracking**

- **Elo Rating System**: Dynamic team strength ratings
- **Streak Effects**: Winning/losing streaks affect performance
- **Form Tracking**: Player performance over recent matches
- **Team Momentum**: Match events influence team performance
- **Player Career Statistics**: Goals, assists, matches, cards, efficiency ratings
- **Tournament Statistics**: Per-tournament performance tracking with leaderboards
- **Advanced Analytics**: Pass accuracy, shots conversion, clean sheet tracking

## 🛠️ **Utilities**

The `utilities/` folder contains helpful scripts:

- **`migrate_data.py`**: Migrate existing players to use authentic international names
- **`regenerate_teams.py`**: Recreate teams with new players while preserving team characteristics
- **`dependency_checker.py`**: Check if required dependencies (faker) are installed
- **`requirements.txt`**: List of required Python packages

### **Usage**
```bash
# Check dependencies
python utilities/dependency_checker.py

# Migrate to international names
python utilities/migrate_data.py

# Regenerate teams with new players
python utilities/regenerate_teams.py
```

