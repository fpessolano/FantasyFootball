# Fantasy Football Manager - Test Suite Documentation

## Overview

The Fantasy Football Manager includes a comprehensive automated test suite that validates core functionality, data integrity, and system reliability. This document describes the test coverage and how to run the tests.

## Test Coverage

### Comprehensive Test Suite (9 Tests)

Run the complete test suite with:
```bash
python tests/run_all_tests.py
```

**Core Functionality Tests:**
1. **Core Module Imports** - Verifies all core modules can be imported
2. **Team Creation** - Tests team object creation and basic functionality  
3. **League Creation** - Tests league object creation and team management
4. **Match Simulation** - Tests match simulation and goal scoring mechanics
5. **Save/Load System** - Tests game save and load functionality
6. **Goal Averages** - Tests that goal averages are in target range (2.08-2.6)
7. **Team Storage** - Tests team data loading and storage system
8. **User Preferences** - Tests user preference saving and loading
9. **Color Schemes** - Tests Rich UI color scheme functionality

### Individual Test Files

### `test_save_load.py`
Comprehensive test for the save/load system:
- Tests the JSON-based save system
- Validates data integrity
- Tests metadata handling
- Tests error scenarios

### `test_game_save_load.py`
Game-specific save/load test:
- Tests actual game save/load process
- Tests with real League and Team objects
- Tests error handling
- Tests the SaveGameManager directly

### `test_goal_average.py`
Interactive and automated goal average testing:
- Verifies 2.08-2.6 goals per match target
- Statistical analysis of goal distributions
- Can be run interactively or automated

## Running Tests

```bash
# Run complete test suite (recommended)
python tests/run_all_tests.py

# Run individual tests
python tests/test_save_load.py
python tests/test_game_save_load.py
python tests/test_goal_average.py --auto
```

## Quality Standards

- **Target Success Rate**: 100%
- **Performance**: All tests complete in under 60 seconds
- **Coverage**: Core functionality, edge cases, error handling
- **Reliability**: Consistent results across different environments

## Expected Results

All 9 tests should pass with 100% success rate:
✅ Core Module Imports
✅ Team Creation  
✅ League Creation
✅ Match Simulation
✅ Save/Load System
✅ Goal Averages
✅ Team Storage
✅ User Preferences
✅ Color Schemes

Any test failures indicate potential issues that should be investigated.

## Save System Features

The save system (`utils/save_system.py`) provides:

### ✅ Key Features:
- **JSON-based**: Portable and human-readable format
- **Atomic saves**: Prevents corruption with temporary files
- **Rich metadata**: Timestamps, descriptions, version info
- **Better error handling**: Graceful failure recovery
- **Context manager**: Proper resource cleanup
- **Cross-platform**: Works on all operating systems

### 🔧 Technical Features:
- Atomic saves using temporary files
- Automatic directory creation
- Save metadata with timestamps and descriptions
- Circular reference detection
- Beautiful save listing with metadata display

### 📁 Save File Structure:
```json
{
  "metadata": {
    "save_name": "my_save",
    "timestamp": "2025-07-27T00:27:32.801156",
    "description": "Arsenal - Match Day 15",
    "version": "0.9.0"
  },
  "game_state": {
    "league_name": "Premier League",
    "teams": [...],
    "my_team_index": 0,
    "current_match_day": 15
  }
}
```

### 💾 Save Location:
- Saves are stored in `saves_json/[user_id]/` directory
- Each save is a separate JSON file
- Metadata file tracks user information