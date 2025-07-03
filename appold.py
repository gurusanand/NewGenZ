"""
Zurich Edge AI Insurance Platform
Multi-Agentic AI System with ReAct and Hierarchical Frameworks
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import time
from typing import Dict, List, Any
import uuid

# Import our agent configuration
import sys
sys.path.append('/home/ubuntu/zurich_edge_app')
from config.agent_config import (
    AgentHierarchy, ReActFramework, CreditOptimizer, 
    AgentType, TaskComplexity, WorkflowStep
)
from components.openai_client import OpenAIClient

# Page configuration
st.set_page_config(
    page_title="Zurich Edge AI Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .agent-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .workflow-step {
        background: #fff;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0 8px 8px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .credit-indicator {
        background: #fef3c7;
        border: 1px solid #f59e0b;
        border-radius: 6px;
        padding: 0.5rem;
        margin: 0.25rem 0;
    }
    
    .success-indicator {
        background: #d1fae5;
        border: 1px solid #10b981;
        border-radius: 6px;
        padding: 0.5rem;
        margin: 0.25rem 0;
    }
    
    .warning-indicator {
        background: #fef2f2;
        border: 1px solid #ef4444;
        border-radius: 6px;
        padding: 0.5rem;
        margin: 0.25rem 0;
    }
</style>
""", unsafe_allow_html=True)

