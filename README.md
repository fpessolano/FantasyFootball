# Fantasy Football Manager v2.0

A modern, scalable football management simulation application built with clean architecture principles.

## 🚀 Project Status

This is the development branch for Fantasy Football Manager v2.0 - a complete rewrite focusing on:
- Clean architecture and SOLID principles
- Modern Python practices (type hints, async/await)
- Comprehensive testing strategy
- API-first design
- Multi-platform support (CLI, Web, Mobile-ready API)

## 🏗️ Architecture

```
src/
├── core/           # Business logic & domain models
├── api/            # REST/GraphQL API layer  
├── ui/             # User interfaces (CLI/Web/GUI)
├── data/           # Data access & repositories
└── config/         # Configuration management

tests/
├── unit/           # Unit tests
├── integration/    # Integration tests
└── e2e/            # End-to-end tests

docs/
├── api/            # API documentation
├── user/           # User guides
└── developer/      # Developer documentation
```

## 🛠️ Technology Stack

- **Language**: Python 3.11+
- **Framework**: FastAPI (API), Rich (CLI), React (Web)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Testing**: Pytest, Factory Boy, Faker
- **Code Quality**: Black, Ruff, MyPy
- **Containerization**: Docker & Docker Compose
- **CI/CD**: GitHub Actions

## 🚀 Quick Start

### Development Setup

1. Clone the repository:
```bash
git clone https://github.com/fpessolano/FantasyFootball.git
cd FantasyFootball
git checkout development
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
make dev
```

4. Run tests:
```bash
make test
```

5. Run the application:
```bash
make run
```

### Docker Setup

```bash
make docker-build
make docker-up
```

## 📋 Development Roadmap

### Phase 1: Core Architecture (Current)
- [ ] Domain models and business logic
- [ ] Repository pattern implementation
- [ ] Service layer design
- [ ] Event-driven architecture

### Phase 2: API Development
- [ ] RESTful API with FastAPI
- [ ] GraphQL endpoint
- [ ] WebSocket support for live updates
- [ ] Authentication & authorization

### Phase 3: User Interfaces
- [ ] Modern CLI with Rich
- [ ] Web UI with React
- [ ] Mobile API endpoints

### Phase 4: Advanced Features
- [ ] AI-powered match prediction
- [ ] Real-time multiplayer
- [ ] Advanced analytics dashboard
- [ ] Plugin system

## 📚 Documentation

- [API Documentation](docs/api/README.md)
- [User Guide](docs/user/README.md)
- [Developer Guide](docs/developer/README.md)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Legacy Version

The stable v1.0 version is available in the `main` branch. Legacy code from v1.0 is preserved in the `legacy/` folder for reference.

---

**Note**: This is an active development branch. For the stable version, please use the `main` branch.