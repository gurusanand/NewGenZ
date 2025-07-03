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
from components.openai_client import OpenAIClient
from components.claim_validator import ClaimValidator
from components.hierarchical_framework import HierarchicalFramework

# Import helper functions from appplus1
from appplus1 import *
from openapi_handler import OpenAPIHandler
from multi_agent_visualizer import MultiAgentVisualizer

# Page configuration
st.set_page_config(
    page_title="NewGenZ AI Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""<style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
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

# Helper Functions for Dynamic OpenAI Integration

def generate_travel_insurance_response(user_input):
    """Generate AI response for travel insurance chatbot"""
    openai_client = OpenAIClient()
    response = openai_client.get_chat_completion(f"Provide a concise travel insurance recommendation for {user_input}. Focus on key coverage aspects and any relevant travel advisories.")
    return response.get("response", "I'm sorry, I couldn't generate a response at this time.")

def generate_travel_quote(destination, departure_date, return_date, travelers, coverage_type, trip_cost):
    """Generate a travel insurance quote using OpenAI."""
    openai_client = OpenAIClient()
    prompt = f"""Generate a realistic travel insurance quote for a trip to {destination} from {departure_date} to {return_date} for {travelers} travelers with {coverage_type} coverage and a trip cost of ${trip_cost}. 

    Consider current risk factors, weather conditions, political stability, and health advisories for {destination}. 

    Provide a realistic quote with the following structure:
    - Base premium calculation based on trip cost and coverage type
    - Weather risk adjustment based on current conditions
    - Duration adjustment for trip length
    - Traveler adjustment for group size
    - Detailed explanation of factors

    Return the response in JSON format with these exact keys:
    {{
        "quote_id": "TQ-XXXXXX",
        "destination": "{destination}",
        "departure_date": "{departure_date}",
        "return_date": "{return_date}",
        "duration": number_of_days,
        "travelers": {travelers},
        "coverage_type": "{coverage_type}",
        "trip_cost": {trip_cost},
        "total_premium": calculated_total,
        "base_premium": base_amount,
        "weather_adjustment": weather_risk_amount,
        "duration_adjustment": duration_risk_amount,
        "traveler_adjustment": group_size_amount,
        "explanation": "detailed explanation of factors",
        "weather_risk_factor": risk_score_0_to_1,
        "valid_until": "YYYY-MM-DD",
        "timestamp": "ISO_timestamp"
    }}"""
    
    response = openai_client.get_chat_completion(prompt)
    try:
        # Try to extract JSON from the response
        response_text = response.get("response", "{}")
        
        # Sometimes OpenAI wraps JSON in markdown code blocks
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
        
        quote_data = json.loads(response_text)
        
        # Ensure all required fields are present with fallbacks
        quote_data["quote_id"] = quote_data.get("quote_id", f"TQ-{random.randint(100000, 999999)}")
        quote_data["duration"] = quote_data.get("duration", (return_date - departure_date).days)
        quote_data["valid_until"] = quote_data.get("valid_until", (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"))
        quote_data["timestamp"] = quote_data.get("timestamp", datetime.now().isoformat())
        quote_data["destination"] = quote_data.get("destination", destination)
        quote_data["departure_date"] = quote_data.get("departure_date", departure_date.strftime("%Y-%m-%d"))
        quote_data["return_date"] = quote_data.get("return_date", return_date.strftime("%Y-%m-%d"))
        quote_data["travelers"] = quote_data.get("travelers", travelers)
        quote_data["coverage_type"] = quote_data.get("coverage_type", coverage_type)
        quote_data["trip_cost"] = quote_data.get("trip_cost", trip_cost)
        
        # Ensure numeric fields are properly typed
        quote_data["total_premium"] = float(quote_data.get("total_premium", 0))
        quote_data["base_premium"] = float(quote_data.get("base_premium", 0))
        quote_data["weather_adjustment"] = float(quote_data.get("weather_adjustment", 0))
        quote_data["duration_adjustment"] = float(quote_data.get("duration_adjustment", 0))
        quote_data["traveler_adjustment"] = float(quote_data.get("traveler_adjustment", 0))
        quote_data["weather_risk_factor"] = float(quote_data.get("weather_risk_factor", 0.1))
        
        quote_data["explanation"] = quote_data.get("explanation", "Quote generated based on destination risk assessment and coverage requirements.")
        
        return quote_data
    except (json.JSONDecodeError, ValueError) as e:
        st.error(f"Failed to parse quote response from OpenAI: {str(e)}")
        # Return a fallback quote structure
        return {
            "quote_id": f"TQ-{random.randint(100000, 999999)}",
            "destination": destination,
            "departure_date": departure_date.strftime("%Y-%m-%d"),
            "return_date": return_date.strftime("%Y-%m-%d"),
            "duration": (return_date - departure_date).days,
            "travelers": travelers,
            "coverage_type": coverage_type,
            "trip_cost": trip_cost,
            "total_premium": 0.0,
            "base_premium": 0.0,
            "weather_adjustment": 0.0,
            "duration_adjustment": 0.0,
            "traveler_adjustment": 0.0,
            "explanation": "Unable to generate dynamic quote. Please try again.",
            "weather_risk_factor": 0.1,
            "valid_until": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
            "timestamp": datetime.now().isoformat()
        }

def display_travel_quote(quote):
    """Display travel insurance quote with enhanced formatting"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 Quote Details")
        st.markdown(f"**Quote ID:** {quote['quote_id']}")
        st.markdown(f"**Destination:** {quote['destination']}")
        st.markdown(f"**Travel Dates:** {quote['departure_date']} to {quote['return_date']}")
        st.markdown(f"**Duration:** {quote['duration']} days")
        st.markdown(f"**Travelers:** {quote['travelers']}")
        st.markdown(f"**Coverage:** {quote['coverage_type']}")
        st.markdown(f"**Trip Cost:** ${quote['trip_cost']:,}")
    
    with col2:
        st.markdown("### 💰 Premium Breakdown")
        st.markdown(f"**Base Premium:** ${quote['base_premium']:.2f}")
        if quote['weather_adjustment'] > 0:
            st.markdown(f"**Weather Risk Adjustment:** +${quote['weather_adjustment']:.2f}")
        if quote['duration_adjustment'] > 0:
            st.markdown(f"**Extended Duration:** +${quote['duration_adjustment']:.2f}")
        if quote['traveler_adjustment'] > 0:
            st.markdown(f"**Additional Travelers:** +${quote['traveler_adjustment']:.2f}")
        st.markdown(f"**Total Premium:** ${quote['total_premium']:.2f}")
        st.markdown(f"**Valid Until:** {quote['valid_until']}")
    
    # Weather risk indicator
    weather_risk = quote.get('weather_risk_factor', 0.1)
    if weather_risk > 0.7:
        st.error(f"🚨 Very high weather risk detected for {quote['destination']}. Consider comprehensive coverage.")
    elif weather_risk > 0.4:
        st.warning(f"⚠️ High weather risk detected for {quote['destination']}. Enhanced coverage recommended.")
    elif weather_risk > 0.2:
        st.info(f"🌤️ Moderate weather risk for {quote['destination']}. Standard coverage should be sufficient.")
    else:
        st.success(f"☀️ Low weather risk for {quote['destination']}. Basic coverage may be adequate.")
    
    # Explanation
    st.markdown("### 📝 Quote Explanation")
    st.markdown(quote['explanation'])
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.form_submit_button("📧 Email Quote"):
            st.success("Quote emailed successfully!")
    with col2:
        if st.form_submit_button("💾 Save Quote"):
            st.success("Quote saved to your account!")
    with col3:
        if st.form_submit_button("🛒 Purchase Now"):
            st.success("Redirecting to purchase page...")

class NewGenZAppPlus:
    def __init__(self):
        # Initialize all components and session state variables
        self.initialize_session_state()
        self.openapi_handler = OpenAPIHandler()
        self.agent_visualizer = MultiAgentVisualizer()
        self.openai_client = OpenAIClient()
        
        # Load OpenAPI specs on initialization
        self.openapi_handler.load_openapi_spec()

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
        """Render the workflow designer interface with real multi-agent visualization"""
        st.header("🔧 Intelligent Workflow Designer")
        
        # Get sample agents for visualization
        agents = self.agent_visualizer.get_sample_agents()
        
        # Display real-time agent metrics
        st.subheader("📊 Real-Time Agent Status")
        self.agent_visualizer.create_real_time_metrics(agents)
        
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

        # Multi-Agent Network Visualization
        st.subheader("🤖 Multi-Agent Network")
        workflow_steps = self.generate_dynamic_workflow(user_task, context, credit_budget)
        workflow_diagram = self.agent_visualizer.create_workflow_diagram(user_task, workflow_steps)
        st.plotly_chart(workflow_diagram, use_container_width=True)

        # Generate workflow button
        if st.button("🚀 Generate & Execute Workflow", type="primary"):
            if user_task.strip():
                self.execute_real_workflow(user_task, context, credit_budget)
            else:
                st.error("Please enter a task description!")

    def execute_real_workflow(self, task: str, context: dict, credit_budget: int):
        """Execute workflow with real multi-agent visualization and animation"""
        
        # Generate dynamic workflow steps using OpenAI
        workflow_steps = self.generate_dynamic_workflow(task, context, credit_budget)
        
        if not workflow_steps:
            st.error("Failed to generate workflow. Please try again.")
            return
        
        # Create animated workflow execution
        st.subheader("🎬 Workflow Execution Animation")
        
        # Create progress containers
        progress_bar = st.progress(0)
        status_text = st.empty()
        workflow_container = st.container()
        
        # Execute workflow with animation
        total_steps = len(workflow_steps)
        
        with workflow_container:
            # Create columns for each agent
            agent_columns = st.columns(min(len(workflow_steps), 4))
            agent_status = {}
            
            for i, step in enumerate(workflow_steps):
                agent_name = step['agent']
                col_index = i % len(agent_columns)
                
                with agent_columns[col_index]:
                    # Create agent card
                    agent_card = st.empty()
                    agent_status[agent_name] = {
                        'card': agent_card,
                        'status': 'waiting',
                        'step': step
                    }
        
        # Animate workflow execution
        for i, step in enumerate(workflow_steps):
            agent_name = step['agent']
            
            # Update progress
            progress = (i + 1) / total_steps
            progress_bar.progress(progress)
            status_text.text(f"Executing step {i+1}/{total_steps}: {step['action']}")
            
            # Update agent status to "working"
            agent_status[agent_name]['status'] = 'working'
            self.update_agent_card(agent_status[agent_name])
            
            # Perform actual validation if this is the Claims Validation Agent
            if agent_name == 'Claims Validation Agent':
                validation_result = self._perform_real_validation(task, step)
                step['result'] = validation_result['summary']
                step['validation_details'] = validation_result
            
            # Simulate processing time
            time.sleep(step.get('estimated_duration', 2))
            
            # Update agent status to "completed"
            agent_status[agent_name]['status'] = 'completed'
            agent_status[agent_name]['result'] = step.get('result', 'Task completed successfully')
            self.update_agent_card(agent_status[agent_name])
            
            # Small delay between steps
            time.sleep(0.5)
        
        # Final status
        status_text.text("✅ Workflow completed successfully!")
        
        # Display final results
        st.subheader("📊 Workflow Results")
        self.display_workflow_results(workflow_steps)
        
        # Display enhanced framework information
        self.display_enhanced_workflow_info(task)
        
        # Update credit balance
        credits_used = sum(step.get('credits_used', 1) for step in workflow_steps)
        st.session_state.credit_balance = max(0, st.session_state.credit_balance - credits_used)
        st.success(f"Workflow completed! Used {credits_used} credits.")

    def generate_dynamic_workflow(self, task: str, context: dict, credit_budget: int):
        """Generate dynamic workflow using Hierarchical Framework"""
        
        # Initialize the hierarchical framework
        framework = HierarchicalFramework()
        
        # Use the framework to select agents dynamically
        framework_result = framework.select_agents_dynamically(task, context, credit_budget)
        
        # Convert framework result to workflow steps
        workflow_steps = []
        
        for i, agent_info in enumerate(framework_result['optimized_sequence']):
            agent_name = agent_info['agent_name']
            
            # Generate AI-powered action for each agent
            action_prompt = f"""
            You are a {agent_name} in an insurance workflow. Generate a specific action for this task:
            
            Task: "{task}"
            Context: {json.dumps(context)}
            Agent Specializations: {agent_info['specializations']}
            Complexity Level: {framework_result['complexity']}
            
            Generate a specific, actionable step that this agent would perform.
            Return only the action description (1-2 sentences).
            """
            
            try:
                response = self.openai_client.get_chat_completion(action_prompt)
                action = response.get('response', f'Perform {agent_name} analysis for the task')
            except:
                action = f'Perform {agent_name} analysis and provide recommendations'
            
            # Generate AI-powered result
            result_prompt = f"""
            As a {agent_name}, provide a realistic result for this action:
            Action: "{action}"
            Task: "{task}"
            
            Generate a brief, realistic result that this agent would produce.
            Return only the result description (1-2 sentences).
            """
            
            try:
                response = self.openai_client.get_chat_completion(result_prompt)
                result = response.get('response', f'{agent_name} analysis completed successfully')
            except:
                result = f'{agent_name} has completed the assigned task with positive outcome'
            
            # Generate reasoning steps
            reasoning_steps = [
                f"Analyzing task from {agent_name} perspective",
                f"Applying {', '.join(agent_info['specializations'])} expertise",
                f"Generating recommendations based on {framework_result['complexity']} complexity"
            ]
            
            workflow_step = {
                'agent': agent_name,
                'action': action,
                'estimated_duration': agent_info['estimated_duration'],
                'confidence': 0.85 + (0.1 * (5 - len(framework_result['optimized_sequence']))),  # Higher confidence with fewer agents
                'reasoning_steps': reasoning_steps,
                'result': result,
                'credits_used': agent_info['credit_cost'],
                'tier': agent_info['tier'],
                'specializations': agent_info['specializations'],
                'dependencies': agent_info['dependencies']
            }
            
            workflow_steps.append(workflow_step)
        
        # Add framework metadata to session state for later use
        if 'workflow_metadata' not in st.session_state:
            st.session_state.workflow_metadata = {}
        
        st.session_state.workflow_metadata[task] = {
            'framework_version': '2.0_hierarchical',
            'complexity_analysis': framework_result['complexity_analysis'],
            'total_agents': len(workflow_steps),
            'resource_allocation': framework_result['resource_allocation'],
            'search_context': framework_result.get('search_context'),
            'generation_timestamp': datetime.now().isoformat()
        }
        
        return workflow_steps

    def update_agent_card(self, agent_info):
        """Update agent card display with current status"""
        step = agent_info['step']
        status = agent_info['status']
        
        # Status colors and icons
        status_config = {
            'waiting': {'color': '#FFA500', 'icon': '⏳', 'text': 'Waiting'},
            'working': {'color': '#1E90FF', 'icon': '⚡', 'text': 'Working'},
            'completed': {'color': '#32CD32', 'icon': '✅', 'text': 'Completed'}
        }
        
        config = status_config.get(status, status_config['waiting'])
        
        card_html = f"""
        <div style="
            border: 2px solid {config['color']};
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
            backdrop-filter: blur(10px);
        ">
            <h4 style="color: {config['color']}; margin: 0 0 10px 0;">
                {config['icon']} {step['agent']}
            </h4>
            <p style="margin: 5px 0; font-size: 14px;">
                <strong>Status:</strong> {config['text']}
            </p>
            <p style="margin: 5px 0; font-size: 14px;">
                <strong>Action:</strong> {step['action']}
            </p>
            <p style="margin: 5px 0; font-size: 14px;">
                <strong>Confidence:</strong> {step['confidence']:.0%}
            </p>
        """
        
        if status == 'completed' and 'result' in agent_info:
            card_html += f"""
            <p style="margin: 5px 0; font-size: 14px;">
                <strong>Result:</strong> {agent_info['result'][:100]}{'...' if len(agent_info['result']) > 100 else ''}
            </p>
            """
        
        card_html += "</div>"
        
        agent_info['card'].markdown(card_html, unsafe_allow_html=True)

    def display_workflow_results(self, workflow_steps):
        """Display comprehensive workflow results"""
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        total_credits = sum(step.get('credits_used', 1) for step in workflow_steps)
        avg_confidence = sum(step.get('confidence', 0.8) for step in workflow_steps) / len(workflow_steps)
        total_agents = len(set(step['agent'] for step in workflow_steps))
        
        with col1:
            st.metric("Total Steps", len(workflow_steps))
        with col2:
            st.metric("Credits Used", total_credits)
        with col3:
            st.metric("Avg Confidence", f"{avg_confidence:.0%}")
        with col4:
            st.metric("Agents Involved", total_agents)
        
        # Detailed results
        st.markdown("### 📋 Detailed Results")
        
        for i, step in enumerate(workflow_steps, 1):
            with st.expander(f"Step {i}: {step['agent']} - {step['action'][:50]}..."):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Agent:** {step['agent']}")
                    st.markdown(f"**Action:** {step['action']}")
                    st.markdown(f"**Confidence:** {step['confidence']:.0%}")
                    st.markdown(f"**Credits Used:** {step['credits_used']}")
                
                with col2:
                    st.markdown("**Reasoning Steps:**")
                    for j, reasoning in enumerate(step.get('reasoning_steps', []), 1):
                        st.markdown(f"{j}. {reasoning}")
                
                st.markdown("**Result:**")
                st.markdown(step.get('result', 'No result available'))
        
        # Export options
        st.markdown("### 📤 Export Options")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Export to CSV"):
                # Create CSV data
                csv_data = []
                for i, step in enumerate(workflow_steps, 1):
                    csv_data.append({
                        'Step': i,
                        'Agent': step['agent'],
                        'Action': step['action'],
                        'Confidence': step['confidence'],
                        'Credits Used': step['credits_used'],
                        'Result': step.get('result', '')
                    })
                
                df = pd.DataFrame(csv_data)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"workflow_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("📄 Export to JSON"):
                json_data = json.dumps(workflow_steps, indent=2)
                st.download_button(
                    label="Download JSON",
                    data=json_data,
                    file_name=f"workflow_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        
        with col3:
            if st.button("📧 Email Results"):
                st.success("Results emailed successfully!")

    def create_enhanced_workflow_visualization(self, task: str, agents: list):
        """Create enhanced animated workflow visualization"""
        # This function can be expanded for additional visualization features
        pass

    def display_enhanced_workflow_info(self, task: str):
        """Display enhanced workflow information from hierarchical framework"""
        
        if 'workflow_metadata' not in st.session_state or task not in st.session_state.workflow_metadata:
            return
        
        metadata = st.session_state.workflow_metadata[task]
        
        # Display framework information
        st.subheader("🔧 Hierarchical Framework Analysis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Framework Version", 
                metadata['framework_version'],
                help="Version of the hierarchical framework used"
            )
        
        with col2:
            st.metric(
                "Total Agents", 
                metadata['total_agents'],
                help="Number of agents selected for this workflow"
            )
        
        with col3:
            complexity_analysis = metadata.get('complexity_analysis', {})
            complexity = complexity_analysis.get('final_complexity', 'moderate')
            st.metric(
                "Task Complexity", 
                complexity.name.title(),
                help="Assessed complexity level of the task"
            )
        
        # Display complexity analysis details
        if complexity_analysis:
            with st.expander("📊 Detailed Complexity Analysis"):
                st.write("**Entity Analysis:**")
                entities = complexity_analysis.get('entities', [])
                if entities:
                    for entity in entities:
                        st.write(f"• {entity}")
                else:
                    st.write("No specific entities identified")
                
                st.write("**Context Factors:**")
                context_factors = complexity_analysis.get('context_factors', [])
                if context_factors:
                    for factor in context_factors:
                        st.write(f"• {factor.replace('_', ' ').title()}")
                else:
                    st.write("No additional context factors")
                
                ai_assessment = complexity_analysis.get('ai_assessment', {})
                if ai_assessment:
                    st.write("**AI Assessment:**")
                    st.write(f"• Complexity Score: {ai_assessment.get('complexity_score', 'N/A')}/10")
                    st.write(f"• Risk Level: {ai_assessment.get('risk_level', 'N/A').title()}")
                    st.write(f"• Estimated Steps: {ai_assessment.get('estimated_steps', 'N/A')}")
                    
                    reasoning = ai_assessment.get('reasoning', '')
                    if reasoning:
                        st.write("**Reasoning:**")
                        st.write(reasoning)
        
        # Display resource allocation
        resource_allocation = metadata.get('resource_allocation', {})
        if resource_allocation:
            with st.expander("💰 Resource Allocation Analysis"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Base Cost", f"{resource_allocation.get('base_cost', 0)} credits")
                    st.metric("Adjusted Cost", f"{resource_allocation.get('adjusted_cost', 0)} credits")
                    st.metric("Budget Utilization", f"{resource_allocation.get('budget_utilization', 0):.1%}")
                
                with col2:
                    st.metric("Base Duration", f"{resource_allocation.get('base_duration', 0)} min")
                    st.metric("Adjusted Duration", f"{resource_allocation.get('adjusted_duration', 0)} min")
                    st.metric("Resource Efficiency", f"{resource_allocation.get('resource_efficiency', 0):.2f}")
        
        # Display search context if available
        search_context = metadata.get('search_context')
        if search_context:
            with st.expander("🔍 Real-Time Search Context"):
                st.write(f"**Task:** {search_context.get('task', 'N/A')}")
                st.write(f"**Location:** {search_context.get('location', 'N/A')}")
                st.write(f"**Total Sources:** {search_context.get('total_sources', 0)}")
                
                context_searches = search_context.get('context_searches', [])
                if context_searches:
                    for search_type, search_data in context_searches:
                        st.write(f"**{search_type.title()} Search:**")
                        st.write(f"• Query: {search_data.get('query', 'N/A')}")
                        st.write(f"• Results: {len(search_data.get('results', []))}")
                        st.write(f"• Summary: {search_data.get('summary', 'No summary available')}")

    def _perform_real_validation(self, task: str, step: dict) -> dict:
        """Perform actual claim validation using external APIs"""
        try:
            # Initialize the claim validator
            validator = ClaimValidator()
            
            # Extract claim details from the task
            claim_details = self._extract_claim_from_task(task)
            
            if claim_details:
                # Perform validation
                validation_result = validator.validate_claim(
                    claim_details['claim_text'],
                    claim_details['date'],
                    claim_details['location']
                )
                
                # Generate summary for display
                summary = f"""
                Validation Status: {validation_result.get('validation_status', 'UNKNOWN')}
                Confidence: {validation_result.get('confidence_score', 0.0):.2f}
                Sources Checked: {', '.join(validation_result.get('data_sources_checked', []))}
                Evidence Found: {len(validation_result.get('evidence_found', []))} items
                """
                
                return {
                    'summary': summary.strip(),
                    'full_validation': validation_result,
                    'report': validator.get_validation_report(validation_result)
                }
            else:
                return {
                    'summary': 'Unable to extract claim details for validation',
                    'full_validation': None,
                    'report': 'Claim validation requires specific claim details (event, date, location)'
                }
                
        except Exception as e:
            return {
                'summary': f'Validation failed: {str(e)}',
                'full_validation': None,
                'report': f'Error during validation: {str(e)}'
            }

    def _extract_claim_from_task(self, task: str) -> dict:
        """Extract claim details from task description"""
        try:
            # Use AI to extract claim details
            prompt = f"""
            Extract claim details from this task description:
            "{task}"
            
            If this appears to be an insurance claim, extract:
            1. The event/incident description
            2. Date (if mentioned)
            3. Location (if mentioned)
            
            Return in JSON format:
            {{
                "is_claim": true/false,
                "claim_text": "description of the incident",
                "date": "extracted date or 'unknown'",
                "location": "extracted location or 'unknown'"
            }}
            
            If this is not a claim (e.g., just a question), set is_claim to false.
            """
            
            response = self.openai_client.get_chat_completion(prompt)
            result = json.loads(response.get('response', '{}'))
            
            if result.get('is_claim', False):
                return result
            else:
                return None
                
        except Exception as e:
            # Try simple pattern matching as fallback
            task_lower = task.lower()
            claim_keywords = ['claim', 'damage', 'accident', 'earthquake', 'flood', 'fire', 'theft', 'loss']
            
            if any(keyword in task_lower for keyword in claim_keywords):
                return {
                    'is_claim': True,
                    'claim_text': task,
                    'date': 'unknown',
                    'location': 'unknown'
                }
            
            return None

    def render_agent_dashboard(self):
        """Render the agent management dashboard"""
        st.header("🤖 Multi-Agent Management Dashboard")
        st.markdown("*Real-time agent monitoring and performance analytics*")
        
        # Agent status overview
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("🏗️ Agent Hierarchy")
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
            all_agents = get_all_agents()  # Implement this to return all agent names/classes
            default_len = len(all_agents)
            def pad(lst, fill=0):
                return lst + [fill] * (default_len - len(lst))

            performance_data = {
                'Agent': all_agents,
                'Tasks Completed': pad([15, 23, 8, 31, 12, 19]),
                'Avg Response Time (s)': pad([2.1, 1.8, 3.2, 1.5, 2.8, 2.3]),
                'Success Rate (%)': pad([98, 96, 99, 97, 95, 98])
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
        """Display embedded insurance APIs interface with real OpenAPI integration"""
        st.header("🔌 Embedded Insurance APIs")
        st.markdown("*Real OpenAPI integration with dynamic form generation*")
        
        # OpenAPI Configuration
        st.subheader("⚙️ OpenAPI Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            spec_source = st.radio("OpenAPI Spec Source", ["Built-in Insurance API", "Custom URL", "Upload Spec"])
            
            if spec_source == "Custom URL":
                spec_url = st.text_input("OpenAPI Spec URL", placeholder="https://api.example.com/openapi.json")
                if st.button("Load Spec from URL"):
                    if self.openapi_handler.load_openapi_spec(spec_url=spec_url):
                        st.success("✅ OpenAPI specification loaded successfully!")
                    else:
                        st.error("❌ Failed to load OpenAPI specification")
            
            elif spec_source == "Upload Spec":
                uploaded_file = st.file_uploader("Upload OpenAPI Spec", type=['yaml', 'yml', 'json'])
                if uploaded_file:
                    spec_content = uploaded_file.read().decode('utf-8')
                    if self.openapi_handler.load_openapi_spec(spec_content=spec_content):
                        st.success("✅ OpenAPI specification uploaded successfully!")
        
        with col2:
            st.markdown("**Available Endpoints:**")
            endpoints = self.openapi_handler.get_available_endpoints()
            for endpoint in endpoints:
                st.markdown(f"• `{endpoint}`")
        
        # Dynamic API Testing Interface
        st.subheader("🧪 Dynamic API Testing")
        
        if endpoints:
            selected_endpoint = st.selectbox("Select Endpoint", endpoints)
            endpoint_info = self.openapi_handler.get_endpoint_info(selected_endpoint)
            
            # Display endpoint information
            if endpoint_info:
                st.markdown(f"**Endpoint:** `{selected_endpoint}`")
                
                # Get request schema for form generation
                post_info = endpoint_info.get('post', {})
                request_body = post_info.get('requestBody', {})
                content = request_body.get('content', {})
                json_content = content.get('application/json', {})
                schema_ref = json_content.get('schema', {}).get('$ref', '')
                
                if schema_ref:
                    schema_name = schema_ref.split('/')[-1]  # Extract schema name from $ref
                    
                    st.markdown(f"**Request Schema:** `{schema_name}`")
                    
                    # Generate dynamic form
                    with st.form(f"api_form_{selected_endpoint}"):
                        st.markdown("### 📝 Request Parameters")
                        form_data = self.openapi_handler.generate_form_from_schema(schema_name)
                        
                        submitted = st.form_submit_button("🚀 Make API Call")
                        
                        if submitted:
                            # Filter out empty values
                            clean_data = {k: v for k, v in form_data.items() if v}
                            
                            with st.spinner("Making API call..."):
                                response = self.openapi_handler.make_api_call(selected_endpoint, "POST", clean_data)
                            
                            st.success("✅ API call successful!")
                            
                            # Display response
                            st.subheader("📤 API Response")
                            st.json(response)
                            
                            # Display response analysis
                            if selected_endpoint == "/quotes" and 'monthlyPremium' in response:
                                st.subheader("📊 Quote Analysis")
                                col1, col2, col3 = st.columns(3)
                                
                                with col1:
                                    st.metric("Monthly Premium", f"${response['monthlyPremium']}")
                                
                                with col2:
                                    st.metric("Annual Premium", f"${response['annualPremium']}")
                                
                                with col3:
                                    st.metric("Quote ID", response['quoteId'])
                            
                            elif selected_endpoint == "/claims" and 'claimId' in response:
                                st.subheader("📋 Claim Status")
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    st.metric("Claim ID", response['claimId'])
                                
                                with col2:
                                    st.metric("Status", response['status'])
                                
                                st.info(f"⏱️ Estimated processing time: {response.get('estimatedProcessingTime', 'N/A')}")
        
        # API Performance Metrics
        st.subheader("📈 API Performance Metrics")
        
        # Mock performance data
        performance_data = {
            'Endpoint': ['/claims', '/quotes', '/policies'],
            'Calls Today': [45, 123, 67],
            'Success Rate': ['98%', '99%', '97%'],
            'Avg Response Time': ['245ms', '180ms', '320ms'],
            'Last Call': ['2 min ago', '30 sec ago', '5 min ago']
        }
        
        df_performance = pd.DataFrame(performance_data)
        st.dataframe(df_performance, use_container_width=True)
        
        # Real-time API monitoring
        st.subheader("🔍 Real-Time Monitoring")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**API Health Status:**")
            st.success("🟢 All APIs operational")
            st.info("🔵 Claims API: Normal load")
            st.warning("🟡 Quotes API: High traffic")
        
        with col2:
            st.markdown("**Recent API Calls:**")
            recent_calls = [
                "✅ POST /quotes - 180ms",
                "✅ POST /claims - 245ms", 
                "✅ GET /policies - 120ms",
                "❌ POST /quotes - Timeout",
                "✅ POST /claims - 190ms"
            ]
            
            for call in recent_calls:
                st.markdown(f"• {call}")
        
        # Schema Documentation
        with st.expander("📚 API Schema Documentation"):
            st.markdown("### Available Schemas")
            
            for schema_name, schema_def in self.openapi_handler.schemas.items():
                st.markdown(f"#### {schema_name}")
                
                properties = schema_def.get('properties', {})
                required_fields = schema_def.get('required', [])
                
                for prop_name, prop_def in properties.items():
                    required_indicator = " **(required)**" if prop_name in required_fields else ""
                    prop_type = prop_def.get('type', 'unknown')
                    description = prop_def.get('description', 'No description')
                    
                    st.markdown(f"• **{prop_name}** ({prop_type}){required_indicator}: {description}")
                
                st.markdown("---")

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

def get_all_agents():
    # Replace this list with all your actual agent names
    return [
        "Enhanced Coordinator",
        "Claims Specialist",
        "Risk Analyst",
        "Fraud Detector",
        "Policy Advisor",
        "Customer Service",
        "Underwriter",
        "Weather Analyst", 
        "Fraud Investigator",
        "Data Analyst",
        "ESG Specialist",
        "Compliance Officer",
        "Dynamic Search Agent",
        "Workflow Coordinator",
        "Quality Assurance Agent",
        "Emergency Response Agent"
    ]

if __name__ == "__main__":
    main()

