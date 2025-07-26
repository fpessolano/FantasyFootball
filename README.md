# Fantasy Football Manager  
**About:**      A CLI football manager game in Python3  
**Author:**     F. Pessolano  
**Version:**    0.9.1

## Description  
A comprehensive football manager simulation with a beautiful Rich terminal interface. Experience realistic match simulation, team management, and complete season play with over 80 real-world leagues and authentic team data.

The application combines modern terminal UI design with sophisticated match simulation, creating an engaging football management experience entirely in your command line.

## Features

### ✨ Rich Terminal Experience
- **Beautiful UI**: Colored tables, panels, and live match simulation
- **Dynamic Theming**: Automatic light/dark theme detection for optimal readability
- **Live Match Simulation**: Real-time match progression with minute-by-minute updates
- **Follow Your Team Mode**: Focused view highlighting your team with other matches dimmed
- **Smart Table Sizing**: Tables automatically resize based on content length

### 🏟️ Gameplay Features
- **League Management**: Choose from 80+ real-world leagues or create custom leagues
- **Team Management**: Manage your chosen team through complete seasons
- **Realistic Match Simulation**: Enhanced scoring system with authentic goal frequencies
- **Season Play**: Multi-season continuation with promotion/relegation system
- **ELO-Based Ratings**: Advanced team strength calculation with similarity matching
- **Persistent Data**: Modern JSON-based save system with compression and data integrity checks

### 📊 Real World Data
- **34 Major Leagues**: Premier League, La Liga, Serie A, Bundesliga, and many more
- **670+ Teams**: Authentic team data from around the world
- **Realistic Statistics**: Goal frequencies calibrated to real-world averages
- **Dynamic Calibration**: Rolling average system ensures accurate season-long statistics

## Quick Start

### Installation
```bash
# Clone or download the repository
cd FantasyFootball

# Install dependencies
pip install -r requirements.txt

# Run the game
python run.py
```

### Requirements
- Python 3.7+
- Rich terminal library (automatically installed)
- Modern terminal with color support

## Interface Guide

### Main Menu
Choose from a clean, intuitive interface:
- **New Game**: Start fresh with league and team selection
- **Load Game**: Continue your saved career with rich save metadata display
- **Delete**: Manage saved games - delete individual saves or all saves with safety confirmations
- **Help**: View in-game help and controls
- **Exit**: Quit the application

### Match Day Experience
When a match day arrives, choose your viewing experience:

- **S** - **Simulate All**: Quick results table for all matches
- **W** - **Watch All**: Live minute-by-minute simulation with real-time updates
- **F** - **Follow Your Team**: Detailed view focusing on your team's match
- **C** - **Choose Matches**: Select specific matches to watch live

### Live Match Features
- **Real-time Scores**: Watch goals as they happen with minute markers
- **Goal Events**: See who scored and when during the match
- **Visual Progress**: Match timer and status updates
- **Optimized Speed**: 3x faster simulation (0.2-0.5s per minute) for smooth viewing

### League Table
Enhanced league display with:
- **Color-coded Positions**: Green for European spots, red for relegation
- **Team Highlighting**: Your team stands out with special highlighting
- **Complete Statistics**: Matches, wins, draws, losses, goals, and points
- **Recent Form**: Visual representation of last 5 match results

## Controls

- **Standard Navigation**: Type menu options and press Enter
- **Ctrl+C**: Interrupt simulation at any time
- **Enter**: Continue after match completion
- **Simple Commands**: All interactions use intuitive text commands

## Project Structure

```
FantasyFootball/
├── run.py                 # Main game launcher
├── core/                  # Core game engine
│   ├── entities/          # Game objects (Team, League)
│   ├── simulation/        # Match engine & realistic goal calibration
│   └── storage/           # Data management & ELO estimation
├── interfaces/cli/        # Rich terminal interface
├── utils/                 # Utilities (JSON save system, screen helpers)
├── stats/                 # Statistics and analytics
├── assets/                # Game data
│   ├── data/             # 670+ teams across 34 leagues
│   └── league_average_goals.csv  # Real-world goal calibration data
└── tests/                 # Testing tools
    ├── goal_average_test.py         # Goal calibration testing tool
    ├── random_leagues_test.py       # Random league goal average testing
    └── save_load_test.py            # Save/load functionality testing
```

