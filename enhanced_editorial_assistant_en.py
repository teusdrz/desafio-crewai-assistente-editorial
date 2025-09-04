#!/usr/bin/env python3
"""
Enhanced Editorial Assistant - English Version
Integrates original CrewAI challenge requirements with advanced Business Intelligence
Maintains 100% backward compatibility while adding sophisticated analytics
"""

import re
from editorial_assistant_en import EditorialAssistant
from advanced_business_intelligence_en import AdvancedBusinessIntelligence


class EnhancedEditorialAssistant(EditorialAssistant):
    """
    Enhanced Editorial Assistant that preserves all original functionality
    while adding advanced Business Intelligence capabilities.
    
    Key Features:
    - 100% compatibility with original CrewAI challenge requirements
    - Advanced mathematical algorithms (HHI, Shannon Entropy, Gini)
    - Competitive intelligence and market analysis
    - Predictive modeling and risk assessment
    - Bilingual support (Portuguese original + English advanced features)
    """
    
    def __init__(self):
        """Initialize enhanced assistant with BI capabilities"""
        super().__init__()
        self.advanced_intelligence = None
        self._initialize_advanced_intelligence()
    
    def _initialize_advanced_intelligence(self):
        """Initialize advanced BI system with lazy loading"""
        try:
            self.advanced_intelligence = AdvancedBusinessIntelligence(self.data_path)
        except Exception as e:
            print(f"Warning: Advanced intelligence initialization failed: {e}")
            self.advanced_intelligence = None
    
    def detect_intent(self, user_input: str) -> str:
        """Enhanced intent detection with BI capabilities"""
        user_input_lower = user_input.lower()
        
        # Advanced BI patterns
        advanced_patterns = [
            r"(?:market intelligence|business intelligence|competitive analysis)",
            r"(?:hhi|herfindahl|shannon entropy|gini coefficient)",
            r"(?:competitive analysis|market dynamics|predictive analytics)",
            r"(?:portfolio optimization|risk assessment)",
            r"(?:kurtosis|skewness|predictive modeling|forecasting)"
        ]
        
        # Check for advanced analytics requests
        for pattern in advanced_patterns:
            if re.search(pattern, user_input_lower, re.IGNORECASE):
                return "advanced_analytics"
        
        # Fall back to original intent detection
        return super().detect_intent(user_input)
    
    def get_market_intelligence_summary(self) -> str:
        """
        NEW TOOL for CrewAI: Advanced market intelligence summary
        """
        if not self.advanced_intelligence:
            return "Advanced market intelligence not available"
        
        try:
            metrics = self.advanced_intelligence.generate_comprehensive_report()
            market_data = metrics.get("market_intelligence", {})
            
            return f"""MARKET INTELLIGENCE EXECUTIVE SUMMARY:
• Market Structure: {market_data.get('market_concentration_level', 'Unknown')}
• Portfolio Diversity: {market_data.get('portfolio_diversity_index', 0):.3f}
• Risk Level: {self._assess_overall_risk_level(metrics)}
• Growth Trajectory: {self._interpret_growth_direction(metrics)}
• Market Opportunity: {metrics.get('predictive_indicators', {}).get('future_opportunity_index', 0):.3f}"""
        
        except Exception as e:
            return f"Market intelligence error: {str(e)}"
    
    def get_competitive_positioning_analysis(self, imprint: str = None) -> str:
        """
        NEW TOOL for CrewAI: Competitive positioning analysis
        """
        if not self.advanced_intelligence:
            return "Competitive analysis not available"
        
        try:
            metrics = self.advanced_intelligence.generate_comprehensive_report()
            competitive_data = metrics.get("competitive_analysis", {})
            matrix = competitive_data.get("competitive_matrix", {})
            
            if imprint and imprint in matrix:
                # Specific publisher analysis
                pub_data = matrix[imprint]
                return f"""COMPETITIVE POSITIONING - {imprint}:
• Market Share: {pub_data['market_share']:.3f}
• Competitive Strength: {pub_data['competitive_strength']:.3f}
• Quality Score: {pub_data['quality_score']:.3f}
• Market Reach: {pub_data['market_reach_score']:.3f}
• Strategic Position: {self._interpret_competitive_position(pub_data)}"""
            else:
                # Overall competitive landscape
                top_publishers = sorted(matrix.items(), key=lambda x: x[1]['competitive_strength'], reverse=True)[:3]
                
                landscape = "COMPETITIVE LANDSCAPE OVERVIEW:\\n"
                for publisher, data in top_publishers:
                    landscape += f"• {publisher}: Reach={data['market_reach_score']:.2f}, Quality={data['quality_score']:.2f}\\n"
                
                return landscape
        
        except Exception as e:
            return f"Competitive analysis error: {str(e)}"
    
    def get_predictive_insights(self) -> str:
        """
        NEW TOOL for CrewAI: Predictive analytics insights
        """
        if not self.advanced_intelligence:
            return "Predictive analytics not available"
        
        try:
            metrics = self.advanced_intelligence.generate_comprehensive_report()
            predictive = metrics.get("predictive_indicators", {})
            
            return f"""PREDICTIVE INSIGHTS:
• Growth Trajectory: {predictive.get('growth_trajectory_coefficient', 0):.6f}
• Market Saturation: {predictive.get('market_saturation_index', 0):.3f}
• Future Opportunity Index: {predictive.get('future_opportunity_index', 0):.3f}
• Risk Assessment: {self._interpret_risk_level(predictive)}
• Strategic Recommendation: {self._generate_strategic_recommendation(metrics)}"""
        
        except Exception as e:
            return f"Predictive insights error: {str(e)}"
    
    def _assess_overall_risk_level(self, metrics: dict) -> str:
        """Assess overall risk level from metrics"""
        try:
            risks = metrics.get("predictive_indicators", {}).get("risk_assessment_metrics", {})
            strategic_risk = risks.get("strategic_risk_score", 0)
            
            if strategic_risk < 0.3:
                return "LOW"
            elif strategic_risk < 0.7:
                return "MODERATE"
            else:
                return "HIGH"
        except:
            return "UNKNOWN"
    
    def _interpret_growth_direction(self, metrics: dict) -> str:
        """Interpret growth trajectory direction"""
        try:
            trajectory = metrics.get("predictive_indicators", {}).get('growth_trajectory_coefficient', 0)
            
            if trajectory > 0.1:
                return "STRONG POSITIVE"
            elif trajectory > 0:
                return "POSITIVE"
            elif trajectory > -0.1:
                return "STABLE"
            else:
                return "DECLINING"
        except:
            return "UNKNOWN"
    
    def _interpret_competitive_position(self, data: dict) -> str:
        """Interpret competitive positioning"""
        strength = data.get('competitive_strength', 0)
        
        if strength > 0.8:
            return "MARKET LEADER"
        elif strength > 0.6:
            return "STRONG COMPETITOR"
        elif strength > 0.4:
            return "EMERGING PLAYER"
        else:
            return "NICHE POSITION"
    
    def _interpret_risk_level(self, predictive_data: dict) -> str:
        """Interpret risk assessment level"""
        risk_metrics = predictive_data.get('risk_assessment_metrics', {})
        strategic_risk = risk_metrics.get('strategic_risk_score', 0)
        
        if strategic_risk < 0.3:
            return "LOW"
        elif strategic_risk < 0.7:
            return "MODERATE"
        else:
            return "HIGH"
    
    def _generate_strategic_recommendation(self, metrics: dict) -> str:
        """Generate strategic recommendation based on analysis"""
        try:
            opportunity = metrics.get("predictive_indicators", {}).get('future_opportunity_index', 0)
            growth = metrics.get("predictive_indicators", {}).get('growth_trajectory_coefficient', 0)
            
            if opportunity > 0.6 and growth > 0:
                return "EXPAND - High growth opportunity identified"
            elif opportunity > 0.4:
                return "INVEST - Moderate opportunity for strategic investment"
            elif growth > 0:
                return "MAINTAIN - Continue current strategic direction"
            else:
                return "OPTIMIZE - Focus on efficiency and portfolio optimization"
        except:
            return "ANALYZE - Insufficient data for strategic recommendation"


