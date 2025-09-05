# CrewAI Editorial Assistant

## Overview

A multiagent system built with CrewAI framework for book discovery, store location, and customer support. Features authentic CrewAI agents with task orchestration and session management capabilities.

## Architecture

### Agents
- **Orchestrator Agent**: Analyzes user requests and delegates tasks
- **Catalog Specialist**: Handles book details and store information  
- **Customer Support**: Creates and manages support tickets

### Tools
- `get_book_details(book_title: string)` - Retrieves book information
- `find_stores_selling_book(book_title: string, city?: string)` - Finds store locations
- `open_support_ticket(name, email, subject, message)` - Creates support tickets

### Data Sources
- `data/mock_catalog.json` - Book catalog with DD/MM/YYYY dates
- `data/mock_tickets.json` - Support ticket storage

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Add your GEMINI_API_KEY

# Run demo
python3 -m src.interfaces.cli.demo_crewai_compliant

# Or start API server
python3 -m src.interfaces.api.api
```

## Usage Examples

### Basic Usage
```python
from src.application.use_cases.real_crewai_editorial_assistant import RealCrewAIEditorialAssistant

assistant = RealCrewAIEditorialAssistant()
response = assistant.process("Tell me about Dom Casmurro")
```

### Session Management
```python
# Create session for context awareness
session_id = assistant.get_session_id()

# First interaction
response1 = assistant.process("Tell me about A Baleia-azul", session_id)

# Context-aware follow-up
response2 = assistant.process("Where can I buy it?", session_id)
```

### API Usage
```bash
# Start server
python3 -m src.interfaces.api.api

# Make request
curl -X POST "http://localhost:8000/chat" 
     -H "Content-Type: application/json" 
     -d '{"message": "Tell me about A Abelha", "session_id": "user123"}'
```

## Project Structure

```
src/
├── application/use_cases/
│   ├── real_crewai_editorial_assistant.py    # Main CrewAI implementation
│   └── crewai_compliant_editorial_assistant.py
├── infrastructure/
│   └── logging_config.py
└── interfaces/
    ├── cli/
    │   ├── demo_crewai_compliant.py
    │   └── main.py
    └── api/
        └── api.py
data/
├── mock_catalog.json
└── mock_tickets.json
```

## Implementation Details

### CrewAI Integration
```python
# Real CrewAI agents with defined roles
self.orchestrator_agent = Agent(
    role="Intent Orchestrator",
    goal="Analyze user requests and coordinate with specialists",
    backstory="Intelligent request coordinator...",
    llm=self.llm,
    allow_delegation=True
)

# Task execution with CrewAI
crew = Crew(
    agents=[self.orchestrator_agent, self.catalog_agent, self.support_agent],
    tasks=tasks,
    process=Process.sequential
)
result = crew.kickoff()
```

### Session Context
- Conversation history preservation
- Context-aware intent detection
- Automatic session cleanup with timeout

## Requirements

### Dependencies
```
crewai>=0.36.0
crewai-tools>=0.4.0
langchain-google-genai>=1.0.0
google-generativeai>=0.7.0
fastapi>=0.104.0
uvicorn>=0.24.0
```

### Environment Variables
```bash
GEMINI_API_KEY=your_api_key_here
LOG_LEVEL=INFO
SESSION_TIMEOUT_MINUTES=30
```

## Testing

Run the interactive demo to test all features:

```bash
python3 -m src.interfaces.cli.demo_crewai_compliant
```

Test cases include:
- Book detail retrieval
- Store location finding
- Support ticket creation
- Session context preservation

## Features

- Real CrewAI framework implementation
- Context-aware conversations
- Professional error handling
- Structured logging
- Multiple interfaces (CLI, API)
- Session management with timeout
- Demo mode fallback for API-free operation
