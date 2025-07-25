# Changelog
All notable changes to this project will be documented in this file.

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
