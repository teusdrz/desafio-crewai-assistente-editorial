#!/usr/bin/env python3
"""
Mathematical Analytics Agent for Editorial Assistant
Specialized agent for statistical analysis and mathematical insights.
"""

from crewai import Agent, Task, Crew
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'tools'))
from math_analytics import get_catalog_analytics
import json


class MathAnalyticsAgent:
    """Specialized agent for mathematical and statistical analysis"""
    
    def __init__(self, llm):
        """Initialize the math analytics agent"""
        self.llm = llm
        self.agent = self._create_agent()
    
    def _create_agent(self) -> Agent:
        """Create the mathematical analytics agent"""
        return Agent(
            role="Analista Matemático e Estatístico Editorial",
            goal="Fornecer análises matemáticas e estatísticas abrangentes do catálogo editorial, incluindo métricas de publicação, produtividade de autores, distribuição de mercado e insights quantitativos",
            backstory="""Você é um especialista em análise de dados editoriais com forte formação em matemática e estatística. 
            Sua expertise inclui análise estatística descritiva e inferencial, métricas de diversidade, correlações, 
            e interpretação de padrões complexos em dados de publicação. Você transforma números em insights acionáveis 
            para a indústria editorial.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def create_analysis_task(self, query: str) -> Task:
        """Create a mathematical analysis task"""
        # Determine analysis type from query
        analysis_type = "comprehensive"
        if "publicação" in query.lower() or "publication" in query.lower():
            analysis_type = "publications"
        elif "autor" in query.lower() or "author" in query.lower():
            analysis_type = "authors"
        elif "mercado" in query.lower() or "market" in query.lower():
            analysis_type = "market"
        elif "editora" in query.lower() or "imprint" in query.lower():
            analysis_type = "imprints"
        
        return Task(
            description=f"""
            Realize uma análise matemática e estatística completa baseada na consulta: "{query}"
            
            Tipo de análise requerida: {analysis_type}
            
            Sua resposta deve incluir:
            1. **Resumo Executivo**: Principais insights em linguagem acessível
            2. **Métricas Estatísticas**: Dados quantitativos relevantes
            3. **Interpretação**: Significado prático dos números
            4. **Recomendações**: Sugestões baseadas nos dados
            
            Use a função get_catalog_analytics para obter os dados analíticos.
            Apresente os resultados de forma clara e profissional em português.
            """,
            agent=self.agent,
            expected_output="Relatório analítico estruturado com métricas estatísticas, interpretações e recomendações práticas"
        )
    
    def get_analytics_tools(self):
        """Get available analytics tools"""
        return [
            {
                "name": "get_catalog_analytics",
                "description": "Obter análises matemáticas e estatísticas do catálogo editorial",
                "function": get_catalog_analytics
            }
        ]


def create_analytics_agent(llm) -> MathAnalyticsAgent:
    """Factory function to create math analytics agent"""
    return MathAnalyticsAgent(llm)
