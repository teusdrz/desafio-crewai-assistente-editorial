#!/usr/bin/env python3
"""
Quick start example for Editorial Assistant
Simple demonstration of core features
"""

from enhanced_editorial_assistant import EnhancedEditorialAssistant


def quick_demo():
    """Quick demonstration of assistant capabilities"""
    print("📚 Editorial Assistant - Quick Start")
    print("=" * 40)
    
    # Initialize assistant
    assistant = EnhancedEditorialAssistant()
    
    # Test book search
    print("\n1. Searching for a book...")
    book_info = assistant.get_book_details("Dom Casmurro")
    print(f"Found: {book_info[:100]}...")
    
    # Test store finder
    print("\n2. Finding stores...")
    stores = assistant.find_stores("Dom Casmurro", "Rio de Janeiro")
    print(f"Stores: {stores[:100]}...")
    
    # Create support ticket
    print("\n3. Creating support ticket...")
    ticket = assistant.create_support_ticket("Need help finding a book")
    print(f"Ticket: {ticket[:100]}...")
    
    print("\n✅ Quick demo completed!")


if __name__ == "__main__":
    quick_demo()
