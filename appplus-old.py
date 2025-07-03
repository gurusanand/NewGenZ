"""
NewGenZ AI Insurance Platform - Consolidated Main Application

This is the main entry point for the NewGenZ AI Insurance Platform.
Run this file with: streamlit run appplus.py

Features:
- Multi-Agentic AI System with ReAct and Hierarchical Frameworks
- Real OpenAPI Integration for live data
- Model Explainability for transparent AI decisions
- ESG Climate Risk Framework for sustainable insurance
- Credit-Optimized Implementation for efficiency
- Comprehensive UI with dashboards and real-time analytics
- Customer-facing travel insurance chatbot
- Embedded insurance APIs
- Broker portal and ecosystem integrations
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import time
import uuid
import sys
import os
import random

# Import helper functions from appplus1
from appplus1 import *

# Page configuration
st.set_page_config(
    page_title="NewGenZ AI Platform - Plus",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""<style>
    .main-header {
        background: linear-gradient(90deg, #232526 0%, #414345 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: #111111;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2a5298;
        margin: 1rem 0;
        color: #fff;
    }
    .metric-card {
        background: #111111;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        color: #fff;
    }
    .credit-optimization {
        background: #222;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #4caf50;
        color: #fff;
    }
    .workflow-step {
        background: #181818;
        border: 1px solid #222;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        color: #fff;
    }
    .api-status {
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        background: #181818;
        color: #fff;
    }
    .api-success {
        background-color: #1a3a1a;
        color: #10b981;
        border: 1px solid #10b981;
    }
    .api-error {
        background-color: #3a1a1a;
        color: #ef4444;
        border: 1px solid #ef4444;
    }
    .chat-message {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        color: #fff;
    }
    .user-message {
        background-color: #232526;
        margin-left: 2rem;
    }
    .bot-message {
        background-color: #181818;
        margin-right: 2rem;
    }
    /* Override Streamlit's default white/gray backgrounds */
    .stApp {
        background-color: #000 !important;
    }
    .main .block-container {
        background-color: #000 !important;
    }
    .stSelectbox > div > div {
        background-color: #181818 !important;
        color: #fff !important;
    }
    .stTextInput > div > div > input {
        background-color: #181818 !important;
        color: #fff !important;
    }
    .stTextArea > div > div > textarea {
        background-color: #181818 !important;
        color: #fff !important;
    }
    .stNumberInput > div > div > input {
        background-color: #181818 !important;
        color: #fff !important;
    }
    .stDateInput > div > div > input {
        background-color: #181818 !important;
        color: #fff !important;
    }
    .stDataFrame {
        background-color: #181818 !important;
        color: #fff !important;
    }
    .stExpander {
        background-color: #181818 !important;
        border: 1px solid #222;
        color: #fff !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        background-color: #232526 !important;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #181818 !important;
        color: #fff !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #222 !important;
        color: #fff !important;
    }
    .stForm {
        background-color: #181818 !important;
        border: 1px solid #222;
        border-radius: 8px;
        padding: 1rem;
        color: #fff !important;
    }
    .stSidebar {
        background-color: #181818 !important;
        color: #fff !important;
    }
    .stSidebar .stSelectbox > div > div {
        background-color: #232526 !important;
        color: #fff !important;
    }
    .stMetric {
        background-color: #181818 !important;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #222;
        color: #fff !important;
    }
</style>""", unsafe_allow_html=True)

