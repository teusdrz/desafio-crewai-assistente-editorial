"""
CrewAI Compliant Editorial Assistant
Wrapper for the real CrewAI implementation to maintain interface compatibility
"""

from src.application.use_cases.real_crewai_editorial_assistant import RealCrewAIEditorialAssistant

class CrewAICompliantEditorialAssistant:
    """Interface wrapper for real CrewAI implementation"""
    
    def __init__(self):
        self.real_assistant = RealCrewAIEditorialAssistant()
    
    def process(self, user_input: str, session_id: str = None) -> str:
        """Process user input using real CrewAI implementation"""
        return self.real_assistant.process(user_input, session_id)
    
    def get_session_id(self, session_id: str = None) -> str:
        """Get or create session ID"""
        return self.real_assistant.get_session_id(session_id)


def main():
    """Demo of the CrewAI compliant editorial assistant"""
    assistant = CrewAICompliantEditorialAssistant()
    
    print("🎮 CREWAI COMPLIANT EDITORIAL ASSISTANT DEMO")
    print("=" * 50)
    
    # Test cases
    test_cases = [
        "Tell me about A Abelha",
        "Where can I buy A Baleia-azul in São Paulo?", 
        "I need help with my order"
    ]
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\n🔸 Test {i}: {test_input}")
        print("-" * 30)
        result = assistant.process(test_input)
        print(result)
    
    print("\n✅ Demo completed successfully!")


if __name__ == "__main__":
    main()
