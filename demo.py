"""
Demo Script for Zurich Edge AI Insurance Platform
Showcases multi-agentic system with ReAct and Hierarchical frameworks
"""

import sys
import time
import json
from datetime import datetime
from typing import Dict, List, Any

# Add the app directory to Python path
sys.path.append('/home/ubuntu/zurich_edge_app')

from config.agent_config import (
    AgentHierarchy, ReActFramework, CreditOptimizer, 
    AgentType, TaskComplexity, WorkflowStep
)
from components.agent_implementations import AgentFactory, CoordinatorAgent, ClaimsSpecialistAgent, RiskAnalystAgent

class ZurichEdgeDemo:
    """Demo class to showcase the multi-agentic AI system"""
    
    def __init__(self):
        self.agent_hierarchy = AgentHierarchy()
        self.react_framework = ReActFramework()
        self.credit_optimizer = CreditOptimizer()
        self.agent_factory = AgentFactory()
        
        print("🛡️ Zurich Edge AI Insurance Platform Demo")
        print("=" * 50)
        print("Multi-Agentic AI with ReAct & Hierarchical Frameworks")
        print("=" * 50)
    
    def demonstrate_workflow_optimization(self):
        """Demonstrate workflow optimization and credit management"""
        
        print("\n🔧 WORKFLOW OPTIMIZATION DEMO")
        print("-" * 30)
        
        # Sample tasks with different complexities
        demo_tasks = [
            {
                "task": "What is my policy status?",
                "context": {"customer_id": "CUST_001", "urgency": "Low"},
                "budget": 10
            },
            {
                "task": "I need to file a claim for car damage from yesterday's accident",
                "context": {"customer_id": "CUST_002", "urgency": "Medium", "policy_number": "POL_12345"},
                "budget": 20
            },
            {
                "task": "Emergency claim: house fire, need immediate assistance",
                "context": {"customer_id": "CUST_003", "urgency": "Critical", "policy_number": "POL_67890"},
                "budget": 50
            },
            {
                "task": "Investigate suspicious claim patterns for policy #12345",
                "context": {"customer_id": "CUST_004", "urgency": "High", "investigation_type": "fraud"},
                "budget": 35
            }
        ]
        
        for i, demo in enumerate(demo_tasks, 1):
            print(f"\n📋 Demo {i}: {demo['task'][:50]}...")
            print(f"💳 Budget: {demo['budget']} credits")
            
            # Generate workflow using ReAct framework
            workflow_steps = self.react_framework.create_reasoning_chain(demo['task'], demo['context'])
            
            # Optimize for budget
            optimized_steps = self.credit_optimizer.optimize_workflow(workflow_steps, demo['budget'])
            
            # Get cost breakdown
            cost_breakdown = self.credit_optimizer.get_cost_breakdown(optimized_steps)
            
            print(f"🔍 Generated {len(workflow_steps)} steps, optimized to {len(optimized_steps)} steps")
            print(f"💰 Total cost: {cost_breakdown['total_credits']} credits")
            print(f"⚡ Efficiency: {((demo['budget'] - cost_breakdown['total_credits']) / demo['budget'] * 100):.1f}%")
            
            # Show workflow steps
            print("📝 Workflow Steps:")
            for j, step in enumerate(optimized_steps, 1):
                agent_name = step.agent_type.value.replace('_', ' ').title()
                print(f"   {j}. {agent_name} ({step.credit_estimate} credits)")
                print(f"      Action: {step.action}")
                print(f"      Reasoning: {step.reasoning[:80]}...")
            
            time.sleep(1)  # Pause for readability
    
    def demonstrate_react_framework(self):
        """Demonstrate ReAct (Reasoning and Acting) framework"""
        
        print("\n🧠 REACT FRAMEWORK DEMO")
        print("-" * 25)
        
        # Create sample agents
        coordinator = CoordinatorAgent()
        claims_agent = ClaimsSpecialistAgent()
        risk_agent = RiskAnalystAgent()
        
        agents = [coordinator, claims_agent, risk_agent]
        
        # Sample task for demonstration
        task = "Analyze flood risk for property in Miami and process related insurance claim"
        context = {
            "customer_id": "CUST_DEMO",
            "property_location": "Miami, FL",
            "policy_number": "POL_DEMO_001",
            "urgency": "High"
        }
        
        print(f"📋 Task: {task}")
        print(f"🔧 Context: {json.dumps(context, indent=2)}")
        
        for agent in agents:
            print(f"\n🤖 Agent: {agent.name}")
            print("-" * 20)
            
            # Execute ReAct pattern
            response = agent.execute(task, context)
            
            print(f"🧠 Reasoning: {response.reasoning[:100]}...")
            print(f"⚡ Action: {response.action_taken}")
            print(f"💳 Credits Used: {response.credits_used}")
            print(f"🎯 Confidence: {response.confidence:.2f}")
            print(f"⏱️ Execution Time: {response.execution_time:.2f}s")
            
            # Show key results
            if response.result:
                print("📊 Key Results:")
                for key, value in list(response.result.items())[:3]:  # Show first 3 items
                    if isinstance(value, dict):
                        print(f"   {key}: {type(value).__name__} with {len(value)} items")
                    else:
                        print(f"   {key}: {str(value)[:50]}...")
            
            time.sleep(1)  # Pause for readability
    
    def demonstrate_hierarchical_coordination(self):
        """Demonstrate hierarchical agent coordination"""
        
        print("\n🏗️ HIERARCHICAL COORDINATION DEMO")
        print("-" * 35)
        
        # Show hierarchy structure
        print("📊 Agent Hierarchy:")
        for level, agents in self.agent_hierarchy.hierarchy_levels.items():
            print(f"   Level {level}:")
            for agent_type in agents:
                agent_info = self.agent_hierarchy.agents[agent_type]
                print(f"      • {agent_info.name} (Cost: {agent_info.credit_cost}, Max Tasks: {agent_info.max_concurrent_tasks})")
        
        # Demonstrate coordination scenario
        print("\n🎯 Coordination Scenario:")
        print("Complex claim requiring multiple agents...")
        
        # Simulate coordinator decision-making
        coordinator = CoordinatorAgent()
        complex_task = "Process emergency auto claim with potential fraud indicators and high damage value"
        context = {
            "claim_value": 45000,
            "urgency": "Critical",
            "fraud_indicators": ["unusual_timing", "multiple_claims"],
            "damage_type": "total_loss"
        }
        
        print(f"📋 Task: {complex_task}")
        
        # Coordinator analyzes and creates workflow
        response = coordinator.execute(complex_task, context)
        execution_plan = response.result.get('execution_plan', {})
        
        print("\n📋 Coordinator's Execution Plan:")
        print(f"   Workflow ID: {execution_plan.get('workflow_id', 'N/A')}")
        print(f"   Agent Sequence: {', '.join(execution_plan.get('agent_sequence', []))}")
        print(f"   Estimated Duration: {execution_plan.get('estimated_duration', 'N/A')} seconds")
        print(f"   Estimated Credits: {response.result.get('estimated_credits', 'N/A')}")
        
        # Show parallel execution groups
        parallel_groups = execution_plan.get('parallel_execution_groups', [])
        if parallel_groups:
            print("\n⚡ Parallel Execution Groups:")
            for i, group in enumerate(parallel_groups, 1):
                print(f"   Group {i}: {', '.join(group)}")
        
        # Show fallback plans
        fallback_plans = execution_plan.get('fallback_plans', {})
        if fallback_plans:
            print("\n🔄 Fallback Plans:")
            for agent, fallback in fallback_plans.items():
                print(f"   {agent} → {fallback}")
    
    def demonstrate_credit_optimization(self):
        """Demonstrate credit optimization strategies"""
        
        print("\n💳 CREDIT OPTIMIZATION DEMO")
        print("-" * 28)
        
        # Create scenarios with different budgets
        scenarios = [
            {"budget": 50, "name": "High Budget"},
            {"budget": 25, "name": "Medium Budget"},
            {"budget": 10, "name": "Low Budget"}
        ]
        
        task = "Comprehensive risk analysis with claim processing and fraud detection"
        context = {"complexity": "high", "urgency": "medium"}
        
        print(f"📋 Task: {task}")
        
        # Generate base workflow
        base_workflow = self.react_framework.create_reasoning_chain(task, context)
        base_cost = sum(step.credit_estimate for step in base_workflow)
        
        print(f"🔧 Base Workflow: {len(base_workflow)} steps, {base_cost} credits")
        
        for scenario in scenarios:
            budget = scenario['budget']
            name = scenario['name']
            
            print(f"\n💰 {name} Scenario (Budget: {budget} credits):")
            
            # Optimize for budget
            optimized_workflow = self.credit_optimizer.optimize_workflow(base_workflow, budget)
            optimized_cost = sum(step.credit_estimate for step in optimized_workflow)
            
            # Calculate metrics
            steps_reduction = len(base_workflow) - len(optimized_workflow)
            cost_reduction = base_cost - optimized_cost
            efficiency = (cost_reduction / base_cost * 100) if base_cost > 0 else 0
            
            print(f"   ✂️ Steps: {len(base_workflow)} → {len(optimized_workflow)} (-{steps_reduction})")
            print(f"   💰 Cost: {base_cost} → {optimized_cost} (-{cost_reduction})")
            print(f"   ⚡ Efficiency Gain: {efficiency:.1f}%")
            print(f"   📊 Budget Utilization: {(optimized_cost/budget*100):.1f}%")
            
            # Show which agents were selected
            selected_agents = [step.agent_type.value for step in optimized_workflow]
            print(f"   🤖 Selected Agents: {', '.join(selected_agents)}")
    
    def demonstrate_real_time_monitoring(self):
        """Demonstrate real-time workflow monitoring"""
        
        print("\n📊 REAL-TIME MONITORING DEMO")
        print("-" * 30)
        
        # Simulate active workflows
        active_workflows = [
            {
                "id": "WF_001",
                "task": "Auto claim processing",
                "start_time": datetime.now().isoformat(),
                "current_step": 2,
                "total_steps": 4,
                "credits_used": 8,
                "status": "in_progress"
            },
            {
                "id": "WF_002", 
                "task": "Risk assessment",
                "start_time": datetime.now().isoformat(),
                "current_step": 1,
                "total_steps": 3,
                "credits_used": 4,
                "status": "in_progress"
            },
            {
                "id": "WF_003",
                "task": "Fraud investigation",
                "start_time": datetime.now().isoformat(),
                "current_step": 3,
                "total_steps": 3,
                "credits_used": 15,
                "status": "completing"
            }
        ]
        
        print("🔄 Active Workflows:")
        for workflow in active_workflows:
            progress = (workflow['current_step'] / workflow['total_steps']) * 100
            print(f"   {workflow['id']}: {workflow['task']}")
            print(f"      Progress: {progress:.1f}% ({workflow['current_step']}/{workflow['total_steps']})")
            print(f"      Credits Used: {workflow['credits_used']}")
            print(f"      Status: {workflow['status']}")
        
        # Show system metrics
        total_active = len(active_workflows)
        total_credits_used = sum(w['credits_used'] for w in active_workflows)
        avg_progress = sum((w['current_step']/w['total_steps']) for w in active_workflows) / len(active_workflows) * 100
        
        print(f"\n📈 System Metrics:")
        print(f"   Active Workflows: {total_active}")
        print(f"   Total Credits in Use: {total_credits_used}")
        print(f"   Average Progress: {avg_progress:.1f}%")
        print(f"   System Load: {'High' if total_active > 5 else 'Medium' if total_active > 2 else 'Low'}")
    
    def run_full_demo(self):
        """Run the complete demonstration"""
        
        print("🚀 Starting Zurich Edge AI Platform Demo...")
        print("This demo showcases the multi-agentic system with ReAct and Hierarchical frameworks")
        print("Focus: Credit optimization and clear workflow visualization\n")
        
        try:
            # Run all demonstrations
            self.demonstrate_workflow_optimization()
            time.sleep(2)
            
            self.demonstrate_react_framework()
            time.sleep(2)
            
            self.demonstrate_hierarchical_coordination()
            time.sleep(2)
            
            self.demonstrate_credit_optimization()
            time.sleep(2)
            
            self.demonstrate_real_time_monitoring()
            
            print("\n" + "=" * 50)
            print("✅ Demo completed successfully!")
            print("🎯 Key Highlights:")
            print("   • Multi-agentic AI with 7 specialized agents")
            print("   • ReAct framework for intelligent reasoning")
            print("   • Hierarchical coordination for complex tasks")
            print("   • Credit optimization for cost efficiency")
            print("   • Real-time monitoring and analytics")
            print("   • Clear workflow visualization")
            print("\n🚀 Ready for production deployment!")
            print("=" * 50)
            
        except Exception as e:
            print(f"\n❌ Demo error: {str(e)}")
            print("Please check the configuration and try again.")

if __name__ == "__main__":
    demo = ZurichEdgeDemo()
    demo.run_full_demo()

