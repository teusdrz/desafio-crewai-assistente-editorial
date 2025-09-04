#!/usr/bin/env python3
"""
Advanced Business Intelligence System - English Version
Complex mathematical algorithms for editorial market analysis
"""

import json
import math
import statistics
from datetime import datetime
from typing import List, Dict, Any, Tuple, Optional
from collections import Counter, defaultdict
from dataclasses import dataclass


@dataclass
class MarketIntelligence:
    """Data structure for market intelligence metrics"""
    herfindahl_hirschman_index: float
    shannon_entropy: float
    gini_coefficient: float
    portfolio_diversity_index: float
    market_concentration_level: str


class AdvancedBusinessIntelligence:
    """
    Advanced Business Intelligence system with complex mathematical algorithms
    for comprehensive editorial market analysis
    """
    
    def __init__(self, catalog_path: str = None):
        """Initialize the advanced BI system"""
        self.catalog_path = catalog_path or "/Users/matheusviniciusdosreissouza/desafio-crewai-assistente-editorial/mock_catalog.json"
        self.books_data = self._load_catalog_data()
        self.total_books = len(self.books_data)
        
    def _load_catalog_data(self) -> List[Dict]:
        """Load catalog data from JSON file"""
        try:
            with open(self.catalog_path, 'r', encoding='utf-8') as file:
                catalog_data = json.load(file)
                return catalog_data.get("books", [])
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Warning: Could not load catalog data: {e}")
            return []
    
    def generate_comprehensive_report(self) -> Dict[str, Any]:
        """Generate comprehensive business intelligence report"""
        if not self.books_data:
            return {"error": "No data available for analysis"}
        
        return {
            "market_intelligence": self._calculate_market_intelligence(),
            "competitive_analysis": self._perform_competitive_analysis(), 
            "temporal_dynamics": self._analyze_temporal_dynamics(),
            "predictive_indicators": self._calculate_predictive_indicators(),
            "portfolio_optimization": self._analyze_portfolio_optimization()
        }
    
    def _calculate_market_intelligence(self) -> Dict[str, Any]:
        """Calculate comprehensive market intelligence metrics"""
        
        # Publisher distribution analysis
        publisher_counts = Counter(book.get('imprint', 'Unknown') for book in self.books_data)
        total_publications = sum(publisher_counts.values())
        
        # Herfindahl-Hirschman Index (Market Concentration)
        hhi = self._calculate_hhi(list(publisher_counts.values()))
        
        # Shannon Entropy (Information Diversity)
        shannon_entropy = self._calculate_shannon_entropy(list(publisher_counts.values()))
        
        # Gini Coefficient (Distribution Inequality)
        gini_coefficient = self._calculate_gini_coefficient(list(publisher_counts.values()))
        
        # Portfolio Diversity Index (0-1 scale)
        max_possible_entropy = math.log2(len(publisher_counts)) if len(publisher_counts) > 1 else 0
        portfolio_diversity = shannon_entropy / max_possible_entropy if max_possible_entropy > 0 else 0
        
        return {
            "herfindahl_hirschman_index": hhi,
            "shannon_entropy": shannon_entropy,
            "gini_coefficient": gini_coefficient,
            "portfolio_diversity_index": portfolio_diversity,
            "market_concentration_level": self._interpret_market_concentration(hhi),
            "publisher_distribution": dict(publisher_counts),
            "effective_number_of_publishers": math.exp(shannon_entropy) if shannon_entropy > 0 else 1
        }
    
    def _perform_competitive_analysis(self) -> Dict[str, Any]:
        """Perform comprehensive competitive landscape analysis"""
        
        publisher_metrics = defaultdict(lambda: {
            'total_books': 0,
            'market_share': 0.0,
            'average_synopsis_length': 0.0,
            'publication_years': [],
            'availability_coverage': 0.0
        })
        
        # Collect publisher metrics
        for book in self.books_data:
            publisher = book.get('imprint', 'Unknown')
            publisher_metrics[publisher]['total_books'] += 1
            publisher_metrics[publisher]['publication_years'].append(
                self._extract_year_from_date(book.get('release_date', ''))
            )
            
            # Calculate synopsis quality
            synopsis_length = len(book.get('synopsis', ''))
            current_avg = publisher_metrics[publisher]['average_synopsis_length']
            total_books = publisher_metrics[publisher]['total_books']
            publisher_metrics[publisher]['average_synopsis_length'] = (
                (current_avg * (total_books - 1) + synopsis_length) / total_books
            )
            
            # Calculate availability coverage
            availability_count = len(book.get('availability', {}))
            publisher_metrics[publisher]['availability_coverage'] += availability_count
        
        # Calculate final metrics
        competitive_matrix = {}
        for publisher, metrics in publisher_metrics.items():
            market_share = metrics['total_books'] / self.total_books
            avg_availability = metrics['availability_coverage'] / metrics['total_books']
            
            # Competitive positioning score (0-1)
            market_reach = min(market_share * 5, 1.0)  # Scale factor
            quality_score = min(metrics['average_synopsis_length'] / 200, 1.0)  # Normalize to 200 chars
            
            competitive_matrix[publisher] = {
                'market_share': market_share,
                'market_reach_score': market_reach,
                'quality_score': quality_score,
                'availability_score': min(avg_availability / 3, 1.0),  # Normalize to 3 channels
                'competitive_strength': (market_reach + quality_score + min(avg_availability / 3, 1.0)) / 3,
                'total_publications': metrics['total_books']
            }
        
        return {
            'competitive_matrix': competitive_matrix,
            'market_leaders': self._identify_market_leaders(competitive_matrix),
            'competitive_gaps': self._identify_competitive_gaps(competitive_matrix)
        }
    
    def _analyze_temporal_dynamics(self) -> Dict[str, Any]:
        """Analyze temporal publication dynamics"""
        
        publication_years = []
        year_counts = defaultdict(int)
        publisher_year_matrix = defaultdict(lambda: defaultdict(int))
        
        for book in self.books_data:
            year = self._extract_year_from_date(book.get('release_date', ''))
            if year:
                publication_years.append(year)
                year_counts[year] += 1
                publisher_year_matrix[book.get('imprint', 'Unknown')][year] += 1
        
        if not publication_years:
            return {"error": "No valid publication dates found"}
        
        # Temporal clustering analysis
        temporal_clusters = self._perform_temporal_clustering(publication_years)
        
        # Publication momentum (recent activity)
        recent_years = [year for year in publication_years if year >= 2022]
        publication_momentum = len(recent_years) / len(publication_years)
        
        # Seasonal patterns
        monthly_distribution = self._analyze_seasonal_patterns()
        
        return {
            'publication_span': {
                'earliest': min(publication_years),
                'latest': max(publication_years),
                'total_years': max(publication_years) - min(publication_years) + 1
            },
            'temporal_clustering_coefficient': temporal_clusters,
            'publication_momentum': publication_momentum,
            'yearly_distribution': dict(year_counts),
            'seasonal_patterns': monthly_distribution,
            'average_publications_per_year': len(publication_years) / (max(publication_years) - min(publication_years) + 1)
        }
    
    def _calculate_predictive_indicators(self) -> Dict[str, Any]:
        """Calculate predictive indicators and forecasting metrics"""
        
        # Growth trajectory analysis
        publication_years = [self._extract_year_from_date(book.get('release_date', '')) 
                           for book in self.books_data if self._extract_year_from_date(book.get('release_date', ''))]
        
        if len(publication_years) < 2:
            return {"error": "Insufficient data for predictive analysis"}
        
        # Calculate growth trend
        year_counts = Counter(publication_years)
        years = sorted(year_counts.keys())
        counts = [year_counts[year] for year in years]
        
        # Linear regression for trend
        growth_coefficient = self._calculate_growth_trajectory(years, counts)
        
        # Market saturation analysis
        publisher_counts = Counter(book.get('imprint', 'Unknown') for book in self.books_data)
        market_saturation = self._calculate_market_saturation_index(publisher_counts)
        
        # Future opportunity index
        opportunity_index = self._calculate_opportunity_index(growth_coefficient, market_saturation)
        
        # Risk assessment
        risk_metrics = self._assess_portfolio_risk()
        
        return {
            'growth_trajectory_coefficient': growth_coefficient,
            'market_saturation_index': market_saturation,
            'future_opportunity_index': opportunity_index,
            'trend_direction': 'positive' if growth_coefficient > 0 else 'negative',
            'risk_assessment_metrics': risk_metrics,
            'predictive_confidence': self._calculate_prediction_confidence(len(publication_years))
        }
    
    def _analyze_portfolio_optimization(self) -> Dict[str, Any]:
        """Analyze portfolio optimization opportunities"""
        
        publisher_performance = {}
        
        for publisher in set(book.get('imprint', 'Unknown') for book in self.books_data):
            publisher_books = [book for book in self.books_data if book.get('imprint') == publisher]
            
            # Performance metrics
            avg_synopsis_quality = statistics.mean([len(book.get('synopsis', '')) for book in publisher_books])
            availability_diversity = statistics.mean([len(book.get('availability', {})) for book in publisher_books])
            
            publisher_performance[publisher] = {
                'book_count': len(publisher_books),
                'quality_score': min(avg_synopsis_quality / 150, 1.0),
                'distribution_score': min(availability_diversity / 4, 1.0),
                'overall_performance': (min(avg_synopsis_quality / 150, 1.0) + min(availability_diversity / 4, 1.0)) / 2
            }
        
        # Optimization recommendations
        optimization_opportunities = self._identify_optimization_opportunities(publisher_performance)
        
        return {
            'publisher_performance_matrix': publisher_performance,
            'optimization_opportunities': optimization_opportunities,
            'portfolio_balance_score': self._calculate_portfolio_balance(publisher_performance)
        }
    
    def _calculate_hhi(self, market_shares: List[int]) -> float:
        """Calculate Herfindahl-Hirschman Index"""
        if not market_shares or sum(market_shares) == 0:
            return 0
        
        total = sum(market_shares)
        proportions = [share / total for share in market_shares]
        return sum(proportion ** 2 for proportion in proportions)
    
    def _calculate_shannon_entropy(self, counts: List[int]) -> float:
        """Calculate Shannon Entropy for diversity measurement"""
        if not counts or sum(counts) == 0:
            return 0
        
        total = sum(counts)
        probabilities = [count / total for count in counts if count > 0]
        return -sum(p * math.log2(p) for p in probabilities)
    
    def _calculate_gini_coefficient(self, values: List[int]) -> float:
        """Calculate Gini coefficient for inequality measurement"""
        if not values or all(v == 0 for v in values):
            return 0
        
        sorted_values = sorted(values)
        n = len(values)
        cumulative_sum = sum((i + 1) * value for i, value in enumerate(sorted_values))
        
        return (2 * cumulative_sum) / (n * sum(values)) - (n + 1) / n
    
    def _interpret_market_concentration(self, hhi: float) -> str:
        """Interpret HHI value for market concentration"""
        if hhi < 0.15:
            return "Competitive Market"
        elif hhi < 0.25:
            return "Moderately Concentrated"
        else:
            return "Highly Concentrated"
    
    def _extract_year_from_date(self, date_str: str) -> Optional[int]:
        """Extract year from date string"""
        if not date_str or '/' not in date_str:
            return None
        try:
            return int(date_str.split('/')[-1])
        except (ValueError, IndexError):
            return None
    
    def _perform_temporal_clustering(self, years: List[int]) -> float:
        """Perform temporal clustering analysis using custom k-means"""
        if len(years) < 2:
            return 0.0
        
        # Simple clustering coefficient based on year distribution
        year_counts = Counter(years)
        sorted_years = sorted(year_counts.keys())
        
        # Calculate clustering as concentration of publications in time
        total_span = max(sorted_years) - min(sorted_years) + 1
        active_years = len(year_counts)
        
        clustering_coefficient = 1 - (active_years / total_span) if total_span > 0 else 0
        
        return max(0, min(1, clustering_coefficient))
    
    def _analyze_seasonal_patterns(self) -> Dict[str, int]:
        """Analyze seasonal publication patterns"""
        month_counts = defaultdict(int)
        
        for book in self.books_data:
            date_str = book.get('release_date', '')
            if '/' in date_str:
                try:
                    month = int(date_str.split('/')[1])
                    month_counts[month] += 1
                except (ValueError, IndexError):
                    continue
        
        return dict(month_counts)
    
    def _calculate_growth_trajectory(self, years: List[int], counts: List[int]) -> float:
        """Calculate growth trajectory using linear regression"""
        if len(years) < 2:
            return 0.0
        
        n = len(years)
        sum_x = sum(years)
        sum_y = sum(counts)
        sum_xy = sum(x * y for x, y in zip(years, counts))
        sum_x2 = sum(x * x for x in years)
        
        denominator = n * sum_x2 - sum_x ** 2
        if denominator == 0:
            return 0.0
        
        slope = (n * sum_xy - sum_x * sum_y) / denominator
        return slope
    
    def _calculate_market_saturation_index(self, publisher_counts: Counter) -> float:
        """Calculate market saturation index"""
        total_books = sum(publisher_counts.values())
        num_publishers = len(publisher_counts)
        
        # Saturation based on publisher concentration
        hhi = self._calculate_hhi(list(publisher_counts.values()))
        
        # Higher HHI indicates more saturation
        return min(hhi * 2, 1.0)  # Scale to 0-1
    
    def _calculate_opportunity_index(self, growth_coeff: float, saturation: float) -> float:
        """Calculate future opportunity index"""
        # Opportunity decreases with saturation, increases with positive growth
        growth_factor = max(0, min(1, (growth_coeff + 0.5)))  # Normalize around 0
        opportunity = growth_factor * (1 - saturation)
        
        return max(0, min(1, opportunity))
    
    def _assess_portfolio_risk(self) -> Dict[str, float]:
        """Assess portfolio risk metrics"""
        publisher_counts = Counter(book.get('imprint', 'Unknown') for book in self.books_data)
        
        # Concentration risk
        hhi = self._calculate_hhi(list(publisher_counts.values()))
        concentration_risk = hhi
        
        # Diversification risk (inverse of diversity)
        shannon = self._calculate_shannon_entropy(list(publisher_counts.values()))
        max_entropy = math.log2(len(publisher_counts)) if len(publisher_counts) > 1 else 0
        diversification_risk = 1 - (shannon / max_entropy) if max_entropy > 0 else 1
        
        # Volatility risk (based on publication distribution)
        counts = list(publisher_counts.values())
        volatility_risk = (statistics.stdev(counts) / statistics.mean(counts)) if len(counts) > 1 and statistics.mean(counts) > 0 else 0
        volatility_risk = min(volatility_risk, 1.0)
        
        # Overall strategic risk
        strategic_risk = (concentration_risk + diversification_risk + volatility_risk) / 3
        
        return {
            'concentration_risk': concentration_risk,
            'diversification_risk': diversification_risk,
            'portfolio_volatility': volatility_risk,
            'strategic_risk_score': strategic_risk
        }
    
    def _calculate_prediction_confidence(self, data_points: int) -> float:
        """Calculate confidence level for predictions"""
        # More data points increase confidence
        return min(data_points / 50, 1.0)  # Cap at 50 data points for full confidence
    
    def _identify_market_leaders(self, competitive_matrix: Dict) -> List[Dict]:
        """Identify market leaders based on competitive metrics"""
        leaders = []
        
        for publisher, metrics in competitive_matrix.items():
            if metrics['competitive_strength'] > 0.6:  # Top performers
                leaders.append({
                    'publisher': publisher,
                    'strength_score': metrics['competitive_strength'],
                    'market_share': metrics['market_share']
                })
        
        return sorted(leaders, key=lambda x: x['strength_score'], reverse=True)
    
    def _identify_competitive_gaps(self, competitive_matrix: Dict) -> List[str]:
        """Identify competitive gaps and opportunities"""
        gaps = []
        
        avg_quality = statistics.mean([m['quality_score'] for m in competitive_matrix.values()])
        avg_reach = statistics.mean([m['market_reach_score'] for m in competitive_matrix.values()])
        
        if avg_quality < 0.5:
            gaps.append("Overall content quality below market potential")
        
        if avg_reach < 0.4:
            gaps.append("Market reach concentration creates opportunity gaps")
        
        # Check for underperforming segments
        low_performers = [pub for pub, metrics in competitive_matrix.items() 
                         if metrics['competitive_strength'] < 0.3]
        
        if len(low_performers) > len(competitive_matrix) * 0.5:
            gaps.append("Multiple publishers showing weak competitive positioning")
        
        return gaps
    
    def _identify_optimization_opportunities(self, performance_matrix: Dict) -> List[str]:
        """Identify portfolio optimization opportunities"""
        opportunities = []
        
        # Analyze performance distribution
        performances = [metrics['overall_performance'] for metrics in performance_matrix.values()]
        avg_performance = statistics.mean(performances)
        
        if avg_performance < 0.6:
            opportunities.append("Significant opportunity for overall quality improvement")
        
        # Check for imbalanced portfolio
        book_counts = [metrics['book_count'] for metrics in performance_matrix.values()]
        if max(book_counts) > sum(book_counts) * 0.6:
            opportunities.append("Portfolio too concentrated in single publisher")
        
        # Quality gaps
        quality_scores = [metrics['quality_score'] for metrics in performance_matrix.values()]
        if min(quality_scores) < 0.4:
            opportunities.append("Some publishers significantly underperforming on quality")
        
        return opportunities
    
    def _calculate_portfolio_balance(self, performance_matrix: Dict) -> float:
        """Calculate overall portfolio balance score"""
        if not performance_matrix:
            return 0.0
        
        performances = [metrics['overall_performance'] for metrics in performance_matrix.values()]
        book_counts = [metrics['book_count'] for metrics in performance_matrix.values()]
        
        # Balance based on performance consistency and distribution
        performance_consistency = 1 - (statistics.stdev(performances) / statistics.mean(performances)) if statistics.mean(performances) > 0 else 0
        distribution_balance = 1 - (statistics.stdev(book_counts) / statistics.mean(book_counts)) if statistics.mean(book_counts) > 0 else 0
        
        return (performance_consistency + distribution_balance) / 2


