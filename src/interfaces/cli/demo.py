#!/usr/bin/env python3
"""
Demo script to test the editorial tools functionality
This script demonstrates the tools working independently without CrewAI dependencies
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import directly from the standalone tools file
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'tools'))
from editorial_tools_standalone import get_book_details, find_stores_selling_book, open_support_ticket


def demo_book_search():
    """Demonstrate book search functionality"""
    print("🔍 BOOK SEARCH DEMO")
    print("="*50)
    
    # Test book that exists
    print("\n1. Searching for 'A Abelha':")
    result = get_book_details("A Abelha")
    print(f"   Result: {result}")
    
    # Test partial match
    print("\n2. Searching for 'Abelha' (partial match):")
    result = get_book_details("Abelha")
    print(f"   Result: {result}")
    
    # Test book that doesn't exist
    print("\n3. Searching for 'Nonexistent Book':")
    result = get_book_details("Nonexistent Book")
    print(f"   Result: {result}")


def demo_store_finder():
    """Demonstrate store finder functionality"""
    print("\n\n🏪 STORE FINDER DEMO")
    print("="*50)
    
    # Test finding stores without city
    print("\n1. Finding stores for 'A Abelha' (all locations):")
    result = find_stores_selling_book("A Abelha")
    print(f"   Result: {result}")
    
    # Test finding stores with specific city
    print("\n2. Finding stores for 'A Abelha' in São Paulo:")
    result = find_stores_selling_book("A Abelha", "São Paulo")
    print(f"   Result: {result}")
    
    # Test city that doesn't have the book
    print("\n3. Finding stores for 'A Abelha' in Salvador:")
    result = find_stores_selling_book("A Abelha", "Salvador")
    print(f"   Result: {result}")
    
    # Test online-only book
    print("\n4. Finding stores for 'A Borboleta' (online only):")
    result = find_stores_selling_book("A Borboleta")
    print(f"   Result: {result}")


def demo_support_ticket():
    """Demonstrate support ticket functionality"""
    print("\n\n🎫 SUPPORT TICKET DEMO")
    print("="*50)
    
    # Create a test ticket
    print("\n1. Creating a support ticket:")
    result = open_support_ticket(
        name="John Doe",
        email="john.doe@example.com",
        subject="Book submission inquiry",
        message="I would like to know more about the submission process for children's books."
    )
    print(f"   Result: {result}")
    
    # Create another ticket
    print("\n2. Creating another support ticket:")
    result = open_support_ticket(
        name="Jane Smith",
        email="jane.smith@example.com",
        subject="Store availability question",
        message="Why is my favorite book not available in my city?"
    )
    print(f"   Result: {result}")


def main():
    """Run all demos"""
    print("📚 EDITORIAL ASSISTANT TOOLS DEMO")
    print("="*60)
    print("This demo shows the core functionality of the editorial tools")
    print("without requiring CrewAI or Gemini API dependencies.")
    
    try:
        demo_book_search()
        demo_store_finder()
        demo_support_ticket()
        
        print("\n\n✅ Demo completed successfully!")
        print("\nTo see the created tickets, check: data/mock_tickets.json")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {str(e)}")
        print("Please ensure you're running from the project root directory.")


if __name__ == "__main__":
    main()
