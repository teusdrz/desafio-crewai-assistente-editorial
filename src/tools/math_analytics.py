#!/usr/bin/env python3
"""
Mathematical and Statistical Analytics for Editorial Assistant
Comprehensive mathematical tools for catalog analysis and insights.
"""

import json
import math
import statistics
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple, Optional
from collections import Counter, defaultdict
import re


class EditorialMathAnalytics:
    """Advanced mathematical and statistical analytics for editorial data"""
    
    def __init__(self, catalog_path: str):
        """Initialize with catalog data"""
        self.catalog_path = catalog_path
        self.books_data = self._load_catalog()
        
    def _load_catalog(self) -> List[Dict]:
        """Load and parse catalog data"""
        try:
            with open(self.catalog_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return data.get("books", [])
        except Exception as e:
            print(f"Error loading catalog: {e}")
            return []
    
    def calculate_publication_statistics(self) -> Dict[str, Any]:
        """Calculate comprehensive publication statistics"""
        if not self.books_data:
            return {"error": "No data available"}
        
        # Parse release dates
        dates = []
        for book in self.books_data:
            try:
                date_str = book.get("release_date", "")
                if date_str:
                    date_obj = datetime.strptime(date_str, "%d/%m/%Y")
                    dates.append(date_obj)
            except ValueError:
                continue
        
        if not dates:
            return {"error": "No valid dates found"}
        
        # Calculate time-based statistics
        years = [date.year for date in dates]
        months = [date.month for date in dates]
        
        # Statistical measures
        stats = {
            "total_books": len(self.books_data),
            "publication_span": {
                "earliest": min(dates).strftime("%d/%m/%Y"),
                "latest": max(dates).strftime("%d/%m/%Y"),
                "span_days": (max(dates) - min(dates)).days,
                "span_years": round((max(dates) - min(dates)).days / 365.25, 2)
            },
            "yearly_distribution": {
                "mean_year": round(statistics.mean(years), 2),
                "median_year": statistics.median(years),
                "mode_year": statistics.mode(years) if years else None,
                "std_deviation": round(statistics.stdev(years), 2) if len(years) > 1 else 0,
                "variance": round(statistics.variance(years), 2) if len(years) > 1 else 0
            },
            "monthly_patterns": {
                "distribution": dict(Counter(months)),
                "peak_month": max(Counter(months).items(), key=lambda x: x[1])[0],
                "seasonal_analysis": self._analyze_seasonal_patterns(months)
            },
            "publication_frequency": self._calculate_publication_frequency(dates)
        }
        
        return stats
    
    def _analyze_seasonal_patterns(self, months: List[int]) -> Dict[str, Any]:
        """Analyze seasonal publication patterns"""
        seasons = {
            "Spring": [3, 4, 5],    # March, April, May
            "Summer": [6, 7, 8],    # June, July, August
            "Autumn": [9, 10, 11],  # September, October, November
            "Winter": [12, 1, 2]    # December, January, February
        }
        
        seasonal_counts = {}
        for season, season_months in seasons.items():
            count = sum(1 for month in months if month in season_months)
            seasonal_counts[season] = count
        
        total = sum(seasonal_counts.values())
        seasonal_percentages = {
            season: round((count / total) * 100, 2) if total > 0 else 0
            for season, count in seasonal_counts.items()
        }
        
        return {
            "counts": seasonal_counts,
            "percentages": seasonal_percentages,
            "dominant_season": max(seasonal_counts, key=seasonal_counts.get)
        }
    
    def _calculate_publication_frequency(self, dates: List[datetime]) -> Dict[str, Any]:
        """Calculate publication frequency metrics"""
        if len(dates) < 2:
            return {"error": "Insufficient data for frequency analysis"}
        
        sorted_dates = sorted(dates)
        intervals = []
        
        for i in range(1, len(sorted_dates)):
            interval_days = (sorted_dates[i] - sorted_dates[i-1]).days
            intervals.append(interval_days)
        
        return {
            "average_interval_days": round(statistics.mean(intervals), 2),
            "median_interval_days": statistics.median(intervals),
            "min_interval_days": min(intervals),
            "max_interval_days": max(intervals),
            "std_deviation_days": round(statistics.stdev(intervals), 2) if len(intervals) > 1 else 0,
            "publications_per_year": round(365.25 / statistics.mean(intervals), 2) if statistics.mean(intervals) > 0 else 0
        }
    
    def analyze_author_productivity(self) -> Dict[str, Any]:
        """Comprehensive author productivity analysis"""
        author_books = defaultdict(list)
        
        for book in self.books_data:
            author = book.get("author", "Unknown")
            author_books[author].append(book)
        
        # Calculate productivity metrics
        productivity_stats = {}
        author_book_counts = [len(books) for books in author_books.values()]
        
        if author_book_counts:
            productivity_stats = {
                "total_authors": len(author_books),
                "books_per_author": {
                    "mean": round(statistics.mean(author_book_counts), 2),
                    "median": statistics.median(author_book_counts),
                    "mode": statistics.mode(author_book_counts) if author_book_counts else None,
                    "std_deviation": round(statistics.stdev(author_book_counts), 2) if len(author_book_counts) > 1 else 0,
                    "min": min(author_book_counts),
                    "max": max(author_book_counts)
                },
                "productivity_distribution": dict(Counter(author_book_counts)),
                "top_authors": sorted(
                    [(author, len(books)) for author, books in author_books.items()],
                    key=lambda x: x[1],
                    reverse=True
                )[:5],
                "collaboration_index": self._calculate_collaboration_index(author_books)
            }
        
        return productivity_stats
    
    def _calculate_collaboration_index(self, author_books: Dict[str, List]) -> Dict[str, Any]:
        """Calculate author collaboration metrics"""
        single_author_books = sum(1 for books in author_books.values() if len(books) == 1)
        multi_author_books = sum(1 for books in author_books.values() if len(books) > 1)
        total_books = len(self.books_data)
        
        return {
            "single_author_percentage": round((single_author_books / total_books) * 100, 2) if total_books > 0 else 0,
            "multi_author_percentage": round((multi_author_books / total_books) * 100, 2) if total_books > 0 else 0,
            "average_books_per_productive_author": round(
                sum(len(books) for books in author_books.values() if len(books) > 1) / max(1, multi_author_books), 2
            )
        }
    
    def analyze_market_distribution(self) -> Dict[str, Any]:
        """Analyze geographical market distribution"""
        city_availability = defaultdict(int)
        online_stores = defaultdict(int)
        total_availability_points = 0
        
        for book in self.books_data:
            availability = book.get("availability", {})
            
            for location, stores in availability.items():
                if location.lower() == "online":
                    for store in stores:
                        online_stores[store] += 1
                else:
                    city_availability[location] += 1
                    total_availability_points += len(stores)
        
        # Calculate distribution metrics
        city_counts = list(city_availability.values())
        online_counts = list(online_stores.values())
        
        market_stats = {
            "geographical_distribution": {
                "total_cities": len(city_availability),
                "total_physical_stores": total_availability_points,
                "cities_per_book": round(sum(city_counts) / len(self.books_data), 2) if self.books_data else 0,
                "city_coverage": {
                    "mean": round(statistics.mean(city_counts), 2) if city_counts else 0,
                    "median": statistics.median(city_counts) if city_counts else 0,
                    "std_deviation": round(statistics.stdev(city_counts), 2) if len(city_counts) > 1 else 0,
                    "top_cities": sorted(city_availability.items(), key=lambda x: x[1], reverse=True)[:5]
                }
            },
            "online_distribution": {
                "total_online_stores": len(online_stores),
                "online_presence": {
                    "mean": round(statistics.mean(online_counts), 2) if online_counts else 0,
                    "median": statistics.median(online_counts) if online_counts else 0,
                    "std_deviation": round(statistics.stdev(online_counts), 2) if len(online_counts) > 1 else 0,
                    "top_online_stores": sorted(online_stores.items(), key=lambda x: x[1], reverse=True)
                }
            },
            "market_penetration": self._calculate_market_penetration(city_availability, online_stores)
        }
        
        return market_stats
    
    def _calculate_market_penetration(self, cities: Dict, online: Dict) -> Dict[str, Any]:
        """Calculate market penetration metrics"""
        total_books = len(self.books_data)
        
        physical_coverage = sum(cities.values())
        online_coverage = sum(online.values())
        total_coverage = physical_coverage + online_coverage
        
        return {
            "physical_penetration_rate": round((physical_coverage / total_books) * 100, 2) if total_books > 0 else 0,
            "online_penetration_rate": round((online_coverage / total_books) * 100, 2) if total_books > 0 else 0,
            "total_penetration_rate": round((total_coverage / total_books) * 100, 2) if total_books > 0 else 0,
            "distribution_efficiency": self._calculate_distribution_efficiency(cities, online)
        }
    
    def _calculate_distribution_efficiency(self, cities: Dict, online: Dict) -> Dict[str, Any]:
        """Calculate distribution efficiency metrics"""
        if not cities and not online:
            return {"error": "No distribution data available"}
        
        # Gini coefficient for distribution inequality
        all_values = list(cities.values()) + list(online.values())
        n = len(all_values)
        
        if n == 0:
            return {"gini_coefficient": 0, "distribution_balance": "Perfect"}
        
        # Sort values
        sorted_values = sorted(all_values)
        
        # Calculate Gini coefficient
        cumsum = 0
        for i, value in enumerate(sorted_values):
            cumsum += (2 * (i + 1) - n - 1) * value
        
        gini = cumsum / (n * sum(sorted_values)) if sum(sorted_values) > 0 else 0
        
        # Interpret distribution balance
        if gini < 0.2:
            balance = "Highly Balanced"
        elif gini < 0.4:
            balance = "Moderately Balanced"
        elif gini < 0.6:
            balance = "Moderately Unbalanced"
        else:
            balance = "Highly Unbalanced"
        
        return {
            "gini_coefficient": round(gini, 4),
            "distribution_balance": balance,
            "concentration_ratio": round(max(all_values) / sum(all_values) * 100, 2) if sum(all_values) > 0 else 0
        }
    
    def calculate_imprint_analysis(self) -> Dict[str, Any]:
        """Analyze publisher imprint performance"""
        imprint_data = defaultdict(list)
        
        for book in self.books_data:
            imprint = book.get("imprint", "Unknown")
            imprint_data[imprint].append(book)
        
        imprint_stats = {}
        imprint_counts = [len(books) for books in imprint_data.values()]
        
        if imprint_counts:
            imprint_stats = {
                "total_imprints": len(imprint_data),
                "books_per_imprint": {
                    "mean": round(statistics.mean(imprint_counts), 2),
                    "median": statistics.median(imprint_counts),
                    "std_deviation": round(statistics.stdev(imprint_counts), 2) if len(imprint_counts) > 1 else 0,
                    "distribution": dict(Counter(imprint_counts))
                },
                "imprint_performance": sorted(
                    [(imprint, len(books)) for imprint, books in imprint_data.items()],
                    key=lambda x: x[1],
                    reverse=True
                ),
                "market_share": {
                    imprint: round((len(books) / len(self.books_data)) * 100, 2)
                    for imprint, books in imprint_data.items()
                },
                "concentration_metrics": self._calculate_imprint_concentration(imprint_data)
            }
        
        return imprint_stats
    
    def _calculate_imprint_concentration(self, imprint_data: Dict) -> Dict[str, Any]:
        """Calculate market concentration metrics for imprints"""
        book_counts = sorted([len(books) for books in imprint_data.values()], reverse=True)
        total_books = sum(book_counts)
        
        if total_books == 0:
            return {"error": "No data available"}
        
        # Herfindahl-Hirschman Index (HHI)
        hhi = sum((count / total_books) ** 2 for count in book_counts)
        
        # Top 3 concentration ratio (CR3)
        cr3 = sum(book_counts[:3]) / total_books if len(book_counts) >= 3 else sum(book_counts) / total_books
        
        # Market concentration interpretation
        if hhi < 0.15:
            concentration_level = "Low Concentration"
        elif hhi < 0.25:
            concentration_level = "Moderate Concentration"
        else:
            concentration_level = "High Concentration"
        
        return {
            "herfindahl_hirschman_index": round(hhi, 4),
            "concentration_ratio_top3": round(cr3 * 100, 2),
            "market_concentration_level": concentration_level,
            "effective_number_of_competitors": round(1 / hhi, 2) if hhi > 0 else float('inf')
        }
    
    def generate_comprehensive_report(self) -> Dict[str, Any]:
        """Generate a comprehensive mathematical and statistical report"""
        report = {
            "analysis_timestamp": datetime.now().isoformat(),
            "dataset_overview": {
                "total_books": len(self.books_data),
                "data_completeness": self._calculate_data_completeness()
            },
            "publication_analytics": self.calculate_publication_statistics(),
            "author_analytics": self.analyze_author_productivity(),
            "market_analytics": self.analyze_market_distribution(),
            "imprint_analytics": self.calculate_imprint_analysis(),
            "advanced_metrics": self._calculate_advanced_metrics()
        }
        
        return report
    
    def _calculate_data_completeness(self) -> Dict[str, Any]:
        """Calculate data completeness metrics"""
        required_fields = ["title", "author", "imprint", "release_date", "synopsis", "availability"]
        field_completeness = {}
        
        for field in required_fields:
            complete_count = sum(1 for book in self.books_data if book.get(field))
            field_completeness[field] = round((complete_count / len(self.books_data)) * 100, 2) if self.books_data else 0
        
        overall_completeness = round(statistics.mean(field_completeness.values()), 2) if field_completeness else 0
        
        return {
            "field_completeness": field_completeness,
            "overall_completeness": overall_completeness,
            "data_quality_score": self._calculate_data_quality_score()
        }
    
    def _calculate_data_quality_score(self) -> float:
        """Calculate overall data quality score"""
        if not self.books_data:
            return 0.0
        
        quality_scores = []
        
        for book in self.books_data:
            book_score = 0
            max_score = 0
            
            # Title completeness (weight: 20%)
            if book.get("title"):
                book_score += 20
            max_score += 20
            
            # Author completeness (weight: 20%)
            if book.get("author"):
                book_score += 20
            max_score += 20
            
            # Synopsis length (weight: 15%)
            synopsis = book.get("synopsis", "")
            if len(synopsis) > 50:
                book_score += 15
            elif len(synopsis) > 20:
                book_score += 10
            elif len(synopsis) > 0:
                book_score += 5
            max_score += 15
            
            # Date format validation (weight: 15%)
            release_date = book.get("release_date", "")
            if self._validate_date_format(release_date):
                book_score += 15
            max_score += 15
            
            # Availability completeness (weight: 30%)
            availability = book.get("availability", {})
            if availability:
                if len(availability) >= 3:
                    book_score += 30
                elif len(availability) >= 2:
                    book_score += 20
                elif len(availability) >= 1:
                    book_score += 10
            max_score += 30
            
            quality_scores.append((book_score / max_score) * 100 if max_score > 0 else 0)
        
        return round(statistics.mean(quality_scores), 2) if quality_scores else 0.0
    
    def _validate_date_format(self, date_str: str) -> bool:
        """Validate date format DD/MM/YYYY"""
        try:
            datetime.strptime(date_str, "%d/%m/%Y")
            return True
        except ValueError:
            return False
    
    def _calculate_advanced_metrics(self) -> Dict[str, Any]:
        """Calculate advanced mathematical metrics"""
        if not self.books_data:
            return {"error": "No data available"}
        
        # Text complexity analysis
        synopsis_lengths = [len(book.get("synopsis", "")) for book in self.books_data]
        title_lengths = [len(book.get("title", "")) for book in self.books_data]
        
        # Advanced statistical measures
        advanced_stats = {
            "text_analytics": {
                "synopsis_complexity": {
                    "mean_length": round(statistics.mean(synopsis_lengths), 2) if synopsis_lengths else 0,
                    "median_length": statistics.median(synopsis_lengths) if synopsis_lengths else 0,
                    "length_variance": round(statistics.variance(synopsis_lengths), 2) if len(synopsis_lengths) > 1 else 0,
                    "coefficient_of_variation": round(
                        (statistics.stdev(synopsis_lengths) / statistics.mean(synopsis_lengths)) * 100, 2
                    ) if synopsis_lengths and statistics.mean(synopsis_lengths) > 0 else 0
                },
                "title_analytics": {
                    "mean_title_length": round(statistics.mean(title_lengths), 2) if title_lengths else 0,
                    "title_length_distribution": dict(Counter(title_lengths)),
                    "optimal_title_length_range": self._find_optimal_title_range(title_lengths)
                }
            },
            "diversity_indices": self._calculate_diversity_indices(),
            "correlation_analysis": self._calculate_correlations()
        }
        
        return advanced_stats
    
    def _find_optimal_title_range(self, lengths: List[int]) -> Dict[str, Any]:
        """Find optimal title length range based on statistical analysis"""
        if not lengths:
            return {"error": "No title data available"}
        
        mean_length = statistics.mean(lengths)
        std_dev = statistics.stdev(lengths) if len(lengths) > 1 else 0
        
        optimal_min = max(1, round(mean_length - std_dev))
        optimal_max = round(mean_length + std_dev)
        
        return {
            "optimal_range": [optimal_min, optimal_max],
            "mean_based_recommendation": round(mean_length),
            "titles_in_optimal_range": sum(1 for length in lengths if optimal_min <= length <= optimal_max),
            "percentage_optimal": round(
                (sum(1 for length in lengths if optimal_min <= length <= optimal_max) / len(lengths)) * 100, 2
            )
        }
    
    def _calculate_diversity_indices(self) -> Dict[str, Any]:
        """Calculate diversity indices for various categorical variables"""
        # Author diversity (Shannon entropy)
        authors = [book.get("author", "Unknown") for book in self.books_data]
        author_counts = Counter(authors)
        author_diversity = self._shannon_entropy(list(author_counts.values()))
        
        # Imprint diversity
        imprints = [book.get("imprint", "Unknown") for book in self.books_data]
        imprint_counts = Counter(imprints)
        imprint_diversity = self._shannon_entropy(list(imprint_counts.values()))
        
        return {
            "author_diversity": {
                "shannon_entropy": round(author_diversity, 4),
                "effective_number_of_authors": round(math.exp(author_diversity), 2),
                "evenness_index": round(author_diversity / math.log(len(author_counts)), 4) if len(author_counts) > 1 else 0
            },
            "imprint_diversity": {
                "shannon_entropy": round(imprint_diversity, 4),
                "effective_number_of_imprints": round(math.exp(imprint_diversity), 2),
                "evenness_index": round(imprint_diversity / math.log(len(imprint_counts)), 4) if len(imprint_counts) > 1 else 0
            }
        }
    
    def _shannon_entropy(self, counts: List[int]) -> float:
        """Calculate Shannon entropy for diversity measurement"""
        if not counts or sum(counts) == 0:
            return 0.0
        
        total = sum(counts)
        entropy = 0.0
        
        for count in counts:
            if count > 0:
                proportion = count / total
                entropy -= proportion * math.log(proportion)
        
        return entropy
    
    def _calculate_correlations(self) -> Dict[str, Any]:
        """Calculate correlations between various metrics"""
        # Extract numerical features for correlation analysis
        features = []
        
        for book in self.books_data:
            try:
                # Convert date to days since epoch for correlation
                date_str = book.get("release_date", "")
                if date_str:
                    date_obj = datetime.strptime(date_str, "%d/%m/%Y")
                    days_since_epoch = (date_obj - datetime(1970, 1, 1)).days
                else:
                    days_since_epoch = 0
                
                # Calculate features
                synopsis_length = len(book.get("synopsis", ""))
                title_length = len(book.get("title", ""))
                availability_count = len(book.get("availability", {}))
                
                features.append({
                    "days_since_epoch": days_since_epoch,
                    "synopsis_length": synopsis_length,
                    "title_length": title_length,
                    "availability_count": availability_count
                })
            except:
                continue
        
        if len(features) < 2:
            return {"error": "Insufficient data for correlation analysis"}
        
        # Calculate correlations
        correlations = {}
        feature_names = ["days_since_epoch", "synopsis_length", "title_length", "availability_count"]
        
        for i, feature1 in enumerate(feature_names):
            for j, feature2 in enumerate(feature_names):
                if i < j:  # Only calculate upper triangle
                    values1 = [f[feature1] for f in features if f[feature1] is not None]
                    values2 = [f[feature2] for f in features if f[feature2] is not None]
                    
                    if len(values1) == len(values2) and len(values1) > 1:
                        correlation = self._pearson_correlation(values1, values2)
                        correlations[f"{feature1}_vs_{feature2}"] = round(correlation, 4)
        
        return correlations
    
    def _pearson_correlation(self, x: List[float], y: List[float]) -> float:
        """Calculate Pearson correlation coefficient"""
        if len(x) != len(y) or len(x) < 2:
            return 0.0
        
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(a * b for a, b in zip(x, y))
        sum_x2 = sum(a * a for a in x)
        sum_y2 = sum(a * a for a in y)
        
        numerator = n * sum_xy - sum_x * sum_y
        denominator = math.sqrt((n * sum_x2 - sum_x * sum_x) * (n * sum_y2 - sum_y * sum_y))
        
        if denominator == 0:
            return 0.0
        
        return numerator / denominator


def get_catalog_analytics(query_type: str = "comprehensive") -> str:
    """
    Get mathematical and statistical analytics for the editorial catalog.
    
    Args:
        query_type: Type of analysis ("comprehensive", "publications", "authors", "market", "imprints")
    
    Returns:
        Formatted analytical report
    """
    catalog_path = "/Users/matheusviniciusdosreissouza/desafio-crewai-assistente-editorial/data/mock_catalog.json"
    analytics = EditorialMathAnalytics(catalog_path)
    
    try:
        if query_type.lower() == "publications":
            result = analytics.calculate_publication_statistics()
        elif query_type.lower() == "authors":
            result = analytics.analyze_author_productivity()
        elif query_type.lower() == "market":
            result = analytics.analyze_market_distribution()
        elif query_type.lower() == "imprints":
            result = analytics.calculate_imprint_analysis()
        else:  # comprehensive
            result = analytics.generate_comprehensive_report()
        
        return f"📊 **Análise Matemática e Estatística do Catálogo Editorial**\n\n```json\n{json.dumps(result, indent=2, ensure_ascii=False)}\n```"
    
    except Exception as e:
        return f"❌ Erro na análise: {str(e)}"


if __name__ == "__main__":
    # Test the analytics system
    print("Testing Editorial Math Analytics...")
    print(get_catalog_analytics("comprehensive"))
