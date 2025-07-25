# Changelog
All notable changes to this project will be documented in this file.

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
