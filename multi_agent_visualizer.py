"""
Real Multi-Agent Workflow Visualizer for NewGenZ AI Insurance Platform
Provides clear visualization of agent actions and workflow execution
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
import time
from typing import List, Dict, Any
import uuid

class MultiAgentVisualizer:
    def __init__(self):
        self.workflow_steps = []
        self.agent_states = {}
        self.execution_log = []
        
    def create_workflow_diagram(self, task: str, agents: List[Dict]) -> go.Figure:
        """Create interactive workflow diagram"""
        
        # Create nodes for agents
        node_x = []
        node_y = []
        node_text = []
        node_colors = []
        
        # Position agents in a hierarchical layout
        levels = {
            'coordinator': (0.5, 0.9),
            'specialist': (0.2, 0.6),
            'analyst': (0.8, 0.6),
            'processor': (0.5, 0.3)
        }
        
        for i, agent in enumerate(agents):
            agent_type = agent.get('type')
            if agent_type and agent_type in levels:
                x, y = levels[agent_type]
            else:
                # Spread nodes horizontally if type is missing
                x = 0.1 + 0.8 * i / max(1, len(agents)-1)
                y = 0.5
            node_x.append(x)
            node_y.append(y)
            node_text.append(f"{agent['agent']}<br>Status: {agent.get('status', 'N/A')}<br>Load: {agent.get('current_load', 0)}")
            
            # Color based on status
            color_map = {
                'active': '#10b981',
                'idle': '#6b7280',
                'busy': '#f59e0b',
                'error': '#ef4444'
            }
            node_colors.append(color_map.get(agent.get('status', 'idle'), '#6b7280'))
        
        # Create edges (connections between agents)
        edge_x = []
        edge_y = []
        
        # Connect coordinator to specialists
        if len(agents) > 1:
            for i in range(1, len(agents)):
                edge_x.extend([node_x[0], node_x[i], None])
                edge_y.extend([node_y[0], node_y[i], None])
        
        # Create the figure
        fig = go.Figure()
        
        # Add edges
        fig.add_trace(go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=2, color='#d1d5db'),
            hoverinfo='none',
            mode='lines',
            showlegend=False
        ))
        
        # Add nodes
        fig.add_trace(go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=[agent['agent'] for agent in agents],  # <-- FIXED HERE
            textposition="middle center",
            marker=dict(
                size=50,
                color=node_colors,
                line=dict(width=2, color='white')
            ),
            hovertext=node_text,
            showlegend=False
        ))
        
        fig.update_layout(
            title=f"Multi-Agent Workflow: {task}",
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20,l=5,r=5,t=40),
            annotations=[ dict(
                text="Agent Network Topology",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.005, y=-0.002,
                xanchor='left', yanchor='bottom',
                font=dict(color='#6b7280', size=12)
            )],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor='rgba(0,0,0,0)',
            height=400
        )
        
        return fig
    
    def create_execution_timeline(self, workflow_steps: List[Dict]) -> go.Figure:
        """Create real-time execution timeline"""
        
        df_timeline = pd.DataFrame(workflow_steps)
        
        if df_timeline.empty:
            return go.Figure()
        
        fig = go.Figure()
        
        # Create timeline bars
        for i, step in enumerate(workflow_steps):
            start_time = pd.to_datetime(step.get('start_time', datetime.now()))
            duration = step.get('duration', 1)
            
            fig.add_trace(go.Bar(
                x=[duration],
                y=[step['agent']],
                orientation='h',
                name=step['action'],
                text=f"{step['action']}<br>Duration: {duration}s",
                textposition='inside',
                marker_color=self._get_agent_color(step['agent']),
                hovertemplate=f"<b>{step['agent']}</b><br>" +
                             f"Action: {step['action']}<br>" +
                             f"Status: {step.get('status', 'pending')}<br>" +
                             f"Duration: {duration}s<extra></extra>"
            ))
        
        fig.update_layout(
            title="Agent Execution Timeline",
            xaxis_title="Duration (seconds)",
            yaxis_title="Agents",
            barmode='stack',
            height=300,
            showlegend=False
        )
        
        return fig
    
    def _get_agent_color(self, agent_name: str) -> str:
        """Get consistent color for agent"""
        colors = {
            'Enhanced Coordinator': '#3b82f6',
            'Claims Specialist': '#10b981',
            'Risk Analyst': '#f59e0b',
            'Fraud Detector': '#ef4444',
            'Policy Advisor': '#8b5cf6',
            'Customer Service': '#06b6d4'
        }
        return colors.get(agent_name, '#6b7280')
    
    def display_agent_reasoning(self, agent_name: str, reasoning: Dict):
        """Display detailed agent reasoning process"""
        
        with st.expander(f"🧠 {agent_name} - Reasoning Process", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🎯 Current Task:**")
                st.info(reasoning.get('current_task', 'No active task'))
                
                st.markdown("**🔍 Analysis:**")
                for step in reasoning.get('analysis_steps', []):
                    st.markdown(f"• {step}")
            
            with col2:
                st.markdown("**📊 Confidence Score:**")
                confidence = reasoning.get('confidence', 0.85)
                st.progress(confidence)
                st.caption(f"{confidence:.1%} confidence")
                
                st.markdown("**⚡ Next Actions:**")
                for action in reasoning.get('next_actions', []):
                    st.markdown(f"→ {action}")
    
    def create_real_time_metrics(self, agents: List[Dict]) -> None:
        """Display real-time agent metrics"""
        
        col1, col2, col3, col4 = st.columns(4)
        
        active_agents = len([a for a in agents if a['status'] == 'active'])
        total_tasks = sum(a.get('tasks_completed', 0) for a in agents)
        avg_response_time = sum(a.get('avg_response_time', 0) for a in agents) / len(agents) if agents else 0
        success_rate = sum(a.get('success_rate', 0) for a in agents) / len(agents) if agents else 0
        
        with col1:
            st.metric("Active Agents", active_agents, delta=f"{len(agents)} total")
        
        with col2:
            st.metric("Tasks Completed", total_tasks, delta="+5 this hour")
        
        with col3:
            st.metric("Avg Response Time", f"{avg_response_time:.1f}s", delta="-0.3s")
        
        with col4:
            st.metric("Success Rate", f"{success_rate:.1%}", delta="+2.1%")
    
    def execute_workflow_with_visualization(self, workflow_steps: List[Dict]) -> None:
        """Execute workflow with real-time visualization"""
        
        progress_container = st.container()
        timeline_container = st.container()
        reasoning_container = st.container()
        
        with progress_container:
            progress_bar = st.progress(0)
            status_text = st.empty()
        
        executed_steps = []
        
        for i, step in enumerate(workflow_steps):
            # Update progress
            progress = (i + 1) / len(workflow_steps)
            progress_bar.progress(progress)
            status_text.text(f"Executing: {step['agent']} - {step['action']}")
            
            # Add timing information
            step['start_time'] = datetime.now()
            step['status'] = 'executing'
            
            # Simulate execution time
            execution_time = step.get('estimated_duration', 2)
            time.sleep(min(execution_time, 1))  # Cap at 1 second for demo
            
            step['duration'] = execution_time
            step['status'] = 'completed'
            step['end_time'] = datetime.now()
            
            executed_steps.append(step)
            
            # Update timeline
            with timeline_container:
                if executed_steps:
                    fig_timeline = self.create_execution_timeline(executed_steps)
                    st.plotly_chart(fig_timeline, use_container_width=True, key=f"timeline_{i}")
            
            # Show agent reasoning
            with reasoning_container:
                reasoning = {
                    'current_task': step['action'],
                    'analysis_steps': step.get('reasoning_steps', []),
                    'confidence': step.get('confidence', 0.9),
                    'next_actions': step.get('next_actions', [])
                }
                self.display_agent_reasoning(step['agent'], reasoning)
        
        status_text.text("✅ Workflow execution completed!")
        st.success("🎉 All agents have completed their tasks successfully!")
    
    def get_sample_agents(self) -> List[Dict]:
        """Get sample agent configuration"""
        return [
            {
                'name': 'Enhanced Coordinator',
                'type': 'coordinator',
                'status': 'active',
                'current_load': 3,
                'tasks_completed': 15,
                'avg_response_time': 2.1,
                'success_rate': 0.98
            },
            {
                'name': 'Claims Specialist',
                'type': 'specialist',
                'status': 'active',
                'current_load': 2,
                'tasks_completed': 23,
                'avg_response_time': 1.8,
                'success_rate': 0.96
            },
            {
                'name': 'Risk Analyst',
                'type': 'analyst',
                'status': 'busy',
                'current_load': 1,
                'tasks_completed': 8,
                'avg_response_time': 3.2,
                'success_rate': 0.99
            }
        ]
    
    def get_sample_workflow(self, task: str) -> List[Dict]:
        """Generate sample workflow based on task"""
        
        base_workflow = [
            {
                'agent': 'Enhanced Coordinator',
                'action': 'Analyze task and coordinate workflow',
                'reasoning_steps': [
                    'Parse incoming task requirements',
                    'Identify required agent capabilities',
                    'Optimize resource allocation',
                    'Create execution plan'
                ],
                'estimated_duration': 2,
                'confidence': 0.95,
                'next_actions': ['Delegate to specialist agents', 'Monitor execution']
            },
            {
                'agent': 'Claims Specialist',
                'action': 'Process claim details and validate information',
                'reasoning_steps': [
                    'Extract claim information from request',
                    'Validate policy coverage',
                    'Check claim history',
                    'Assess initial eligibility'
                ],
                'estimated_duration': 3,
                'confidence': 0.92,
                'next_actions': ['Forward to risk analysis', 'Update claim status']
            },
            {
                'agent': 'Risk Analyst',
                'action': 'Perform comprehensive risk assessment',
                'reasoning_steps': [
                    'Analyze historical risk patterns',
                    'Evaluate current market conditions',
                    'Calculate risk probability scores',
                    'Generate risk recommendations'
                ],
                'estimated_duration': 4,
                'confidence': 0.88,
                'next_actions': ['Provide risk score', 'Suggest mitigation strategies']
            }
        ]
        
        return base_workflow

