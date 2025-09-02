#!/usr/bin/env python3
"""
Assistente Editorial Simplificado - Versão de Teste
"""

import json
import os
import re
from typing import Dict, Any, Optional

class SimpleEditorialAssistant:
    """Versão simplificada do assistente que funciona diretamente"""
    
    def __init__(self):
        """Inicializar o assistente"""
        self.data_path = "/Users/matheusviniciusdosreissouza/desafio-crewai-assistente-editorial/data/mock_catalog.json"
        self.tickets_path = "/Users/matheusviniciusdosreissouza/desafio-crewai-assistente-editorial/data/mock_tickets.json"
        
    def get_book_details(self, book_title: str) -> str:
        """Buscar detalhes de um livro"""
        try:
            with open(self.data_path, 'r', encoding='utf-8') as file:
                catalog_data = json.load(file)
            
            books = catalog_data.get("books", [])
            
            for book in books:
                if book["title"].lower() == book_title.lower():
                    response = f"""📚 **{book['title']}**
                    
**Autor:** {book['author']}
**Editora:** {book['imprint']}
**Data de Lançamento:** {book['release_date']}

**Sinopse:** {book['synopsis']}

**Onde Comprar:**"""
                    
                    availability = book.get('availability', {})
                    for location, stores in availability.items():
                        response += f"\n• **{location}:** {', '.join(stores)}"
                    
                    return response
            
            return f"❌ Desculpe, não encontrei o livro '{book_title}' em nosso catálogo. Temos {len(books)} livros disponíveis."
            
        except Exception as e:
            return f"❌ Erro ao buscar informações: {str(e)}"
    
    def find_stores(self, book_title: str, city: Optional[str] = None) -> str:
        """Encontrar lojas que vendem um livro"""
        try:
            with open(self.data_path, 'r', encoding='utf-8') as file:
                catalog_data = json.load(file)
            
            books = catalog_data.get("books", [])
            
            for book in books:
                if book["title"].lower() == book_title.lower():
                    availability = book.get('availability', {})
                    
                    if city:
                        # Buscar por cidade específica
                        city_lower = city.lower()
                        found_stores = []
                        
                        for location, stores in availability.items():
                            if city_lower in location.lower():
                                found_stores.extend(stores)
                        
                        if found_stores:
                            return f"🏪 **Lojas em {city} que vendem '{book_title}':**\n" + \
                                   "\n".join([f"• {store}" for store in found_stores])
                        else:
                            return f"❌ Não encontrei lojas em {city} que vendem '{book_title}', mas o livro está disponível em:\n" + \
                                   "\n".join([f"• **{loc}:** {', '.join(stores)}" for loc, stores in availability.items()])
                    else:
                        # Mostrar todas as lojas
                        response = f"🏪 **Onde comprar '{book_title}':**\n"
                        for location, stores in availability.items():
                            response += f"• **{location}:** {', '.join(stores)}\n"
                        return response
            
            return f"❌ Livro '{book_title}' não encontrado no catálogo."
            
        except Exception as e:
            return f"❌ Erro ao buscar lojas: {str(e)}"
    
    def create_support_ticket(self, message: str) -> str:
        """Criar um ticket de suporte"""
        import hashlib
        ticket_id = f"TICKET-{hashlib.md5(message.encode()).hexdigest()[-6:].upper()}"
        
        response = f"""🎫 **Ticket de Suporte Criado**

**ID do Ticket:** {ticket_id}
**Status:** Aberto
**Mensagem:** {message}

✅ Seu ticket foi criado com sucesso! Nossa equipe de suporte entrará em contato em até 24 horas.

📧 Para acompanhar seu ticket, use o ID: {ticket_id}"""
        
        return response
    
    def detect_intent(self, user_input: str) -> str:
        """Detectar intenção e processar resposta"""
        user_input_lower = user_input.lower()
        
        # Verificar suporte primeiro (mais específico)
        support_patterns = [
            r"(?:help|ajuda|support|suporte|problem|problema|ticket|reclamação|complaint|issue|questão|dúvida|question|order|pedido)"
        ]
        
        for pattern in support_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                return self.create_support_ticket(user_input)
        
        # Padrões para busca de lojas (mais específico que livros)
        store_patterns = [
            r"(?:where|onde).*?(?:can i buy|buy|comprar|get|encontrar).*?([a-zA-ZÀ-ÿ\-\s]+?)(?:\s+in\s+|\s+em\s+)([a-zA-ZÀ-ÿ\s]+)",
            r"(?:buy|comprar).*?([a-zA-ZÀ-ÿ\-\s]+?)(?:\s+in\s+|\s+em\s+)([a-zA-ZÀ-ÿ\s]+)",
            r"(?:stores|lojas).*?(?:selling|vendendo|that sell|que vendem).*?([a-zA-ZÀ-ÿ\-\s]+)"
        ]
        
        # Verificar busca de lojas
        for pattern in store_patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                if match.lastindex >= 2:  # Tem cidade
                    book_title = match.group(1).strip()
                    city = match.group(2).strip()
                    # Limpar títulos
                    book_title = re.sub(r'\s+', ' ', book_title).strip()
                    return self.find_stores(book_title, city)
                else:
                    book_title = match.group(1).strip()
                    return self.find_stores(book_title)
        
        # Padrões para busca de livros (mais específicos)
        book_patterns = [
            r"(?:quero saber sobre|tell me about|about|sobre|details|detalhes|info|informações).*?['\"](.*?)['\"]",
            r"(?:quero saber sobre|tell me about|about|sobre|details|detalhes|info|informações).*?([A-ZÀ-ÿ][a-zA-ZÀ-ÿ\-\s]+)",
            r"(?:book|livro|título).*?['\"](.*?)['\"]",
            r"(?:book|livro|título).*?([A-ZÀ-ÿ][a-zA-ZÀ-ÿ\-\s]+)",
            r"^['\"](.*?)['\"]$",  # Título entre aspas
            r"^([A-ZÀ-ÿ][a-zA-ZÀ-ÿ\-\s]+)$"  # Título simples começando com maiúscula
        ]
        
        # Verificar busca de livros
        for pattern in book_patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                book_title = match.group(1).strip()
                # Limpar e validar título
                book_title = re.sub(r'\s+', ' ', book_title).strip()
                # Filtrar palavras muito curtas ou cumprimentos comuns
                common_words = ['olá', 'oi', 'hello', 'hi', 'tchau', 'bye', 'obrigado', 'thanks']
                if (book_title and len(book_title) > 2 and 
                    book_title.lower() not in common_words and
                    not any(word in book_title.lower() for word in ['where', 'buy', 'help', 'support'])):
                    return self.get_book_details(book_title)
        
        # Resposta padrão
        return """👋 Olá! Sou o Assistente Editorial da Elo Editora.

Posso ajudá-lo com:
• 📖 **Informações sobre livros** - Ex: "Me fale sobre A Abelha"
• 🏪 **Encontrar lojas** - Ex: "Onde posso comprar A Baleia-azul em São Paulo?"
• 🎫 **Suporte ao cliente** - Ex: "Preciso de ajuda com meu pedido"

Como posso ajudá-lo hoje?"""

def main():
    """Função principal do assistente simplificado"""
    assistant = SimpleEditorialAssistant()
    
    print("🚀 Assistente Editorial da Elo Editora - Versão Simplificada")
    print("=" * 60)
    print("✅ Sistema inicializado com sucesso!")
    print("\nDigite 'quit' ou 'sair' para encerrar.\n")
    
    while True:
        try:
            user_input = input("💬 Você: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'sair', 'tchau']:
                print("👋 Obrigado por usar o Assistente Editorial! Até logo!")
                break
            
            if not user_input:
                continue
                
            print("\n🤖 Assistente:")
            response = assistant.detect_intent(user_input)
            print(response)
            print("\n" + "-" * 60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Tchau! Até a próxima!")
            break
        except Exception as e:
            print(f"\n❌ Erro: {e}")

if __name__ == "__main__":
    main()
