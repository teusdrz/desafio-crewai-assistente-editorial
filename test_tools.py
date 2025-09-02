"""
Simple test script for the Editorial Assistant tools
"""

import unittest
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'tools'))

from editorial_tools_standalone import get_book_details, find_stores_selling_book, open_support_ticket


class TestEditorialTools(unittest.TestCase):
    """Test cases for the editorial tools"""
    
    def setUp(self):
        """Set up test data"""
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
    
    def test_get_book_details_success(self):
        """Test successful book lookup"""
        result = get_book_details("A Abelha")
        self.assertIn("title", result)
        self.assertEqual(result["title"], "A Abelha")
        self.assertIn("author", result)
        self.assertIn("synopsis", result)
    
    def test_get_book_details_partial_match(self):
        """Test partial book title match"""
        result = get_book_details("Abelha")
        self.assertIn("title", result)
        self.assertEqual(result["title"], "A Abelha")
    
    def test_get_book_details_not_found(self):
        """Test book not found scenario"""
        result = get_book_details("Nonexistent Book")
        self.assertIn("error", result)
    
    def test_find_stores_all_locations(self):
        """Test finding stores for all locations"""
        result = find_stores_selling_book("A Abelha")
        self.assertIn("book_title", result)
        self.assertIn("availability", result)
        
        availability = result["availability"]
        self.assertIn("São Paulo", availability)
        self.assertIn("Online", availability)
    
    def test_find_stores_specific_city(self):
        """Test finding stores in specific city"""
        result = find_stores_selling_book("A Abelha", "São Paulo")
        self.assertIn("book_title", result)
        self.assertIn("city", result)
        self.assertIn("stores", result)
        self.assertEqual(result["city"], "São Paulo")
    
    def test_find_stores_city_not_available(self):
        """Test finding stores in city where book is not available"""
        result = find_stores_selling_book("A Abelha", "Salvador")
        self.assertIn("book_title", result)
        self.assertIn("message", result)
        self.assertIn("online_stores", result)
    
    def test_open_support_ticket(self):
        """Test creating a support ticket"""
        result = open_support_ticket(
            name="Test User",
            email="test@example.com",
            subject="Test Subject",
            message="Test message content"
        )
        
        self.assertIn("ticket_id", result)
        self.assertIn("status", result)
        self.assertEqual(result["status"], "open")
        self.assertTrue(result["ticket_id"].startswith("TCK-"))


def run_tests():
    """Run all tests"""
    print("🧪 Running Editorial Assistant Tests")
    print("=" * 50)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEditorialTools)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("✅ All tests passed!")
    else:
        print(f"❌ {len(result.failures)} test(s) failed")
        print(f"❌ {len(result.errors)} error(s) occurred")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    run_tests()
