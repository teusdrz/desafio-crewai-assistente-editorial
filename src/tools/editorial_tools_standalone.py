"""
Editorial Tools for the CrewAI Editorial Assistant (Standalone Version)
This module contains all the tools used by the agents to interact with the catalog and ticket system.
This version can work independently without CrewAI for testing purposes.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any

def tool(name):
    """Decorator to mark functions as tools (for compatibility)"""
    def decorator(func):
        func.tool_name = name
        return func
    return decorator


@tool("get_book_details")
def get_book_details(book_title: str) -> Dict[str, Any]:
    """
    Retrieves book details from the catalog by title.
    
    Args:
        book_title (str): The title of the book to search for
        
    Returns:
        Dict containing book information: title, author, imprint, release_date, synopsis, availability
    """
    try:
        # Get the absolute path to the data directory
        # Go up from src/tools to project root, then to data
        current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        catalog_path = os.path.join(current_dir, "data", "mock_catalog.json")
        
        with open(catalog_path, 'r', encoding='utf-8') as file:
            catalog_data = json.load(file)
        
        # Search for the book (case-insensitive)
        book_title_lower = book_title.lower()
        for book in catalog_data["books"]:
            if book_title_lower in book["title"].lower():
                return {
                    "title": book["title"],
                    "author": book["author"],
                    "imprint": book["imprint"],
                    "release_date": book["release_date"],
                    "synopsis": book["synopsis"],
                    "availability": book["availability"]
                }
        
        return {"error": f"Book '{book_title}' not found in catalog"}
        
    except FileNotFoundError:
        return {"error": "Catalog file not found"}
    except json.JSONDecodeError:
        return {"error": "Error reading catalog file"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}


@tool("find_stores_selling_book")
def find_stores_selling_book(book_title: str, city: Optional[str] = None) -> Dict[str, Any]:
    """
    Finds stores selling a specific book, optionally filtered by city.
    
    Args:
        book_title (str): The title of the book to search for
        city (str, optional): The city to filter stores by
        
    Returns:
        Dict containing availability information
    """
    try:
        # Get book details first
        book_details = get_book_details(book_title)
        
        if "error" in book_details:
            return book_details
        
        availability = book_details.get("availability", {})
        
        if city:
            # Search for the city (case-insensitive)
            city_lower = city.lower()
            city_found = None
            
            for available_city in availability.keys():
                if city_lower in available_city.lower():
                    city_found = available_city
                    break
            
            if city_found:
                result = {
                    "book_title": book_details["title"],
                    "city": city_found,
                    "stores": availability[city_found]
                }
                # Always include online stores
                if "Online" in availability:
                    result["online_stores"] = availability["Online"]
                return result
            else:
                # City not found, return only online stores if available
                if "Online" in availability:
                    return {
                        "book_title": book_details["title"],
                        "message": f"Book not available in physical stores in {city}",
                        "online_stores": availability["Online"]
                    }
                else:
                    return {
                        "book_title": book_details["title"],
                        "error": f"Book not available in {city} or online"
                    }
        else:
            # Return all availability information
            return {
                "book_title": book_details["title"],
                "availability": availability
            }
            
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}


@tool("open_support_ticket")
def open_support_ticket(name: str, email: str, subject: str, message: str) -> Dict[str, Any]:
    """
    Opens a new support ticket.
    
    Args:
        name (str): Customer's name
        email (str): Customer's email
        subject (str): Ticket subject
        message (str): Ticket message/description
        
    Returns:
        Dict containing ticket information
    """
    try:
        # Get the absolute path to the data directory
        # Go up from src/tools to project root, then to data
        current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        tickets_path = os.path.join(current_dir, "data", "mock_tickets.json")
        
        # Load existing tickets
        tickets = []
        try:
            with open(tickets_path, 'r', encoding='utf-8') as file:
                tickets = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # File doesn't exist or is empty, start with empty list
            tickets = []
        
        # Generate ticket ID
        ticket_id = f"TCK-{len(tickets) + 1:04d}"
        
        # Create new ticket
        new_ticket = {
            "id": ticket_id,
            "name": name,
            "email": email,
            "subject": subject,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "status": "open"
        }
        
        # Add to tickets list
        tickets.append(new_ticket)
        
        # Save back to file
        with open(tickets_path, 'w', encoding='utf-8') as file:
            json.dump(tickets, file, indent=2, ensure_ascii=False)
        
        return {
            "ticket_id": ticket_id,
            "status": "open",
            "message": f"Support ticket {ticket_id} created successfully"
        }
        
    except Exception as e:
        return {"error": f"Failed to create ticket: {str(e)}"}
