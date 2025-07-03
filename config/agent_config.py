"""
Multi-Agentic AI Configuration for Zurich Edge Insurance Platform
Implements ReAct (Reasoning and Acting) and Hierarchical frameworks
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from enum import Enum

class AgentType(Enum):
    COORDINATOR = "coordinator"
    CLAIMS_SPECIALIST = "claims_specialist"
    RISK_ANALYST = "risk_analyst"
    CUSTOMER_SERVICE = "customer_service"
    POLICY_ADVISOR = "policy_advisor"
    FRAUD_DETECTOR = "fraud_detector"
    PRICING_ENGINE = "pricing_engine"

class TaskComplexity(Enum):
    LOW = 1      # Simple queries, basic info retrieval
    MEDIUM = 2   # Standard processing, moderate analysis
    HIGH = 3     # Complex analysis, multi-step reasoning
    CRITICAL = 4 # Emergency claims, fraud detection

@dataclass
class AgentCapability:
    name: str
    description: str
    credit_cost: int
    max_concurrent_tasks: int
    specializations: List[str]

@dataclass
class WorkflowStep:
    agent_type: AgentType
    action: str
    reasoning: str
    expected_output: str
    credit_estimate: int
    fallback_agent: Optional[AgentType] = None

class AgentHierarchy:
    """Hierarchical Agent Management System"""
    
    def __init__(self):
        self.agents = {
            AgentType.COORDINATOR: AgentCapability(
                name="Master Coordinator",
                description="Orchestrates all agents, optimizes workflows, manages credit allocation",
                credit_cost=2,
                max_concurrent_tasks=10,
                specializations=["workflow_optimization", "resource_allocation", "task_routing"]
            ),
            
            AgentType.CLAIMS_SPECIALIST: AgentCapability(
                name="Claims Processing Agent",
                description="Handles claim submissions, damage assessment, payout calculations",
                credit_cost=5,
                max_concurrent_tasks=3,
                specializations=["damage_assessment", "claim_validation", "payout_calculation", "computer_vision"]
            ),
            
            AgentType.RISK_ANALYST: AgentCapability(
                name="Risk Analysis Agent",
                description="Evaluates risks, predicts outcomes, IoT data analysis",
                credit_cost=4,
                max_concurrent_tasks=2,
                specializations=["risk_modeling", "predictive_analytics", "iot_analysis", "weather_data"]
            ),
            
            AgentType.CUSTOMER_SERVICE: AgentCapability(
                name="Customer Service Agent",
                description="Handles customer queries, provides support, manages communications",
                credit_cost=3,
                max_concurrent_tasks=5,
                specializations=["natural_language", "sentiment_analysis", "multi_language", "voice_processing"]
            ),
            
            AgentType.POLICY_ADVISOR: AgentCapability(
                name="Policy Advisory Agent",
                description="Recommends policies, explains coverage, handles customization",
                credit_cost=4,
                max_concurrent_tasks=3,
                specializations=["policy_analysis", "coverage_optimization", "regulatory_compliance", "personalization"]
            ),
            
            AgentType.FRAUD_DETECTOR: AgentCapability(
                name="Fraud Detection Agent",
                description="Identifies suspicious activities, validates claims authenticity",
                credit_cost=6,
                max_concurrent_tasks=2,
                specializations=["anomaly_detection", "pattern_recognition", "behavioral_analysis", "document_verification"]
            ),
            
            AgentType.PRICING_ENGINE: AgentCapability(
                name="Dynamic Pricing Agent",
                description="Calculates premiums, adjusts pricing based on real-time data",
                credit_cost=3,
                max_concurrent_tasks=4,
                specializations=["actuarial_modeling", "real_time_pricing", "usage_based_insurance", "market_analysis"]
            )
        }
        
        self.hierarchy_levels = {
            1: [AgentType.COORDINATOR],  # Top level
            2: [AgentType.CLAIMS_SPECIALIST, AgentType.RISK_ANALYST, AgentType.FRAUD_DETECTOR],  # Critical operations
            3: [AgentType.POLICY_ADVISOR, AgentType.PRICING_ENGINE],  # Advisory services
            4: [AgentType.CUSTOMER_SERVICE]  # Support services
        }
        
        self.credit_thresholds = {
            TaskComplexity.LOW: 5,
            TaskComplexity.MEDIUM: 15,
            TaskComplexity.HIGH: 30,
            TaskComplexity.CRITICAL: 50
        }

AGENT_HIERARCHY = {
    'Level 1 (Master)': ['Enhanced Coordinator'],
    'Level 2 (Specialists)': ['Claims Specialist', 'Risk Analyst'],
    'Level 3 (Support)': ['Fraud Detector', 'Policy Advisor'],
    'Level 4 (Interface)': ['Customer Service']
}

class ReActFramework:
    """ReAct (Reasoning and Acting) Framework Implementation"""
    
    @staticmethod
    def create_reasoning_chain(task: str, context: Dict[str, Any]) -> List[WorkflowStep]:
        """
        Creates a reasoning chain for task execution
        Optimizes for minimal credit usage while maintaining quality
        """
        steps = []
        
        # Step 1: Analyze task complexity
        complexity = ReActFramework._assess_task_complexity(task, context)
        
        # Step 2: Determine optimal agent sequence
        agent_sequence = ReActFramework._optimize_agent_sequence(task, complexity)
        
        # Step 3: Create workflow steps with reasoning
        for i, agent_type in enumerate(agent_sequence):
            step = WorkflowStep(
                agent_type=agent_type,
                action=ReActFramework._determine_action(agent_type, task, i),
                reasoning=ReActFramework._generate_reasoning(agent_type, task, i),
                expected_output=ReActFramework._define_expected_output(agent_type, task),
                credit_estimate=ReActFramework._estimate_credits(agent_type, complexity)
            )
            steps.append(step)
        
        return steps
    
    @staticmethod
    def _assess_task_complexity(task: str, context: Dict[str, Any]) -> TaskComplexity:
        """Assess task complexity to optimize resource allocation"""
        keywords_high = ["fraud", "emergency", "complex", "investigation", "critical"]
        keywords_medium = ["claim", "analysis", "recommendation", "calculation"]
        keywords_low = ["information", "status", "simple", "basic"]
        
        task_lower = task.lower()
        
        if any(keyword in task_lower for keyword in keywords_high):
            return TaskComplexity.HIGH
        elif any(keyword in task_lower for keyword in keywords_medium):
            return TaskComplexity.MEDIUM
        else:
            return TaskComplexity.LOW
    
    @staticmethod
    def _optimize_agent_sequence(task: str, complexity: TaskComplexity) -> List[AgentType]:
        """Optimize agent sequence for minimal credit usage"""
        task_lower = task.lower()
        
        # Always start with coordinator for complex tasks
        if complexity in [TaskComplexity.HIGH, TaskComplexity.CRITICAL]:
            sequence = [AgentType.COORDINATOR]
        else:
            sequence = []
        
        # Route to appropriate specialists
        if "claim" in task_lower:
            sequence.extend([AgentType.CLAIMS_SPECIALIST])
            if "fraud" in task_lower or complexity == TaskComplexity.CRITICAL:
                sequence.append(AgentType.FRAUD_DETECTOR)
        
        if "risk" in task_lower or "predict" in task_lower:
            sequence.append(AgentType.RISK_ANALYST)
        
        if "policy" in task_lower or "coverage" in task_lower:
            sequence.append(AgentType.POLICY_ADVISOR)
        
        if "price" in task_lower or "premium" in task_lower:
            sequence.append(AgentType.PRICING_ENGINE)
        
        if "customer" in task_lower or "support" in task_lower:
            sequence.append(AgentType.CUSTOMER_SERVICE)
        
        # Default to customer service for simple queries
        if not sequence:
            sequence = [AgentType.CUSTOMER_SERVICE]
        
        return sequence
    
    @staticmethod
    def _determine_action(agent_type: AgentType, task: str, step_index: int) -> str:
        """Determine specific action for each agent"""
        actions = {
            AgentType.COORDINATOR: "Analyze task and coordinate workflow",
            AgentType.CLAIMS_SPECIALIST: "Process claim and assess damage",
            AgentType.RISK_ANALYST: "Analyze risk factors and predict outcomes",
            AgentType.CUSTOMER_SERVICE: "Provide customer support and information",
            AgentType.POLICY_ADVISOR: "Recommend optimal policy configuration",
            AgentType.FRAUD_DETECTOR: "Detect and analyze potential fraud indicators",
            AgentType.PRICING_ENGINE: "Calculate optimal pricing and premiums"
        }
        return actions.get(agent_type, "Execute specialized task")
    
    @staticmethod
    def _generate_reasoning(agent_type: AgentType, task: str, step_index: int) -> str:
        """Generate reasoning for each step"""
        if step_index == 0:
            return f"Initial assessment required by {agent_type.value} to understand task scope and requirements"
        else:
            return f"Specialized processing by {agent_type.value} based on previous analysis results"
    
    @staticmethod
    def _define_expected_output(agent_type: AgentType, task: str) -> str:
        """Define expected output for each agent"""
        outputs = {
            AgentType.COORDINATOR: "Task analysis, workflow plan, resource allocation",
            AgentType.CLAIMS_SPECIALIST: "Claim status, damage assessment, payout recommendation",
            AgentType.RISK_ANALYST: "Risk score, predictive insights, recommendations",
            AgentType.CUSTOMER_SERVICE: "Customer response, support resolution, satisfaction metrics",
            AgentType.POLICY_ADVISOR: "Policy recommendations, coverage analysis, compliance check",
            AgentType.FRAUD_DETECTOR: "Fraud risk score, suspicious activity report, verification status",
            AgentType.PRICING_ENGINE: "Premium calculation, pricing factors, discount eligibility"
        }
        return outputs.get(agent_type, "Specialized analysis results")
    
    @staticmethod
    def _estimate_credits(agent_type: AgentType, complexity: TaskComplexity) -> int:
        """Estimate credit usage for optimization"""
        hierarchy = AgentHierarchy()
        base_cost = hierarchy.agents[agent_type].credit_cost
        
        multipliers = {
            TaskComplexity.LOW: 0.5,
            TaskComplexity.MEDIUM: 1.0,
            TaskComplexity.HIGH: 1.5,
            TaskComplexity.CRITICAL: 2.0
        }
        
        return int(base_cost * multipliers[complexity])

# Credit Optimization Strategies
class CreditOptimizer:
    """Optimizes credit usage across the multi-agent system"""
    
    @staticmethod
    def optimize_workflow(steps: List[WorkflowStep], credit_budget: int) -> List[WorkflowStep]:
        """Optimize workflow to stay within credit budget"""
        total_estimated = sum(step.credit_estimate for step in steps)
        
        if total_estimated <= credit_budget:
            return steps
        
        # Prioritize critical agents and reduce non-essential processing
        optimized_steps = []
        remaining_budget = credit_budget
        
        # Sort by importance (coordinator first, then critical operations)
        priority_order = [
            AgentType.COORDINATOR,
            AgentType.FRAUD_DETECTOR,
            AgentType.CLAIMS_SPECIALIST,
            AgentType.RISK_ANALYST,
            AgentType.POLICY_ADVISOR,
            AgentType.PRICING_ENGINE,
            AgentType.CUSTOMER_SERVICE
        ]
        
        for agent_type in priority_order:
            for step in steps:
                if step.agent_type == agent_type and step.credit_estimate <= remaining_budget:
                    optimized_steps.append(step)
                    remaining_budget -= step.credit_estimate
                    break
        
        return optimized_steps
    
    @staticmethod
    def get_cost_breakdown(steps: List[WorkflowStep]) -> Dict[str, Any]:
        """Provide detailed cost breakdown for transparency"""
        breakdown = {
            "total_credits": sum(step.credit_estimate for step in steps),
            "agent_costs": {},
            "step_details": []
        }
        
        for step in steps:
            agent_name = step.agent_type.value
            if agent_name not in breakdown["agent_costs"]:
                breakdown["agent_costs"][agent_name] = 0
            breakdown["agent_costs"][agent_name] += step.credit_estimate
            
            breakdown["step_details"].append({
                "agent": agent_name,
                "action": step.action,
                "reasoning": step.reasoning,
                "credits": step.credit_estimate
            })
        
        return breakdown

CREDIT_OPTIMIZATION_CONFIG = {
    "optimization_levels": ["Conservative", "Balanced", "Aggressive"],
    "default_level": "Balanced",
    "parallel_processing": True,
    "smart_routing": True
}

