"""
NewGenZ AI Insurance Platform - Helper Functions Module

This module contains all the helper functions and supporting functionality
for the main appplus.py application.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import time
import uuid
import random
from components.openai_client import OpenAIClient

# Mock data and helper functions

def generate_travel_insurance_response(user_input):
    """Generate AI response for travel insurance chatbot"""
    openai_client = OpenAIClient()
    response = openai_client.get_chat_completion(f"Provide a concise travel insurance recommendation for {user_input}. Focus on key coverage aspects and any relevant travel advisories.")
    return response.get("response", "I\"m sorry, I couldn\"t generate a response at this time.")

def generate_travel_quote(destination, departure_date, return_date, travelers, coverage_type, trip_cost):
    """Generate a travel insurance quote using OpenAI."""
    openai_client = OpenAIClient()
    prompt = f"Generate a travel insurance quote for a trip to {destination} from {departure_date} to {return_date} for {travelers} travelers with {coverage_type} coverage and a trip cost of ${trip_cost}. Provide a realistic quote including total premium, base premium, weather adjustment, duration adjustment, traveler adjustment, and a brief explanation of factors influencing the cost. The response should be in a JSON format with keys: quote_id, destination, departure_date, return_date, duration, travelers, coverage_type, trip_cost, total_premium, base_premium, weather_adjustment, duration_adjustment, traveler_adjustment, explanation, valid_until, timestamp."
    response = openai_client.get_chat_completion(prompt)
    try:
        quote_data = json.loads(response.get("response", "{}"))
        # Add missing fields with default/mock values if OpenAI doesn't provide them
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
        quote_data["total_premium"] = quote_data.get("total_premium", 0)
        quote_data["base_premium"] = quote_data.get("base_premium", 0)
        quote_data["weather_adjustment"] = quote_data.get("weather_adjustment", 0)
        quote_data["duration_adjustment"] = quote_data.get("duration_adjustment", 0)
        quote_data["traveler_adjustment"] = quote_data.get("traveler_adjustment", 0)
        quote_data["explanation"] = quote_data.get("explanation", "No explanation provided.")
        quote_data["weather_risk_factor"] = quote_data.get("weather_risk_factor", 0.1) # Add default for weather_risk_factor
        return quote_data
    except json.JSONDecodeError:
        st.error("Failed to parse quote response from OpenAI. Please try again.")
        return None

def get_weather_risk_factor(destination):
    """Get weather risk factor for destination using OpenAI."""
    openai_client = OpenAIClient()
    prompt = f"What is the current weather risk factor for {destination} on a scale of 0 to 1, where 0 is no risk and 1 is extremely high risk? Provide only the numerical value."
    response = openai_client.get_chat_completion(prompt)
    try:
        risk_factor = float(response.get("response", "0.1"))
        return max(0.0, min(1.0, risk_factor)) # Ensure value is between 0 and 1
    except ValueError:
        return 0.1 # Default risk factor if OpenAI response is not a valid number

def display_travel_quote(quote):
    """Display travel insurance quote"""
    
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
    if quote['weather_risk_factor'] > 0.2:
        st.warning(f"⚠️ High weather risk detected for {quote['destination']}. Enhanced coverage recommended.")
    elif quote['weather_risk_factor'] > 0.1:
        st.info(f"🌤️ Moderate weather risk for {quote['destination']}. Standard coverage should be sufficient.")
    else:
        st.success(f"☀️ Low weather risk for {quote['destination']}. Excellent travel conditions expected.")

def display_api_provider_config(provider_name, description, api_key):
    """Display API provider configuration"""
    
    st.subheader(f"{provider_name} Integration")
    st.markdown(f"*{description}*")
    
    # Configuration form
    with st.form(f"{api_key}_config"):
        col1, col2 = st.columns(2)
        
        with col1:
            api_endpoint = st.text_input("API Endpoint", value=f"https://api.{provider_name.lower()}.com/v1")
            api_key_input = st.text_input("API Key", type="password", placeholder="Enter your API key")
            
        with col2:
            environment = st.selectbox("Environment", ["Sandbox", "Production"])
            timeout = st.number_input("Timeout (seconds)", min_value=5, max_value=60, value=30)
        
        # Feature toggles
        st.markdown("**Available Features:**")
        col1, col2 = st.columns(2)
        
        with col1:
            quotes_enabled = st.checkbox("Quote Generation", value=True)
            policies_enabled = st.checkbox("Policy Management", value=True)
            
        with col2:
            claims_enabled = st.checkbox("Claims Processing", value=True)
            webhooks_enabled = st.checkbox("Webhook Notifications", value=False)
        
        submitted = st.form_submit_button("💾 Save Configuration")
        
        if submitted:
            st.success(f"✅ {provider_name} configuration saved successfully!")
    
    # Connection status
    status = random.choice(["Connected", "Disconnected", "Error"])
    status_color = {"Connected": "🟢", "Disconnected": "🔴", "Error": "🟡"}
    
    st.markdown(f"**Connection Status:** {status_color[status]} {status}")
    
    if status == "Connected":
        st.markdown("**Last Successful Call:** 2 minutes ago")
        st.markdown("**Response Time:** 245ms")
    
    # Usage statistics
    st.markdown("**Usage Statistics (Last 30 days):**")
    usage_data = {
        'Metric': ['API Calls', 'Successful Calls', 'Failed Calls', 'Avg Response Time'],
        'Value': [f"{random.randint(1000, 5000):,}", f"{random.randint(950, 4950):,}", f"{random.randint(10, 100)}", f"{random.randint(200, 500)}ms"]
    }
    df_usage = pd.DataFrame(usage_data)
    st.dataframe(df_usage, use_container_width=True)

def simulate_api_call(provider, endpoint, payload):
    """Simulate API call for testing"""
    
    # Mock responses based on provider and endpoint
    responses = {
        "Lemonade": {
            "Get Quote": {
                "quote_id": f"LEM_{random.randint(100000, 999999)}",
                "premium": random.randint(15, 50),
                "coverage_amount": 50000,
                "deductible": 500,
                "valid_until": (datetime.now() + timedelta(days=30)).isoformat()
            },
            "Create Policy": {
                "policy_id": f"POL_LEM_{random.randint(100000, 999999)}",
                "status": "active",
                "effective_date": datetime.now().isoformat(),
                "premium": random.randint(15, 50)
            }
        },
        "Coalition": {
            "Get Quote": {
                "quote_id": f"COA_{random.randint(100000, 999999)}",
                "premium": random.randint(100, 500),
                "coverage_amount": 1000000,
                "cyber_score": random.randint(70, 95)
            }
        }
    }
    
    return responses.get(provider, {}).get(endpoint, {
        "status": "success",
        "message": "API call completed successfully",
        "timestamp": datetime.now().isoformat()
    })

def display_broker_dashboard():
    """Display broker dashboard"""
    
    st.subheader("📊 Broker Performance Dashboard")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Clients", "156", delta="+12 this month")
    
    with col2:
        st.metric("Policies Sold", "89", delta="+15 this month")
    
    with col3:
        st.metric("Total Premium", "$234,567", delta="+$45,678 this month")
    
    with col4:
        st.metric("Commission Earned", "$18,765", delta="+$3,654 this month")
    
    # Recent activities
    st.markdown("### 📈 Recent Activities")
    
    activities = [
        {'Date': '2024-12-07', 'Activity': 'New Client Onboarded', 'Client': 'ABC Corp', 'Value': '$15,000'},
        {'Date': '2024-12-06', 'Activity': 'Policy Renewed', 'Client': 'XYZ Ltd', 'Value': '$8,500'},
        {'Date': '2024-12-05', 'Activity': 'Claim Processed', 'Client': 'Smith Family', 'Value': '$3,200'},
        {'Date': '2024-12-04', 'Activity': 'Quote Generated', 'Client': 'Johnson Inc', 'Value': '$12,000'}
    ]
    
    df_activities = pd.DataFrame(activities)
    st.dataframe(df_activities, use_container_width=True)

def display_client_management():
    """Display client management interface"""
    
    st.subheader("👥 Client Management")
    
    # Client search and filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_term = st.text_input("🔍 Search Clients", placeholder="Enter client name or ID")
    
    with col2:
        client_type = st.selectbox("Client Type", ["All", "Individual", "Business", "Corporate"])
    
    with col3:
        status_filter = st.selectbox("Status", ["All", "Active", "Inactive", "Prospect"])
    
    # Client list
    st.markdown("### 📋 Client List")
    
    clients = [
        {'ID': 'C001', 'Name': 'John Smith', 'Type': 'Individual', 'Policies': 3, 'Premium': '$4,500', 'Status': 'Active'},
        {'ID': 'C002', 'Name': 'ABC Corporation', 'Type': 'Business', 'Policies': 8, 'Premium': '$45,000', 'Status': 'Active'},
        {'ID': 'C003', 'Name': 'Sarah Johnson', 'Type': 'Individual', 'Policies': 2, 'Premium': '$2,800', 'Status': 'Active'},
        {'ID': 'C004', 'Name': 'XYZ Industries', 'Type': 'Corporate', 'Policies': 15, 'Premium': '$125,000', 'Status': 'Active'},
        {'ID': 'C005', 'Name': 'Mike Davis', 'Type': 'Individual', 'Policies': 1, 'Premium': '$1,200', 'Status': 'Prospect'}
    ]
    
    df_clients = pd.DataFrame(clients)
    st.dataframe(df_clients, use_container_width=True)
    
    # Add new client
    if st.button("➕ Add New Client"):
        display_add_client_form()

def display_add_client_form():
    """Display add new client form"""
    
    with st.form("add_client"):
        st.subheader("➕ Add New Client")
        
        col1, col2 = st.columns(2)
        
        with col1:
            client_name = st.text_input("Client Name*")
            client_type = st.selectbox("Client Type*", ["Individual", "Business", "Corporate"])
            email = st.text_input("Email*")
            
        with col2:
            phone = st.text_input("Phone")
            address = st.text_area("Address")
            notes = st.text_area("Notes")
        
        submitted = st.form_submit_button("💾 Add Client")
        
        if submitted and client_name and email:
            client_id = f"C{random.randint(100, 999)}"
            st.success(f"✅ Client {client_name} added successfully! Client ID: {client_id}")

def display_policy_management():
    """Display policy management interface"""
    
    st.subheader("📋 Policy Management")
    
    # Policy summary
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Policies", "281", delta="+23 this month")
    
    with col2:
        st.metric("Active Policies", "267", delta="+18 this month")
    
    with col3:
        st.metric("Pending Renewals", "14", delta="-5 from last month")
    
    with col4:
        st.metric("Avg Policy Value", "$3,456", delta="+$234 this month")
    
    # Policy breakdown by type
    st.markdown("### 📊 Policy Breakdown")
    
    policy_summary = [
        {'Policy Type': 'Auto Insurance', 'Active Policies': 123, 'Total Premium': '$145,000', 'Avg Premium': '$1,179'},
        {'Policy Type': 'Home Insurance', 'Active Policies': 67, 'Total Premium': '$234,500', 'Avg Premium': '$3,500'},
        {'Policy Type': 'Business Insurance', 'Active Policies': 34, 'Total Premium': '$189,600', 'Avg Premium': '$5,576'},
        {'Policy Type': 'Travel Insurance', 'Active Policies': 57, 'Total Premium': '$28,500', 'Avg Premium': '$500'}
    ]
    df_summary = pd.DataFrame(policy_summary)
    st.dataframe(df_summary, use_container_width=True)
    
    # Recent policy activities
    st.markdown("**Recent Policy Activities:**")
    
    activities = [
        {'Date': '2024-12-07', 'Activity': 'Policy Created', 'Client': 'John Smith', 'Policy': 'AUTO-2024-001', 'Amount': '$1,200'},
        {'Date': '2024-12-06', 'Activity': 'Policy Renewed', 'Client': 'Sarah Johnson', 'Policy': 'HOME-2023-045', 'Amount': '$2,400'},
        {'Date': '2024-12-05', 'Activity': 'Policy Modified', 'Client': 'Mike Davis', 'Policy': 'BUS-2024-012', 'Amount': '$5,600'},
        {'Date': '2024-12-04', 'Activity': 'Policy Cancelled', 'Client': 'Lisa Wilson', 'Policy': 'TRAVEL-2024-089', 'Amount': '$350'}
    ]
    
    df_activities = pd.DataFrame(activities)
    st.dataframe(df_activities, use_container_width=True)

def display_commission_tracking():
    """Display commission tracking dashboard"""
    
    st.subheader("💰 Commission Tracking")
    
    # Commission summary
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("This Month", "$8,450", delta="$1,200 vs last month")
    
    with col2:
        st.metric("This Quarter", "$23,670", delta="$3,400 vs last quarter")
    
    with col3:
        st.metric("This Year", "$89,230", delta="$15,600 vs last year")
    
    with col4:
        st.metric("Pending", "$5,680", delta="3 policies pending")
    
    # Commission breakdown
    st.markdown("**Commission Breakdown by Product:**")
    
    commission_data = [
        {'Product': 'Auto Insurance', 'Policies Sold': 23, 'Commission Rate': '8%', 'Total Commission': '$3,456'},
        {'Product': 'Home Insurance', 'Policies Sold': 15, 'Commission Rate': '10%', 'Total Commission': '$2,890'},
        {'Product': 'Business Insurance', 'Policies Sold': 8, 'Commission Rate': '12%', 'Total Commission': '$1,678'},
        {'Product': 'Travel Insurance', 'Policies Sold': 34, 'Commission Rate': '15%', 'Total Commission': '$426'}
    ]
    
    df_commission = pd.DataFrame(commission_data)
    st.dataframe(df_commission, use_container_width=True)

def display_broker_api_access():
    """Display broker API access and integration tools"""
    
    st.subheader("🔌 API Access & Integration")
    
    # API credentials
    st.markdown("**Your API Credentials:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        api_key = "bk_live_" + "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=32))
        st.code(f"API Key: {api_key}")
        
        webhook_url = st.text_input("Webhook URL", placeholder="https://your-system.com/webhooks/zurich")
        
    with col2:
        st.markdown("**API Limits:**")
        st.markdown("• Requests per minute: 1,000")
        st.markdown("• Requests per day: 50,000")
        st.markdown("• Rate limit reset: Every minute")
        
        if st.button("🔄 Regenerate API Key"):
            st.success("New API key generated!")

def display_partner_network():
    """Display partner network and ecosystem integrations"""
    
    st.subheader("🤝 Partner Network & Ecosystem")
    
    # Partner categories
    partner_tabs = st.tabs(["🏢 Insurance Carriers", "🔧 Technology Partners", "📊 Data Providers"])
    
    with partner_tabs[0]:
        st.markdown("**Connected Insurance Carriers:**")
        
        carriers = [
            {'Name': 'Zurich Insurance', 'Status': 'Connected', 'Products': 'Auto, Home, Business', 'Commission': '8-12%'},
            {'Name': 'AIG', 'Status': 'Connected', 'Products': 'Commercial, Specialty', 'Commission': '10-15%'},
            {'Name': 'Travelers', 'Status': 'Pending', 'Products': 'Auto, Home', 'Commission': '7-10%'},
            {'Name': 'Liberty Mutual', 'Status': 'Available', 'Products': 'Auto, Home, Business', 'Commission': '8-11%'}
        ]
        
        df_carriers = pd.DataFrame(carriers)
        st.dataframe(df_carriers, use_container_width=True)
    
    with partner_tabs[1]:
        st.markdown("**Technology Integration Partners:**")
        
        tech_partners = [
            {'Name': 'Salesforce CRM', 'Type': 'CRM Integration', 'Status': 'Active'},
            {'Name': 'DocuSign', 'Type': 'Digital Signatures', 'Status': 'Active'},
            {'Name': 'Stripe', 'Type': 'Payment Processing', 'Status': 'Active'},
            {'Name': 'Twilio', 'Type': 'Communications', 'Status': 'Inactive'}
        ]
        
        df_tech = pd.DataFrame(tech_partners)
        st.dataframe(df_tech, use_container_width=True)
    
    with partner_tabs[2]:
        st.markdown("**Data Provider Integrations:**")
        
        data_providers = [
            {'Provider': 'Weather API', 'Data Type': 'Weather & Climate', 'Usage': 'High', 'Cost': '$0.02/call'},
            {'Provider': 'Credit Bureau', 'Data Type': 'Credit Scores', 'Usage': 'Medium', 'Cost': '$0.50/query'},
            {'Provider': 'Vehicle Data', 'Data Type': 'VIN Lookup', 'Usage': 'High', 'Cost': '$0.10/lookup'},
            {'Provider': 'Property Data', 'Data Type': 'Property Values', 'Usage': 'Medium', 'Cost': '$0.25/query'}
        ]
        
        df_data = pd.DataFrame(data_providers)
        st.dataframe(df_data, use_container_width=True)

def display_claims_explanation_demo():
    """Display claims processing explanation demo"""
    
    st.markdown("**Sample Claim Decision Explanation:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Claim Details:**
        - Claim ID: CLM-2024-001234
        - Type: Auto Collision
        - Amount: $8,500
        - Decision: Approved
        """)
        
        st.markdown("""
        **Key Decision Factors:**
        1. **Policy Coverage (40%)**: Comprehensive coverage active
        2. **Weather Conditions (25%)**: Heavy rain confirmed at incident time
        3. **Location Analysis (20%)**: High-risk intersection with history
        4. **Driver History (15%)**: Clean driving record
        """)
    
    with col2:
        st.markdown("""
        **AI Confidence Score: 94%**
        
        **Data Sources Used:**
        - Policy database
        - Weather API (real-time)
        - Traffic incident reports
        - Driver history records
        
        **Customer Rights:**
        - Right to appeal decision
        - Request human review
        - Access to full explanation
        """)

