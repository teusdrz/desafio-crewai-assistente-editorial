# Session Management

This module provides session management capabilities for the Editorial Assistant, enabling contextual conversations.

## Key Components

### SessionContext
- Maintains conversation history
- Tracks current book and city context
- Handles session expiration

### SessionManager
- Creates and manages multiple sessions
- Automatic cleanup of expired sessions
- Thread-safe operations

## Usage

```python
from src.application.use_cases.crewai_compliant_editorial_assistant import CrewAICompliantEditorialAssistant

assistant = CrewAICompliantEditorialAssistant()
session_id = assistant.get_session_id()

# Contextual conversation
response1 = assistant.process("Tell me about A Abelha", session_id)
response2 = assistant.process("Where can I buy it?", session_id)  # Uses context
```
