"""Domain repository interfaces."""

from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities import Book, SupportTicket


class BookRepository(ABC):
    """Book repository interface."""
    
    @abstractmethod
    def find_by_title(self, title: str) -> Optional[Book]:
        """Find book by title."""
        pass
    
    @abstractmethod
    def find_all(self) -> List[Book]:
        """Find all books."""
        pass
    
    @abstractmethod
    def search_by_partial_title(self, partial_title: str) -> List[Book]:
        """Search books by partial title match."""
        pass


class TicketRepository(ABC):
    """Ticket repository interface."""
    
    @abstractmethod
    def save(self, ticket: SupportTicket) -> None:
        """Save support ticket."""
        pass
    
    @abstractmethod
    def find_by_id(self, ticket_id: str) -> Optional[SupportTicket]:
        """Find ticket by ID."""
        pass
    
    @abstractmethod
    def find_all(self) -> List[SupportTicket]:
        """Find all tickets."""
        pass
