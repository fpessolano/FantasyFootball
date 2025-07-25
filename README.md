# Fantasy Football Manager  
**About:**      A CLI football manager game in Python3  
**Author:**     F. Pessolano  
**Version:**    0.9.0

## Description  
A comprehensive football manager simulation application built using both AI and traditional programming approaches. This project aims to create a realistic football management experience with advanced match simulation, player statistics, team management, and strategic gameplay elements.

The application combines modern AI techniques for realistic player behavior and match outcomes with traditional algorithms for core game mechanics, creating an engaging and sophisticated football management simulation.   

## Vision & Goals
This project aims to build a complete football manager simulation that rivals commercial applications by leveraging:

- **AI-Powered Match Engine**: Realistic match outcomes using machine learning and statistical models
- **Intelligent Player Development**: AI-driven player progression and regression systems
- **Advanced Analytics**: Performance prediction and tactical analysis using data science
- **Dynamic Market System**: AI-controlled transfer market with realistic valuations
- **Adaptive Opponent AI**: Computer-controlled teams that learn and adapt strategies

## Current Features
- **🎨 Rich Terminal UI**: Beautiful colored interface with live match simulation and dynamic theming
- **🌓 Light/Dark Theme Support**: Automatic color adaptation for different terminal backgrounds
- **⚽ Real-time Match Experience**: Live goal events, match timers, and simultaneous match progression
- **👁️ Follow Your Team Mode**: Dedicated view focusing on your team with other matches summary
- **📏 Dynamic Table Sizing**: Tables automatically size to accommodate longest team names
- **🏆 League Management**: Create custom leagues, use existing real-world leagues, or generate random leagues
- **👥 Team Management**: Manage your chosen team through seasons with ELO-based ratings
- **🎲 Realistic Match Simulation**: Enhanced scoring system with authentic goal frequencies
- **🏅 Season Play**: Complete seasons with promotion/relegation system
- **💾 Persistent Data**: Save/load system with user profiles and game state management
- **🌍 Real World Data**: Over 80 real-world leagues with authentic team data and statistics

