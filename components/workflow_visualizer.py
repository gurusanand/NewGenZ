"""
Workflow Visualization Component for Zurich Edge Platform
Provides clear visualization of multi-agentic workflows and credit optimization
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import networkx as nx
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
import json

class WorkflowVisualizer:
    """Advanced workflow visualization with credit optimization display"""
    
    def __init__(self):
        self.color_scheme = {
            'coordinator': '#1f77b4',
            'claims_specialist': '#ff7f0e',
            'risk_analyst': '#2ca02c',
            'customer_service': '#d62728',
            'policy_advisor': '#9467bd',
            'fraud_detector': '#8c564b',
            'pricing_engine': '#e377c2'
        }
        
        self.priority_colors = {
            'LOW': '#90EE90',
            'MEDIUM': '#FFD700',
            'HIGH': '#FFA500',
            'CRITICAL': '#FF6347'
        }
    
    def create_workflow_diagram(self, workflow_steps: List[Dict], execution_results: List[Dict] = None) -> go.Figure:
        """Create an interactive workflow diagram showing agent interactions"""
        
        # Create network graph
        G = nx.DiGraph()
        
        # Add nodes (agents)
        for i, step in enumerate(workflow_steps):
            agent_name = step.get('agent_type', f'Agent_{i}')
            G.add_node(
                agent_name,
                step_number=i+1,
                credit_cost=step.get('credit_estimate', 0),
                action=step.get('action', 'Unknown'),
                status='completed' if execution_results and i < len(execution_results) else 'pending'
            )
        
        # Add edges (workflow connections)
        for i in range(len(workflow_steps) - 1):
            current_agent = workflow_steps[i].get('agent_type', f'Agent_{i}')
            next_agent = workflow_steps[i+1].get('agent_type', f'Agent_{i+1}')
            G.add_edge(current_agent, next_agent, weight=1)
        
        # Calculate layout
        pos = self._calculate_layout(G, workflow_steps)
        
        # Create plotly figure
        fig = go.Figure()
        
        # Add edges
        self._add_edges_to_plot(fig, G, pos)
        
        # Add nodes
        self._add_nodes_to_plot(fig, G, pos, workflow_steps, execution_results)
        
        # Update layout
        fig.update_layout(
            title="Multi-Agentic Workflow Visualization",
            showlegend=True,
            hovermode='closest',
            margin=dict(b=20,l=5,r=5,t=40),
            annotations=[
                dict(
                    text="Hover over nodes for details",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002,
                    xanchor='left', yanchor='bottom',
                    font=dict(color='gray', size=12)
                )
            ],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=500
        )
        
        return fig
    
    def _calculate_layout(self, G: nx.DiGraph, workflow_steps: List[Dict]) -> Dict[str, Tuple[float, float]]:
        """Calculate optimal layout for workflow visualization"""
        
        # Use hierarchical layout for workflow
        pos = {}
        
        # Simple linear layout for workflow steps
        for i, step in enumerate(workflow_steps):
            agent_name = step.get('agent_type', f'Agent_{i}')
            x = i * 2  # Horizontal spacing
            y = 0      # All on same level for linear workflow
            pos[agent_name] = (x, y)
        
        return pos
    
    def _add_edges_to_plot(self, fig: go.Figure, G: nx.DiGraph, pos: Dict[str, Tuple[float, float]]):
        """Add workflow edges to the plot"""
        
        edge_x = []
        edge_y = []
        
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        
        fig.add_trace(go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=2, color='#888'),
            hoverinfo='none',
            mode='lines',
            name='Workflow Flow'
        ))
        
        # Add arrows
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            
            # Calculate arrow position
            arrow_x = x0 + 0.8 * (x1 - x0)
            arrow_y = y0 + 0.8 * (y1 - y0)
            
            fig.add_annotation(
                x=arrow_x, y=arrow_y,
                ax=x0 + 0.6 * (x1 - x0), ay=y0 + 0.6 * (y1 - y0),
                xref='x', yref='y',
                axref='x', ayref='y',
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor='#888'
            )
    
    def _add_nodes_to_plot(self, fig: go.Figure, G: nx.DiGraph, pos: Dict[str, Tuple[float, float]], 
                          workflow_steps: List[Dict], execution_results: List[Dict] = None):
        """Add agent nodes to the plot"""
        
        for i, step in enumerate(workflow_steps):
            agent_name = step.get('agent_type', f'Agent_{i}')
            x, y = pos[agent_name]
            
            # Determine node properties
            credit_cost = step.get('credit_estimate', 0)
            action = step.get('action', 'Unknown')
            status = 'completed' if execution_results and i < len(execution_results) else 'pending'
            
            # Node color based on agent type and status
            base_color = self.color_scheme.get(agent_name, '#1f77b4')
            if status == 'completed':
                node_color = base_color
                opacity = 1.0
            else:
                node_color = base_color
                opacity = 0.5
            
            # Node size based on credit cost
            node_size = max(20, min(60, credit_cost * 3))
            
            # Create hover text
            hover_text = f"""
            <b>{agent_name.replace('_', ' ').title()}</b><br>
            Action: {action}<br>
            Credit Cost: {credit_cost}<br>
            Status: {status.title()}<br>
            Step: {i+1}
            """
            
            if execution_results and i < len(execution_results):
                result = execution_results[i]
                hover_text += f"<br>Execution Time: {result.get('execution_time', 'N/A')}s"
                hover_text += f"<br>Confidence: {result.get('confidence', 'N/A')}"
            
            fig.add_trace(go.Scatter(
                x=[x], y=[y],
                mode='markers+text',
                marker=dict(
                    size=node_size,
                    color=node_color,
                    opacity=opacity,
                    line=dict(width=2, color='white')
                ),
                text=f"{i+1}",
                textposition="middle center",
                textfont=dict(color='white', size=12, family='Arial Black'),
                hovertext=hover_text,
                hoverinfo='text',
                name=agent_name.replace('_', ' ').title(),
                showlegend=True
            ))
    
    def create_credit_optimization_chart(self, workflow_steps: List[Dict], budget: int, 
                                       optimization_history: List[Dict] = None) -> go.Figure:
        """Create credit optimization visualization"""
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Credit Usage by Agent',
                'Cumulative Credit Consumption',
                'Optimization Efficiency',
                'Budget vs Actual Usage'
            ),
            specs=[[{"type": "pie"}, {"type": "scatter"}],
                   [{"type": "bar"}, {"type": "indicator"}]]
        )
        
        # 1. Credit usage by agent (Pie chart)
        agent_credits = {}
        for step in workflow_steps:
            agent = step.get('agent_type', 'Unknown')
            credits = step.get('credit_estimate', 0)
            agent_credits[agent] = agent_credits.get(agent, 0) + credits
        
        fig.add_trace(
            go.Pie(
                labels=list(agent_credits.keys()),
                values=list(agent_credits.values()),
                name="Credit Distribution"
            ),
            row=1, col=1
        )
        
        # 2. Cumulative credit consumption (Line chart)
        cumulative_credits = []
        total = 0
        step_numbers = []
        
        for i, step in enumerate(workflow_steps):
            total += step.get('credit_estimate', 0)
            cumulative_credits.append(total)
            step_numbers.append(i + 1)
        
        fig.add_trace(
            go.Scatter(
                x=step_numbers,
                y=cumulative_credits,
                mode='lines+markers',
                name='Cumulative Usage',
                line=dict(color='blue', width=3)
            ),
            row=1, col=2
        )
        
        # Add budget line
        fig.add_trace(
            go.Scatter(
                x=[1, len(workflow_steps)],
                y=[budget, budget],
                mode='lines',
                name='Budget Limit',
                line=dict(color='red', dash='dash', width=2)
            ),
            row=1, col=2
        )
        
        # 3. Optimization efficiency (Bar chart)
        if optimization_history:
            scenarios = [h['scenario'] for h in optimization_history]
            efficiencies = [h['efficiency'] for h in optimization_history]
        else:
            scenarios = ['Original', 'Optimized', 'Best Case']
            efficiencies = [65, 85, 95]  # Mock data
        
        fig.add_trace(
            go.Bar(
                x=scenarios,
                y=efficiencies,
                name='Efficiency %',
                marker_color=['red', 'orange', 'green']
            ),
            row=2, col=1
        )
        
        # 4. Budget utilization indicator
        total_cost = sum(step.get('credit_estimate', 0) for step in workflow_steps)
        utilization = (total_cost / budget) * 100 if budget > 0 else 0
        
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=utilization,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Budget Utilization %"},
                delta={'reference': 80},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 80], 'color': "gray"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ),
            row=2, col=2
        )
        
        fig.update_layout(
            height=600,
            title_text="Credit Optimization Dashboard",
            showlegend=True
        )
        
        return fig
    
    def create_agent_performance_heatmap(self, agent_performance_data: Dict[str, Dict]) -> go.Figure:
        """Create agent performance heatmap"""
        
        # Prepare data for heatmap
        agents = list(agent_performance_data.keys())
        metrics = ['Response Time', 'Success Rate', 'Credit Efficiency', 'Customer Satisfaction']
        
        # Create performance matrix
        performance_matrix = []
        for agent in agents:
            agent_data = agent_performance_data.get(agent, {})
            row = [
                agent_data.get('response_time', 0),
                agent_data.get('success_rate', 0),
                agent_data.get('credit_efficiency', 0),
                agent_data.get('customer_satisfaction', 0)
            ]
            performance_matrix.append(row)
        
        fig = go.Figure(data=go.Heatmap(
            z=performance_matrix,
            x=metrics,
            y=[agent.replace('_', ' ').title() for agent in agents],
            colorscale='RdYlGn',
            text=performance_matrix,
            texttemplate="%{text:.1f}",
            textfont={"size": 10},
            hoverongaps=False
        ))
        
        fig.update_layout(
            title="Agent Performance Heatmap",
            xaxis_title="Performance Metrics",
            yaxis_title="Agents",
            height=400
        )
        
        return fig
    
    def create_real_time_workflow_monitor(self, active_workflows: List[Dict]) -> go.Figure:
        """Create real-time workflow monitoring dashboard"""
        
        # Create timeline visualization
        fig = go.Figure()
        
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
        
        for i, workflow in enumerate(active_workflows):
            workflow_id = workflow.get('id', f'WF_{i}')
            start_time = datetime.fromisoformat(workflow.get('start_time', datetime.now().isoformat()))
            current_step = workflow.get('current_step', 0)
            total_steps = workflow.get('total_steps', 1)
            
            # Calculate progress
            progress = (current_step / total_steps) * 100
            
            # Create timeline bar
            fig.add_trace(go.Bar(
                x=[progress],
                y=[workflow_id],
                orientation='h',
                name=f'Workflow {i+1}',
                marker_color=colors[i % len(colors)],
                text=f'{progress:.1f}%',
                textposition='inside'
            ))
        
        fig.update_layout(
            title="Real-Time Workflow Monitoring",
            xaxis_title="Progress (%)",
            yaxis_title="Active Workflows",
            height=300,
            showlegend=False
        )
        
        return fig
    
    def create_credit_usage_timeline(self, usage_history: List[Dict]) -> go.Figure:
        """Create credit usage timeline"""
        
        if not usage_history:
            # Create mock data for demonstration
            usage_history = self._generate_mock_usage_history()
        
        timestamps = [datetime.fromisoformat(h['timestamp']) for h in usage_history]
        credits_used = [h['credits_used'] for h in usage_history]
        cumulative_usage = []
        total = 0
        
        for credits in credits_used:
            total += credits
            cumulative_usage.append(total)
        
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Credit Usage per Transaction', 'Cumulative Credit Usage'),
            vertical_spacing=0.1
        )
        
        # Individual usage
        fig.add_trace(
            go.Bar(
                x=timestamps,
                y=credits_used,
                name='Credits per Transaction',
                marker_color='lightblue'
            ),
            row=1, col=1
        )
        
        # Cumulative usage
        fig.add_trace(
            go.Scatter(
                x=timestamps,
                y=cumulative_usage,
                mode='lines+markers',
                name='Cumulative Usage',
                line=dict(color='red', width=2)
            ),
            row=2, col=1
        )
        
        fig.update_layout(
            height=500,
            title_text="Credit Usage Analysis",
            showlegend=True
        )
        
        return fig
    
    def _generate_mock_usage_history(self) -> List[Dict]:
        """Generate mock usage history for demonstration"""
        history = []
        base_time = datetime.now() - timedelta(days=7)
        
        for i in range(20):
            timestamp = base_time + timedelta(hours=i*8)
            credits = random.randint(5, 25)
            
            history.append({
                'timestamp': timestamp.isoformat(),
                'credits_used': credits,
                'workflow_id': f'WF_{i:03d}',
                'task_type': random.choice(['claim', 'risk_analysis', 'policy_query'])
            })
        
        return history
    
    def create_optimization_comparison(self, original_workflow: List[Dict], 
                                     optimized_workflow: List[Dict]) -> go.Figure:
        """Create comparison between original and optimized workflows"""
        
        # Calculate metrics for both workflows
        original_cost = sum(step.get('credit_estimate', 0) for step in original_workflow)
        optimized_cost = sum(step.get('credit_estimate', 0) for step in optimized_workflow)
        
        original_steps = len(original_workflow)
        optimized_steps = len(optimized_workflow)
        
        savings = original_cost - optimized_cost
        efficiency_gain = (savings / original_cost) * 100 if original_cost > 0 else 0
        
        # Create comparison chart
        fig = make_subplots(
            rows=1, cols=3,
            subplot_titles=('Cost Comparison', 'Steps Comparison', 'Efficiency Metrics'),
            specs=[[{"type": "bar"}, {"type": "bar"}, {"type": "indicator"}]]
        )
        
        # Cost comparison
        fig.add_trace(
            go.Bar(
                x=['Original', 'Optimized'],
                y=[original_cost, optimized_cost],
                name='Total Cost',
                marker_color=['red', 'green']
            ),
            row=1, col=1
        )
        
        # Steps comparison
        fig.add_trace(
            go.Bar(
                x=['Original', 'Optimized'],
                y=[original_steps, optimized_steps],
                name='Number of Steps',
                marker_color=['orange', 'blue']
            ),
            row=1, col=2
        )
        
        # Efficiency indicator
        fig.add_trace(
            go.Indicator(
                mode="number+delta",
                value=efficiency_gain,
                title={"text": "Efficiency Gain %"},
                delta={'reference': 0, 'valueformat': '.1f'},
                number={'suffix': '%'}
            ),
            row=1, col=3
        )
        
        fig.update_layout(
            height=400,
            title_text="Workflow Optimization Results",
            showlegend=False
        )
        
        return fig
    
    def render_workflow_summary_cards(self, workflow_data: Dict[str, Any]):
        """Render summary cards for workflow metrics"""
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="agent-card">
                <h4>💳 Total Credits</h4>
                <h2 style="color: #1f77b4;">{}</h2>
                <p>Estimated cost</p>
            </div>
            """.format(workflow_data.get('total_credits', 0)), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="agent-card">
                <h4>🔧 Total Steps</h4>
                <h2 style="color: #ff7f0e;">{}</h2>
                <p>Workflow complexity</p>
            </div>
            """.format(workflow_data.get('total_steps', 0)), unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="agent-card">
                <h4>⚡ Efficiency</h4>
                <h2 style="color: #2ca02c;">{}%</h2>
                <p>Optimization score</p>
            </div>
            """.format(workflow_data.get('efficiency', 0)), unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="agent-card">
                <h4>⏱️ Est. Time</h4>
                <h2 style="color: #d62728;">{}</h2>
                <p>Completion time</p>
            </div>
            """.format(workflow_data.get('estimated_time', 'N/A')), unsafe_allow_html=True)
    
    def create_agent_hierarchy_visualization(self, hierarchy_data: Dict[int, List[str]]) -> go.Figure:
        """Create hierarchical visualization of agent structure"""
        
        fig = go.Figure()
        
        # Define positions for each level
        level_positions = {1: 0, 2: -1, 3: -2, 4: -3}
        
        # Add nodes for each level
        for level, agents in hierarchy_data.items():
            y_pos = level_positions.get(level, -level)
            
            for i, agent in enumerate(agents):
                x_pos = i - (len(agents) - 1) / 2  # Center agents in each level
                
                # Node size based on level (higher level = larger node)
                node_size = 40 - (level - 1) * 8
                
                # Color based on agent type
                color = self.color_scheme.get(agent, '#1f77b4')
                
                fig.add_trace(go.Scatter(
                    x=[x_pos],
                    y=[y_pos],
                    mode='markers+text',
                    marker=dict(size=node_size, color=color, opacity=0.8),
                    text=agent.replace('_', '<br>').title(),
                    textposition="bottom center",
                    name=f"Level {level}",
                    showlegend=False,
                    hovertext=f"Level {level}: {agent.replace('_', ' ').title()}",
                    hoverinfo='text'
                ))
        
        # Add connections between levels
        for level in range(1, max(hierarchy_data.keys())):
            if level in hierarchy_data and level + 1 in hierarchy_data:
                upper_agents = hierarchy_data[level]
                lower_agents = hierarchy_data[level + 1]
                
                upper_y = level_positions[level]
                lower_y = level_positions[level + 1]
                
                # Connect each upper agent to all lower agents
                for i, upper_agent in enumerate(upper_agents):
                    upper_x = i - (len(upper_agents) - 1) / 2
                    
                    for j, lower_agent in enumerate(lower_agents):
                        lower_x = j - (len(lower_agents) - 1) / 2
                        
                        fig.add_trace(go.Scatter(
                            x=[upper_x, lower_x],
                            y=[upper_y, lower_y],
                            mode='lines',
                            line=dict(color='gray', width=1, dash='dot'),
                            showlegend=False,
                            hoverinfo='none'
                        ))
        
        fig.update_layout(
            title="Agent Hierarchy Structure",
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=500,
            showlegend=False
        )
        
        return fig

# Import required modules for mock data
import random

