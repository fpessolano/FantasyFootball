# Changelog
All notable changes to this project will be documented in this file.

## [2.0.2] - 2025-07-29

### 🥅 Enhanced Penalty System
- **Individual Player Mechanics**: Penalty takers selected based on shooting + composure + pressure handling
- **Realistic Goalkeeper vs Penalty Taker**: Detailed skill calculations with saves vs misses distinction
- **Dynamic Success Rates**: 40-95% based on skill difference with pressure factors
- **Situational Pressure**: Sudden death penalties 30% harder, late penalties 10% harder
- **Detailed Event Descriptions**: "brilliant save", "blazes over bar", "hits the post" with player names

### 🧪 Test Infrastructure
- **Comprehensive Test Suite**: `test_penalty_system.py` with 100% pass rate
- **Organized Test Structure**: All tests moved to dedicated `tests/` folder
- **Batch Test Runner**: `run_all_tests.py` for running all test scripts
- **Test Documentation**: Complete test README with usage instructions

### 🔧 Code Organization
- **Project Restructuring**: Clean separation of test and production code
- **Path Corrections**: Proper import paths for test scripts
- **Version Consistency**: Unified version numbering across all files

### 🏆 Tournament Enhancements
- **Enhanced Match Display**: Improved tournament match result presentation
- **Penalty Integration**: Tournament penalty shootouts now use enhanced system
- **Event Attribution**: Clear indication of which team events apply to

## [1.0.0] - 2025-07-27

### 🚀 Production Release - Major Milestone
- **Production Ready**: First stable major release with comprehensive features
- **Quality Assurance**: All critical bugs resolved, stable codebase
- **Complete Feature Set**: Full football management experience ready for public use

### 🔄 User Experience Improvements
- **Graceful Exit Handling**: Ctrl+C signal handling throughout the application
  - Immediate clean exit with proper Rich UI messaging
  - Auto-save functionality when exiting during gameplay
  - No more RuntimeError exceptions during signal handling
- **Enhanced Navigation**: Back options added to all menu systems
  - Game type selection now includes back option
  - Consistent navigation flow throughout the application
  - Better user control and menu traversal

### 🧹 Code Quality & Maintenance
- **Code Cleanup**: Removed debug print statements and comments
  - Cleaned up TODO comments and development artifacts
  - Removed unused debug prints from core modules
  - Streamlined codebase for production deployment
- **Performance Optimization**: Improved error handling and edge cases
  - Better exception handling without exposing debug information
  - Cleaner error recovery and graceful degradation
  - Optimized signal handling to avoid readline conflicts

### 🔧 Technical Improvements
- **Signal Handling**: Robust Ctrl+C handling implementation
  - Fixed readline conflicts during input operations
  - Implemented per-module signal handlers for consistent behavior
  - Auto-save integration with exit handling
- **Version Management**: Updated to semantic versioning 1.0.0
  - Consistent version numbering across all modules
  - Updated documentation and roadmap for future releases

## [0.9.0] - 2025-01-25

### 🎨 Rich Terminal UI - Major Interface Overhaul
- **Rich Terminal Framework**: Complete migration to Rich library for beautiful colored interface
- **Dynamic Light/Dark Theming**: Automatic color adaptation based on terminal background
  - Light theme: Black text on white backgrounds with blue highlights
  - Dark theme: White/cyan text on black backgrounds with proper contrast
- **Theme-Aware Components**: All interface elements (menus, help, tables) use dynamic colors

