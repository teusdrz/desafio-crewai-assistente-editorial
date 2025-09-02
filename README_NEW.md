# Elo Editorial Group - Editorial Assistant

A sophisticated multiagent editorial assistant built with CrewAI and Google's Gemini LLM. This system helps customers find book information, locate stores, and provides customer support for the Elo Editorial Group.

## 🚀 Features

- **📖 Book Catalog Search**: Get detailed information about books including title, author, synopsis, and availability
- **🏪 Store Finder**: Find physical and online stores where books are available, with city-specific searches
- **🎫 Support Ticket System**: Create and manage customer support tickets
- **🤖 Intelligent Intent Detection**: Automatically understands user needs and routes to appropriate agents
- **🎯 Multi-Agent Architecture**: Specialized agents for different types of inquiries

## 🏗️ Architecture

### Agents
- **Orchestrator Agent**: Detects user intent and coordinates with specialized agents
- **Catalog Agent**: Handles book searches and store location queries
- **Support Agent**: Manages customer service and ticket creation

### Tools
- `get_book_details(book_title)`: Retrieves book information from catalog
- `find_stores_selling_book(book_title, city?)`: Finds stores selling specific books
- `open_support_ticket(name, email, subject, message)`: Creates support tickets

## 📦 Installation

### Prerequisites
- Python 3.8+
- Google Gemini API key (free tier available)

### Setup

1. **Clone the repository**:
```bash
git clone <repository-url>
cd desafio-crewai-assistente-editorial
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Environment configuration**:
```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:
```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash
```

### Getting a Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key to your `.env` file

## 🎮 Usage

### Command Line Interface

Run the interactive CLI:
```bash
python main.py
```

### Web API

Start the FastAPI server:
```bash
python api.py
```

The API will be available at `http://localhost:8000` with automatic documentation at `http://localhost:8000/docs`.

#### API Endpoints

- `POST /chat`: Send messages to the assistant
- `POST /ticket`: Create support tickets
- `GET /books`: List available books
- `GET /health`: Health check

## 💬 Example Interactions

### Book Information
```
User: "Tell me about A Abelha"
Assistant: "A Abelha" is a delicate work by Milton Célio de Oliveira Filho, published by Elo Editora on 15/04/2022. The book explores the universe of bees and their importance to nature. With illustrations by Olavo Costa, it's a poetic and educational journey...
```

### Store Finder
```
User: "Where can I buy A Baleia-azul in São Paulo?"
Assistant: You can find "A Baleia-azul" in São Paulo at:
- Blooks Livraria

Online options:
- Amazon.com.br
- Magazine Luiza
- Submarino
```

### Support Ticket
```
User: "I need help with a book submission"
Assistant: I understand you need support regarding book submissions. To create a support ticket, I would need your name, email, and detailed description...
```

## 📁 Project Structure

```
desafio-crewai-assistente-editorial/
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   └── editorial_agents.py      # Agent definitions
│   ├── tasks/
│   │   ├── __init__.py
│   │   └── editorial_tasks.py       # Task definitions
│   ├── tools/
│   │   ├── __init__.py
│   │   └── editorial_tools.py       # Tool implementations
│   ├── config.py                    # Configuration and LLM setup
│   ├── editorial_assistant.py       # Main assistant class
│   └── __init__.py
├── data/
│   ├── mock_catalog.json           # Book catalog data
│   └── mock_tickets.json           # Support tickets storage
├── main.py                         # CLI interface
├── api.py                          # FastAPI web interface
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment template
└── README.md                       # Documentation
```

## 🛠️ Development

### Running Tests
```bash
python -m pytest tests/
```

### Code Quality
```bash
# Format code
black src/

# Lint code
flake8 src/
```

### Adding New Books
Edit `data/mock_catalog.json` to add new books following the existing structure:

```json
{
  "title": "Book Title",
  "author": "Author Name",
  "imprint": "Publisher",
  "release_date": "DD/MM/YYYY",
  "synopsis": "Book description...",
  "availability": {
    "City Name": ["Store 1", "Store 2"],
    "Online": ["Online Store 1", "Online Store 2"]
  }
}
```

## 📊 Logging

The application logs all interactions and errors to:
- Console output (for development)
- `editorial_assistant.log` file

Log levels:
- **INFO**: User interactions, intent detection
- **ERROR**: System errors, API failures

## 🔧 Configuration

### Environment Variables
- `GEMINI_API_KEY`: Your Google Gemini API key (required)
- `GEMINI_MODEL`: Gemini model to use (default: gemini-1.5-flash)

### LLM Configuration
The assistant uses Google's Gemini LLM with the following settings:
- Model: gemini-1.5-flash (configurable)
- Temperature: 0.7 (balanced creativity/consistency)
- Max tokens: 1000

## 🚀 Deployment

### Local Development
```bash
# CLI version
python main.py

# API version
python api.py
```

### Production Deployment
For production deployment, consider:
- Using a production WSGI server (e.g., Gunicorn)
- Setting up proper logging
- Adding authentication/authorization
- Using a proper database instead of JSON files
- Adding rate limiting

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker api:app
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Troubleshooting

### Common Issues

**"GEMINI_API_KEY environment variable is required"**
- Ensure you have created a `.env` file with your API key
- Verify the API key is valid and active

**"Failed to initialize Editorial Assistant"**
- Check your internet connection
- Verify your Gemini API key has sufficient quota
- Ensure all dependencies are installed correctly

**Import errors**
- Run `pip install -r requirements.txt` again
- Check your Python version (3.8+ required)

### Getting Help

If you encounter issues:
1. Check the logs in `editorial_assistant.log`
2. Verify your environment configuration
3. Ensure all dependencies are installed
4. Check the Gemini API status

## 🎯 Future Enhancements

- Integration with real databases
- User authentication and sessions
- Advanced analytics and reporting
- Multi-language support
- Voice interface
- Integration with e-commerce platforms
- Real-time chat interface
- Machine learning for improved intent detection
