#!/usr/bin/env python3
"""
Assistente Editorial Multiagente Simplificado
Sem CrewAI - Apenas Gemini como base LLM
Arquitetura clara e código limpo
"""

import json
import os
import re
import google.generativeai as genai
from datetime import datetime
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

class SimpleMultiagentAssistant:
    """
    Assistente Editorial Multiagente Simples
    Sem uso de CrewAI - Orquestração manual com agentes especializados
    """
    
    def __init__(self):
        """Inicializar assistente com agentes especializados"""
        self.setup_gemini()
        self.catalog_path = "mock_catalog.json"
        self.tickets_path = "mock_tickets.json"
        
        # Agentes especializados (classes internas simples)
        self.catalog_agent = CatalogAgent(self.catalog_path)
        self.store_agent = StoreFinderAgent(self.catalog_path)
        self.support_agent = SupportAgent(self.tickets_path)
        self.orchestrator = OrchestratorAgent(self.model)
    
    def setup_gemini(self):
        """Configurar Gemini LLM"""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("⚠️ GEMINI_API_KEY não encontrada no .env - usando modo offline")
            self.model = None
            return
            
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            print("✅ Gemini LLM configurado com sucesso")
        except Exception as e:
            print(f"❌ Erro ao configurar Gemini: {e}")
            self.model = None
    
    def process_request(self, user_input: str) -> str:
        """
        Processar solicitação do usuário usando orquestração manual
        (Sem CrewAI - controle direto dos agentes)
        """
        # 1. Orquestrador determina intenção e agente apropriado
        intent_info = self.orchestrator.detect_intent(user_input)
        
        # 2. Rotear para agente especializado apropriado
        if intent_info["intent"] == "catalog":
            return self.catalog_agent.get_book_details(intent_info.get("book_title", ""))
        
        elif intent_info["intent"] == "stores":
            return self.store_agent.find_stores(
                intent_info.get("book_title", ""),
                intent_info.get("city")
            )
        
        elif intent_info["intent"] == "support":
            return self.support_agent.create_ticket(user_input)
        
        else:
            return "❓ Não entendi sua solicitação. Posso ajudar com:\n• Informações de livros\n• Onde comprar livros\n• Suporte técnico"