### ⚽ Live Match Experience
- **Real-time Match Simulation**: Matches progress minute-by-minute with live updates
- **Global Match Clock**: Single time display (🕐 Kick-off → 67' → Full-time) replacing individual columns
- **Live Goal Events**: Goals appear in real-time with minute notifications
- **Simultaneous Matches**: All matches progress together on same timeline

### 👁️ Follow Your Team Mode
- **Focused Team View**: Dedicated interface highlighting your team prominently
- **Secondary Matches Table**: Other matches shown in dimmed, separate table for context
- **Enhanced Team Visibility**: Your team uses high-contrast colors (white on red/black on yellow)

### 📏 Smart Interface Design
- **Dynamic Table Sizing**: Tables automatically resize based on longest team names in league
- **Clean Layout**: Removed time columns for more space, added global clock
- **Optimized Spacing**: Perfect fit for any league (EPL, Bundesliga, etc.)

### 🎲 Realistic Match Simulation
- **Improved Goal Frequencies**: More authentic scoring patterns (1-0, 2-1, 1-1 common)
- **Reduced High-Scoring Games**: Fewer unrealistic 4-3, 5-2 scorelines  
- **Enhanced Draw System**: More 0-0 and 1-1 draws matching real football
- **Capped Scoring**: Maximum 5 goals per team (down from 7) for realism

### 🔧 Technical Improvements
- **Comprehensive Bug Fixes**: Resolved all NoneType errors and match simulation crashes
- **Theme System Architecture**: Robust color management supporting any terminal
- **Error Handling**: Graceful degradation for invalid teams or missing data
- **Performance Optimization**: Efficient real-time updates and table rendering

### 🎯 User Experience Enhancements
- **Intuitive Navigation**: Clear visual hierarchy with focused and secondary content
- **Consistent Theming**: Same color scheme across all interface components
- **Responsive Design**: Interface adapts to different terminal sizes and backgrounds
- **Professional Appearance**: Modern CLI interface rivaling commercial applications

### 📱 Cross-Platform Compatibility
- **Universal Terminal Support**: Works on light and dark terminals across all platforms
- **macOS Terminal**: Perfect for both light and dark themes
- **Windows Terminal**: Full color support with theme detection
- **Linux Terminals**: Compatible with all major terminal emulators

## [0.7.1] - 2025-01-25

### Added
- Enhanced help system with screen clearing and title screen redisplay
- Continuous gameplay loop supporting multiple consecutive seasons
- Clean league selection interface with automatic screen clearing

### Fixed
- **MAJOR**: Fixed season progression bug where game would reset to main menu after season end
- **MAJOR**: Fixed team storage initialization preventing two-step league selection
- League selection now properly displays improved country → league interface
- Help command now clears screen, shows help, then returns to title screen
- Game now continues seamlessly through multiple seasons without resetting

### Technical Improvements
- Added `_play_game_loop()` method for continuous multi-season gameplay
- Fixed path resolution in team storage initialization
- Enhanced FFM constructor to support version display in help system
- Improved user experience with proper screen management

## [0.7.0] - 2025-01-25

### Added
- **Modular Architecture**: Complete codebase reorganization into logical modules
  - `core/entities/` - Game objects (Team, League)
  - `core/simulation/` - Match simulation and scheduling
  - `core/storage/` - Data management and ELO estimation
  - `interfaces/cli/` - Command line interface
  - `utils/` - Utilities and helpers
  - `stats/` - Statistics and analytics
- **Advanced ELO System**: Sophisticated team rating management
  - O(1) team lookups with optimized storage
  - Smart ELO estimation for teams with missing data
  - Multi-metric similarity analysis for accurate estimates
  - Bell curve distribution for realistic ELO conversion
- **Enhanced User Interface**: Streamlined league selection system
  - Two-step selection process (country → league)
  - Country grouping with clean 3-column display
  - Improved alignment and consistent formatting
- **Smart Data Management**: Automatic weekly data updates
  - Fallback systems for missing team data
  - Conservative ELO estimation with confidence scoring
  - Robust error handling and data validation

### Changed
- **MAJOR**: Complete modular code reorganization for maintainability
- **MAJOR**: Replaced linear team searches with O(1) dictionary lookups
- **MAJOR**: Enhanced league selection from single list to hierarchical country/league system
- Consolidated entry points from 3 files to 2 streamlined launchers
- Removed ELO estimation warnings for cleaner user experience
- Fixed alignment issues in league selection interface

### Removed
- **Dead Code Cleanup**: Removed unused files and modules
  - `ffmCLI.py` - Redundant CLI interface (consolidated into main.py)
  - `interfaces/gui/` - Empty placeholder module
  - `utils/helpers.py` - Unused utility functions
  - `utils/stack.py` - Unused Stack class
- Legacy import dependencies and redundant code paths

### Fixed
- Import path consistency across all modules
- Asset path resolution for modular structure
- ELO calculation edge cases and validation
- Country/league text alignment in selection interface
- Syntax warnings in ASCII art displays

### Technical Improvements
- **Performance**: O(n) → O(1) team lookup optimization
- **Architecture**: Clear separation of concerns with modular design
- **Maintainability**: Well-organized code structure for future development
- **Scalability**: Ready for GUI, AI, and multiplayer features
- **Testing**: Modules can be tested independently

## [0.6.0] - 2025-01-25
#### Added
- Input validation helper function in `support/helpers.py` for consistent user input handling
- Enhanced screen utilities with improved cross-platform clearing and colored message support
- Comprehensive error handling throughout the application
- Enhanced match simulation engine with realistic outcome probabilities

#### Changed
- **MAJOR**: Completely redesigned match result calculation algorithm
  - Now uses ELO-based probabilities for more realistic outcomes
  - Calculates proper draw probabilities based on team strength similarity
  - Implements realistic score distributions (1-0, 2-1, etc.)
  - Caps maximum goals at 7 for realism
- Replaced all bare `except:` clauses with specific exception handling
- Improved screen clearing with fallback mechanisms
- Enhanced table row highlighting with better color support

#### Fixed
- JSON parsing errors now properly handled in save/load operations
- ValueError exceptions in user input validation
- Cross-platform terminal clearing issues
- Team definition loading errors with descriptive messages

#### Development
- Moved all experimental files to `development/` folder
- Added comprehensive code analysis and improvement recommendations in `IMPROVEMENTS.md`

## [0.5.0]
#### Change 
 - Removed REPLIT support

## [0.4.1]
#### Change 
 - Extract user name from replit
 - Limit to one league temporarily for development (to be started)

#### Add
 - Proper title screen
 - Add players with stats (in progress)
 - Add new similation mechanism using real-world form (ELO), FIFA-like players stats and a new simulation engine  (to be done)
   
## [0.3.1]
#### Change 
 - clean code 
 - improved commenting
 - several bugs fixed
 - improved CLI interface  

#### Add
 - replit compatible
 - automatic download of new stats every week (modifiable)
 - allow selection of a team and introduce focus mode
 
## [0.2.1]
#### Change 
 - fixed bug that does not allow loading saved games with even number of teams  
 - fixed but altering stars for promoted teams  
 - fixed bug that causes custom teams stars not to propagate correctly to the next season  

## [0.2.0]
#### Change    
 - recoded using classes  
 - change of savedata format  
 - scheduling is now based on Berger Tables instead of an iterative discovery algorithm  
 - improved match simulation  
 - added star rating  

## [0.1.0]
#### Add  
 - first functional release   
