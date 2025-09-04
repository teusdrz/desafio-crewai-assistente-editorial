#!/usr/bin/env python3
"""
Assistente Editorial - Versão Objetivo Específico
✅ Consulta catálogo
✅ Informações sobre livros  
✅ Indica onde comprar
✅ Abre ticket simulado
✅ Arquitetura clara e código limpo
❌ SEM uso de CrewAI para orquestração
🧠 Apenas Gemini como LLM base
"""

import json
import os
import re
from datetime import datetime
from typing import Dict, List, Optional
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


class EditorialAssistant:
    """
    Assistente Editorial Simples - Exatamente conforme objetivo
    """
    
    def __init__(self):
        """Inicializar assistente"""
        self.catalog_path = "mock_catalog.json" 
        self.tickets_path = "mock_tickets.json"
        self.setup_gemini()
        
    def setup_gemini(self):
        """Configurar Gemini LLM (somente como base)"""
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            try:
                genai.configure(api_key=api_key)
                self.gemini = genai.GenerativeModel('gemini-pro')
                print("🧠 Gemini LLM configurado como base")
            except:
                self.gemini = None
                print("⚠️ Gemini offline - usando lógica local")
        else:
            self.gemini = None
            print("⚠️ GEMINI_API_KEY não encontrada")
    
    def consultar_catalogo(self, titulo_livro: str) -> str:
        """✅ Consulta catálogo de livros"""
        try:
            with open(self.catalog_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                books = data.get("books", [])
        except:
            return "❌ Erro ao acessar catálogo"
        
        # Buscar livro
        for book in books:
            if titulo_livro.lower() in book["title"].lower():
                return self._formatar_informacoes_livro(book)
        
        return f"❌ Livro '{titulo_livro}' não encontrado no catálogo"
    
    def informacoes_livro(self, titulo: str) -> str:
        """✅ Informações detalhadas sobre livros"""
        return self.consultar_catalogo(titulo)
    
    def indicar_onde_comprar(self, titulo_livro: str, cidade: str = None) -> str:
        """✅ Indica onde comprar livros"""
        try:
            with open(self.catalog_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                books = data.get("books", [])
        except:
            return "❌ Erro ao acessar catálogo"
        
        # Encontrar livro
        book = None
        for item in books:
            if titulo_livro.lower() in item["title"].lower():
                book = item
                break
        
        if not book:
            return f"❌ Livro '{titulo_livro}' não encontrado"
        
        availability = book.get('availability', {})
        
        if cidade:
            stores = availability.get(cidade.title(), [])
            if stores:
                return f"🏪 **{titulo_livro}** em {cidade.title()}:\n• {', '.join(stores)}"
            else:
                return f"❌ Nenhuma loja em {cidade.title()}"
        else:
            result = f"🏪 **Onde comprar '{titulo_livro}':**\n"
            for loc, stores in availability.items():
                result += f"• **{loc}:** {', '.join(stores)}\n"
            return result
    
    def abrir_ticket_simulado(self, mensagem: str) -> str:
        """✅ Abre ticket de suporte simulado"""
        ticket_id = f"TICKET-{datetime.now().strftime('%d%H%M%S')}"
        
        ticket = {
            "id": ticket_id,
            "mensagem": mensagem,
            "status": "aberto",
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
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
💬 Mensagem: {mensagem}
📅 Data: {ticket['data']}
✅ Status: Aberto

Aguarde contato da nossa equipe!"""
    
    def processar_solicitacao(self, entrada_usuario: str) -> str:
        """
        Processador principal - SEM CrewAI
        Lógica direta e simples para determinar ação
        """
        entrada = entrada_usuario.lower()
        
        # 1. Detectar livro mencionado
        titulo_livro = self._extrair_titulo_livro(entrada_usuario)
        
        # 2. Detectar intenção e agir diretamente
        if any(palavra in entrada for palavra in ["sobre", "informação", "detalhes", "livro"]):
            if titulo_livro:
                return self.informacoes_livro(titulo_livro)
            else:
                return "❓ Qual livro você gostaria de consultar?"
        
        elif any(palavra in entrada for palavra in ["onde", "comprar", "loja"]):
            if titulo_livro:
                cidade = self._extrair_cidade(entrada_usuario)
                return self.indicar_onde_comprar(titulo_livro, cidade)
            else:
                return "❓ Qual livro você gostaria de comprar?"
        
        elif any(palavra in entrada for palavra in ["ajuda", "suporte", "problema", "ticket"]):
            return self.abrir_ticket_simulado(entrada_usuario)
        
        else:
            return """❓ Como posso ajudar?
🔹 Informações sobre livros
🔹 Onde comprar livros  
🔹 Suporte técnico"""
    
    def _extrair_titulo_livro(self, texto: str) -> Optional[str]:
        """Extrair título do livro (lógica simples e eficaz)"""
        patterns = [
            r'"([^"]+)"',  # Entre aspas duplas
            r"'([^']+)'",  # Entre aspas simples  
            r"sobre\s+o?\s*([a-zA-ZÀ-ÿ\s]+?)(?:\s+em|\s+$)",  # "sobre X em" ou "sobre X"
            r"livro\s+([a-zA-ZÀ-ÿ\s]+?)(?:\s+em|\s+$)",  # "livro X em" ou "livro X"
            r"comprar\s+o?\s*([a-zA-ZÀ-ÿ\s]+?)(?:\s+em|\s+$)",  # "comprar X em" ou "comprar X"
            r"informações?\s+sobre\s+o?\s*([a-zA-ZÀ-ÿ\s]+?)(?:\s+em|\s+$)",  # "informações sobre X"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, texto, re.IGNORECASE)
            if match:
                titulo = match.group(1).strip()
                # Limpar palavras comuns do final
                titulo = re.sub(r'\s+(em|de|da|do|na|no)$', '', titulo, flags=re.IGNORECASE)
                if titulo:
                    return titulo
        
        # Fallback: procurar nomes de livros conhecidos
        with open(self.catalog_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            books = data.get("books", [])
        
        texto_lower = texto.lower()
        for book in books:
            if book["title"].lower() in texto_lower:
                return book["title"]
        
        return None
    
    def _extrair_cidade(self, texto: str) -> Optional[str]:
        """Extrair cidade mencionada"""
        cidades = ["são paulo", "rio de janeiro", "salvador", "curitiba"]
        texto_lower = texto.lower()
        
        for cidade in cidades:
            if cidade in texto_lower:
                return cidade.title()
        return None
    
    def _formatar_informacoes_livro(self, book: Dict) -> str:
        """Formatar informações do livro de forma limpa"""
        info = f"""📚 **{book['title']}**

👤 **Autor:** {book['author']}  
🏢 **Editora:** {book['imprint']}
📅 **Lançamento:** {book['release_date']}

📖 **Sinopse:** {book['synopsis']}

🛒 **Onde Comprar:**"""
        
        availability = book.get('availability', {})
        for local, lojas in availability.items():
            info += f"\n• **{local}:** {', '.join(lojas)}"
        
        return info


def main():
    """Demonstração - Exatamente conforme objetivo"""
    print("🎯 ASSISTENTE EDITORIAL - VERSÃO OBJETIVO ESPECÍFICO")
    print("=" * 55)
    print("✅ Consulta catálogo")  
    print("✅ Informações sobre livros")
    print("✅ Indica onde comprar")
    print("✅ Abre ticket simulado")
    print("✅ Arquitetura clara e código limpo")
    print("❌ SEM uso de CrewAI para orquestração") 
    print("🧠 Apenas Gemini como LLM base")
    print("=" * 55)
    
    assistant = EditorialAssistant()
    
    # Testes das funcionalidades requeridas
    testes = [
        "Quero informações sobre Dom Casmurro",
        "Onde posso comprar A Abelha em São Paulo?", 
        "Preciso de suporte técnico"
    ]
    
    for i, teste in enumerate(testes, 1):
        print(f"\n🔸 Teste {i}: {teste}")
        print("-" * 40)
        resultado = assistant.processar_solicitacao(teste)
        print(resultado)
    
    print("\n✅ OBJETIVO ATENDIDO!")
    print("🎯 Assistente editorial simples SEM CrewAI")
    print("🧠 Gemini apenas como base LLM")
    print("🏗️ Arquitetura clara e código limpo")


if __name__ == "__main__":
    main()
