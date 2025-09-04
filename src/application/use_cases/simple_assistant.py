#!/usr/bin/env python3
"""
Assistente Editorial Simplificado - Versão de Teste
Inclui análises matemáticas e estatísticas abrangentes
"""

import json
import os
import re
import math
import statistics
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Tuple
from collections import Counter, defaultdict

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
    
    def get_mathematical_analysis(self, query: str) -> str:
        """Gerar análises matemáticas e estatísticas do catálogo"""
        try:
            with open(self.data_path, 'r', encoding='utf-8') as file:
                catalog_data = json.load(file)
            
            books = catalog_data.get("books", [])
            if not books:
                return "❌ Não há dados suficientes para análise."
            
            query_lower = query.lower()
            
            # Determinar tipo de análise baseado na consulta
            if any(word in query_lower for word in ['publicação', 'publication', 'data', 'ano', 'year']):
                return self._analyze_publications(books)
            elif any(word in query_lower for word in ['autor', 'author', 'produtividade', 'productivity']):
                return self._analyze_authors(books)
            elif any(word in query_lower for word in ['mercado', 'market', 'loja', 'store', 'distribuição', 'distribution']):
                return self._analyze_market(books)
            elif any(word in query_lower for word in ['editora', 'imprint', 'selo', 'publisher']):
                return self._analyze_imprints(books)
            else:
                return self._comprehensive_analysis(books)
                
        except Exception as e:
            return f"❌ Erro na análise: {str(e)}"
    
    def _analyze_publications(self, books: List[Dict]) -> str:
        """Análise estatística de publicações"""
        dates = []
        for book in books:
            try:
                date_str = book.get("release_date", "")
                if date_str:
                    date_obj = datetime.strptime(date_str, "%d/%m/%Y")
                    dates.append(date_obj)
            except ValueError:
                continue
        
        if not dates:
            return "❌ Não há datas válidas para análise."
        
        years = [date.year for date in dates]
        months = [date.month for date in dates]
        
        # Análise temporal
        span_years = round((max(dates) - min(dates)).days / 365.25, 2)
        publications_per_year = round(len(dates) / max(1, span_years), 2)
        
        # Distribuição mensal
        month_names = {1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun',
                      7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'}
        month_dist = Counter(months)
        peak_month = max(month_dist.items(), key=lambda x: x[1])
        
        # Análise sazonal
        spring = sum(1 for m in months if m in [3, 4, 5])
        summer = sum(1 for m in months if m in [6, 7, 8])
        autumn = sum(1 for m in months if m in [9, 10, 11])
        winter = sum(1 for m in months if m in [12, 1, 2])
        
        return f"""📊 **Análise Estatística de Publicações**

📈 **Métricas Temporais:**
• Total de livros: {len(books)}
• Período analisado: {span_years} anos
• Taxa de publicação: {publications_per_year} livros/ano
• Primeira publicação: {min(dates).strftime('%d/%m/%Y')}
• Última publicação: {max(dates).strftime('%d/%m/%Y')}

📅 **Distribuição Mensal:**
• Mês com mais publicações: {month_names[peak_month[0]]} ({peak_month[1]} livros)
• Média por mês: {round(len(dates) / 12, 2)} livros

🌱 **Padrão Sazonal:**
• Primavera (Mar-Mai): {spring} livros ({round(spring/len(dates)*100, 1)}%)
• Verão (Jun-Ago): {summer} livros ({round(summer/len(dates)*100, 1)}%)
• Outono (Set-Nov): {autumn} livros ({round(autumn/len(dates)*100, 1)}%)
• Inverno (Dez-Fev): {winter} livros ({round(winter/len(dates)*100, 1)}%)

📊 **Estatísticas Descritivas:**
• Ano médio: {round(statistics.mean(years), 1)}
• Desvio padrão: {round(statistics.stdev(years), 2) if len(years) > 1 else 0} anos
• Mediana: {statistics.median(years)}"""
    
    def _analyze_authors(self, books: List[Dict]) -> str:
        """Análise de produtividade de autores"""
        author_books = defaultdict(list)
        
        for book in books:
            author = book.get("author", "Desconhecido")
            author_books[author].append(book)
        
        # Métricas de produtividade
        book_counts = [len(books) for books in author_books.values()]
        total_authors = len(author_books)
        
        # Top autores
        top_authors = sorted(
            [(author, len(books)) for author, books in author_books.items()],
            key=lambda x: x[1], reverse=True
        )[:5]
        
        # Distribuição de produtividade
        productivity_dist = Counter(book_counts)
        single_book_authors = sum(1 for count in book_counts if count == 1)
        multi_book_authors = sum(1 for count in book_counts if count > 1)
        
        return f"""👨‍📚 **Análise de Produtividade de Autores**

📊 **Métricas Gerais:**
• Total de autores: {total_authors}
• Livros por autor (média): {round(statistics.mean(book_counts), 2)}
• Livros por autor (mediana): {statistics.median(book_counts)}
• Desvio padrão: {round(statistics.stdev(book_counts), 2) if len(book_counts) > 1 else 0}

🏆 **Top 5 Autores Mais Produtivos:**
{chr(10).join([f"• {author}: {count} livros" for author, count in top_authors[:5]])}

📈 **Distribuição de Produtividade:**
• Autores com 1 livro: {single_book_authors} ({round(single_book_authors/total_authors*100, 1)}%)
• Autores com múltiplos livros: {multi_book_authors} ({round(multi_book_authors/total_authors*100, 1)}%)
• Máximo de livros por autor: {max(book_counts)}

🎯 **Índice de Concentração:**
• Coeficiente de Gini: {round(self._calculate_gini_coefficient(book_counts), 4)}
• Entropia de Shannon: {round(self._calculate_shannon_entropy(book_counts), 4)}"""
    
    def _analyze_market(self, books: List[Dict]) -> str:
        """Análise de distribuição de mercado"""
        city_availability = defaultdict(int)
        online_stores = defaultdict(int)
        total_stores = 0
        
        for book in books:
            availability = book.get("availability", {})
            for location, stores in availability.items():
                if location.lower() == "online":
                    for store in stores:
                        online_stores[store] += 1
                else:
                    city_availability[location] += 1
                total_stores += len(stores)
        
        # Top cidades e lojas online
        top_cities = sorted(city_availability.items(), key=lambda x: x[1], reverse=True)[:5]
        top_online = sorted(online_stores.items(), key=lambda x: x[1], reverse=True)
        
        # Métricas de penetração
        books_with_physical = sum(1 for book in books 
                                 if any(k.lower() != "online" for k in book.get("availability", {}).keys()))
        books_with_online = sum(1 for book in books 
                               if "online" in [k.lower() for k in book.get("availability", {}).keys()])
        
        return f"""🏪 **Análise de Distribuição de Mercado**

🌍 **Cobertura Geográfica:**
• Total de cidades: {len(city_availability)}
• Total de pontos de venda: {total_stores}
• Média de cidades por livro: {round(sum(city_availability.values()) / len(books), 2)}

🏙️ **Top 5 Cidades com Maior Cobertura:**
{chr(10).join([f"• {city}: {count} livros disponíveis" for city, count in top_cities[:5]])}

💻 **Distribuição Online:**
• Total de lojas online: {len(online_stores)}
{chr(10).join([f"• {store}: {count} livros" for store, count in top_online])}

📊 **Taxa de Penetração:**
• Livros com venda física: {books_with_physical} ({round(books_with_physical/len(books)*100, 1)}%)
• Livros com venda online: {books_with_online} ({round(books_with_online/len(books)*100, 1)}%)
• Cobertura total média: {round(total_stores / len(books), 2)} pontos/livro

🎯 **Eficiência de Distribuição:**
• Gini de distribuição por cidade: {round(self._calculate_gini_coefficient(list(city_availability.values())), 4)}
• Balanceamento regional: {'Equilibrado' if self._calculate_gini_coefficient(list(city_availability.values())) < 0.4 else 'Desbalanceado'}"""
    
    def _analyze_imprints(self, books: List[Dict]) -> str:
        """Análise de performance de editoras/selos"""
        imprint_data = defaultdict(list)
        
        for book in books:
            imprint = book.get("imprint", "Desconhecido")
            imprint_data[imprint].append(book)
        
        # Métricas de market share
        imprint_counts = [(imprint, len(books)) for imprint, books in imprint_data.items()]
        imprint_counts.sort(key=lambda x: x[1], reverse=True)
        
        total_books = len(books)
        market_shares = [(imprint, count, round(count/total_books*100, 2)) 
                        for imprint, count in imprint_counts]
        
        # Índice de concentração HHI
        shares = [count/total_books for _, count in imprint_counts]
        hhi = sum(share**2 for share in shares)
        
        return f"""🏢 **Análise de Performance de Editoras**

📊 **Market Share:**
{chr(10).join([f"• {imprint}: {count} livros ({share}%)" for imprint, count, share in market_shares])}

📈 **Métricas de Concentração:**
• Total de editoras: {len(imprint_data)}
• Índice HHI: {round(hhi, 4)}
• Nível de concentração: {self._interpret_hhi(hhi)}
• Número efetivo de competidores: {round(1/hhi, 2) if hhi > 0 else float('inf')}

🎯 **Análise de Diversidade:**
• Entropia de Shannon: {round(self._calculate_shannon_entropy([len(books) for books in imprint_data.values()]), 4)}
• Editora dominante: {market_shares[0][0]} ({market_shares[0][2]}%)
• Concentração top-3: {sum(share for _, _, share in market_shares[:3])}%"""
    
    def _comprehensive_analysis(self, books: List[Dict]) -> str:
        """Análise abrangente do catálogo"""
        total_books = len(books)
        
        # Análise de completude dos dados
        complete_fields = 0
        total_fields = 0
        
        for book in books:
            for field in ["title", "author", "imprint", "release_date", "synopsis", "availability"]:
                total_fields += 1
                if book.get(field):
                    complete_fields += 1
        
        completeness = round(complete_fields / total_fields * 100, 2)
        
        # Análise de texto
        synopsis_lengths = [len(book.get("synopsis", "")) for book in books]
        title_lengths = [len(book.get("title", "")) for book in books]
        
        return f"""📊 **Análise Abrangente do Catálogo Editorial**

📚 **Visão Geral:**
• Total de livros no catálogo: {total_books}
• Completude dos dados: {completeness}%
• Período de análise: {datetime.now().strftime('%d/%m/%Y')}

📝 **Análise de Conteúdo:**
• Comprimento médio de sinopse: {round(statistics.mean(synopsis_lengths), 1)} caracteres
• Comprimento médio de título: {round(statistics.mean(title_lengths), 1)} caracteres
• Sinopse mais longa: {max(synopsis_lengths)} caracteres
• Sinopse mais curta: {min(synopsis_lengths)} caracteres

🏆 **Métricas de Qualidade:**
• Score de qualidade dos dados: {round(completeness * 0.7 + (100 if all(s > 20 for s in synopsis_lengths) else 50) * 0.3, 1)}/100
• Consistência de formato: {round(sum(1 for book in books if self._validate_book_format(book)) / total_books * 100, 1)}%

🔍 **Insights Estatísticos:**
• Coeficiente de variação (sinopse): {round(statistics.stdev(synopsis_lengths) / statistics.mean(synopsis_lengths) * 100, 2)}%
• Mediana vs Média (título): {statistics.median(title_lengths)} vs {round(statistics.mean(title_lengths), 1)}
• Distribuição normal (sinopse): {'Sim' if abs(statistics.mean(synopsis_lengths) - statistics.median(synopsis_lengths)) < statistics.stdev(synopsis_lengths) * 0.5 else 'Não'}

💡 **Recomendações:**
{self._generate_recommendations(books)}"""
    
    def _calculate_gini_coefficient(self, values: List[int]) -> float:
        """Calcular coeficiente de Gini para medir desigualdade"""
        if not values or sum(values) == 0:
            return 0.0
        
        sorted_values = sorted(values)
        n = len(sorted_values)
        cumsum = 0
        
        for i, value in enumerate(sorted_values):
            cumsum += (2 * (i + 1) - n - 1) * value
        
        return cumsum / (n * sum(sorted_values))
    
    def _calculate_shannon_entropy(self, counts: List[int]) -> float:
        """Calcular entropia de Shannon para medir diversidade"""
        if not counts or sum(counts) == 0:
            return 0.0
        
        total = sum(counts)
        entropy = 0.0
        
        for count in counts:
            if count > 0:
                proportion = count / total
                entropy -= proportion * math.log(proportion)
        
        return entropy
    
    def _interpret_hhi(self, hhi: float) -> str:
        """Interpretar índice HHI"""
        if hhi < 0.15:
            return "Baixa concentração"
        elif hhi < 0.25:
            return "Concentração moderada"
        else:
            return "Alta concentração"
    
    def _validate_book_format(self, book: Dict) -> bool:
        """Validar formato do livro"""
        required_fields = ["title", "author", "imprint", "release_date", "synopsis", "availability"]
        
        for field in required_fields:
            if not book.get(field):
                return False
        
        # Validar formato da data
        try:
            datetime.strptime(book["release_date"], "%d/%m/%Y")
        except ValueError:
            return False
        
        return True
    
    def _generate_recommendations(self, books: List[Dict]) -> str:
        """Gerar recomendações baseadas na análise"""
        recommendations = []
        
        # Análise de sinopses
        synopsis_lengths = [len(book.get("synopsis", "")) for book in books]
        if statistics.mean(synopsis_lengths) < 100:
            recommendations.append("• Considere expandir as sinopses (média atual muito baixa)")
        
        # Análise de distribuição
        total_availability = sum(len(book.get("availability", {})) for book in books)
        if total_availability / len(books) < 2:
            recommendations.append("• Ampliar rede de distribuição (poucos pontos de venda por livro)")
        
        # Análise temporal
        dates = []
        for book in books:
            try:
                date_obj = datetime.strptime(book["release_date"], "%d/%m/%Y")
                dates.append(date_obj)
            except:
                continue
        
        if dates:
            recent_books = sum(1 for date in dates if (datetime.now() - date).days < 365)
            if recent_books / len(dates) < 0.3:
                recommendations.append("• Acelerar cronograma de publicações (poucas publicações recentes)")
        
        return "\n".join(recommendations) if recommendations else "• Catálogo bem estruturado, manter qualidade atual"
    def detect_intent(self, user_input: str) -> str:
        """Detectar intenção e processar resposta"""
        user_input_lower = user_input.lower()
        
        # Verificar análises matemáticas e estatísticas
        math_patterns = [
            r"(?:análise|analise|analysis|estatística|estatistica|statistics|mathematical|matemática|matematica|metrics|métricas|report|relatório|relatorio)",
            r"(?:dados|data|números|numbers|insights|tendências|trends|padrões|patterns)",
            r"(?:publicação|publication|autor|author|mercado|market|editora|imprint|distribuição|distribution)"
        ]
        
        for pattern in math_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                return self.get_mathematical_analysis(user_input)
        
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
• 📊 **Análises matemáticas e estatísticas** - Ex: "Análise de publicações", "Estatísticas de autores", "Relatório do mercado"
• 🎫 **Suporte ao cliente** - Ex: "Preciso de ajuda com meu pedido"

**Novidade!** Agora também ofereço análises avançadas:
• 📈 Métricas de publicação por período
• 👨‍📚 Produtividade de autores  
• 🌍 Distribuição geográfica do mercado
• 🏢 Performance de editoras
• 📊 Relatórios estatísticos completos

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
