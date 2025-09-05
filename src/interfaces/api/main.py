#!/usr/bin/env python3
"""
Main entry point for CrewAI Editorial Assistant
Command-line interface for the real CrewAI implementation
"""

import sys
import os
from typing import Optional

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from src.application.use_cases.real_crewai_editorial_assistant import RealCrewAIEditorialAssistant


def interactive_mode():
    """Interactive chat mode"""
    print("🤖 CrewAI Editorial Assistant")
    print("=" * 40)
    print("Ask about books, stores, or get support!")
    print("Type 'quit' or 'exit' to leave\n")
    
    assistant = RealCrewAIEditorialAssistant()
    session_id = assistant.get_session_id()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
                
            if not user_input:
                continue
                
            print("🤖 Assistant:", end=" ")
            response = assistant.process(user_input, session_id)
            print(response)
            print()
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")


def single_command_mode(message: str, session_id: Optional[str] = None):
    """Process single command"""
    assistant = RealCrewAIEditorialAssistant()
    
    if not session_id:
        session_id = assistant.get_session_id()
    
    response = assistant.process(message, session_id)
    print(response)
    return session_id


def main():
    """Main entry point"""
    if len(sys.argv) == 1:
        # Interactive mode
        interactive_mode()
    elif len(sys.argv) >= 2:
        # Single command mode
        message = " ".join(sys.argv[1:])
        single_command_mode(message)
    else:
        print("Usage:")
        print("  python main.py                    # Interactive mode")
        print("  python main.py <message>          # Single command")
        sys.exit(1)


if __name__ == "__main__":
    main()
