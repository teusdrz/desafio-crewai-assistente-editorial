"""
Command Line Interface for the Editorial Assistant
"""

import sys
import os
from typing import Optional

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.editorial_assistant import EditorialAssistant
from src.config import get_logger


class EditorialAssistantCLI:
    """
    Command Line Interface for the Editorial Assistant
    """
    
    def __init__(self):
        """Initialize the CLI"""
        self.logger = get_logger(__name__)
        self.assistant: Optional[EditorialAssistant] = None
        
    def initialize_assistant(self) -> bool:
        """
        Initialize the Editorial Assistant
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            print("🚀 Initializing Editorial Assistant...")
            self.assistant = EditorialAssistant()
            print("✅ Editorial Assistant ready!")
            return True
        except Exception as e:
            print(f"❌ Failed to initialize Editorial Assistant: {str(e)}")
            print("\nPlease ensure you have:")
            print("1. Set the GEMINI_API_KEY in your .env file")
            print("2. Installed all required dependencies: pip install -r requirements.txt")
            return False
    
    def display_welcome_message(self):
        """Display welcome message"""
        print("\n" + "="*60)
        print("📚 Welcome to Elo Editorial Group Assistant")
        print("="*60)
        print("\nI can help you with:")
        print("• 📖 Book details and information")
        print("• 🏪 Finding stores where books are sold")
        print("• 🎫 Opening support tickets")
        print("• 📝 General inquiries about our publishing group")
        print("\nExamples:")
        print('• "Tell me about A Abelha"')
        print('• "Where can I buy A Baleia-azul in São Paulo?"')
        print('• "I need help with a submission"')
        print("\nType 'quit' or 'exit' to end the conversation.")
        print("-"*60)
    
    def display_help(self):
        """Display help information"""
        print("\n📋 Available Commands:")
        print("• help - Show this help message")
        print("• quit/exit - Exit the assistant")
        print("• ticket <name> <email> <subject> <message> - Create a support ticket")
        print("\n📖 Book Queries:")
        print('• "Details about [book title]"')
        print('• "Tell me about [book title]"')
        print("\n🏪 Store Queries:")
        print('• "Where to buy [book title]"')
        print('• "Stores selling [book title] in [city]"')
        print("\n🎫 Support:")
        print('• "I need help with..."')
        print('• "Open a support ticket"')
    
    def parse_ticket_command(self, user_input: str) -> Optional[dict]:
        """
        Parse ticket creation command
        
        Args:
            user_input (str): User input starting with 'ticket'
            
        Returns:
            dict or None: Parsed ticket data or None if invalid
        """
        parts = user_input.split(maxsplit=4)
        if len(parts) < 5:
            return None
        
        _, name, email, subject, message = parts
        return {
            "name": name,
            "email": email, 
            "subject": subject,
            "message": message
        }
    
    def run(self):
        """Run the CLI interface"""
        if not self.initialize_assistant():
            return
        
        self.display_welcome_message()
        
        while True:
            try:
                user_input = input("\n💬 You: ").strip()
                
                if not user_input:
                    continue
                
                # Handle special commands
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("\n👋 Thank you for using Elo Editorial Assistant! Goodbye!")
                    break
                
                if user_input.lower() == 'help':
                    self.display_help()
                    continue
                
                if user_input.lower().startswith('ticket '):
                    ticket_data = self.parse_ticket_command(user_input)
                    if ticket_data:
                        print("\n🤖 Assistant: Creating your support ticket...")
                        response = self.assistant.create_support_ticket(**ticket_data)
                        print(f"\n🤖 Assistant: {response}")
                    else:
                        print("\n❌ Invalid ticket format. Use: ticket <name> <email> <subject> <message>")
                    continue
                
                # Process regular queries
                print("\n🤖 Assistant: Let me help you with that...")
                response = self.assistant.process_request(user_input)
                print(f"\n🤖 Assistant: {response}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                self.logger.error(f"CLI error: {str(e)}")
                print(f"\n❌ An error occurred: {str(e)}")


def main():
    """Main entry point"""
    cli = EditorialAssistantCLI()
    cli.run()


if __name__ == "__main__":
    main()
