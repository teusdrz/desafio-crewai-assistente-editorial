#!/usr/bin/env python3
"""
Teste direto dos agentes sem CrewAI
"""

import os
import sys
sys.path.append('/Users/matheusviniciusdosreissouza/desafio-crewai-assistente-editorial/src')

from config import Config
from agents.editorial_agents import create_catalog_agent
from tools.editorial_tools import get_book_details

def test_direct_agent():
    """Teste direto do agente sem Crew"""
    print("🧪 TESTE DIRETO DO AGENTE")
    print("=" * 40)
    
    try:
        # Inicializar configuração
        config = Config()
        llm = config.create_llm()
        
        # Criar agente
        agent = create_catalog_agent(llm)
        print("✅ Agente criado com sucesso")
        
        # Testar ferramenta diretamente
        print("\n📖 Testando ferramenta get_book_details:")
        result = get_book_details("A Abelha")
        print(f"Resultado: {result}")
        
        # Testar invoke do agente diretamente
        print("\n🤖 Testando agente diretamente:")
        
        # Usar o agent execute diretamente se possível
        if hasattr(agent, 'execute'):
            response = agent.execute("Me conte sobre o livro A Abelha")
            print(f"Resposta do agente: {response}")
        else:
            print("Agente não tem método execute direto")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

def test_tools_directly():
    """Teste das ferramentas diretamente"""
    print("\n🛠️ TESTE DAS FERRAMENTAS")
    print("=" * 40)
    
    try:
        # Importar ferramentas
        from tools.editorial_tools import get_book_details, find_stores_selling_book, open_support_ticket
        
        # Testar get_book_details
        print("📖 Testando get_book_details:")
        result1 = get_book_details("A Abelha")
        print(f"Resultado: {result1}")
        
        # Testar find_stores_selling_book
        print("\n🏪 Testando find_stores_selling_book:")
        result2 = find_stores_selling_book("A Abelha", "São Paulo")
        print(f"Resultado: {result2}")
        
        # Testar open_support_ticket
        print("\n🎫 Testando open_support_ticket:")
        result3 = open_support_ticket("João Silva", "joao@email.com", "Problema com pedido", "Não recebi meu livro")
        print(f"Resultado: {result3}")
        
    except Exception as e:
        print(f"❌ Erro nas ferramentas: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Mudar para o diretório correto
    os.chdir('/Users/matheusviniciusdosreissouza/desafio-crewai-assistente-editorial')
    
    test_tools_directly()
    test_direct_agent()
