# Fantasy Football Manager - Project Structure

## Core Application Structure

```
.
├── run.py                    # Main entry point
├── requirements.txt          # Python dependencies
│
├── core/                     # Core game engine
│   ├── entities/            # Game objects
│   │   ├── team.py         # Team class with ELO ratings
│   │   └── league.py       # League management and simulation
│   ├── simulation/          # Match simulation
│   │   ├── simulator.py    # Match outcome calculation
│   │   └── scheduling.py   # Fixture generation
│   └── storage/             # Data management
│       ├── team_storage.py # Team data loading/caching
│       ├── data_updater.py # Weekly data updates
│       └── elo_estimator.py # ELO rating estimation
│
├── interfaces/              # User interfaces
│   └── cli/                # Command line interface
│       ├── rich_game_cli.py      # Main game controller (Rich UI)
│       ├── rich_interface_simple.py # Rich terminal UI components
│       └── user_input.py         # User input handling
│
├── utils/                   # Utility modules
│   ├── screen.py           # Screen management utilities
│   ├── database.py         # Legacy save file operations
│   └── shelve_db_store.py  # Game save/load system
│
├── stats/                   # Statistics module
│   └── gamestats.py        # Game statistics tracking
│
└── assets/                  # Game data
    ├── data/               # Team data by country/league
    │   └── [Country]/[League]/  # CSV files for each team
    └── raw/                # Raw data files for updates
```

## Key Features

- **Rich Terminal UI**: Beautiful colored interface with live match simulation
- **Real World Data**: 80+ leagues with 670+ teams
- **ELO Rating System**: Realistic team strength modeling
- **Save/Load System**: Persistent game state management
- **Modular Architecture**: Clean separation of concerns

## Data Flow

1. **Team Storage** loads team data from CSV files
2. **League** manages teams and season progression
3. **Simulator** calculates match outcomes using ELO ratings
4. **Rich Interface** displays everything beautifully
5. **Shelve DB** persists game state between sessions