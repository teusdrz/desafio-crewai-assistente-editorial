#!/usr/bin/env python3
"""
Editorial Assistant - English Version
Complete implementation meeting CrewAI challenge requirements
Includes comprehensive mathematical and statistical analysis
"""

import json
import os
import re
import math
import statistics
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Tuple
from collections import Counter, defaultdict

class EditorialAssistant:
    """Editorial Assistant that meets all CrewAI challenge requirements"""
    
    def __init__(self):
        """Initialize the assistant"""
        self.data_path = "/Users/matheusviniciusdosreissouza/desafio-crewai-assistente-editorial/mock_catalog.json"
        self.tickets_path = "/Users/matheusviniciusdosreissouza/desafio-crewai-assistente-editorial/mock_tickets.json"
        
    def get_book_details(self, book_title: str) -> str:
        """Search for book details - Core CrewAI requirement"""
        try:
            with open(self.data_path, 'r', encoding='utf-8') as file:
                catalog_data = json.load(file)
            
            books = catalog_data.get("books", [])
            
            # Find book by title (case insensitive)
            found_book = None
            for book in books:
                if book["title"].lower() == book_title.lower():
                    found_book = book
                    break
            
            if not found_book:
                return f"❌ Sorry, book '{book_title}' not found in our catalog. We have {len(books)} books available."
            
            # Format availability information
            availability_text = "**Where to Buy:**\\n"
            for location, stores in found_book["availability"].items():
                stores_list = ", ".join(stores)
                availability_text += f"• **{location}:** {stores_list}\\n"
            
            return f"""📚 **{found_book["title"]}**
                    
**Author:** {found_book["author"]}
**Publisher:** {found_book["imprint"]}
**Release Date:** {found_book["release_date"]}

**Synopsis:** {found_book["synopsis"]}

{availability_text}"""
        
        except Exception as e:
            return f"❌ Error searching for book: {str(e)}"
    
    def find_stores(self, book_title: str, city: Optional[str] = None) -> str:
        """Find stores selling a book - Core CrewAI requirement"""
        try:
            with open(self.data_path, 'r', encoding='utf-8') as file:
                catalog_data = json.load(file)
            
            books = catalog_data.get("books", [])
            
            # Find book by title
            found_book = None
            for book in books:
                if book["title"].lower() == book_title.lower():
                    found_book = book
                    break
            
            if not found_book:
                return f"❌ Book '{book_title}' not found in catalog."
            
            availability = found_book.get("availability", {})
            
            if city:
                # Search for specific city
                city_stores = availability.get(city, [])
                online_stores = availability.get("Online", [])
                
                result = f"🏪 **Stores for '{book_title}' in {city}:**\\n"
                
                if city_stores:
                    result += f"**Physical Stores:** {', '.join(city_stores)}\\n"
                else:
                    result += "**Physical Stores:** Not available in this city\\n"
                
                if online_stores:
                    result += f"**Online Stores:** {', '.join(online_stores)}"
                
                return result
            else:
                # Return all availability
                result = f"🏪 **All stores for '{book_title}':**\\n"
                for location, stores in availability.items():
                    stores_list = ", ".join(stores)
                    result += f"• **{location}:** {stores_list}\\n"
                return result
                
        except Exception as e:
            return f"❌ Error finding stores: {str(e)}"
    
    def create_support_ticket(self, message: str) -> str:
        """Create support ticket - Core CrewAI requirement"""
        try:
            # Generate unique ticket ID
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            ticket_id = f"TICKET-{timestamp[-6:]}"
            
            # Create ticket object
            ticket = {
                "id": ticket_id,
                "message": message,
                "status": "open",
                "timestamp": datetime.now().isoformat(),
                "created_date": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            }
            
            # Load existing tickets
            try:
                with open(self.tickets_path, 'r', encoding='utf-8') as file:
                    tickets_data = json.load(file)
            except FileNotFoundError:
                tickets_data = []
            
            # Add new ticket
            tickets_data.append(ticket)
            
            # Save updated tickets
            with open(self.tickets_path, 'w', encoding='utf-8') as file:
                json.dump(tickets_data, file, indent=2, ensure_ascii=False)
            
            return f"""🎫 **Support Ticket Created**

**Ticket ID:** {ticket_id}
**Status:** Open
**Message:** {message}

✅ Your ticket has been created successfully! Our support team will contact you within 24 hours.

📧 To track your ticket, use ID: {ticket_id}"""
        
        except Exception as e:
            return f"❌ Error creating ticket: {str(e)}"
    
    def get_mathematical_analysis(self, query: str) -> str:
        """Comprehensive mathematical analysis - Value-added feature"""
        try:
            with open(self.data_path, 'r', encoding='utf-8') as file:
                catalog_data = json.load(file)
            
            books = catalog_data.get("books", [])
            
            if not books:
                return "❌ No books available for analysis"
            
            # Comprehensive analysis
            analysis_results = []
            analysis_results.append("📊 **Comprehensive Editorial Catalog Analysis**\\n")
            
            # General overview
            analysis_results.append("📚 **Overview:**")
            analysis_results.append(f"• Total books in catalog: {len(books)}")
            analysis_results.append(f"• Data completeness: {self._calculate_data_completeness(books):.1f}%")
            analysis_results.append(f"• Analysis date: {datetime.now().strftime('%d/%m/%Y')}\\n")
            
            # Content analysis
            synopsis_lengths = [len(book.get('synopsis', '')) for book in books]
            title_lengths = [len(book.get('title', '')) for book in books]
            
            analysis_results.append("📝 **Content Analysis:**")
            analysis_results.append(f"• Average synopsis length: {statistics.mean(synopsis_lengths):.1f} characters")
            analysis_results.append(f"• Average title length: {statistics.mean(title_lengths):.1f} characters")
            analysis_results.append(f"• Longest synopsis: {max(synopsis_lengths)} characters")
            analysis_results.append(f"• Shortest synopsis: {min(synopsis_lengths)} characters\\n")
            
            # Quality metrics
            analysis_results.append("🏆 **Quality Metrics:**")
            quality_score = self._calculate_quality_score(books)
            analysis_results.append(f"• Data quality score: {quality_score:.1f}/100")
            analysis_results.append(f"• Format consistency: {self._calculate_format_consistency(books):.1f}%\\n")
            
            # Statistical insights
            analysis_results.append("🔍 **Statistical Insights:**")
            synopsis_cv = (statistics.stdev(synopsis_lengths) / statistics.mean(synopsis_lengths)) * 100
            analysis_results.append(f"• Coefficient of variation (synopsis): {synopsis_cv:.2f}%")
            analysis_results.append(f"• Median vs Mean (title): {statistics.median(title_lengths)} vs {statistics.mean(title_lengths):.1f}")
            
            # Check for normal distribution
            is_normal = self._test_normality(synopsis_lengths)
            analysis_results.append(f"• Normal distribution (synopsis): {'Yes' if is_normal else 'No'}\\n")
            
            # Advanced analytics
            analysis_results.extend(self._advanced_publisher_analysis(books))
            analysis_results.extend(self._temporal_analysis(books))
            analysis_results.extend(self._market_concentration_analysis(books))
            
            # Recommendations
            analysis_results.append("💡 **Recommendations:**")
            recommendations = self._generate_strategic_recommendations(books)
            analysis_results.extend(recommendations)
            
            return "\\n".join(analysis_results)
            
        except Exception as e:
            return f"❌ Error in mathematical analysis: {str(e)}"
    
    def _calculate_data_completeness(self, books: List[Dict]) -> float:
        """Calculate data completeness percentage"""
        required_fields = ['title', 'author', 'imprint', 'release_date', 'synopsis', 'availability']
        total_fields = len(books) * len(required_fields)
        complete_fields = 0
        
        for book in books:
            for field in required_fields:
                if field in book and book[field]:
                    complete_fields += 1
        
        return (complete_fields / total_fields) * 100 if total_fields > 0 else 0
    
    def _calculate_quality_score(self, books: List[Dict]) -> float:
        """Calculate overall quality score"""
        scores = []
        
        for book in books:
            book_score = 0
            
            # Check completeness
            if all(field in book and book[field] for field in ['title', 'author', 'synopsis']):
                book_score += 40
            
            # Check synopsis quality
            synopsis_length = len(book.get('synopsis', ''))
            if 50 <= synopsis_length <= 300:
                book_score += 30
            
            # Check availability
            availability = book.get('availability', {})
            if availability and len(availability) >= 1:
                book_score += 30
            
            scores.append(book_score)
        
        return statistics.mean(scores) if scores else 0
    
    def _calculate_format_consistency(self, books: List[Dict]) -> float:
        """Calculate format consistency"""
        consistent_count = 0
        
        for book in books:
            # Check date format consistency
            date_str = book.get('release_date', '')
            if re.match(r'\\d{2}/\\d{2}/\\d{4}', date_str):
                consistent_count += 1
        
        return (consistent_count / len(books)) * 100 if books else 0
    
    def _test_normality(self, data: List[float]) -> bool:
        """Simple normality test using skewness"""
        if len(data) < 3:
            return False
        
        mean_val = statistics.mean(data)
        std_val = statistics.stdev(data)
        
        # Calculate skewness
        n = len(data)
        skewness = sum(((x - mean_val) / std_val) ** 3 for x in data) / n
        
        # Consider normal if skewness is close to 0
        return abs(skewness) < 1.0
    
    def _advanced_publisher_analysis(self, books: List[Dict]) -> List[str]:
        """Advanced publisher analysis"""
        publisher_counts = Counter(book.get('imprint', 'Unknown') for book in books)
        
        results = ["📈 **Publisher Analysis:**"]
        
        # Publisher distribution
        for publisher, count in publisher_counts.most_common():
            percentage = (count / len(books)) * 100
            results.append(f"• {publisher}: {count} books ({percentage:.1f}%)")
        
        # Market concentration (HHI)
        hhi = self._calculate_hhi([count for count in publisher_counts.values()])
        results.append(f"• Herfindahl-Hirschman Index: {hhi:.4f}")
        results.append(f"• Market interpretation: {self._interpret_hhi(hhi)}")
        
        return results + [""]
    
    def _temporal_analysis(self, books: List[Dict]) -> List[str]:
        """Temporal publication analysis"""
        results = ["📅 **Temporal Analysis:**"]
        
        publication_years = []
        for book in books:
            date_str = book.get('release_date', '')
            if '/' in date_str:
                try:
                    year = int(date_str.split('/')[-1])
                    publication_years.append(year)
                except ValueError:
                    continue
        
        if publication_years:
            year_counts = Counter(publication_years)
            results.append(f"• Publication span: {min(publication_years)} - {max(publication_years)}")
            results.append(f"• Most productive year: {year_counts.most_common(1)[0][0]} ({year_counts.most_common(1)[0][1]} books)")
            results.append(f"• Average publications per year: {len(publication_years) / (max(publication_years) - min(publication_years) + 1):.1f}")
        
        return results + [""]
    
    def _market_concentration_analysis(self, books: List[Dict]) -> List[str]:
        """Market concentration analysis"""
        results = ["🎯 **Market Concentration:**"]
        
        # Calculate diversity metrics
        publisher_counts = Counter(book.get('imprint', 'Unknown') for book in books)
        
        # Shannon Entropy
        total_books = sum(publisher_counts.values())
        shannon_entropy = -sum((count/total_books) * math.log2(count/total_books) 
                              for count in publisher_counts.values() if count > 0)
        
        # Gini Coefficient
        gini = self._calculate_gini_coefficient(list(publisher_counts.values()))
        
        results.append(f"• Shannon Entropy: {shannon_entropy:.4f}")
        results.append(f"• Gini Coefficient: {gini:.4f}")
        results.append(f"• Portfolio Diversity: {self._interpret_diversity(shannon_entropy, len(publisher_counts))}")
        
        return results + [""]
    
    def _calculate_hhi(self, market_shares: List[int]) -> float:
        """Calculate Herfindahl-Hirschman Index"""
        total = sum(market_shares)
        if total == 0:
            return 0
        
        proportions = [share / total for share in market_shares]
        return sum(p ** 2 for p in proportions)
    
    def _calculate_gini_coefficient(self, values: List[int]) -> float:
        """Calculate Gini coefficient for inequality measurement"""
        if not values or all(v == 0 for v in values):
            return 0
        
        sorted_values = sorted(values)
        n = len(values)
        cumsum = sum((i + 1) * v for i, v in enumerate(sorted_values))
        
        return (2 * cumsum) / (n * sum(values)) - (n + 1) / n
    
    def _interpret_hhi(self, hhi: float) -> str:
        """Interpret HHI value"""
        if hhi < 0.15:
            return "Competitive market"
        elif hhi < 0.25:
            return "Moderately concentrated"
        else:
            return "Highly concentrated"
    
    def _interpret_diversity(self, entropy: float, num_publishers: int) -> str:
        """Interpret diversity metrics"""
        max_entropy = math.log2(num_publishers) if num_publishers > 1 else 0
        diversity_ratio = entropy / max_entropy if max_entropy > 0 else 0
        
        if diversity_ratio > 0.8:
            return "Highly diverse"
        elif diversity_ratio > 0.5:
            return "Moderately diverse"
        else:
            return "Low diversity"
    
    def _generate_strategic_recommendations(self, books: List[Dict]) -> List[str]:
        """Generate strategic recommendations"""
        recommendations = []
        
        # Analyze publication timing
        publication_years = []
        for book in books:
            date_str = book.get('release_date', '')
            if '/' in date_str:
                try:
                    year = int(date_str.split('/')[-1])
                    publication_years.append(year)
                except ValueError:
                    continue
        
        if publication_years:
            recent_books = sum(1 for year in publication_years if year >= 2023)
            if recent_books < len(books) * 0.3:
                recommendations.append("• Accelerate publication schedule (few recent publications)")
        
        # Analyze publisher balance
        publisher_counts = Counter(book.get('imprint', 'Unknown') for book in books)
        if len(publisher_counts) == 1:
            recommendations.append("• Consider diversifying publisher portfolio")
        
        # Analyze synopsis quality
        synopsis_lengths = [len(book.get('synopsis', '')) for book in books]
        avg_length = statistics.mean(synopsis_lengths)
        if avg_length < 100:
            recommendations.append("• Improve synopsis quality and length")
        
        if not recommendations:
            recommendations.append("• Current catalog shows good balance and quality")
        
        return recommendations
    
    def detect_intent(self, user_input: str) -> str:
        """Detect user intent from input - Enhanced for mathematical analysis"""
        user_input_lower = user_input.lower()
        
        # Mathematical analysis patterns
        math_patterns = [
            r"mathematical analysis", r"statistics", r"analysis", r"metrics",
            r"data analysis", r"numbers", r"calculate", r"mathematical",
            r"statistical", r"analytics", r"insights"
        ]
        
        # Book details patterns  
        book_patterns = [
            r"details about", r"tell me about", r"information about",
            r"what is", r"describe", r"book", r"author", r"synopsis"
        ]
        
        # Store finder patterns
        store_patterns = [
            r"where.*buy", r"find.*store", r"purchase", r"available",
            r"bookstore", r"shop", r"location", r"where.*find"
        ]
        
        # Support patterns
        support_patterns = [
            r"help", r"support", r"ticket", r"problem", r"issue",
            r"assistance", r"contact", r"question"
        ]
        
        # Check patterns in order of specificity
        for pattern in math_patterns:
            if re.search(pattern, user_input_lower):
                return "mathematical_analysis"
        
        for pattern in book_patterns:
            if re.search(pattern, user_input_lower):
                return "book_details"
                
        for pattern in store_patterns:
            if re.search(pattern, user_input_lower):
                return "find_stores"
                
        for pattern in support_patterns:
            if re.search(pattern, user_input_lower):
                return "support_ticket"
        
        # Default to general inquiry
        return "general_inquiry"


def main():
    """Main function for testing"""
    print("🎯 Editorial Assistant - CrewAI Challenge Implementation")
    print("=" * 60)
    print("✅ All original requirements implemented")
    print("🚀 Enhanced with mathematical analysis")
    print("=" * 60)
    
    assistant = EditorialAssistant()
    
    print("\\n📚 Testing book details:")
    print(assistant.get_book_details("A Abelha"))
    
    print("\\n🏪 Testing store finder:")
    print(assistant.find_stores("A Abelha", "São Paulo"))
    
    print("\\n🎫 Testing support ticket:")
    print(assistant.create_support_ticket("I need help finding a science fiction book"))
    
    print("\\n📊 Testing mathematical analysis:")
    result = assistant.get_mathematical_analysis("Complete catalog analysis")
    print(result[:500] + "..." if len(result) > 500 else result)

if __name__ == "__main__":
    main()
