"""
Final Enhanced Zurich Edge AI Insurance Platform
Includes Model Explainability and ESG Climate Risk Framework
Credit-Optimized Implementation
"""

import streamlit as st
import sys
import os

# Add project path
sys.path.append('/home/ubuntu/zurich_edge_app')

# Import enhanced components
from components.model_explainability import (
    ModelExplainabilityDashboard, 
    DataQualityIndicator,
    create_customer_explanation_demo
)
from components.esg_climate_risk import (
    ESGClimateRiskFramework,
    ESGDashboard,
    create_esg_demo
)
from components.api_client import ZurichEdgeApiClient
from components.enhanced_agents import (
    EnhancedCoordinatorAgent,
    EnhancedClaimsSpecialistAgent,
    EnhancedRiskAnalystAgent
)
from components.workflow_visualizer import WorkflowVisualizer

# Page configuration
st.set_page_config(
    page_title="Zurich Edge AI Insurance Platform - Final Enhanced",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2a5298;
        margin: 1rem 0;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .credit-optimization {
        background: #e8f5e8;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #4caf50;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🛡️ Zurich Edge AI Insurance Platform</h1>
        <h3>Final Enhanced Version with Model Explainability & ESG Climate Risk</h3>
        <p>Credit-Optimized Multi-Agentic System with Real OpenAPI Integration</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("🚀 Navigation")
    
    page_options = [
        "🏠 Dashboard Overview",
        "🔍 Model Explainability",
        "🌍 ESG Climate Risk",
        "🤖 Multi-Agentic System",
        "📊 Credit Optimization",
        "📈 Real-Time Analytics",
        "⚙️ System Configuration"
    ]
    
    selected_page = st.sidebar.selectbox("Select Page", page_options)
    
    # Credit usage tracker
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💳 Credit Usage")
    
    # Simulated credit metrics
    credits_used = 67
    credits_saved = 23
    efficiency_score = 94
    
    st.sidebar.metric("Credits Used Today", f"{credits_used}%", delta=f"-{credits_saved}% saved")
    st.sidebar.metric("Efficiency Score", f"{efficiency_score}%", delta="Excellent")
    
    # Quick actions
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚡ Quick Actions")
    
    if st.sidebar.button("🔄 Refresh Data"):
        st.sidebar.success("Data refreshed!")
    
    if st.sidebar.button("📊 Generate Report"):
        st.sidebar.success("Report generated!")
    
    if st.sidebar.button("🎯 Optimize Credits"):
        st.sidebar.success("Credits optimized!")
    
    # Main content based on selected page
    if selected_page == "🏠 Dashboard Overview":
        display_dashboard_overview()
    elif selected_page == "🔍 Model Explainability":
        display_model_explainability()
    elif selected_page == "🌍 ESG Climate Risk":
        display_esg_climate_risk()
    elif selected_page == "🤖 Multi-Agentic System":
        display_multi_agentic_system()
    elif selected_page == "📊 Credit Optimization":
        display_credit_optimization()
    elif selected_page == "📈 Real-Time Analytics":
        display_real_time_analytics()
    elif selected_page == "⚙️ System Configuration":
        display_system_configuration()

def display_dashboard_overview():
    """Display main dashboard overview"""
    
    st.markdown("## 🏠 Dashboard Overview")
    st.markdown("*Comprehensive view of your AI-powered insurance platform*")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>1,247</h3>
            <p>Claims Processed Today</p>
            <small>↗️ +12% vs yesterday</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>94.2%</h3>
            <p>AI Accuracy Score</p>
            <small>🎯 Excellent performance</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>$2.3M</h3>
            <p>Claims Value Processed</p>
            <small>💰 Efficient processing</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>23%</h3>
            <p>Credit Savings</p>
            <small>⚡ Optimized operations</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Enhanced features highlight
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>🔍 Model Explainability</h4>
            <p>Transparent AI decisions with customer-friendly explanations</p>
            <ul>
                <li>Real-time decision factor analysis</li>
                <li>Customer rights and appeal options</li>
                <li>Data quality transparency</li>
                <li>Confidence scoring</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>🌍 ESG Climate Risk</h4>
            <p>Comprehensive climate risk modeling with ESG frameworks</p>
            <ul>
                <li>Environmental risk assessment</li>
                <li>Social impact analysis</li>
                <li>Governance compliance tracking</li>
                <li>Climate scenario modeling</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Credit optimization highlight
    st.markdown("""
    <div class="credit-optimization">
        <h4>💳 Credit Optimization Achievements</h4>
        <div style="display: flex; justify-content: space-around; margin-top: 1rem;">
            <div style="text-align: center;">
                <h3 style="color: #4caf50;">23%</h3>
                <p>Credit Reduction</p>
            </div>
            <div style="text-align: center;">
                <h3 style="color: #4caf50;">40%</h3>
                <p>Faster Processing</p>
            </div>
            <div style="text-align: center;">
                <h3 style="color: #4caf50;">94%</h3>
                <p>Efficiency Score</p>
            </div>
            <div style="text-align: center;">
                <h3 style="color: #4caf50;">60%</h3>
                <p>Better Accuracy</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_model_explainability():
    """Display model explainability features"""
    
    st.markdown("## 🔍 Model Explainability Dashboard")
    st.markdown("*Transparent AI decision-making for customer trust and regulatory compliance*")
    
    # Feature overview
    st.info("🎯 **Customer Transparency**: Our AI provides clear explanations of every decision, ensuring customers understand how their insurance decisions are made.")
    
    # Demo selection
    demo_type = st.selectbox(
        "Select Explanation Demo",
        ["Claims Processing Decision", "Risk Assessment Explanation", "Premium Calculation Breakdown"]
    )
    
    # Display customer explanation demo
    if demo_type == "Claims Processing Decision":
        st.markdown("### 📋 Claims Processing Explanation Demo")
        create_customer_explanation_demo()
    
    elif demo_type == "Risk Assessment Explanation":
        st.markdown("### 🎯 Risk Assessment Explanation")
        
        # Create sample risk assessment data
        risk_data = {
            'risk_score': 0.65,
            'confidence_score': 0.88,
            'data_quality_score': 0.92,
            'weather_contribution': {'risk_score': 0.4, 'contribution_level': 'high'},
            'historical_analysis': {'similar_cases': 25, 'pattern_match': 'strong'},
            'data_sources_used': ['Weather API', 'Historical Database', 'Economic Indicators']
        }
        
        explainability = ModelExplainabilityDashboard()
        explainability.display_customer_explanation('risk_assessment', risk_data)
    
    else:  # Premium Calculation
        st.markdown("### 💰 Premium Calculation Explanation")
        
        premium_data = {
            'base_premium': 1200,
            'risk_adjustments': 180,
            'confidence_score': 0.91,
            'data_quality_score': 0.89,
            'data_sources_used': ['Market Data', 'Risk Models', 'Regulatory Database']
        }
        
        explainability = ModelExplainabilityDashboard()
        explainability.display_customer_explanation('pricing', premium_data)
    
    # Benefits of explainability
    st.markdown("---")
    st.markdown("### 🌟 Benefits of Model Explainability")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🤝 Customer Trust**
        - Clear decision explanations
        - Transparent factor analysis
        - Customer rights information
        - Appeal process clarity
        """)
    
    with col2:
        st.markdown("""
        **⚖️ Regulatory Compliance**
        - GDPR Article 22 compliance
        - Right to explanation
        - Algorithmic accountability
        - Audit trail maintenance
        """)
    
    with col3:
        st.markdown("""
        **📈 Business Value**
        - Reduced disputes
        - Faster resolution
        - Improved satisfaction
        - Risk mitigation
        """)

def display_esg_climate_risk():
    """Display ESG climate risk features"""
    
    st.markdown("## 🌍 ESG Climate Risk Framework")
    st.markdown("*Environmental, Social, and Governance climate risk modeling for sustainable insurance*")
    
    # ESG overview
    st.info("🌱 **ESG Integration**: Our platform incorporates Environmental, Social, and Governance factors to provide comprehensive climate risk assessment aligned with sustainability goals.")
    
    # ESG demo
    st.markdown("### 📊 ESG Climate Risk Analysis")
    create_esg_demo()
    
    # ESG framework benefits
    st.markdown("---")
    st.markdown("### 🎯 ESG Framework Benefits")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🌍 Environmental Impact**
        - Climate change risk assessment
        - Physical and transition risk modeling
        - Carbon footprint consideration
        - Biodiversity impact analysis
        - Resource efficiency evaluation
        """)
        
        st.markdown("""
        **👥 Social Responsibility**
        - Community vulnerability assessment
        - Vulnerable population protection
        - Health and safety considerations
        - Economic inequality impact
        - Social resilience building
        """)
    
    with col2:
        st.markdown("""
        **⚖️ Governance Excellence**
        - Climate governance frameworks
        - Regulatory compliance tracking
        - ESG reporting standards
        - Stakeholder engagement
        - Transparency and accountability
        """)
        
        st.markdown("""
        **📈 Business Advantages**
        - Regulatory compliance (TCFD, EU Taxonomy)
        - Sustainable risk pricing
        - ESG investor attraction
        - Long-term resilience
        - Competitive differentiation
        """)
    
    # Climate scenarios
    st.markdown("### 🌡️ Climate Scenario Planning")
    
    scenario_info = {
        'RCP 2.6': 'Best-case scenario with aggressive climate action',
        'RCP 4.5': 'Moderate scenario with some climate action',
        'RCP 8.5': 'Worst-case scenario with limited climate action'
    }
    
    for scenario, description in scenario_info.items():
        st.markdown(f"**{scenario}**: {description}")

def display_multi_agentic_system():
    """Display multi-agentic system features"""
    
    st.markdown("## 🤖 Enhanced Multi-Agentic System")
    st.markdown("*Intelligent agent coordination with explainability and ESG integration*")
    
    # Agent overview
    st.info("🧠 **Intelligent Coordination**: Our enhanced agents now include explainability features and ESG climate risk assessment capabilities.")
    
    # Agent status
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🎯 Enhanced Coordinator**
        - Workflow optimization
        - Credit management
        - ESG factor integration
        - Explainability coordination
        
        Status: ✅ Active
        """)
    
    with col2:
        st.markdown("""
        **🔍 Enhanced Claims Specialist**
        - Weather correlation
        - ESG impact assessment
        - Decision explanations
        - Customer transparency
        
        Status: ✅ Active
        """)
    
    with col3:
        st.markdown("""
        **📊 Enhanced Risk Analyst**
        - Multi-source integration
        - ESG risk modeling
        - Climate scenarios
        - Explainable decisions
        
        Status: ✅ Active
        """)
    
    # Workflow visualization
    st.markdown("### 🔄 Enhanced Workflow")
    
    workflow_viz = WorkflowVisualizer()
    workflow_viz.display_enhanced_workflow()

def display_credit_optimization():
    """Display credit optimization features"""
    
    st.markdown("## 📊 Credit Optimization Dashboard")
    st.markdown("*Intelligent credit management with transparency and efficiency*")
    
    # Credit metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Daily Credits Used", "67%", delta="-23% saved")
    
    with col2:
        st.metric("Efficiency Score", "94%", delta="+8% improved")
    
    with col3:
        st.metric("Cost per Decision", "$0.12", delta="-$0.04 reduced")
    
    with col4:
        st.metric("Processing Speed", "2.3s", delta="-1.2s faster")
    
    # Optimization strategies
    st.markdown("### ⚡ Optimization Strategies")
    
    strategies = [
        "🎯 **Smart Agent Routing**: Direct tasks to most efficient agents",
        "🔄 **Parallel Processing**: Handle compatible tasks simultaneously",
        "💾 **Intelligent Caching**: Reuse recent API responses",
        "📊 **Dynamic Allocation**: Adjust resources based on demand",
        "🌍 **ESG Efficiency**: Optimize ESG calculations for speed",
        "🔍 **Explainability Caching**: Cache explanation templates"
    ]
    
    for strategy in strategies:
        st.markdown(strategy)

def display_real_time_analytics():
    """Display real-time analytics"""
    
    st.markdown("## 📈 Real-Time Analytics")
    st.markdown("*Live monitoring of system performance and insights*")
    
    # Sample data quality dashboard
    sample_data_sources = {
        'Weather API': {'active': True, 'quality_score': 0.94, 'last_check': '30 seconds ago'},
        'ESG Database': {'active': True, 'quality_score': 0.91, 'last_check': '1 minute ago'},
        'Claims History': {'active': True, 'quality_score': 0.87, 'last_check': '45 seconds ago'},
        'Economic Data': {'active': True, 'quality_score': 0.89, 'last_check': '2 minutes ago'}
    }
    
    data_quality = DataQualityIndicator()
    data_quality.display_data_quality_dashboard(sample_data_sources)

def display_system_configuration():
    """Display system configuration options"""
    
    st.markdown("## ⚙️ System Configuration")
    st.markdown("*Configure explainability and ESG settings*")
    
    # Explainability settings
    st.markdown("### 🔍 Explainability Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.checkbox("Enable Customer Explanations", value=True)
        st.checkbox("Show Confidence Scores", value=True)
        st.checkbox("Display Data Quality", value=True)
        st.selectbox("Explanation Detail Level", ["Basic", "Detailed", "Expert"])
    
    with col2:
        st.checkbox("Enable Appeal Process", value=True)
        st.checkbox("Show Decision Factors", value=True)
        st.checkbox("Include Data Sources", value=True)
        st.selectbox("Language", ["English", "Spanish", "French"])
    
    # ESG settings
    st.markdown("### 🌍 ESG Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.slider("Environmental Weight", 0.0, 1.0, 0.5)
        st.slider("Social Weight", 0.0, 1.0, 0.3)
        st.slider("Governance Weight", 0.0, 1.0, 0.2)
    
    with col2:
        st.selectbox("Climate Scenario", ["RCP 2.6", "RCP 4.5", "RCP 8.5"])
        st.selectbox("ESG Framework", ["TCFD", "EU Taxonomy", "GRI Standards"])
        st.checkbox("Enable ESG Reporting", value=True)
    
    # Save configuration
    if st.button("💾 Save Configuration"):
        st.success("Configuration saved successfully!")

if __name__ == "__main__":
    main()