class NewGenZAppPlus:
    def __init__(self):
        # Initialize all components and session state variables
        self.initialize_session_state()

    def initialize_session_state(self):
        """Initialize session state variables"""
        if 'credit_balance' not in st.session_state:
            st.session_state.credit_balance = 100
        if 'workflow_history' not in st.session_state:
            st.session_state.workflow_history = []
        if 'active_agents' not in st.session_state:
            st.session_state.active_agents = {}
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        if 'travel_quotes' not in st.session_state:
            st.session_state.travel_quotes = []

    def run(self):
        """Main application runner"""
        self.render_header()
        self.render_sidebar()
        self.render_main_content()

    def render_header(self):
        """Render the main header"""
        st.markdown("""
        <div class="main-header">
            <h1>🛡️ NewGenZ AI Insurance Platform - Plus</h1>
            <h3>Comprehensive Multi-Agentic System with Real-Time Data, Explainability, and ESG Risk Analysis</h3>
        </div>
        """, unsafe_allow_html=True)

    def render_sidebar(self):
        """Render the sidebar navigation"""
        st.sidebar.title("🚀 Navigation")
        page_options = [
            "🏠 Dashboard Overview",
            "🔧 Workflow Designer",
            "🤖 Agent Management",
            "🧳 Travel Insurance Chatbot",
            "🔌 Embedded Insurance APIs",
            "🤝 Broker Portal",
            "🔍 Model Explainability",
            "🌍 ESG Climate Risk",
            "📊 Credit Optimization",
            "📈 Real-Time Analytics",
            "⚙️ System Configuration"
        ]
        selected_page = st.sidebar.selectbox("Select Page", page_options)

        # Credit management
        st.sidebar.markdown("---")
        st.sidebar.header("🎛️ System Control Panel")
        st.sidebar.markdown(f"""
        <div class="credit-indicator">
            <strong>💳 Credit Balance: {st.session_state.credit_balance}</strong>
        </div>
        """, unsafe_allow_html=True)
        
        if st.sidebar.button("🔄 Reset Credits (100)"):
            st.session_state.credit_balance = 100
            st.sidebar.success("Credits reset!")
        
        add_credits = st.sidebar.number_input("Add Credits", min_value=0, max_value=500, value=0)
        if st.sidebar.button("➕ Add Credits") and add_credits > 0:
            st.session_state.credit_balance += add_credits
            st.sidebar.success(f"Added {add_credits} credits!")

        # Quick actions
        st.sidebar.markdown("---")
        st.sidebar.markdown("### ⚡ Quick Actions")
        if st.sidebar.button("🔄 Refresh Data"):
            st.sidebar.success("Data refreshed!")
        if st.sidebar.button("📊 Generate Report"):
            st.sidebar.success("Report generated!")

        # Store selected page in session state
        st.session_state.selected_page = selected_page

    def render_main_content(self):
        """Render the main content based on selected page"""
        page = st.session_state.get('selected_page', '🏠 Dashboard Overview')

        if page == "🏠 Dashboard Overview":
            self.display_dashboard_overview()
        elif page == "🔧 Workflow Designer":
            self.render_workflow_designer()
        elif page == "🤖 Agent Management":
            self.render_agent_dashboard()
        elif page == "🧳 Travel Insurance Chatbot":
            self.display_travel_insurance_chatbot()
        elif page == "🔌 Embedded Insurance APIs":
            self.display_embedded_insurance_apis()
        elif page == "🤝 Broker Portal":
            self.display_broker_portal()
        elif page == "🔍 Model Explainability":
            self.display_model_explainability()
        elif page == "🌍 ESG Climate Risk":
            self.display_esg_climate_risk()
        elif page == "📊 Credit Optimization":
            self.display_credit_optimization()
        elif page == "📈 Real-Time Analytics":
            self.display_real_time_analytics()
        elif page == "⚙️ System Configuration":
            self.display_system_configuration()

    def display_dashboard_overview(self):
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

    def render_workflow_designer(self):
        """Render the workflow designer interface"""
        st.header("🔧 Intelligent Workflow Designer")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Task Input")
            task_templates = {
                "Simple Query": "What is my policy status?",
                "Claim Processing": "I need to file a claim for car damage from yesterday's accident",
                "Risk Assessment": "Analyze flood risk for my property in Miami",
                "Fraud Investigation": "Investigate suspicious claim patterns for policy #12345",
                "Policy Recommendation": "Recommend optimal coverage for a family of 4 with 2 cars",
                "Emergency Claim": "Emergency claim: house fire, need immediate assistance"
            }
            
            selected_template = st.selectbox("Choose Template", ["Custom"] + list(task_templates.keys()))
            if selected_template != "Custom":
                default_task = task_templates[selected_template]
            else:
                default_task = ""
            
            user_task = st.text_area(
                "Describe your task or query:",
                value=default_task,
                height=100,
                placeholder="Enter your insurance-related task here..."
            )
            
            # Additional context
            context = {}
            with st.expander("🔧 Advanced Context (Optional)"):
                context['customer_id'] = st.text_input("Customer ID", "CUST_001")
                context['policy_number'] = st.text_input("Policy Number", "POL_12345")
                context['urgency'] = st.selectbox("Urgency Level", ["Low", "Medium", "High", "Critical"])
                context['channel'] = st.selectbox("Channel", ["Web", "Mobile", "Phone", "Email"])

        with col2:
            st.subheader("Credit Budget")
            max_credits = min(st.session_state.credit_balance, 100)
            credit_budget = st.slider(
                "Maximum Credits to Use",
                min_value=1,
                max_value=max_credits,
                value=min(20, max_credits),
                help="Set the maximum credits you want to spend on this task"
            )
            st.info(f"💡 Remaining after task: {st.session_state.credit_balance - credit_budget} credits")

        # Generate workflow button
        if st.button("🚀 Generate Optimal Workflow", type="primary"):
            if user_task.strip():
                generate_and_display_workflow(user_task, context, credit_budget)
            else:
                st.error("Please enter a task description!")

    def render_agent_dashboard(self):
        """Render the agent management dashboard"""
        st.header("🤖 Agent Management Dashboard")
        
        # Agent status overview
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("🏗️ Hierarchy Overview")
            hierarchy_levels = {
                1: ["Enhanced Coordinator"],
                2: ["Claims Specialist", "Risk Analyst"],
                3: ["Fraud Detector", "Policy Advisor"],
                4: ["Customer Service"]
            }
            
            for level, agents in hierarchy_levels.items():
                st.write(f"**Level {level}:**")
                for agent in agents:
                    status = "🟢 Active" if agent in st.session_state.active_agents else "⚪ Idle"
                    st.write(f"  {status} {agent}")
        
        with col2:
            st.subheader("📊 Agent Performance")
            performance_data = {
                'Agent': ['Enhanced Coordinator', 'Claims Specialist', 'Risk Analyst', 'Fraud Detector', 'Policy Advisor', 'Customer Service'],
                'Tasks Completed': [15, 23, 8, 31, 12, 19],
                'Avg Response Time (s)': [2.1, 1.8, 3.2, 1.5, 2.8, 2.3],
                'Success Rate (%)': [98, 96, 99, 97, 95, 98]
            }
            df_performance = pd.DataFrame(performance_data)
            st.dataframe(df_performance, use_container_width=True)
        
        with col3:
            st.subheader("💳 Credit Efficiency")
            efficiency_data = {
                'Agent': ['Enhanced Coordinator', 'Claims Specialist', 'Risk Analyst', 'Fraud Detector', 'Policy Advisor', 'Customer Service'],
                'Cost per Task': [5, 8, 12, 15, 10, 3],
                'Max Concurrent': [10, 5, 3, 2, 4, 8],
                'Efficiency Score': [2.0, 0.63, 0.25, 0.13, 0.4, 2.67]
            }
            df_efficiency = pd.DataFrame(efficiency_data)
            st.dataframe(df_efficiency, use_container_width=True)

    def display_travel_insurance_chatbot(self):
        """Display customer-facing travel insurance chatbot"""
        st.header("🧳 Travel Insurance Chatbot")
        st.markdown("*Get instant travel insurance quotes with AI-powered assistance*")
        
        # Chat interface
        st.subheader("💬 Chat with our AI Assistant")
        
        # Display chat history
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>You:</strong> {message['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message bot-message">
                    <strong>AI Assistant:</strong> {message['content']}
                </div>
                """, unsafe_allow_html=True)
        
        # Chat input
        user_input = st.text_input("Type your message here...", placeholder="Hi, I need travel insurance for my trip to Japan")
        
        if st.button("Send") and user_input:
            # Add user message to history
            st.session_state.chat_history.append({'role': 'user', 'content': user_input})
            
            # Generate AI response
            ai_response = generate_travel_insurance_response(user_input)
            st.session_state.chat_history.append({'role': 'assistant', 'content': ai_response})
            
            st.rerun()
        
        # Quick quote form
        st.markdown("---")
        st.subheader("⚡ Quick Quote Form")
        
        with st.form("travel_quote_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                destination = st.text_input("Destination", placeholder="e.g., Tokyo, Japan")
                departure_date = st.date_input("Departure Date", value=datetime.now().date() + timedelta(days=30))
                travelers = st.number_input("Number of Travelers", min_value=1, max_value=10, value=1)
            
            with col2:
                return_date = st.date_input("Return Date", value=datetime.now().date() + timedelta(days=37))
                coverage_type = st.selectbox("Coverage Type", ["Basic", "Standard", "Premium", "Comprehensive"])
                trip_cost = st.number_input("Trip Cost ($)", min_value=0, value=2000)
            
            submitted = st.form_submit_button("🚀 Get Quote")
            
            if submitted and destination:
                quote = generate_travel_quote(destination, departure_date, return_date, travelers, coverage_type, trip_cost)
                st.session_state.travel_quotes.append(quote)
                
                st.success("✅ Quote generated successfully!")
                display_travel_quote(quote)

    def display_embedded_insurance_apis(self):
        """Display embedded insurance APIs interface"""
        st.header("🔌 Embedded Insurance APIs")
        st.markdown("*Integrate with leading insurance providers through our unified API platform*")
        
        # API provider tabs
        provider_tabs = st.tabs(["🍋 Lemonade", "🛡️ Coalition", "🔄 Qover", "✅ Sure"])
        
        with provider_tabs[0]:
            display_api_provider_config("Lemonade", "Renters & Homeowners Insurance", "lemonade_api")
        
        with provider_tabs[1]:
            display_api_provider_config("Coalition", "Cyber Insurance", "coalition_api")
        
        with provider_tabs[2]:
            display_api_provider_config("Qover", "On-Demand Insurance", "qover_api")
        
        with provider_tabs[3]:
            display_api_provider_config("Sure", "Embedded Insurance Platform", "sure_api")
        
        # API testing interface
        st.markdown("---")
        st.subheader("🧪 API Testing Interface")
        
        test_provider = st.selectbox("Select Provider", ["Lemonade", "Coalition", "Qover", "Sure"])
        test_endpoint = st.selectbox("Select Endpoint", ["Get Quote", "Create Policy", "Submit Claim", "Get Status"])
        
        test_payload = st.text_area(
            "Request Payload (JSON)",
            value='{\n  "product_type": "renters",\n  "coverage_amount": 50000,\n  "location": "New York, NY"\n}',
            height=150
        )
        
        if st.button("🚀 Test API Call"):
            with st.spinner("Making API call..."):
                time.sleep(2)
                test_result = simulate_api_call(test_provider, test_endpoint, test_payload)
                st.success("✅ API call successful!")
                st.json(test_result)

    def display_broker_portal(self):
        """Display broker portal interface"""
        st.header("🤝 Broker Portal & Ecosystem")
        st.markdown("*Comprehensive broker management and ecosystem integration platform*")
        
        # Broker portal tabs
        portal_tabs = st.tabs(["👤 Broker Dashboard", "👥 Client Management", "📋 Policy Management", "💰 Commission Tracking", "🔌 API Access", "🤝 Partner Network"])
        
        with portal_tabs[0]:
            display_broker_dashboard()
        
        with portal_tabs[1]:
            display_client_management()
        
        with portal_tabs[2]:
            display_policy_management()
        
        with portal_tabs[3]:
            display_commission_tracking()
        
        with portal_tabs[4]:
            display_broker_api_access()
        
        with portal_tabs[5]:
            display_partner_network()

    def display_model_explainability(self):
        """Display model explainability features"""
        st.markdown("## 🔍 Model Explainability Dashboard")
        st.markdown("*Transparent AI decision-making for customer trust and regulatory compliance*")
        
        st.info("🎯 **Customer Transparency**: Our AI provides clear explanations of every decision, ensuring customers understand how their insurance decisions are made.")
        
        demo_type = st.selectbox(
            "Select Explanation Demo",
            ["Claims Processing Decision", "Risk Assessment Explanation", "Premium Calculation Breakdown"]
        )
        
        if demo_type == "Claims Processing Decision":
            st.markdown("### 📋 Claims Processing Explanation Demo")
            display_claims_explanation_demo()
        
        elif demo_type == "Risk Assessment Explanation":
            st.markdown("### 🎯 Risk Assessment Explanation")
            display_risk_explanation_demo()
        
        else:  # Premium Calculation
            st.markdown("### 💰 Premium Calculation Explanation")
            display_premium_explanation_demo()

    def display_esg_climate_risk(self):
        """Display ESG climate risk features"""
        st.markdown("## 🌍 ESG Climate Risk Framework")
        st.markdown("*Environmental, Social, and Governance climate risk modeling for sustainable insurance*")
        
        st.info("🌱 **ESG Integration**: Our platform incorporates Environmental, Social, and Governance factors to provide comprehensive climate risk assessment aligned with sustainability goals.")
        
        st.markdown("### 📊 ESG Climate Risk Analysis")
        display_esg_demo()

    def display_credit_optimization(self):
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

    def display_real_time_analytics(self):
        """Display real-time analytics"""
        st.markdown("## 📈 Real-Time Analytics")
        st.markdown("*Live monitoring of system performance and insights*")
        
        # Real-time metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Active Claims", "1,247", delta="↑ 12 from yesterday")
        
        with col2:
            st.metric("Weather Risk Level", "35%", delta="↓ 5% from last week")
        
        with col3:
            st.metric("Economic Health", "78/100", delta="↑ 3 points")
        
        with col4:
            st.metric("API Integration", "94%", delta="Real-time data")
        
        # Real-time visualizations
        display_real_time_visualizations()

    def display_system_configuration(self):
        """Display system configuration options"""
        st.markdown("## ⚙️ System Configuration")
        st.markdown("*Configure explainability and ESG settings*")
        
        # Configuration tabs
        config_tabs = st.tabs(["🔍 Explainability", "🌍 ESG Settings", "🤖 Agent Config", "🔌 API Settings"])
        
        with config_tabs[0]:
            display_explainability_config()
        
        with config_tabs[1]:
            display_esg_config()
        
        with config_tabs[2]:
            display_agent_config()
        
        with config_tabs[3]:
            display_api_config()

def main():
    """Main function to run the application"""
    app = NewGenZAppPlus()
    app.run()

if __name__ == "__main__":
    main()

