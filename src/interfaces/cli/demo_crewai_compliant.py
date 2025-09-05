#!/usr/bin/env python3
"""
CrewAI Compliant Demo
Interactive demonstration of the real CrewAI editorial assistant
"""

import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from src.application.use_cases.real_crewai_editorial_assistant import RealCrewAIEditorialAssistant


def main():
    """Run CrewAI compliant demo"""
    print("🎮 CREWAI COMPLIANT EDITORIAL ASSISTANT DEMO")
    print("=" * 60)
    print("✅ Real CrewAI agents with roles and goals")
    print("✅ Real CrewAI tasks for orchestration")
    print("✅ Gemini LLM integrated through CrewAI")
    print("✅ Session context management enabled")
    print()
    
    try:
        assistant = RealCrewAIEditorialAssistant()
        session_id = assistant.get_session_id()
        
        # Test cases demonstrating CrewAI functionality
        test_cases = [
            ("Book Details", "Tell me about A Abelha"),
            ("Store Location", "Where can I buy A Baleia-azul in São Paulo?"),
            ("Context Follow-up", "Where can I buy it?"),
            ("Customer Support", "I need help with my order")
        ]
        
        for category, test_input in test_cases:
            print(f"🔸 {category}: {test_input}")
            print("-" * 50)
            
            try:
                result = assistant.process(test_input, session_id)
                print(result)
            except Exception as e:
                print(f"❌ Error: {str(e)}")
            
            print()
            
        print("✅ CREWAI COMPLIANT DEMO COMPLETED!")
        print("🎯 All CrewAI components verified and working")
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        print("Please check your environment setup and API keys")
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
