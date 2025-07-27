# Fantasy Football Manager v2.0 - Development Guide

## Overview

This is a complete rewrite of Fantasy Football Manager, focusing on modern architecture and best practices.

## Architecture Principles

1. **Clean Architecture** - Separation of concerns with clear boundaries
2. **Domain-Driven Design** - Business logic at the core
3. **SOLID Principles** - Maintainable and extensible code
4. **Test-Driven Development** - Comprehensive test coverage

## Getting Started

```bash
# Clone and setup
git clone https://github.com/fpessolano/FantasyFootball.git
cd FantasyFootball
git checkout development

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e ".[dev]"
```

## Development Workflow

1. Write tests first (TDD)
2. Implement features
3. Ensure all tests pass
4. Format code with Black
5. Check with Ruff and MyPy
6. Submit PR

## Project Structure

- `src/core/` - Domain models and business logic (no external dependencies)
- `src/data/` - Data access layer (repositories, database)
- `src/api/` - External API layer (REST, GraphQL)
- `src/ui/` - User interfaces (CLI, Web)
- `src/config/` - Configuration management

## Current Status

Starting fresh with v2.0 development. No legacy code dependencies.