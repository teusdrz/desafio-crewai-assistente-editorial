# 🤖 CrewAI Editorial Assistant

> A thoughtfully crafted editorial assistant that bridges the gap between technology and the human love for books. Built with precision, designed with care.

## Why This Project Matters ✨

In a world of endless digital noise, finding the right book shouldn't feel like searching for a needle in a haystack. This assistant was born from a simple belief: **great books deserve great discovery experiences**.

Whether you're a curious reader hunting for your next favorite story, a publisher managing complex catalogs, or someone who just needs a helping hand - we've got you covered with intelligence that actually understands what you're looking for.

## What It Does (The Human Way) 📚

**🔍 Smart Book Discovery**  
Ask naturally: "Tell me about that bee book" or "What's A Abelha about?" - no rigid commands, just conversation.

**🏪 Where to Buy Intelligence**  
"Where can I get this book in São Paulo?" We'll find every bookstore, online shop, and reading nook where it's available.

**🎫 Real Support That Cares**  
Need help? Open a ticket and know that someone will actually read it and respond. No bot hell, just human connection.

**🧠 Intent That Gets You**  
Speaks Portuguese, thinks like a human, understands context. Because good conversations shouldn't feel robotic.

## Technical Excellence (For The Geeks) ⚙️

### Architecture That Makes Sense
- **Orchestrator Agent**: The conductor of our symphony, routing your requests intelligently
- **Catalog/Commercial Agent**: Your book expert, knowing every title and where to find it  
- **Support Agent**: The caring voice when you need assistance

### CrewAI Integration Done Right
- ✅ **Perfect Tool Signatures**: `get_book_details()`, `find_stores_selling_book()`, `open_support_ticket()`
- ✅ **No Over-Engineering**: CrewAI tools without unnecessary orchestration complexity
- ✅ **Clean Data**: DD/MM/YYYY dates, "Online" availability - everything where it should be

### Built With Love For
- **Publishers** managing complex catalogs
- **Readers** discovering their next great read
- **Developers** who appreciate clean, well-documented code
- **Anyone** who believes technology should feel human

## Quick Start (Get Up & Running) 🚀

### The Simple Way
```bash
git clone https://github.com/teusdrz/desafio-crewai-assistente-editorial.git
cd desafio-crewai-assistente-editorial
python3 demo_crewai_compliant.py
```

### The Code Way
```python
from crewai_compliant_editorial_assistant import CrewAICompliantEditorialAssistant

# Start the magic
assistant = CrewAICompliantEditorialAssistant()

# Ask naturally
result = assistant.process("Tell me about A Abelha")
print(result)

# Find stores  
stores = assistant.process("Where can I buy A Cuca in São Paulo?")
print(stores)

# Get help
ticket = assistant.process("I need help with my order")
print(ticket)
```

## What's Under The Hood 🔧

### The Smart Parts
- **Intent Detection**: Understands what you really want, not just what you typed
- **Book Recognition**: Knows our catalog inside and out
- **City Intelligence**: Finds local bookstores and online alternatives
- **Ticket System**: Creates real support tickets that get real attention

### The Data
- **49 Carefully Curated Books**: From classics to contemporary gems
- **Real Store Locations**: Actual bookstores you can visit today  
- **Live Ticket System**: Your requests become actionable support items

## Files That Matter 📁

```
├── crewai_compliant_editorial_assistant.py  # The heart of our system
├── demo_crewai_compliant.py                 # See it in action
├── data/
│   ├── mock_catalog.json                    # Our book collection
│   └── mock_tickets.json                    # Your support requests
└── README.md                                # You are here
```

## Try It Out (Examples That Work) 💬

**Book Discovery**
```
"Tell me about A Abelha"
→ Complete book details with author, publisher, synopsis, and availability
```

**Store Hunting**
```
"Where can I buy A Baleia-azul in São Paulo?"
→ "🏪 A Baleia-azul in São Paulo: Blooks Livraria"
```

**Support**
```
"I need help with my order"
→ Creates ticket TCK-20250904... with all your details
```

## Behind The Scenes (Technical Specs) 🏗️

| Feature | Status | What It Means |
|---------|--------|---------------|
| Agent Architecture | ✅ | Three specialized agents working in harmony |
| Tool Signatures | ✅ | Exact API compliance for enterprise integration |
| Data Integrity | ✅ | Proper date formats, consistent structure |
| English Codebase | ✅ | International-ready, professional standards |
| Error Handling | ✅ | Graceful failures, helpful error messages |

## The Philosophy 🌟

This isn't just code - it's a bridge between the digital and physical worlds of books. Every function was written with the understanding that behind every query is a human being looking for something meaningful.

We believe:
- **Technology should feel human**
- **Good books deserve good discovery**
- **Simple questions deserve simple answers**
- **Support should actually support**

## What's Next? 🛣️

- **Enhanced Search**: Even smarter book recommendations
- **More Languages**: Because great stories transcend borders
- **Community Features**: Connect readers with similar tastes
- **Publisher Tools**: Advanced catalog management

## Made With Care By Humans ❤️

Built with dedication to the craft of both coding and storytelling. Every line of code respects the importance of the books it serves.

---

*"The best technology disappears into the background, leaving only the magic of discovery."*
