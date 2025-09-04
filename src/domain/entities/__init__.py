"""Domain entities for the editorial assistant system."""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum


class TicketStatus(Enum):
    """Ticket status enumeration."""
    OPEN = "open"
    CLOSED = "closed"
    IN_PROGRESS = "in_progress"


@dataclass(frozen=True)
class Book:
    """Book entity representing a catalog item."""
    
    title: str
    author: str
    imprint: str
    release_date: str
    synopsis: str
    availability: Dict[str, List[str]]
    
    def has_availability_in_city(self, city: str) -> bool:
        """Check if book is available in specific city."""
        return city in self.availability and len(self.availability[city]) > 0
    
    def get_online_stores(self) -> List[str]:
        """Get online store availability."""
        return self.availability.get("Online", [])
    
    def get_physical_stores_in_city(self, city: str) -> List[str]:
        """Get physical stores in specific city."""
        return self.availability.get(city, [])


@dataclass
class SupportTicket:
    """Support ticket entity."""
    
    id: str
    name: str
    email: str
    subject: str
    message: str
    timestamp: datetime
    status: TicketStatus = TicketStatus.OPEN
    
    def mark_as_resolved(self) -> None:
        """Mark ticket as resolved."""
        self.status = TicketStatus.CLOSED
    
    def assign_to_agent(self) -> None:
        """Assign ticket to support agent."""
        self.status = TicketStatus.IN_PROGRESS


@dataclass(frozen=True)
class BookQuery:
    """Book search query value object."""
    
    title: str
    city: Optional[str] = None
    
    def has_city_filter(self) -> bool:
        """Check if query has city filter."""
        return self.city is not None


@dataclass(frozen=True)
class AgentResponse:
    """Agent response value object."""
    
    success: bool
    message: str
    data: Optional[Dict] = None
