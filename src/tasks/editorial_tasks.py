"""
Editorial Assistant Tasks
This module defines the CrewAI tasks for the editorial assistant system.
"""

from crewai import Task, Agent
from typing import List
from ..tools.editorial_tools import get_book_details, find_stores_selling_book, open_support_ticket


def create_book_details_task(agent: Agent, book_title: str) -> Task:
    """
    Creates a task to get detailed information about a specific book.
    """
    return Task(
        description=f"""
        Encontre detalhes abrangentes sobre o livro intitulado "{book_title}".
        
        Sua tarefa é:
        1. Buscar o livro no catálogo
        2. Fornecer informações completas incluindo título, autor, editora, data de lançamento e sinopse
        3. Se o livro for encontrado, apresentar as informações de forma clara e envolvente
        4. Se o livro não for encontrado, sugerir títulos similares ou pedir esclarecimentos
        
        IMPORTANTE: Responda sempre em português brasileiro.
        Resultado esperado: Uma resposta detalhada sobre o livro com todas as informações disponíveis.
        """,
        agent=agent,
        tools=[get_book_details],
        expected_output="A comprehensive description of the book including all catalog details in Portuguese"
    )


def create_store_finder_task(agent: Agent, book_title: str, city: str = None) -> Task:
    """
    Creates a task to find stores selling a specific book.
    """
    city_context = f" em {city}" if city else ""
    
    return Task(
        description=f"""
        Encontre onde os clientes podem comprar o livro "{book_title}"{city_context}.
        
        Sua tarefa é:
        1. Buscar as informações de disponibilidade do livro
        2. Se uma cidade for especificada, focar nas lojas dessa cidade
        3. Sempre incluir opções de compra online
        4. Apresentar as informações de forma útil e organizada
        5. Se o livro não estiver disponível na cidade especificada, sugerir alternativas online
        
        IMPORTANTE: Responda sempre em português brasileiro.
        Resultado esperado: Uma lista clara de lojas e opções de compra para o cliente.
        """,
        agent=agent,
        tools=[find_stores_selling_book],
        expected_output="A detailed list of purchasing options including store names and locations in Portuguese"
    )


def create_support_ticket_task(agent: Agent, name: str, email: str, subject: str, message: str) -> Task:
    """
    Creates a task to open a customer support ticket.
    """
    return Task(
        description=f"""
        Crie um ticket de suporte para o cliente com os seguintes detalhes:
        - Nome: {name}
        - Email: {email}
        - Assunto: {subject}
        - Mensagem: {message}
        
        Sua tarefa é:
        1. Criar o ticket de suporte com todas as informações fornecidas
        2. Confirmar a criação do ticket com o cliente
        3. Fornecer o ID do ticket e status
        4. Explicar os próximos passos para acompanhamento
        
        IMPORTANTE: Responda sempre em português brasileiro.
        Resultado esperado: Confirmação da criação do ticket com ID do ticket e próximos passos.
        """,
        agent=agent,
        tools=[open_support_ticket],
        expected_output="Confirmation message with ticket details and follow-up instructions in Portuguese"
    )


def create_intent_detection_task(agent: Agent, user_input: str) -> Task:
    """
    Creates a task to detect user intent and classify the type of request.
    """
    return Task(
        description=f"""
        Analise a seguinte entrada do usuário e determine sua intenção:
        
        Entrada do usuário: "{user_input}"
        
        Sua tarefa é:
        1. Analisar o texto e identificar a intenção principal do usuário
        2. Classificar a intenção como uma das opções:
           - "book_details": Se o usuário está perguntando sobre um livro específico (título, autor, sinopse, preço, etc.)
           - "store_finder": Se o usuário quer encontrar lojas que vendem um livro específico
           - "support": Se o usuário tem uma reclamação, problema ou precisa abrir um ticket de suporte
           - "general": Para outros tipos de consultas
        3. Extrair informações relevantes como títulos de livros, nomes de autores, ou detalhes do problema
        4. Fornecer uma explicação clara da classificação
        
        IMPORTANTE: Responda sempre em português brasileiro.
        Resultado esperado: Classificação da intenção com informações extraídas relevantes.
        """,
        agent=agent,
        expected_output="Intent classification with relevant extracted information in Portuguese"
    )
