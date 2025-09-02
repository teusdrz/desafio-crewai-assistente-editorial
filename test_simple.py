#!/usr/bin/env python3
"""
Teste das funções core sem decorators CrewAI
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any

def get_book_details_simple(book_title: str) -> Dict[str, Any]:
    """Versão simples da função get_book_details"""
    try:
        catalog_path = "/Users/matheusviniciusdosreissouza/desafio-crewai-assistente-editorial/data/mock_catalog.json"
        
        with open(catalog_path, 'r', encoding='utf-8') as file:
            catalog_data = json.load(file)
        
        books = catalog_data.get("books", [])
        
        for book in books:
            if book["title"].lower() == book_title.lower():
                return {
                    "found": True,
                    "book": book
                }
        
        return {
            "found": False,
            "message": f"Livro '{book_title}' não encontrado no catálogo"
        }
        
    except Exception as e:
        return {
            "found": False,
            "error": str(e)
        }

def find_stores_simple(book_title: str, city: Optional[str] = None) -> Dict[str, Any]:
    """Versão simples da função find_stores_selling_book"""
    try:
        catalog_path = "/Users/matheusviniciusdosreissouza/desafio-crewai-assistente-editorial/data/mock_catalog.json"
        
        with open(catalog_path, 'r', encoding='utf-8') as file:
            catalog_data = json.load(file)
        
        stores = catalog_data.get("stores", [])
        
        # Filtrar por cidade se especificada
        if city:
            stores = [store for store in stores if city.lower() in store.get("city", "").lower()]
        
        return {
            "found": True,
            "stores": stores,
            "book_title": book_title,
            "city": city
        }
        
    except Exception as e:
        return {
            "found": False,
            "error": str(e)
        }

def test_simple_functions():
    """Teste das funções simples"""
    print("🧪 TESTE DAS FUNÇÕES SIMPLES")
    print("=" * 50)
    
    # Teste 1: Buscar livro
    print("\n📖 TESTE 1: Buscar livro 'A Abelha'")
    result1 = get_book_details_simple("A Abelha")
    print(f"Resultado: {json.dumps(result1, indent=2, ensure_ascii=False)}")
    
    # Teste 2: Buscar livro inexistente
    print("\n📖 TESTE 2: Buscar livro inexistente")
    result2 = get_book_details_simple("Livro Inexistente")
    print(f"Resultado: {json.dumps(result2, indent=2, ensure_ascii=False)}")
    
    # Teste 3: Buscar lojas
    print("\n🏪 TESTE 3: Buscar lojas em São Paulo")
    result3 = find_stores_simple("A Abelha", "São Paulo")
    print(f"Resultado: {json.dumps(result3, indent=2, ensure_ascii=False)}")
    
    # Teste 4: Verificar arquivos
    print("\n📁 TESTE 4: Verificar arquivos de dados")
    data_files = [
        "/Users/matheusviniciusdosreissouza/desafio-crewai-assistente-editorial/data/mock_catalog.json",
        "/Users/matheusviniciusdosreissouza/desafio-crewai-assistente-editorial/mock_catalog.json"
    ]
    
    for file_path in data_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} - Existe")
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                books_count = len(data.get("books", []))
                stores_count = len(data.get("stores", []))
                print(f"   📚 Livros: {books_count}")
                print(f"   🏪 Lojas: {stores_count}")
        else:
            print(f"❌ {file_path} - Não encontrado")

if __name__ == "__main__":
    test_simple_functions()