class OrchestratorAgent:
    """Agente Orquestrador - Detecta intenções e coordena outros agentes"""
    
    def __init__(self, gemini_model=None):
        self.model = gemini_model
    
    def detect_intent(self, user_input: str) -> Dict[str, Any]:
        """Detectar intenção usando padrões simples (sem CrewAI)"""
        user_lower = user_input.lower()
        
        # Padrões para catálogo de livros
        if any(word in user_lower for word in ["livro", "autor", "detalhes", "sobre", "informação"]):
            book_title = self._extract_book_title(user_input)
            return {"intent": "catalog", "book_title": book_title}
        
        # Padrões para encontrar lojas
        if any(word in user_lower for word in ["onde", "comprar", "loja", "vender"]):
            book_title = self._extract_book_title(user_input)
            city = self._extract_city(user_input)
            return {"intent": "stores", "book_title": book_title, "city": city}
        
        # Padrões para suporte
        if any(word in user_lower for word in ["ajuda", "suporte", "problema", "ticket"]):
            return {"intent": "support"}
        
        return {"intent": "unknown"}
    
    def _extract_book_title(self, text: str) -> str:
        """Extrair título do livro usando regex simples"""
        patterns = [
            r'"([^"]+)"',
            r"'([^']+)'",
            r"livro\s+([a-zA-ZÀ-ÿ\s]+)",
            r"sobre\s+([a-zA-ZÀ-ÿ\s]+)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return ""
    
    def _extract_city(self, text: str) -> Optional[str]:
        """Extrair cidade mencionada"""
        cities = ["são paulo", "rio de janeiro", "salvador", "curitiba", "belo horizonte"]
        text_lower = text.lower()
        
        for city in cities:
            if city in text_lower:
                return city.title()
        
        return None


class CatalogAgent:
    """Agente especializado em consulta ao catálogo"""
    
    def __init__(self, catalog_path: str):
        self.catalog_path = catalog_path
        self.catalog_data = self._load_catalog()
    
    def _load_catalog(self) -> List[Dict]:
        """Carregar dados do catálogo"""
        try:
            with open(self.catalog_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("books", [])
        except FileNotFoundError:
            print(f"❌ Arquivo {self.catalog_path} não encontrado")
            return []
        except json.JSONDecodeError:
            print(f"❌ Erro ao decodificar JSON do arquivo {self.catalog_path}")
            return []
    
    def get_book_details(self, book_title: str) -> str:
        """Buscar detalhes de um livro"""
        if not book_title:
            return "❓ Por favor, especifique o título do livro que deseja consultar."
        
        # Buscar livro no catálogo
        for book in self.catalog_data:
            if book_title.lower() in book["title"].lower():
                return self._format_book_details(book)
        
        return f"❌ Livro '{book_title}' não encontrado no catálogo.\n📚 Temos {len(self.catalog_data)} livros disponíveis."
    
    def _format_book_details(self, book: Dict) -> str:
        """Formatar detalhes do livro"""
        details = f"""📚 **{book['title']}**

📝 **Autor:** {book['author']}
🏢 **Editora:** {book['imprint']}
📅 **Data de Lançamento:** {book['release_date']}

📖 **Sinopse:** {book['synopsis']}

🛒 **Onde Comprar:**"""
        
        availability = book.get('availability', {})
        for location, stores in availability.items():
            details += f"\n• **{location}:** {', '.join(stores)}"
        
        return details


class StoreFinderAgent:
    """Agente especializado em encontrar lojas"""
    
    def __init__(self, catalog_path: str):
        self.catalog_path = catalog_path
        self.catalog_data = self._load_catalog()
    
    def _load_catalog(self) -> List[Dict]:
        """Carregar dados do catálogo"""
        try:
            with open(self.catalog_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("books", [])
        except:
            return []
    
    def find_stores(self, book_title: str, city: Optional[str] = None) -> str:
        """Encontrar lojas que vendem o livro"""
        if not book_title:
            return "❓ Por favor, especifique o livro que deseja comprar."
        
        # Encontrar o livro
        book = None
        for item in self.catalog_data:
            if book_title.lower() in item["title"].lower():
                book = item
                break
        
        if not book:
            return f"❌ Livro '{book_title}' não encontrado no catálogo."
        
        # Buscar lojas
        availability = book.get('availability', {})
        
        if city:
            city_stores = availability.get(city.title(), availability.get(city, []))
            if city_stores:
                return f"🏪 **Lojas em {city.title()} que vendem '{book['title']}':**\n• {', '.join(city_stores)}"
            else:
                return f"❌ Nenhuma loja encontrada em {city.title()} para '{book['title']}'"
        else:
            # Listar todas as lojas
            all_stores = []
            for location, stores in availability.items():
                all_stores.append(f"**{location}:** {', '.join(stores)}")
            
            return f"🏪 **Lojas que vendem '{book['title']}':**\n• " + "\n• ".join(all_stores)


class SupportAgent:
    """Agente especializado em suporte"""
    
    def __init__(self, tickets_path: str):
        self.tickets_path = tickets_path
        self.tickets_data = self._load_tickets()
    
    def _load_tickets(self) -> List[Dict]:
        """Carregar tickets existentes"""
        try:
            with open(self.tickets_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def create_ticket(self, message: str) -> str:
        """Criar ticket de suporte"""
        # Gerar ID único
        ticket_id = f"TICKET-{datetime.now().strftime('%d%H%M')}"
        
        # Criar novo ticket
        new_ticket = {
            "id": ticket_id,
            "message": message,
            "status": "aberto",
            "timestamp": datetime.now().isoformat(),
            "created_date": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        
        # Salvar ticket
        try:
            self.tickets_data.append(new_ticket)
            with open(self.tickets_path, 'w', encoding='utf-8') as f:
                json.dump(self.tickets_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            return f"❌ Erro ao criar ticket: {e}"
        
        return f"""🎫 **Ticket de Suporte Criado**

📋 **ID:** {ticket_id}
📝 **Status:** Aberto  
💬 **Mensagem:** {message}

✅ Ticket criado com sucesso! Nossa equipe entrará em contato em até 24 horas.
📞 Para acompanhar, use o ID: {ticket_id}"""


def main():
    """Demonstração do assistente multiagente simples"""
    print("🤖 Assistente Editorial Multiagente Simplificado")
    print("=" * 50)
    print("✅ Sem CrewAI - Orquestração manual")
    print("🧠 Gemini apenas como LLM base")
    print("🎯 Arquitetura clara e código limpo")
    print("=" * 50)
    
    assistant = SimpleMultiagentAssistant()
    
    # Testes básicos
    test_cases = [
        "Quero saber sobre o livro Dom Casmurro",
        "Onde posso comprar A Abelha em São Paulo?",
        "Preciso de ajuda com um problema"
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n🔸 Teste {i}: {test}")
        print("-" * 40)
        result = assistant.process_request(test)
        print(result)
    
    print(f"\n✅ Demonstração concluída!")
    print("🎯 Objetivo atendido: Assistente multiagente SIMPLES sem CrewAI")


if __name__ == "__main__":
    main()
