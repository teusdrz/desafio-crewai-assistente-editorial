"""Domain services."""

from typing import Optional
from ..entities import Book, BookQuery
from ..repositories import BookRepository


class BookSearchService:
    """Service for book search operations."""
    
    def __init__(self, book_repository: BookRepository):
        self.book_repository = book_repository
    
    def find_book(self, query: BookQuery) -> Optional[Book]:
        """Find book using intelligent matching."""
        # Try exact title match first
        book = self.book_repository.find_by_title(query.title)
        if book:
            return book
        
        # Try partial matches
        partial_matches = self.book_repository.search_by_partial_title(query.title)
        if partial_matches:
            return partial_matches[0]  # Return best match
        
        return None
    
    def get_store_availability(self, book: Book, city: Optional[str] = None) -> str:
        """Get formatted store availability information."""
        if not book:
            return "Book not found"
        
        if city:
            if book.has_availability_in_city(city):
                stores = book.get_physical_stores_in_city(city)
                return f"🏪 **{book.title}** in {city}:\n• {', '.join(stores)}"
            else:
                online_stores = book.get_online_stores()
                if online_stores:
                    return f"❌ Not available in {city}, but available online:\n• {', '.join(online_stores)}"
                return f"❌ '{book.title}' not available in {city}"
        else:
            # Show all locations
            result = f"🏪 **Where to buy '{book.title}':**\n"
            for location, stores in book.availability.items():
                result += f"• {location}: {', '.join(stores)}\n"
            return result.strip()


class IntentDetectionService:
    """Service for detecting user intent."""
    
    def detect_intent(self, user_input: str) -> str:
        """Detect user intent from input."""
        text_lower = user_input.lower()
        
        # Book details intent patterns
        if any(word in text_lower for word in [
            "details", "about", "information", "info", "book", "author", 
            "synopsis", "summary", "tell me", "what is", "describe"
        ]):
            return "book_details"
        
        # Store/purchase intent patterns  
        if any(word in text_lower for word in [
            "where", "buy", "purchase", "store", "shop", "selling", 
            "available", "find", "locate"
        ]):
            return "store_info"
        
        # Support intent patterns
        if any(word in text_lower for word in [
            "help", "support", "problem", "issue", "ticket", "contact",
            "assistance", "trouble", "error"
        ]):
            return "support"
        
        return "unknown"