## Latest Updates (v0.9.1)

### Performance Optimizations
- **3x Faster Simulation**: Live matches now progress at optimal speed
- **Improved UX**: Better visual flow and cleaner match displays
- **Enhanced Calibration**: More accurate goal frequencies across all leagues

### Visual Improvements
- **Fixed Alignment**: Corrected table layouts and column spacing
- **Consistent Interface**: Streamlined design across all game modes
- **Better Theme Support**: Enhanced light/dark theme adaptation

### Save System Improvements
- **JSON-Based Storage**: Modern, reliable replacement for problematic shelve system
- **Data Compression**: 50-70% size reduction with gzip compression
- **Integrity Protection**: SHA256 checksums prevent data corruption
- **Save Metadata**: Rich information about saves including progress details
- **Automatic Backups**: Keeps last 3 versions for safety
- **Smart Save Names**: Remembers original save name when re-saving loaded games
- **Save Management**: Delete individual saves or all saves with safety confirmations

## Development Features

### Goal Calibration System
The game includes a sophisticated calibration system that ensures realistic match outcomes:

- **Real-World Data**: Goal averages from 34 major football leagues
- **Rolling Average Tracking**: Season-long calibration maintains accuracy
- **Dynamic Adjustment**: Match-day flexibility with season accuracy
- **Comprehensive Testing**: Automated testing ensures 80-110% of target averages

### Advanced Architecture
- **Modular Design**: Clear separation between game logic, UI, and data
- **O(1) Team Lookups**: Optimized for instant access to 670+ teams
- **Extensible Framework**: Ready for AI, web interfaces, and advanced features
- **Modern Save System**: JSON-based storage with compression and integrity verification

## Future Roadmap

### Next Phase (v0.10.x)
- **Match History**: Detailed records and statistics tracking
- **Enhanced Analytics**: Performance insights and predictions
- **Advanced Save Features**: Multi-save management with quick preview
- **League Composition Review**: Annual verification and updates of team rosters to reflect real-world season changes

### Planned Features
- **AI Integration**: Machine learning for match prediction and player development
- **Transfer Market**: Dynamic player trading with AI valuations
- **Advanced Statistics**: Comprehensive analytics dashboard
- **Web Interface**: Optional browser-based UI

## Troubleshooting

### Common Issues
1. **Tables appear cut off**: Ensure terminal is at least 80 characters wide
2. **Colors not displaying**: Use a modern terminal with full color support
3. **Performance issues**: Try a smaller league (10-12 teams) for faster simulation

### System Requirements
- **Terminal**: Modern terminal with 256+ color support
- **Font**: Monospace font recommended for proper table alignment
- **Screen Size**: Minimum 80x24 characters for optimal experience

## Testing & Calibration

The project includes comprehensive testing tools:

```bash
cd tests

# Test goal calibration across all leagues
python goal_average_test.py

# Test random league goal calibration
python random_leagues_test.py

# Test save/load game functionality
python save_load_test.py
```

These tools verify that:
- **Goal Calibration**: Match simulation produces realistic goal averages that match real-world football statistics
- **Random League Calibration**: Random leagues maintain realistic goal averages using weighted averages based on team league origins
- **Save/Load System**: JSON-based saves work correctly with compression, integrity checks, and proper data restoration

## Technology Stack

- **Python 3.x**: Core application language
- **Rich**: Modern terminal UI framework with theming
- **Pandas**: Data analysis for team statistics
- **Modular Architecture**: Clean separation of concerns

## License
See LICENSE file for details.

---

**Enjoy realistic football management in your terminal!**

*The beautiful game deserves a beautiful interface.*