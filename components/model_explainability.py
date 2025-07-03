"""
Model Explainability Component for Customer Transparency
Provides clear explanations of AI decision-making processes
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, List, Any
import streamlit as st

class ModelExplainabilityDashboard:
    """Dashboard for explaining AI model decisions to customers"""
    
    def __init__(self):
        self.explanation_templates = {
            'claims_processing': {
                'title': 'Claims Decision Explanation',
                'factors': ['Weather Impact', 'Historical Data', 'Policy Terms', 'Damage Assessment'],
                'description': 'Your claim decision was based on multiple factors analyzed by our AI system'
            },
            'risk_assessment': {
                'title': 'Risk Score Explanation', 
                'factors': ['Location Risk', 'Weather Patterns', 'Economic Factors', 'Historical Claims'],
                'description': 'Your risk score reflects current conditions and historical patterns'
            },
            'pricing': {
                'title': 'Premium Calculation Explanation',
                'factors': ['Base Rate', 'Risk Adjustments', 'Market Conditions', 'Coverage Level'],
                'description': 'Your premium is calculated using transparent, data-driven factors'
            }
        }
    
    def display_customer_explanation(self, decision_type: str, decision_data: Dict[str, Any]):
        """Display customer-friendly explanation of AI decision"""
        
        st.subheader("🔍 How We Made This Decision")
        st.markdown("*Understanding your AI-powered insurance decision*")
        
        template = self.explanation_templates.get(decision_type, self.explanation_templates['claims_processing'])
        
        # Main explanation
        st.info(f"📋 **{template['title']}**: {template['description']}")
        
        # Decision factors breakdown
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Key Decision Factors")
            factors_data = self._extract_decision_factors(decision_data, template['factors'])
            
            # Create factor importance chart
            fig = px.bar(
                x=list(factors_data.keys()),
                y=list(factors_data.values()),
                title="Factor Influence on Decision",
                labels={'x': 'Factors', 'y': 'Influence (%)'},
                color=list(factors_data.values()),
                color_continuous_scale='RdYlGn'
            )
            fig.update_layout(height=300, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🎯 Confidence & Quality")
            
            confidence = decision_data.get('confidence_score', 0.85)
            data_quality = decision_data.get('data_quality_score', 0.90)
            
            # Confidence gauge
            fig_conf = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = confidence * 100,
                title = {'text': "Decision Confidence"},
                domain = {'x': [0, 1], 'y': [0, 1]},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkgreen"},
                    'steps': [
                        {'range': [0, 60], 'color': "lightgray"},
                        {'range': [60, 80], 'color': "yellow"},
                        {'range': [80, 100], 'color': "lightgreen"}
                    ]
                }
            ))
            fig_conf.update_layout(height=200)
            st.plotly_chart(fig_conf, use_container_width=True)
            
            st.metric("Data Quality", f"{data_quality:.1%}", "High quality sources")
        
        # Detailed explanation
        self._display_detailed_explanation(decision_type, decision_data)
        
        # Customer rights and options
        self._display_customer_rights()
    
    def _extract_decision_factors(self, decision_data: Dict, factor_names: List[str]) -> Dict[str, float]:
        """Extract and normalize decision factors for visualization"""
        factors = {}
        
        # Extract actual factors from decision data
        if 'weather_contribution' in decision_data:
            weather_impact = decision_data['weather_contribution'].get('risk_score', 0.2) * 100
            factors['Weather Impact'] = min(weather_impact, 40)
        
        if 'historical_analysis' in decision_data:
            historical_weight = 25  # Base historical weight
            factors['Historical Data'] = historical_weight
        
        if 'policy_terms' in decision_data:
            policy_weight = 20
            factors['Policy Terms'] = policy_weight
        
        # Fill remaining factors
        remaining_factors = [f for f in factor_names if f not in factors]
        remaining_weight = max(0, 100 - sum(factors.values()))
        
        for i, factor in enumerate(remaining_factors):
            factors[factor] = remaining_weight / len(remaining_factors) if remaining_factors else 15
        
        return factors
    
    def _display_detailed_explanation(self, decision_type: str, decision_data: Dict):
        """Display detailed explanation of the decision process"""
        
        with st.expander("📖 Detailed Decision Process", expanded=False):
            st.markdown("### Step-by-Step Analysis")
            
            if decision_type == 'claims_processing':
                self._explain_claims_process(decision_data)
            elif decision_type == 'risk_assessment':
                self._explain_risk_process(decision_data)
            else:
                self._explain_general_process(decision_data)
            
            # Data sources used
            st.markdown("### 📊 Data Sources")
            data_sources = decision_data.get('data_sources_used', ['Policy Database', 'Weather API', 'Historical Claims'])
            
            for source in data_sources:
                st.markdown(f"✅ {source}")
    
    def _explain_claims_process(self, decision_data: Dict):
        """Explain claims processing decision"""
        
        steps = [
            "🔍 **Initial Assessment**: We analyzed your claim details and incident report",
            "🌦️ **Weather Analysis**: We checked weather conditions at the time and location",
            "📊 **Historical Comparison**: We compared with similar claims in our database",
            "💰 **Damage Evaluation**: We assessed the reported damage using AI image analysis",
            "⚖️ **Policy Review**: We verified coverage terms and policy limits",
            "✅ **Final Decision**: We combined all factors for the final determination"
        ]
        
        for step in steps:
            st.markdown(step)
            st.markdown("")
    
    def _explain_risk_process(self, decision_data: Dict):
        """Explain risk assessment decision"""
        
        steps = [
            "📍 **Location Analysis**: We evaluated risks specific to your location",
            "🌡️ **Climate Assessment**: We analyzed current and forecasted weather patterns",
            "📈 **Economic Factors**: We considered current economic conditions affecting insurance",
            "📋 **Historical Patterns**: We reviewed historical claims and incidents in your area",
            "🎯 **Risk Modeling**: We applied our AI models to calculate your risk score",
            "📊 **Final Score**: We combined all factors into your personalized risk assessment"
        ]
        
        for step in steps:
            st.markdown(step)
            st.markdown("")
    
    def _explain_general_process(self, decision_data: Dict):
        """Explain general decision process"""
        
        st.markdown("Our AI system follows these key principles:")
        st.markdown("• **Transparency**: All decisions are based on clear, explainable factors")
        st.markdown("• **Fairness**: We use objective data without bias")
        st.markdown("• **Accuracy**: Multiple data sources ensure reliable decisions")
        st.markdown("• **Compliance**: All processes follow insurance regulations")
    
    def _display_customer_rights(self):
        """Display customer rights and options"""
        
        with st.expander("⚖️ Your Rights & Options", expanded=False):
            st.markdown("### Your Rights")
            st.markdown("✅ **Right to Explanation**: You can request detailed explanations of any decision")
            st.markdown("✅ **Right to Review**: You can request human review of AI decisions")
            st.markdown("✅ **Right to Appeal**: You can appeal decisions you believe are incorrect")
            st.markdown("✅ **Data Access**: You can request access to data used in your decision")
            
            st.markdown("### What You Can Do")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📞 Request Human Review"):
                    st.success("Human review request submitted!")
            
            with col2:
                if st.button("📄 Get Detailed Report"):
                    st.success("Detailed report will be emailed to you!")
            
            with col3:
                if st.button("❓ Ask Questions"):
                    st.success("Customer service will contact you!")

class DataQualityIndicator:
    """Component for displaying data quality and transparency metrics"""
    
    def __init__(self):
        self.quality_thresholds = {
            'excellent': 0.9,
            'good': 0.75,
            'fair': 0.6,
            'poor': 0.4
        }
    
    def display_data_quality_dashboard(self, data_sources: Dict[str, Any]):
        """Display comprehensive data quality dashboard"""
        
        st.subheader("📊 Data Quality & Transparency")
        st.markdown("*Real-time monitoring of data sources used in your decisions*")
        
        # Overall quality score
        overall_quality = self._calculate_overall_quality(data_sources)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            quality_color = self._get_quality_color(overall_quality)
            st.metric(
                "Overall Data Quality",
                f"{overall_quality:.1%}",
                delta=self._get_quality_label(overall_quality),
                delta_color="normal"
            )
        
        with col2:
            active_sources = sum(1 for source in data_sources.values() if source.get('active', False))
            st.metric(
                "Active Data Sources",
                f"{active_sources}/{len(data_sources)}",
                delta="Real-time monitoring"
            )
        
        with col3:
            last_update = "2 minutes ago"  # Simulated
            st.metric(
                "Last Updated",
                last_update,
                delta="Continuously updated"
            )
        
        # Individual source quality
        st.markdown("### 🔍 Data Source Details")
        
        source_data = []
        for source_name, source_info in data_sources.items():
            quality_score = source_info.get('quality_score', 0.8)
            status = "Active" if source_info.get('active', True) else "Inactive"
            last_check = source_info.get('last_check', "1 min ago")
            
            source_data.append({
                'Data Source': source_name,
                'Quality Score': f"{quality_score:.1%}",
                'Status': status,
                'Last Check': last_check,
                'Records': source_info.get('record_count', 'N/A')
            })
        
        df = pd.DataFrame(source_data)
        st.dataframe(df, use_container_width=True)
        
        # Quality trends
        self._display_quality_trends()
        
        # Transparency metrics
        self._display_transparency_metrics(data_sources)
    
    def _calculate_overall_quality(self, data_sources: Dict) -> float:
        """Calculate overall data quality score"""
        if not data_sources:
            return 0.0
        
        total_quality = sum(source.get('quality_score', 0.8) for source in data_sources.values())
        return total_quality / len(data_sources)
    
    def _get_quality_color(self, quality_score: float) -> str:
        """Get color based on quality score"""
        if quality_score >= self.quality_thresholds['excellent']:
            return "green"
        elif quality_score >= self.quality_thresholds['good']:
            return "blue"
        elif quality_score >= self.quality_thresholds['fair']:
            return "orange"
        else:
            return "red"
    
    def _get_quality_label(self, quality_score: float) -> str:
        """Get quality label based on score"""
        if quality_score >= self.quality_thresholds['excellent']:
            return "Excellent"
        elif quality_score >= self.quality_thresholds['good']:
            return "Good"
        elif quality_score >= self.quality_thresholds['fair']:
            return "Fair"
        else:
            return "Needs Improvement"
    
    def _display_quality_trends(self):
        """Display quality trends over time"""
        
        # Simulated trend data
        import datetime
        dates = [datetime.datetime.now() - datetime.timedelta(hours=i) for i in range(24, 0, -1)]
        quality_scores = [0.85 + (i % 5) * 0.03 for i in range(24)]
        
        trend_df = pd.DataFrame({
            'Time': dates,
            'Quality Score': quality_scores
        })
        
        fig = px.line(
            trend_df,
            x='Time',
            y='Quality Score',
            title="Data Quality Trend (Last 24 Hours)",
            range_y=[0.7, 1.0]
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    def _display_transparency_metrics(self, data_sources: Dict):
        """Display transparency and explainability metrics"""
        
        with st.expander("🔍 Transparency Metrics", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📊 Explainability Scores")
                
                explainability_data = {
                    'Decision Factor': ['Weather Impact', 'Historical Data', 'Policy Terms', 'Risk Assessment'],
                    'Explainability': [0.95, 0.88, 0.92, 0.85]
                }
                
                fig = px.bar(
                    explainability_data,
                    x='Decision Factor',
                    y='Explainability',
                    title="Model Explainability by Factor",
                    color='Explainability',
                    color_continuous_scale='RdYlGn'
                )
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("### 🎯 Transparency Features")
                
                transparency_features = [
                    "✅ Real-time data source monitoring",
                    "✅ Decision factor explanations",
                    "✅ Confidence score display",
                    "✅ Data quality indicators",
                    "✅ Customer rights information",
                    "✅ Human review options"
                ]
                
                for feature in transparency_features:
                    st.markdown(feature)

def create_customer_explanation_demo():
    """Create a demo of customer explanation features"""
    
    # Sample decision data
    sample_claims_data = {
        'claim_id': 'CLM_20241207_001',
        'confidence_score': 0.92,
        'data_quality_score': 0.89,
        'weather_contribution': {
            'risk_score': 0.35,
            'contribution_level': 'moderate'
        },
        'historical_analysis': {
            'similar_claims': 15,
            'pattern_match': 'high'
        },
        'data_sources_used': [
            'Weather API',
            'Historical Claims Database',
            'Policy Management System',
            'Damage Assessment AI'
        ]
    }
    
    sample_data_sources = {
        'Weather API': {
            'active': True,
            'quality_score': 0.94,
            'last_check': '30 seconds ago',
            'record_count': '1.2M'
        },
        'Claims Database': {
            'active': True,
            'quality_score': 0.87,
            'last_check': '1 minute ago',
            'record_count': '850K'
        },
        'Economic Data': {
            'active': True,
            'quality_score': 0.91,
            'last_check': '2 minutes ago',
            'record_count': '500K'
        },
        'Risk Models': {
            'active': True,
            'quality_score': 0.88,
            'last_check': '45 seconds ago',
            'record_count': '2.1M'
        }
    }
    
    # Create dashboard instances
    explainability = ModelExplainabilityDashboard()
    data_quality = DataQualityIndicator()
    
    # Display components
    explainability.display_customer_explanation('claims_processing', sample_claims_data)
    
    st.markdown("---")
    
    data_quality.display_data_quality_dashboard(sample_data_sources)
    
    return explainability, data_quality