class ZurichEdgeApp:
    def __init__(self):
        self.agent_hierarchy = AgentHierarchy()
        self.react_framework = ReActFramework()
        self.credit_optimizer = CreditOptimizer()
        
        # Initialize session state
        if 'credit_balance' not in st.session_state:
            st.session_state.credit_balance = 100
        if 'workflow_history' not in st.session_state:
            st.session_state.workflow_history = []
        if 'active_agents' not in st.session_state:
            st.session_state.active_agents = {}
    
    def render_header(self):
        """Render the main application header"""
        st.markdown("""
        <div class="main-header">
            <h1>🛡️ Zurich Edge AI Insurance Platform</h1>
            <p>Multi-Agentic AI System with ReAct & Hierarchical Frameworks</p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_sidebar(self):
        """Render the sidebar with system controls"""
        st.sidebar.header("🎛️ System Control Panel")
        
        # Credit balance display
        st.sidebar.markdown(f"""
        <div class="credit-indicator">
            <strong>💳 Credit Balance: {st.session_state.credit_balance}</strong>
        </div>
        """, unsafe_allow_html=True)
        
        # Credit management
        st.sidebar.subheader("Credit Management")
        if st.sidebar.button("🔄 Reset Credits (100)"):
            st.session_state.credit_balance = 100
            st.sidebar.success("Credits reset!")
        
        add_credits = st.sidebar.number_input("Add Credits", min_value=0, max_value=500, value=0)
        if st.sidebar.button("➕ Add Credits") and add_credits > 0:
            st.session_state.credit_balance += add_credits
            st.sidebar.success(f"Added {add_credits} credits!")
        
        # System status
        st.sidebar.subheader("🔍 System Status")
        active_count = len(st.session_state.active_agents)
        st.sidebar.metric("Active Agents", active_count)
        st.sidebar.metric("Completed Workflows", len(st.session_state.workflow_history))
        
        # Agent hierarchy visualization
        st.sidebar.subheader("🏗️ Agent Hierarchy")
        for level, agents in self.agent_hierarchy.hierarchy_levels.items():
            st.sidebar.write(f"**Level {level}:**")
            for agent in agents:
                agent_info = self.agent_hierarchy.agents[agent]
                st.sidebar.write(f"  • {agent_info.name} (Cost: {agent_info.credit_cost})")
    
    def render_workflow_designer(self):
        """Render the workflow designer interface"""
        st.header("🔧 Intelligent Workflow Designer")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Task Input")
            
            # Predefined task templates
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
                self.generate_and_display_workflow(user_task, context, credit_budget)
            else:
                st.error("Please enter a task description!")
    
    def generate_and_display_workflow(self, task: str, context: Dict, credit_budget: int):
        """Generate and display the optimal workflow"""
        
        # Generate workflow using ReAct framework
        with st.spinner("🧠 AI Agents analyzing task and optimizing workflow..."):
            time.sleep(1)  # Simulate processing time
            
            # Create reasoning chain
            workflow_steps = self.react_framework.create_reasoning_chain(task, context)
            
            # Optimize for credit budget
            optimized_steps = self.credit_optimizer.optimize_workflow(workflow_steps, credit_budget)
            
            # Get cost breakdown
            cost_breakdown = self.credit_optimizer.get_cost_breakdown(optimized_steps)
        
        # Display workflow
        st.success("✅ Workflow Generated Successfully!")
        
        # Create tabs for different views
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Workflow Steps", "💰 Cost Analysis", "🔄 Execution", "📊 Visualization"])
        
        with tab1:
            self.display_workflow_steps(optimized_steps, cost_breakdown)
        
        with tab2:
            self.display_cost_analysis(cost_breakdown, credit_budget)
        
        with tab3:
            self.display_execution_interface(optimized_steps, task, context)
        
        with tab4:
            self.display_workflow_visualization(optimized_steps)
    
    def display_workflow_steps(self, steps: List[WorkflowStep], cost_breakdown: Dict):
        """Display the workflow steps with reasoning"""
        st.subheader("🔍 ReAct Framework: Reasoning & Acting Chain")
        
        for i, step in enumerate(steps, 1):
            agent_info = self.agent_hierarchy.agents[step.agent_type]
            
            st.markdown(f"""
            <div class="workflow-step">
                <h4>Step {i}: {agent_info.name}</h4>
                <p><strong>🎯 Action:</strong> {step.action}</p>
                <p><strong>🧠 Reasoning:</strong> {step.reasoning}</p>
                <p><strong>📤 Expected Output:</strong> {step.expected_output}</p>
                <p><strong>💳 Credit Cost:</strong> {step.credit_estimate}</p>
                <p><strong>🔧 Specializations:</strong> {', '.join(agent_info.specializations)}</p>
            </div>
            """, unsafe_allow_html=True)
    
    def display_cost_analysis(self, cost_breakdown: Dict, budget: int):
        """Display detailed cost analysis"""
        st.subheader("💰 Credit Usage Analysis")
        
        total_cost = cost_breakdown['total_credits']
        
        # Cost summary
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Cost", f"{total_cost} credits")
        with col2:
            st.metric("Budget", f"{budget} credits")
        with col3:
            remaining = budget - total_cost
            st.metric("Remaining", f"{remaining} credits", delta=remaining)
        with col4:
            efficiency = (budget - total_cost) / budget * 100 if budget > 0 else 0
            st.metric("Efficiency", f"{efficiency:.1f}%")
        
        # Cost breakdown by agent
        st.subheader("Agent Cost Breakdown")
        agent_costs = cost_breakdown['agent_costs']
        
        # Create pie chart
        fig_pie = px.pie(
            values=list(agent_costs.values()),
            names=list(agent_costs.keys()),
            title="Credit Distribution by Agent"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Detailed breakdown table
        df_breakdown = pd.DataFrame(cost_breakdown['step_details'])
        st.dataframe(df_breakdown, use_container_width=True)
    
    def display_execution_interface(self, steps: List[WorkflowStep], task: str, context: Dict):
        """Display the workflow execution interface"""
        st.subheader("🚀 Workflow Execution")
        
        if st.button("▶️ Execute Workflow", type="primary"):
            self.execute_workflow(steps, task, context)
    
    def execute_workflow(self, steps: List[WorkflowStep], task: str, context: Dict):
        """Execute the workflow with real-time updates"""
        
        # Check if user has enough credits
        total_cost = sum(step.credit_estimate for step in steps)
        if total_cost > st.session_state.credit_balance:
            st.error(f"❌ Insufficient credits! Need {total_cost}, have {st.session_state.credit_balance}")
            return
        
        # Create execution container
        execution_container = st.container()
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        results = []
        
        for i, step in enumerate(steps):
            # Update progress
            progress = (i + 1) / len(steps)
            progress_bar.progress(progress)
            status_text.text(f"Executing Step {i+1}/{len(steps)}: {step.agent_type.value}")
            
            # Simulate agent execution
            with execution_container:
                with st.expander(f"Step {i+1}: {step.agent_type.value}", expanded=True):
                    st.write(f"**Action:** {step.action}")
                    
                    # Simulate processing time
                    time.sleep(1)
                    
                    # Generate mock result based on agent type
                    result = self.simulate_agent_execution(step, task, context)
                    results.append(result)
                    
                    st.success(f"✅ Completed: {result['summary']}")
                    st.json(result['details'])
            
            # Deduct credits
            st.session_state.credit_balance -= step.credit_estimate
        
        # Final results
        status_text.text("✅ Workflow completed successfully!")
        
        # Store in history
        workflow_record = {
            'id': str(uuid.uuid4()),
            'timestamp': datetime.now().isoformat(),
            'task': task,
            'context': context,
            'steps': len(steps),
            'total_cost': total_cost,
            'results': results
        }
        st.session_state.workflow_history.append(workflow_record)
        
        st.balloons()
        st.success(f"🎉 Workflow completed! Used {total_cost} credits. Remaining: {st.session_state.credit_balance}")
    
    def simulate_agent_execution(self, step: WorkflowStep, task: str, context: Dict) -> Dict:
        """Simulate agent execution with realistic results"""
        
        agent_type = step.agent_type
        
        # Mock results based on agent type
        if agent_type == AgentType.COORDINATOR:
            return {
                'summary': 'Task analyzed and workflow coordinated',
                'details': {
                    'task_complexity': 'Medium',
                    'estimated_duration': '5 minutes',
                    'agents_assigned': 3,
                    'priority_level': 'Standard'
                }
            }
        
        elif agent_type == AgentType.CLAIMS_SPECIALIST:
            return {
                'summary': 'Claim processed and damage assessed',
                'details': {
                    'claim_id': 'CLM_' + str(uuid.uuid4())[:8],
                    'damage_assessment': 'Moderate damage detected',
                    'estimated_payout': '$2,500',
                    'approval_status': 'Pre-approved',
                    'next_steps': 'Document verification required'
                }
            }
        
        elif agent_type == AgentType.RISK_ANALYST:
            return {
                'summary': 'Risk analysis completed with recommendations',
                'details': {
                    'risk_score': 7.2,
                    'risk_factors': ['Weather patterns', 'Location history', 'Property age'],
                    'recommendations': ['Install flood sensors', 'Update coverage limits'],
                    'confidence_level': '94%'
                }
            }
        
        elif agent_type == AgentType.CUSTOMER_SERVICE:
            return {
                'summary': 'Customer query resolved successfully',
                'details': {
                    'response_time': '2.3 seconds',
                    'satisfaction_score': 4.8,
                    'resolution_type': 'Automated',
                    'follow_up_required': False
                }
            }
        
        elif agent_type == AgentType.POLICY_ADVISOR:
            return {
                'summary': 'Policy recommendations generated',
                'details': {
                    'recommended_coverage': 'Comprehensive Plus',
                    'potential_savings': '$240/year',
                    'coverage_gaps': 'None identified',
                    'customization_options': ['Deductible adjustment', 'Add-on coverage']
                }
            }
        
        elif agent_type == AgentType.FRAUD_DETECTOR:
            return {
                'summary': 'Fraud analysis completed - No suspicious activity',
                'details': {
                    'fraud_score': 0.15,
                    'risk_indicators': 'None detected',
                    'verification_status': 'Verified',
                    'confidence_level': '99.2%'
                }
            }
        
        elif agent_type == AgentType.PRICING_ENGINE:
            return {
                'summary': 'Dynamic pricing calculated',
                'details': {
                    'base_premium': '$1,200',
                    'discounts_applied': ['Safe driver: -15%', 'Multi-policy: -10%'],
                    'final_premium': '$918',
                    'next_review_date': '2024-06-01'
                }
            }
        
        else:
            return {
                'summary': 'Task completed successfully',
                'details': {'status': 'completed', 'timestamp': datetime.now().isoformat()}
            }
    
    def display_workflow_visualization(self, steps: List[WorkflowStep]):
        """Display workflow visualization"""
        st.subheader("📊 Workflow Visualization")
        
        # Create workflow diagram
        fig = go.Figure()
        
        # Add nodes for each agent
        x_positions = list(range(len(steps)))
        y_positions = [0] * len(steps)
        
        agent_names = [step.agent_type.value.replace('_', ' ').title() for step in steps]
        credit_costs = [step.credit_estimate for step in steps]
        
        # Add workflow steps as connected nodes
        fig.add_trace(go.Scatter(
            x=x_positions,
            y=y_positions,
            mode='markers+lines+text',
            marker=dict(size=20, color=credit_costs, colorscale='Viridis', showscale=True),
            text=agent_names,
            textposition="top center",
            line=dict(width=3, color='blue'),
            name='Workflow'
        ))
        
        fig.update_layout(
            title="Agent Workflow Sequence",
            xaxis_title="Execution Order",
            yaxis_title="",
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Credit usage over time
        cumulative_credits = []
        total = 0
        for step in steps:
            total += step.credit_estimate
            cumulative_credits.append(total)
        
        fig2 = px.line(
            x=list(range(1, len(steps) + 1)),
            y=cumulative_credits,
            title="Cumulative Credit Usage",
            labels={'x': 'Step Number', 'y': 'Credits Used'}
        )
        fig2.add_hline(y=st.session_state.credit_balance, line_dash="dash", 
                      annotation_text="Current Balance")
        
        st.plotly_chart(fig2, use_container_width=True)
    
    def render_agent_dashboard(self):
        """Render the agent management dashboard"""
        st.header("🤖 Agent Management Dashboard")
        
        # Agent status overview
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("🏗️ Hierarchy Overview")
            for level, agents in self.agent_hierarchy.hierarchy_levels.items():
                st.write(f"**Level {level}:**")
                for agent in agents:
                    agent_info = self.agent_hierarchy.agents[agent]
                    status = "🟢 Active" if agent in st.session_state.active_agents else "⚪ Idle"
                    st.write(f"  {status} {agent_info.name}")
        
        with col2:
            st.subheader("📊 Agent Performance")
            # Create mock performance data
            performance_data = {
                'Agent': [info.name for info in self.agent_hierarchy.agents.values()],
                'Tasks Completed': [15, 23, 8, 31, 12, 19, 27],
                'Avg Response Time (s)': [2.1, 1.8, 3.2, 1.5, 2.8, 2.3, 1.9],
                'Success Rate (%)': [98, 96, 99, 97, 95, 98, 99]
            }
            df_performance = pd.DataFrame(performance_data)
            st.dataframe(df_performance, use_container_width=True)
        
        with col3:
            st.subheader("💳 Credit Efficiency")
            # Calculate efficiency metrics
            efficiency_data = []
            for agent_type, agent_info in self.agent_hierarchy.agents.items():
                efficiency_data.append({
                    'Agent': agent_info.name,
                    'Cost per Task': agent_info.credit_cost,
                    'Max Concurrent': agent_info.max_concurrent_tasks,
                    'Efficiency Score': round(agent_info.max_concurrent_tasks / agent_info.credit_cost, 2)
                })
            
            df_efficiency = pd.DataFrame(efficiency_data)
            st.dataframe(df_efficiency, use_container_width=True)
    
    def render_workflow_history(self):
        """Render workflow history and analytics"""
        st.header("📈 Workflow History & Analytics")
        
        if not st.session_state.workflow_history:
            st.info("No workflows executed yet. Try the Workflow Designer!")
            return
        
        # Summary metrics
        total_workflows = len(st.session_state.workflow_history)
        total_credits_used = sum(w['total_cost'] for w in st.session_state.workflow_history)
        avg_steps = sum(w['steps'] for w in st.session_state.workflow_history) / total_workflows
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Workflows", total_workflows)
        with col2:
            st.metric("Credits Used", total_credits_used)
        with col3:
            st.metric("Avg Steps", f"{avg_steps:.1f}")
        with col4:
            st.metric("Efficiency", f"{(100-total_credits_used):.1f}%")
        
        # Workflow history table
        st.subheader("Recent Workflows")
        history_data = []
        for workflow in st.session_state.workflow_history[-10:]:  # Show last 10
            history_data.append({
                'Timestamp': workflow['timestamp'][:19],
                'Task': workflow['task'][:50] + '...' if len(workflow['task']) > 50 else workflow['task'],
                'Steps': workflow['steps'],
                'Cost': workflow['total_cost'],
                'Status': '✅ Completed'
            })
        
        if history_data:
            df_history = pd.DataFrame(history_data)
            st.dataframe(df_history, use_container_width=True)
        
        # Analytics charts
        if len(st.session_state.workflow_history) > 1:
            st.subheader("📊 Usage Analytics")
            
            # Credits usage over time
            timestamps = [w['timestamp'] for w in st.session_state.workflow_history]
            costs = [w['total_cost'] for w in st.session_state.workflow_history]
            
            fig = px.line(x=timestamps, y=costs, title="Credit Usage Over Time")
            st.plotly_chart(fig, use_container_width=True)
    
    def run(self):
        """Main application runner"""
        self.render_header()
        self.render_sidebar()
        
        # Main navigation
        tab1, tab2, tab3, tab4 = st.tabs([
            "🔧 Workflow Designer", 
            "🤖 Agent Dashboard", 
            "📈 Analytics", 
            "📚 Documentation"
        ])
        
        with tab1:
            self.render_workflow_designer()
        
        with tab2:
            self.render_agent_dashboard()
        
        with tab3:
            self.render_workflow_history()
        
        with tab4:
            self.render_documentation()
    
    def render_documentation(self):
        """Render system documentation"""
        st.header("📚 System Documentation")
        
        st.markdown("""
        ## 🎯 Multi-Agentic AI System Overview
        
        The Zurich Edge platform implements a sophisticated multi-agentic AI system using:
        
        ### 🧠 ReAct Framework (Reasoning and Acting)
        - **Reasoning**: Each agent analyzes the task and determines the best approach
        - **Acting**: Agents execute specific actions based on their reasoning
        - **Optimization**: The system optimizes for minimal credit usage while maintaining quality
        
        ### 🏗️ Hierarchical Agent Structure
        
        **Level 1 - Coordinator**
        - Master Coordinator: Orchestrates workflows and manages resources
        
        **Level 2 - Critical Operations**
        - Claims Specialist: Processes claims and damage assessment
        - Risk Analyst: Evaluates risks and predicts outcomes
        - Fraud Detector: Identifies suspicious activities
        
        **Level 3 - Advisory Services**
        - Policy Advisor: Recommends optimal coverage
        - Pricing Engine: Calculates dynamic pricing
        
        **Level 4 - Support Services**
        - Customer Service: Handles queries and support
        
        ### 💳 Credit Optimization Strategies
        
        1. **Task Complexity Assessment**: Automatically determines required resources
        2. **Agent Selection**: Routes tasks to the most efficient agents
        3. **Budget Management**: Stays within specified credit limits
        4. **Fallback Mechanisms**: Provides alternatives when primary agents are unavailable
        
        ### 🔄 Workflow Optimization
        
        - **Parallel Processing**: Multiple agents can work simultaneously
        - **Smart Routing**: Tasks are routed to the most appropriate agents
        - **Resource Pooling**: Agents share resources for efficiency
        - **Real-time Monitoring**: Continuous monitoring of agent performance
        
        ### 📊 Key Features
        
        - **Real-time Workflow Generation**: Dynamic workflow creation based on task analysis
        - **Cost Transparency**: Clear breakdown of credit usage
        - **Performance Analytics**: Detailed metrics and insights
        - **Scalable Architecture**: Easily add new agents and capabilities
        """)

# Run the application
if __name__ == "__main__":
    app = ZurichEdgeApp()
    app.run()

