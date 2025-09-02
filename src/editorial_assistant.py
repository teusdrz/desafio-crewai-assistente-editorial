"""
Main Editorial Assistant Class
This module contains the main assistant that coordinates all agents and tasks.
"""

import re
from typing import Dict, Any, Optional
from crewai import Crew
from .config import Config, setup_logging, get_logger
from .agents import create_orchestrator_agent, create_catalog_agent, create_support_agent
from .tasks import (
    create_book_details_task,
    create_store_finder_task, 
    create_support_ticket_task,
    create_intent_detection_task
)


class EditorialAssistant:
    """
    Main Editorial Assistant class that coordinates agents and tasks using CrewAI
    """
    
    def __init__(self):
        """Initialize the Editorial Assistant"""
        setup_logging()
        self.logger = get_logger(__name__)
        
        try:
            self.config = Config()
            self.llm = self.config.create_llm()
            
            # Create agents
            self.orchestrator_agent = create_orchestrator_agent(self.llm)
            self.catalog_agent = create_catalog_agent(self.llm)
            self.support_agent = create_support_agent(self.llm)
            
            self.logger.info("Editorial Assistant initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Editorial Assistant: {str(e)}")
            raise
    
    def detect_intent(self, user_input: str) -> Dict[str, Any]:
        """
        Detect user intent from input
        
        Args:
            user_input (str): User's input text
            
        Returns:
            Dict containing intent and extracted information
        """
        user_input_lower = user_input.lower()
        
        # Intent patterns
        book_patterns = [
            r"(about|details|information|tell me about|what is)\s+['\"]?([^'\"]+)['\"]?",
            r"book\s+['\"]?([^'\"]+)['\"]?",
            r"['\"]([^'\"]+)['\"]",
            r"quero saber sobre\s+['\"]?([^'\"]+)['\"]?",
        ]
        
        store_patterns = [
            r"(where|onde|buy|purchase|comprar)\s+.*['\"]?([^'\"]+)['\"]?",
            r"stores?.*['\"]?([^'\"]+)['\"]?",
            r"lojas?.*['\"]?([^'\"]+)['\"]?",
        ]
        
        support_patterns = [
            r"(ticket|support|help|suporte|ajuda|submission|submissão)",
            r"(open|create|abrir|criar)\s+(ticket|suporte)",
        ]
        
        # Check for book details intent
        for pattern in book_patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                book_title = match.group(-1).strip()
                return {
                    "intent": "book_details",
                    "book_title": book_title
                }
        
        # Check for store finder intent
        for pattern in store_patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                book_title = match.group(-1).strip()
                
                # Check for city mentions
                city_patterns = [
                    r"(in|em|na|no)\s+([a-zA-ZÀ-ÿ\s]+)",
                    r"(são paulo|rio de janeiro|salvador|curitiba|belo horizonte|porto alegre|manaus)"
                ]
                
                city = None
                for city_pattern in city_patterns:
                    city_match = re.search(city_pattern, user_input, re.IGNORECASE)
                    if city_match:
                        city = city_match.group(-1).strip()
                        break
                
                return {
                    "intent": "store_finder",
                    "book_title": book_title,
                    "city": city
                }
        
        # Check for support intent
        for pattern in support_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                return {
                    "intent": "support",
                    "message": user_input
                }
        
        # Default to general inquiry
        return {
            "intent": "general",
            "message": user_input
        }
    
    def process_request(self, user_input: str) -> str:
        """
        Process user request and return response
        
        Args:
            user_input (str): User's input text
            
        Returns:
            str: Response from the assistant
        """
        self.logger.info(f"Processing request: {user_input}")
        
        try:
            # Detect intent
            intent_data = self.detect_intent(user_input)
            intent = intent_data["intent"]
            
            self.logger.info(f"Detected intent: {intent}")
            
            if intent == "book_details":
                return self._handle_book_details(intent_data)
            elif intent == "store_finder":
                return self._handle_store_finder(intent_data)
            elif intent == "support":
                return self._handle_support_request(intent_data)
            else:
                return self._handle_general_inquiry(intent_data)
                
        except Exception as e:
            self.logger.error(f"Error processing request: {str(e)}")
            return "I apologize, but I encountered an error while processing your request. Please try again."
    
    def _handle_book_details(self, intent_data: Dict[str, Any]) -> str:
        """Handle book details requests"""
        try:
            book_title = intent_data["book_title"]
            
            task = create_book_details_task(self.catalog_agent, book_title)
            crew = Crew(
                agents=[self.catalog_agent],
                tasks=[task],
                verbose=False,
                memory=False
            )
            
            result = crew.kickoff()
            return str(result)
        except Exception as e:
            self.logger.error(f"Error in book details handler: {str(e)}")
            return f"Desculpe, encontrei um problema ao buscar informações sobre '{intent_data.get('book_title', 'o livro')}'. Tente novamente."
    
    def _handle_store_finder(self, intent_data: Dict[str, Any]) -> str:
        """Handle store finder requests"""
        try:
            book_title = intent_data["book_title"]
            city = intent_data.get("city")
            
            task = create_store_finder_task(self.catalog_agent, book_title, city)
            crew = Crew(
                agents=[self.catalog_agent],
                tasks=[task],
                verbose=False,
                memory=False
            )
            
            result = crew.kickoff()
            return str(result)
        except Exception as e:
            self.logger.error(f"Error in store finder handler: {str(e)}")
            return f"Desculpe, encontrei um problema ao buscar lojas para '{intent_data.get('book_title', 'o livro')}'. Tente novamente."
        
        result = crew.kickoff()
        return str(result)
    
    def _handle_support_request(self, intent_data: Dict[str, Any]) -> str:
        """Handle support requests"""
        message = intent_data["message"]
        
        # For demo purposes, create a generic support response
        # In a real application, you would collect user details interactively
        return self._create_demo_support_response(message)
    
    def _handle_general_inquiry(self, intent_data: Dict[str, Any]) -> str:
        """Handle general inquiries"""
        try:
            user_input = intent_data["message"]
            
            task = create_intent_detection_task(self.orchestrator_agent, user_input)
            crew = Crew(
                agents=[self.orchestrator_agent],
                tasks=[task],
                verbose=False,
                memory=False
            )
            
            result = crew.kickoff()
            return str(result)
        except Exception as e:
            self.logger.error(f"Error in general inquiry handler: {str(e)}")
            return f"Desculpe, não consegui processar sua consulta no momento. Como posso ajudá-lo de forma específica com livros, lojas ou suporte?"
    
    def _create_demo_support_response(self, message: str) -> str:
        """Create a demo support response"""
        return f"""I understand you need support regarding: {message}

To create a support ticket, I would need the following information:
- Your full name
- Your email address
- A detailed description of your inquiry

For demonstration purposes, here's how the ticket creation process works.
In a full implementation, this would be handled interactively.

Would you like me to help you with:
1. Information about book submissions
2. General customer service questions
3. Author relations inquiries
4. Technical support

Please let me know how I can best assist you!"""

    def create_support_ticket(self, name: str, email: str, subject: str, message: str) -> str:
        """
        Create a support ticket with provided details
        
        Args:
            name (str): Customer name
            email (str): Customer email
            subject (str): Ticket subject
            message (str): Ticket message
            
        Returns:
            str: Ticket creation confirmation
        """
        try:
            task = create_support_ticket_task(self.support_agent, name, email, subject, message)
            crew = Crew(
                agents=[self.support_agent],
                tasks=[task],
                verbose=True
            )
            
            result = crew.kickoff()
            return str(result)
            
        except Exception as e:
            self.logger.error(f"Error creating support ticket: {str(e)}")
            return "I apologize, but I encountered an error while creating your support ticket. Please try again."