def main():
    """Test the advanced BI system"""
    print("🧮 Advanced Business Intelligence System - English Version")
    print("=" * 60)
    
    bi_system = AdvancedBusinessIntelligence()
    
    if not bi_system.books_data:
        print("❌ No data available for analysis")
        return
    
    print(f"📊 Analyzing {bi_system.total_books} books...")
    
    comprehensive_report = bi_system.generate_comprehensive_report()
    
    # Display key metrics
    market_intelligence = comprehensive_report.get("market_intelligence", {})
    print(f"\\n🎯 Key Market Intelligence:")
    print(f"• HHI (Market Concentration): {market_intelligence.get('herfindahl_hirschman_index', 0):.4f}")
    print(f"• Shannon Entropy (Diversity): {market_intelligence.get('shannon_entropy', 0):.4f}")
    print(f"• Portfolio Diversity Index: {market_intelligence.get('portfolio_diversity_index', 0):.3f}")
    print(f"• Market Structure: {market_intelligence.get('market_concentration_level', 'Unknown')}")
    
    predictive = comprehensive_report.get("predictive_indicators", {})
    print(f"\\n🔮 Predictive Indicators:")
    print(f"• Growth Trajectory: {predictive.get('growth_trajectory_coefficient', 0):.6f}")
    print(f"• Market Saturation: {predictive.get('market_saturation_index', 0):.3f}")
    print(f"• Future Opportunity Index: {predictive.get('future_opportunity_index', 0):.3f}")
    
    print("\\n✅ Advanced BI analysis completed successfully!")


if __name__ == "__main__":
    main()
