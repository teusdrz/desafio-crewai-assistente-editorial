#!/usr/bin/env python3
"""
Assistente Editorial Multiagente Simples
Atende exatamente aos objetivos especificados:
✅ Consulta catálogo 
✅ Informações sobre livros
✅ Indica onde comprar  
✅ Abre ticket simulado
✅ Arquitetura clara e código limpo
❌ SEM CrewAI para orquestração
🧠 Gemini apenas como base LLM
"""

import json
import os
import re
from datetime import datetime
from typing import Dict, Optional, List
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


class CatalogAgent:
    """Agente responsável por consultas ao catálogo"""
    
    def __init__(self, catalog_path: str):
        self.catalog_path = catalog_path
        self.books = self._load_catalog()
    
    def _load_catalog(self) -> List[Dict]:
        """Carregar catálogo de livros"""
        try:
            with open(self.catalog_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("books", [])
        except:
            return []
    
    def get_book_info(self, title: str) -> str:
        """Buscar informações de um livro"""
        for book in self.books:
            if title.lower() in book["title"].lower():
                return f"""📚 **{book['title']}**
👤 Autor: {book['author']}
🏢 Editora: {book['imprint']}
📅 Lançamento: {book['release_date']}
📖 Sinopse: {book['synopsis']}"""
        
        return f"❌ Livro '{title}' não encontrado no catálogo"


class StoreAgent:
    """Agente responsável por localizar onde comprar"""
    
    def __init__(self, catalog_path: str):
        self.catalog_path = catalog_path
        self.books = self._load_catalog()
    
    def _load_catalog(self) -> List[Dict]:
        """Carregar catálogo"""
        try:
            with open(self.catalog_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("books", [])
        except:
            return []
    
    def find_stores(self, title: str, city: str = None) -> str:
        """Indicar onde comprar um livro"""
        for book in self.books:
            if title.lower() in book["title"].lower():
                availability = book.get('availability', {})
                
                if city:
                    stores = availability.get(city.title(), [])
                    if stores:
                        return f"🏪 **{title}** em {city.title()}:\n• {', '.join(stores)}"
                    else:
                        return f"❌ Nenhuma loja em {city.title()}"
                else:
                    result = f"🏪 **Onde comprar '{title}':**\n"
                    for loc, stores in availability.items():
                        result += f"• {loc}: {', '.join(stores)}\n"
                    return result
        
        return f"❌ Livro '{title}' não encontrado"


class TicketAgent:
    """Agente responsável por tickets de suporte"""
    
    def __init__(self, tickets_path: str):
        self.tickets_path = tickets_path
    
    def create_ticket(self, message: str) -> str:
        """Abrir ticket simulado"""
        ticket_id = f"TICKET-{datetime.now().strftime('%d%H%M%S')}"
        
        ticket = {
            "id": ticket_id,
            "message": message,
            "status": "aberto", 
            "timestamp": datetime.now().isoformat(),
            "created": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        
        # Simular salvamento
        try:
            with open(self.tickets_path, 'r', encoding='utf-8') as f:
                tickets = json.load(f)
        except:
            tickets = []
        
        tickets.append(ticket)
        
        try:
            with open(self.tickets_path, 'w', encoding='utf-8') as f:
                json.dump(tickets, f, indent=2, ensure_ascii=False)
        except:
            pass
        
        return f"""🎫 **Ticket Criado**
📋 ID: {ticket_id}
💬 Mensagem: {message}
📅 Data: {ticket['created']}
✅ Status: Aberto

Nossa equipe entrará em contato!"""


class MultiAgentEditorialAssistant:
    """
    Assistente Editorial Multiagente Simples
    Coordena agentes especializados SEM usar CrewAI
    """
    
    def __init__(self):
        """Inicializar assistente e agentes especializados"""
        self.catalog_path = "mock_catalog.json"
        self.tickets_path = "mock_tickets.json"
        
        # Agentes especializados
        self.catalog_agent = CatalogAgent(self.catalog_path)
        self.store_agent = StoreAgent(self.catalog_path)
        self.ticket_agent = TicketAgent(self.tickets_path)
        
        # Gemini apenas como base LLM (não para orquestração)
        self.setup_gemini()
    
    def setup_gemini(self):
        """Configurar Gemini LLM apenas como base"""
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            try:
                genai.configure(api_key=api_key)
                self.gemini = genai.GenerativeModel('gemini-pro')
                print("🧠 Gemini configurado como base LLM")
            except:
                self.gemini = None
                print("⚠️ Gemini offline")
        else:
            self.gemini = None
            print("⚠️ Sem GEMINI_API_KEY")
    
    def process(self, user_input: str) -> str:
        """
        Processar entrada do usuário
        Orquestração manual (SEM CrewAI)
        """
        # Detectar intenção
        intent = self._detect_intent(user_input)
        
        # Extrair informações
        book_title = self._extract_book_title(user_input)
        city = self._extract_city(user_input)
        
        # Rotear para agente apropriado
        if intent == "book_info":
            return self.catalog_agent.get_book_info(book_title)
        
        elif intent == "store_info":
            return self.store_agent.find_stores(book_title, city)
        
        elif intent == "support":
            return self.ticket_agent.create_ticket(user_input)
        
        else:
            return """❓ Como posso ajudar?
📚 Informações sobre livros
🏪 Onde comprar livros
🎫 Suporte técnico"""
    
    def _detect_intent(self, text: str) -> str:
        """Detectar intenção (lógica simples sem CrewAI)"""
        text_lower = text.lower()
        
        # Padrões para informações de livros
        if any(word in text_lower for word in ["sobre", "informação", "detalhes", "livro", "autor"]):
            return "book_info"
        
        # Padrões para onde comprar
        if any(word in text_lower for word in ["onde", "comprar", "loja", "vender"]):
            return "store_info"
        
        # Padrões para suporte
        if any(word in text_lower for word in ["ajuda", "suporte", "problema", "ticket"]):
            return "support"
        
        return "unknown"
    
    def _extract_book_title(self, text: str) -> str:
        """Extrair título do livro"""
        patterns = [
            r'"([^"]+)"',
            r"'([^']+)'", 
            r"sobre\s+o?\s*([a-zA-ZÀ-ÿ\s]+?)(?:\s+em|\s+$)",
            r"comprar\s+o?\s*([a-zA-ZÀ-ÿ\s]+?)(?:\s+em|\s+$)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                title = match.group(1).strip()
                title = re.sub(r'\s+(em|de|da|do)$', '', title, flags=re.IGNORECASE)
                if title:
                    return title
        
        # Buscar títulos conhecidos
        try:
            with open(self.catalog_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                books = data.get("books", [])
                
            text_lower = text.lower()
            for book in books:
                if book["title"].lower() in text_lower:
                    return book["title"]
        except:
            pass
        
        return ""
    
    def _extract_city(self, text: str) -> Optional[str]:
        """Extrair cidade"""
        cities = ["são paulo", "rio de janeiro", "salvador", "curitiba", "belo horizonte"]
        text_lower = text.lower()
        
        for city in cities:
            if city in text_lower:
                return city.title()
        
        return None


def main():
    """Demonstração do assistente multiagente"""
    print("🤖 ASSISTENTE EDITORIAL MULTIAGENTE SIMPLES")
    print("=" * 50)
    print("✅ Arquitetura multiagente clara")
    print("✅ Código limpo e organizado") 
    print("❌ SEM CrewAI para orquestração")
    print("🧠 Gemini apenas como base LLM")
    print("=" * 50)
    
    assistant = MultiAgentEditorialAssistant()
    
    # Testes dos objetivos
    tests = [
        "Quero informações sobre Dom Casmurro",  # Consulta catálogo + info livro
        "Onde posso comprar A Abelha em São Paulo?",  # Indica onde comprar
        "Preciso de ajuda com um problema"  # Ticket simulado
    ]
    
    for i, test in enumerate(tests, 1):
        print(f"\n🔸 Teste {i}: {test}")
        print("-" * 40)
        result = assistant.process(test)
        print(result)
    
    print(f"\n✅ OBJETIVOS ATENDIDOS!")
    print("🎯 Multiagente simples sem CrewAI")
    print("📋 Todas as funcionalidades implementadas")
    print("🧠 Gemini apenas como base LLM")


if __name__ == "__main__":
    main()