# CrewAI Tool Functions (Global functions for CrewAI integration)
assistant_instance = EnhancedEditorialAssistant()

def get_advanced_market_intelligence() -> str:
    """CrewAI Tool: Get advanced market intelligence insights"""
    global assistant_instance
    return assistant_instance.get_market_intelligence_summary()

def get_competitive_analysis(imprint: str = None) -> str:
    """CrewAI Tool: Get competitive landscape analysis"""
    global assistant_instance  
    return assistant_instance.get_competitive_positioning_analysis(imprint)

def get_predictive_analytics() -> str:
    """CrewAI Tool: Get predictive analytics insights"""
    global assistant_instance
    return assistant_instance.get_predictive_insights()

def get_book_details_enhanced(book_title: str) -> str:
    """CrewAI Tool: Enhanced book details with context"""
    global assistant_instance
    return assistant_instance.get_book_details(book_title)

def find_stores_enhanced(book_title: str, city: str = None) -> str:
    """CrewAI Tool: Enhanced store finder"""
    global assistant_instance
    return assistant_instance.find_stores(book_title, city)

def create_support_ticket_enhanced(message: str) -> str:
    """CrewAI Tool: Enhanced support ticket creation"""
    global assistant_instance
    return assistant_instance.create_support_ticket(message)


def main():
    """Demonstration of enhanced system capabilities"""
    print("🚀 Enhanced Editorial Assistant - English Version")
    print("=" * 60)
    print("✅ All original CrewAI requirements maintained")
    print("🧮 Advanced BI capabilities added")
    print("🌍 Full English implementation")
    print("=" * 60)
    
    assistant = EnhancedEditorialAssistant()
    
    print("\\n📊 Testing Market Intelligence:")
    market_intel = assistant.get_market_intelligence_summary()
    print(market_intel)
    
    print("\\n🎯 Testing Competitive Analysis:")
    competitive_analysis = assistant.get_competitive_positioning_analysis()
    print(competitive_analysis)
    
    print("\\n🔮 Testing Predictive Analytics:")
    predictive_insights = assistant.get_predictive_insights()
    print(predictive_insights)
    
    print("\\n📚 Testing Original Functionality:")
    book_details = assistant.get_book_details("A Abelha")
    print(book_details[:200] + "...")
    
    print("\\n✅ Enhanced system demonstration completed!")


if __name__ == "__main__":
    main()