def display_risk_explanation_demo():
    """Display risk assessment explanation demo"""
    
    st.markdown("**Sample Risk Assessment Explanation:**")
    
    # Risk score visualization
    risk_score = 0.65
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = risk_score * 100,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Risk Score"},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkred" if risk_score > 0.7 else "orange" if risk_score > 0.4 else "green"},
            'steps': [
                {'range': [0, 40], 'color': "lightgreen"},
                {'range': [40, 70], 'color': "yellow"},
                {'range': [70, 100], 'color': "lightcoral"}
            ]
        }
    ))
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    **Risk Factors Contributing to Score:**
    - **Weather Risk (40%)**: High precipitation expected
    - **Location Risk (30%)**: Flood-prone area
    - **Historical Data (20%)**: 3 similar incidents in past 5 years
    - **Property Age (10%)**: Built in 1985, older construction
    """)

def display_premium_explanation_demo():
    """Display premium calculation explanation demo"""
    
    st.markdown("**Sample Premium Calculation Explanation:**")
    
    # Premium breakdown
    base_premium = 1200
    risk_adjustment = 180
    discount = -150
    final_premium = base_premium + risk_adjustment + discount
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        **Premium Breakdown:**
        - Base Premium: ${base_premium:,}
        - Risk Adjustment: +${risk_adjustment:,}
        - Safe Driver Discount: -${abs(discount):,}
        - **Final Premium: ${final_premium:,}**
        """)
    
    with col2:
        st.markdown("""
        **Calculation Factors:**
        - Vehicle type and age
        - Driving history
        - Location risk factors
        - Coverage selections
        - Market conditions
        """)