## Major New Features (v0.9.0)
- **🎨 Rich Terminal UI**: Complete interface overhaul with beautiful colored tables and panels
- **🌓 Dynamic Theme System**: Automatic light/dark theme detection for optimal readability
- **⚽ Live Match Simulation**: Real-time match progression with minute-by-minute updates
- **🎯 Follow Your Team Mode**: Focused view highlighting your team with dimmed other matches
- **🕒 Global Match Clock**: Single time display showing match progression (Kick-off → 90' → Full-time)
- **📏 Smart Table Sizing**: Tables automatically resize based on longest team names in league
- **🎲 Realistic Scoring**: Improved match simulator with authentic goal frequencies (more 1-0, 2-1 games)
- **🔧 Comprehensive Bug Fixes**: Resolved NoneType errors and match simulation crashes
- **🎨 Theme-Aware Interface**: All components (menus, help, tables) adapt to terminal background
- **⚡ Enhanced Performance**: Optimized team lookups and match processing

## Previous Improvements (v0.7.1-v0.8.0)
- **🔄 Seamless Seasons**: Multi-season continuation without resets
- **🎯 Enhanced League Selection**: Two-step country → league interface
- **📚 Improved Help System**: Clean help display with screen management
- **⚡ Performance Optimization**: O(1) team lookups (670 teams loaded instantly)
- **🧠 Smart ELO System**: Advanced estimation using similarity matching
- **🏗️ Modular Architecture**: Complete codebase reorganization
- **🧹 Code Cleanup**: Removed unused files and consolidated entry points

## Dependencies  
See `requirements.txt`  

## Usage  

### Quick Start
```bash
# Rich Terminal UI (RECOMMENDED - v0.9.0)
python run_rich.py

# Standard UI (legacy support)
python run.py

# Legacy entry point (backward compatibility)
python main.py
```

The Rich UI provides a beautiful terminal interface with:
- **🎨 Colored tables and panels** that adapt to your terminal theme
- **⚽ Live match simulation** with real-time goal events and timing
- **👁️ Follow Your Team mode** for focused match viewing
- **📏 Dynamic sizing** that fits any team name length perfectly
- **🌓 Light/Dark theme support** for optimal readability

### Requirements
```bash
pip install -r requirements.txt
```

## Project Structure

The project now uses a modular architecture for better maintainability:

```
├── run.py               # Modern game launcher (recommended)
├── main.py              # Legacy game launcher (backward compatibility)
├── core/                # Core game engine
│   ├── entities/        # Game objects (Team, League)
│   ├── simulation/      # Match simulation & scheduling
│   └── storage/         # Data management & ELO estimation
├── interfaces/          # User interfaces
│   ├── cli/             # Command line interface
│   └── gui/             # Future GUI (placeholder)
├── utils/               # Utilities (screen, database, helpers)
├── stats/               # Statistics and analytics
├── assets/              # Game data (leagues, teams, historical data)
└── development/         # Experimental code (ignored)
```

### Architecture Benefits
- **🎯 Modular Design**: Clear separation of concerns with logical module organization
- **🔮 Future-Proof**: Easy to extend with GUI, AI, multiplayer, and advanced features
- **🛠️ Maintainable**: Well-organized code structure for team development
- **🧪 Testable**: Independent modules can be unit tested separately
- **⚡ Performance**: O(1) team lookups and optimized data structures
- **🔄 Backwards Compatible**: Legacy entry points preserved for existing users
- **📱 Scalable**: Ready for mobile apps, web interfaces, and cloud deployment

## Development Roadmap

### ✅ Phase 1: Core Infrastructure (v0.7.1) - **COMPLETED**
- [x] **Modular Architecture**: Complete codebase reorganization ✅
- [x] **Team Storage Optimization**: O(1) dictionary-based lookups ✅
- [x] **Advanced ELO System**: Smart estimation with similarity matching ✅
- [x] **Enhanced UI**: Two-step country/league selection ✅
- [x] **Performance Optimization**: Instant loading of 670+ teams ✅
- [x] **Code Cleanup**: Removed unused files and consolidated entry points ✅
- [x] **Seamless Gameplay**: Multi-season continuation without resets ✅
- [x] **Enhanced UX**: Improved help system and screen management ✅

### ✅ Phase 2: Rich Terminal UI (v0.9.0) - **COMPLETED**
- [x] **Rich Terminal UI**: Modern CLI interface with colored tables and live simulation ✅
- [x] **Dynamic Theming**: Light/dark theme support for all terminal backgrounds ✅
- [x] **Live Match Experience**: Real-time goal events and match progression ✅
- [x] **Follow Your Team Mode**: Focused viewing experience for your team ✅
- [x] **Smart Table Sizing**: Dynamic column widths based on content ✅
- [x] **Realistic Match Simulation**: Improved goal frequencies and scoring patterns ✅

### 🚧 Phase 3: Database & Performance (v0.10.x) - **NEXT**
- [ ] **SQLite Migration**: Replace shelve with proper database for concurrent access
- [ ] **Logging & Monitoring**: Comprehensive system for debugging and performance tracking
- [ ] **Match History**: Detailed match records and statistics tracking

### Phase 4: AI Integration (v0.11.x)
- [ ] **ML Match Prediction**: Train models on historical match data for outcome prediction
- [ ] **Player Performance AI**: Machine learning models for player form and development
- [ ] **Tactical Analysis**: AI-powered analysis of team formations and strategies  
- [ ] **Dynamic Difficulty**: Adaptive AI opponents that adjust to player skill level

### Phase 5: Advanced Features (v0.12.x)
- [ ] **Transfer Market AI**: Intelligent agent-based transfer negotiations and valuations
- [ ] **Injury Simulation**: Realistic injury models based on player workload and age
- [ ] **Media System**: Press conferences, fan reactions, and reputation management
- [ ] **Financial Management**: Budget constraints, sponsorships, and economic simulation

### Phase 6: Data Science & Analytics (v0.13.x)
- [ ] **Performance Analytics**: Advanced statistics dashboard with predictive insights
- [ ] **Scout Network**: AI-powered player discovery and recommendation system
- [ ] **Competition Analysis**: Deep analysis of opponent strengths and weaknesses
- [ ] **Season Simulation**: Fast-forward capabilities with statistical projections

### Phase 7: Polish & Distribution (v1.0.x)
- [ ] **Web Interface**: Optional web-based UI for enhanced user experience
- [ ] **Multi-platform Support**: Cross-platform compatibility and packaging
- [ ] **Save Game Cloud Sync**: Cloud-based save synchronization
- [ ] **Modding Support**: Plugin system for community modifications

## Known Issues  
- Schedule generation can be slow for large leagues (16+ teams)
- No progress indicators during season simulation
- Limited match detail information

## Technology Stack

### Current Implementation
- **Python 3.x**: Core application language
- **Rich**: Modern terminal UI framework with theming support
- **Pandas**: Data manipulation and analysis  
- **Termcolor**: Terminal UI coloring (legacy UI only)
- **Tabulate**: Table formatting (legacy UI only)
- **Shelve**: Current database storage (to be replaced)

### Planned AI/ML Integration
- **Scikit-learn**: Machine learning models for player development and match prediction
- **TensorFlow/PyTorch**: Deep learning for advanced tactical analysis
- **NumPy**: Numerical computing for statistical calculations
- **Matplotlib/Seaborn**: Data visualization for analytics dashboard

### Future Infrastructure
- **SQLite/PostgreSQL**: Robust database management
- **FastAPI**: Web interface backend
- **Redis**: Caching for performance optimization  





