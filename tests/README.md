# Fantasy Football Manager Tests

This directory contains all test scripts for the Fantasy Football Manager application.

## Test Scripts

### `test_penalty_system.py`
Comprehensive test suite for the enhanced penalty simulation system:
- Individual penalty mechanics testing
- Pressure system validation  
- Full penalty shootout simulation
- Tournament integration verification

## Running Tests

### Individual Test
```bash
cd tests
python3 test_penalty_system.py
```

### All Tests
```bash
cd tests  
python3 run_all_tests.py
```

## Test Structure

Tests are organized to validate:
1. **Core Game Mechanics** - Match engine, player management, team systems
2. **Enhanced Features** - Penalty system, tournament mode, performance tracking
3. **Data Integrity** - Save/load functionality, data migration
4. **UI Components** - Menu systems, display formatting

## Adding New Tests

When adding new test files:
1. Follow the naming convention: `test_[feature_name].py`
2. Add proper imports with parent directory path adjustment
3. Include comprehensive test documentation
4. Update this README with new test descriptions
5. Add to `run_all_tests.py` for batch execution