def display_esg_demo():
    """Display ESG climate risk demo"""
    
    st.markdown("**ESG Climate Risk Assessment:**")
    
    # ESG scores
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Environmental Score", "7.2/10", delta="Climate risk moderate")
    
    with col2:
        st.metric("Social Score", "8.5/10", delta="Community resilience high")
    
    with col3:
        st.metric("Governance Score", "9.1/10", delta="Compliance excellent")
    
    # Climate scenarios
    st.markdown("**Climate Scenario Analysis:**")
    
    scenarios = {
        'RCP 2.6 (Best Case)': {'probability': 0.25, 'impact': 'Low'},
        'RCP 4.5 (Moderate)': {'probability': 0.50, 'impact': 'Medium'},
        'RCP 8.5 (Worst Case)': {'probability': 0.25, 'impact': 'High'}
    }
    
    for scenario, data in scenarios.items():
        st.markdown(f"- **{scenario}**: {data['probability']:.0%} probability, {data['impact']} impact")

def generate_and_display_workflow(task, context, credit_budget):
    """Generate and display workflow for a given task"""
    
    with st.spinner("🧠 AI Agents analyzing task and optimizing workflow..."):
        time.sleep(2)  # Simulate processing time
    
    # Mock workflow steps
    workflow_steps = [
        {
            'step': 1,
            'agent': 'Enhanced Coordinator',
            'action': 'Analyze task and coordinate workflow',
            'reasoning': 'Task requires multi-agent coordination for optimal processing',
            'expected_output': 'Workflow plan and agent assignments',
            'credit_cost': 5
        },
        {
            'step': 2,
            'agent': 'Claims Specialist',
            'action': 'Process claim details and assess damage',
            'reasoning': 'Specialized knowledge needed for accurate claim evaluation',
            'expected_output': 'Damage assessment and initial approval',
            'credit_cost': 8
        },
        {
            'step': 3,
            'agent': 'Risk Analyst',
            'action': 'Analyze risk factors and weather correlation',
            'reasoning': 'Weather data integration required for comprehensive risk assessment',
            'expected_output': 'Risk score and recommendations',
            'credit_cost': 12
        }
    ]
    
    total_cost = sum(step['credit_cost'] for step in workflow_steps)
    
    st.success("✅ Workflow Generated Successfully!")
    
    # Display workflow steps
    st.subheader("📋 Workflow Steps")
    
    for step in workflow_steps:
        st.markdown(f"""
        <div class="workflow-step">
            <h4>Step {step['step']}: {step['agent']}</h4>
            <p><strong>🎯 Action:</strong> {step['action']}</p>
            <p><strong>🧠 Reasoning:</strong> {step['reasoning']}</p>
            <p><strong>📤 Expected Output:</strong> {step['expected_output']}</p>
            <p><strong>💳 Credit Cost:</strong> {step['credit_cost']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Cost analysis
    st.subheader("💰 Cost Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Cost", f"{total_cost} credits")
    
    with col2:
        st.metric("Budget", f"{credit_budget} credits")
    
    with col3:
        remaining = credit_budget - total_cost
        st.metric("Remaining", f"{remaining} credits", delta=remaining)
    
    # Execute workflow button
    if st.button("▶️ Execute Workflow", type="primary"):
        execute_workflow_simulation(workflow_steps, total_cost)

def execute_workflow_simulation(workflow_steps, total_cost):
    """Simulate workflow execution"""
    
    if total_cost > st.session_state.credit_balance:
        st.error(f"❌ Insufficient credits! Need {total_cost}, have {st.session_state.credit_balance}")
        return
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, step in enumerate(workflow_steps):
        progress = (i + 1) / len(workflow_steps)
        progress_bar.progress(progress)
        status_text.text(f"Executing Step {i+1}/{len(workflow_steps)}: {step['agent']}")
        
        time.sleep(1)  # Simulate processing time
        
        # Deduct credits
        st.session_state.credit_balance -= step['credit_cost']
    
    status_text.text("✅ Workflow completed successfully!")
    st.balloons()
    st.success(f"🎉 Workflow completed! Used {total_cost} credits. Remaining: {st.session_state.credit_balance}")

def display_real_time_visualizations():
    """Display real-time analytics visualizations"""
    
    # Risk heatmap
    st.subheader("🌍 Real-Time Risk Heatmap")
    
    locations = ['New York', 'California', 'Florida', 'Texas', 'Illinois']
    risk_scores = [random.uniform(0.2, 0.8) for _ in locations]
    
    risk_data = pd.DataFrame({
        'Location': locations,
        'Risk Score': risk_scores,
        'Risk Level': ['High' if score > 0.6 else 'Medium' if score > 0.4 else 'Low' for score in risk_scores]
    })
    
    fig = px.bar(
        risk_data, 
        x='Location', 
        y='Risk Score',
        color='Risk Score',
        color_continuous_scale='RdYlGn_r',
        title="Weather Risk by Location"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # API activity log
    st.subheader("📡 Recent API Activity")
    
    api_calls = []
    current_time = datetime.now()
    
    for i in range(5):
        call_time = current_time - timedelta(minutes=i*2)
        api_calls.append({
            'Timestamp': call_time.strftime('%H:%M:%S'),
            'API': ['Weather API', 'Economic API', 'Claims API'][i % 3],
            'Endpoint': ['get_weather_data', 'get_economic_indicators', 'get_claims_data'][i % 3],
            'Status': '✅ Success' if i != 2 else '❌ Failed',
            'Response Time': f"{50 + i*10}ms"
        })
    
    df_api = pd.DataFrame(api_calls)
    st.dataframe(df_api, use_container_width=True)

def display_explainability_config():
    """Display explainability configuration"""
    
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

def display_esg_config():
    """Display ESG configuration"""
    
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

def display_agent_config():
    """Display agent configuration"""
    
    st.markdown("### 🤖 Agent Configuration")
    
    agents = [
        {"name": "Enhanced Coordinator", "active": True, "max_concurrent": 10, "credit_cost": 5},
        {"name": "Claims Specialist", "active": True, "max_concurrent": 5, "credit_cost": 8},
        {"name": "Risk Analyst", "active": True, "max_concurrent": 3, "credit_cost": 12},
        {"name": "Fraud Detector", "active": False, "max_concurrent": 2, "credit_cost": 15},
        {"name": "Policy Advisor", "active": False, "max_concurrent": 4, "credit_cost": 10},
        {"name": "Customer Service", "active": True, "max_concurrent": 8, "credit_cost": 3}
    ]
    
    for agent in agents:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.checkbox(agent["name"], value=agent["active"])
        
        with col2:
            st.number_input(f"Max Concurrent ({agent['name']})", 
                          min_value=1, max_value=20, value=agent["max_concurrent"], key=f"concurrent_{agent['name']}")
        
        with col3:
            st.number_input(f"Credit Cost ({agent['name']})", 
                          min_value=1, max_value=50, value=agent["credit_cost"], key=f"cost_{agent['name']}")
        
        with col4:
            status = "🟢 Active" if agent["active"] else "🔴 Inactive"
            st.markdown(f"**Status:** {status}")

def display_api_config():
    """Display API configuration"""
    
    st.markdown("### 🔌 API Configuration")
    
    api_endpoints = [
        {"name": "Weather API", "url": "https://api.weather.com/v1", "active": True},
        {"name": "Economic API", "url": "https://api.economic.com/v1", "active": True},
        {"name": "Claims API", "url": "https://api.claims.com/v1", "active": True},
        {"name": "Risk Assessment API", "url": "https://api.risk.com/v1", "active": False}
    ]
    
    for api in api_endpoints:
        with st.expander(f"{api['name']} Configuration"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.text_input("API URL", value=api["url"], key=f"url_{api['name']}")
                st.text_input("API Key", type="password", key=f"key_{api['name']}")
            
            with col2:
                st.checkbox("Active", value=api["active"], key=f"active_{api['name']}")
                st.number_input("Timeout (seconds)", min_value=5, max_value=60, value=30, key=f"timeout_{api['name']}")
    
    if st.button("💾 Save API Configuration"):
        st.success("✅ API configuration saved successfully!")

