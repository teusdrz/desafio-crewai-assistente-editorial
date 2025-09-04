# 📚 Editorial Assistant - Intelligent Book Discovery Platform

## About This Project

Welcome to the Editorial Assistant, a sophisticated multiagent system designed to revolutionize how readers discover and access books. Built with modern software architecture principles, this platform combines the power of artificial intelligence with a clean, maintainable codebase.

### What Makes This Different

This isn't just another chatbot. We've crafted an intelligent assistant that understands the nuances of book discovery, store locations, and customer support - all while maintaining professional software development standards.

## 🚀 Getting Started

Ready to explore? Here's how to get up and running:

```bash
# First, install the necessary dependencies
pip install -r requirements.txt

# Launch the assistant for an interactive demo
python3 -m src.interfaces.cli.demo_crewai_compliant

# Or start the API server for integration
python3 -m src.interfaces.api.main
```

## 💬 Usage Examples

### Book Discovery
```python
# Simple book search
assistant = CrewAICompliantEditorialAssistant()
response = assistant.process("Tell me about A Abelha")

# Expected output:
# 📚 **Book Details**
# 📖 Title: A Abelha  
# ✍️ Author: Milton Célio de Oliveira Filho
# 🏢 Publisher: Elo Editora
# 📅 Release Date: 15/04/2022
# 📝 Synopsis: Uma obra delicada que explora...
```

### Store Location with Context
```python
# Find stores (with contextual follow-up)
session_id = assistant.get_session_id()
response1 = assistant.process("Tell me about A Baleia-azul", session_id)
response2 = assistant.process("Where can I buy it?", session_id)  # Uses context!

# Or specify location directly
response = assistant.process("Where can I buy A Baleia-azul in São Paulo?")
```

### Support System
```python
# Create support ticket
response = assistant.process("I need help with my order", session_id)

# Expected output:
# 🎫 **Support Ticket Created**
# 📋 Ticket ID: TCK-20250904160834
# 👤 Name: Demo User
# ✅ Status: Open
```

### Conversational Flow
```python
# Maintaining context across interactions
session_id = assistant.get_session_id()

# User: "Tell me about A Abelha"
# Assistant: [Book details]

# User: "Where can I buy it?" ← Uses context from previous interaction
# Assistant: [Store locations for A Abelha]

# User: "I need help with ordering this book" ← Context-aware support
# Assistant: [Support ticket with book reference]
```

### API Integration
```bash
# Start the API server
python3 -m src.interfaces.api.api

# Make requests with curl
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Tell me about A Abelha", "session_id": "user123"}'

# Follow-up with context
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Where can I buy it?", "session_id": "user123"}'
```

### Command Line Demo
```bash
# Run comprehensive testing
python3 -m src.interfaces.cli.demo_crewai_compliant

# Example output:
# 🎮 CREWAI COMPLIANT EDITORIAL ASSISTANT DEMO  
# ✅ Agent structure: Orchestrator + Catalog/Commercial + Support
# ✅ Tool signatures: get_book_details(), find_stores_selling_book()
# ✅ Session context management enabled
```

## 🏛️ Architecture Philosophy

We believe great software starts with great architecture. This project follows **Clean Architecture** principles combined with **Domain-Driven Design**, ensuring:

- **Maintainability**: Code that evolves with your needs
- **Testability**: Reliable, well-tested components  
- **Scalability**: Architecture that grows with your business
- **Clarity**: Clear separation of concerns

### Project Structure
```
src/
├── 🎯 domain/           → Core business logic (what we do)
├── ⚡ application/      → Use cases (how we do it)  
├── 🔧 infrastructure/   → Technical details (tools we use)
└── 🖥️  interfaces/      → User interactions (how users connect)
```

## ✨ Core Features

### 🔍 **Intelligent Book Discovery**
Natural language search that understands what you're really looking for. No more rigid search terms - just ask naturally.

### 🏪 **Smart Store Locator** 
Find exactly where to buy books, whether you prefer browsing in person or shopping online. Location-aware recommendations included.

### 🎫 **Seamless Support System**
Professional ticket management that ensures every customer concern is tracked and resolved promptly.

### 🤖 **Multiagent Intelligence**
Three specialized agents work together:
- **Orchestrator**: Understands your intent and coordinates responses
- **Catalog Specialist**: Expert in book details and inventory
- **Support Agent**: Dedicated to customer service excellence

## 🛠️ Technical Excellence

### Modern Standards
- **Clean Architecture**: Sustainable, professional codebase
- **Domain-Driven Design**: Business logic that makes sense
- **Session Management**: Conversational context across interactions
- **Comprehensive Logging**: Production-ready monitoring and debugging
- **Comprehensive Testing**: Reliable, well-tested functionality
- **API-First Design**: Easy integration with existing systems

### Quality Assurance
Every component is designed with reliability in mind:
- 100% specification compliance testing
- Session-based context management for natural conversations
- Professional error handling with detailed logging
- Performance monitoring and optimization
- Comprehensive logging and monitoring
- Production-ready deployment patterns

### Advanced Features
- **Context Awareness**: Remember previous interactions within sessions
- **Intelligent Routing**: Context-aware intent detection
- **Performance Monitoring**: Built-in performance tracking and logging
- **Session Management**: Automatic cleanup and timeout handling
- **Error Recovery**: Graceful handling of edge cases

## 📖 Documentation & Learning

Explore deeper:
- **[Complete Documentation](docs/README.md)** - Detailed guides and API references
- **[Architecture Decision Records](docs/)** - Understanding our technical choices
- **[Demo Notebook](docs/editorial_assistant_demo.ipynb)** - Interactive examples

## 🎯 Perfect For

- **Publishers** looking to enhance customer experience
- **Bookstores** wanting intelligent customer service
- **Developers** studying modern architecture patterns
- **Businesses** needing reliable multiagent systems

## 💡 Philosophy

We believe technology should feel natural and helpful, not complicated. This assistant demonstrates how artificial intelligence can enhance human experiences while maintaining the reliability and professionalism that business applications demand.

---

*Crafted with attention to detail, built for the real world.*
