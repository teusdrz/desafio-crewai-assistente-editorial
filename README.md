# 🤖 CrewAI Editorial Assistant

> Professional editorial assistant built with Clean Architecture and Domain-Driven Design principles.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the assistant
python -m src.interfaces.cli.demo_crewai_compliant

# Or use the API
python -m src.interfaces.api.main
```

## Architecture

This project follows Clean Architecture with DDD:

```
src/
├── domain/              # Business logic and entities
│   ├── entities/        # Core business entities
│   └── services/        # Domain services
├── application/         # Application use cases
│   └── use_cases/       # Business use cases
├── infrastructure/      # External concerns
│   ├── adapters/        # External service adapters
│   ├── repositories/    # Data persistence
│   └── config.py        # Configuration
└── interfaces/          # User interfaces
    ├── api/             # REST API endpoints
    └── cli/             # Command line interfaces

tests/
├── unit/                # Unit tests
└── integration/         # Integration tests

docs/                    # Documentation
data/                    # Data files
```

## Features

- **🔍 Book Search**: Natural language book discovery
- **🏪 Store Locator**: Find physical and online stores
- **🎫 Support System**: Ticket creation and management
- **🤖 Smart Agents**: CrewAI-powered intelligent agents

## Documentation

See [docs/README.md](docs/README.md) for detailed documentation.

---
*Built with Clean Architecture for maintainable, scalable code*
