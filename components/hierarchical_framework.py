"""
Hierarchical Framework for Dynamic Agent Selection

This module implements a sophisticated agent selection system that can
dynamically choose and coordinate multiple agents based on task complexity,
context, and available resources.
"""

import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
import re

from .openai_client import OpenAIClient
from .search_integration import SearchIntegration, DynamicSearchAgent

class TaskComplexity(Enum):
    SIMPLE = "simple"
    MODERATE = "moderate" 
    COMPLEX = "complex"
    HIGHLY_COMPLEX = "highly_complex"
    CRITICAL = "critical"

class AgentTier(Enum):
    CORE = "core"           # Essential agents for basic tasks
    SPECIALIZED = "specialized"  # Domain-specific agents
    ADVANCED = "advanced"   # Complex analysis agents
    SUPPORT = "support"     # Supporting/auxiliary agents

@dataclass
class AgentCapability:
    agent_name: str
    tier: AgentTier
    specializations: List[str]
    complexity_threshold: TaskComplexity
    credit_cost: int
    estimated_duration: int
    dependencies: List[str]
    conflict_agents: List[str]

class HierarchicalFramework:
    """
    Dynamic agent selection and coordination framework
    """
    
    def __init__(self):
        self.openai_client = OpenAIClient()
        self.search_agent = DynamicSearchAgent()
        self.search_integration = SearchIntegration()
        
        # Define all available agents with their capabilities
        self.agent_registry = self._initialize_agent_registry()
        
        # Task complexity analysis patterns
        self.complexity_indicators = {
            TaskComplexity.SIMPLE: {
                'keywords': ['status', 'information', 'basic', 'simple', 'quick'],
                'max_entities': 1,
                'max_steps': 2,
                'credit_threshold': 10
            },
            TaskComplexity.MODERATE: {
                'keywords': ['claim', 'quote', 'policy', 'coverage', 'assessment'],
                'max_entities': 3,
                'max_steps': 4,
                'credit_threshold': 25
            },
            TaskComplexity.COMPLEX: {
                'keywords': ['investigation', 'analysis', 'validation', 'fraud', 'risk'],
                'max_entities': 5,
                'max_steps': 7,
                'credit_threshold': 50
            },
            TaskComplexity.HIGHLY_COMPLEX: {
                'keywords': ['comprehensive', 'multi-factor', 'cross-reference', 'detailed'],
                'max_entities': 8,
                'max_steps': 10,
                'credit_threshold': 75
            },
            TaskComplexity.CRITICAL: {
                'keywords': ['emergency', 'urgent', 'critical', 'immediate', 'crisis'],
                'max_entities': 12,
                'max_steps': 15,
                'credit_threshold': 100
            }
        }
    
    def _initialize_agent_registry(self) -> Dict[str, AgentCapability]:
        """Initialize the registry of all available agents"""
        
        agents = {
            # Core Tier - Essential for basic operations
            'Customer Service': AgentCapability(
                agent_name='Customer Service',
                tier=AgentTier.CORE,
                specializations=['communication', 'basic_support', 'routing'],
                complexity_threshold=TaskComplexity.SIMPLE,
                credit_cost=3,
                estimated_duration=2,
                dependencies=[],
                conflict_agents=[]
            ),
            
            'Policy Expert': AgentCapability(
                agent_name='Policy Expert',
                tier=AgentTier.CORE,
                specializations=['policy_analysis', 'coverage_details', 'regulations'],
                complexity_threshold=TaskComplexity.SIMPLE,
                credit_cost=4,
                estimated_duration=3,
                dependencies=[],
                conflict_agents=[]
            ),
            
            # Specialized Tier - Domain-specific expertise
            'Claims Processor': AgentCapability(
                agent_name='Claims Processor',
                tier=AgentTier.SPECIALIZED,
                specializations=['claim_processing', 'documentation', 'workflow'],
                complexity_threshold=TaskComplexity.MODERATE,
                credit_cost=5,
                estimated_duration=4,
                dependencies=['Policy Expert'],
                conflict_agents=[]
            ),
            
            'Claims Validation Agent': AgentCapability(
                agent_name='Claims Validation Agent',
                tier=AgentTier.SPECIALIZED,
                specializations=['external_validation', 'real_time_data', 'verification'],
                complexity_threshold=TaskComplexity.MODERATE,
                credit_cost=7,
                estimated_duration=5,
                dependencies=['Dynamic Search Agent'],
                conflict_agents=[]
            ),
            
            'Risk Analyst': AgentCapability(
                agent_name='Risk Analyst',
                tier=AgentTier.SPECIALIZED,
                specializations=['risk_assessment', 'threat_analysis', 'safety'],
                complexity_threshold=TaskComplexity.MODERATE,
                credit_cost=6,
                estimated_duration=4,
                dependencies=[],
                conflict_agents=[]
            ),
            
            'Underwriter': AgentCapability(
                agent_name='Underwriter',
                tier=AgentTier.SPECIALIZED,
                specializations=['pricing', 'risk_evaluation', 'approval'],
                complexity_threshold=TaskComplexity.MODERATE,
                credit_cost=6,
                estimated_duration=4,
                dependencies=['Risk Analyst'],
                conflict_agents=[]
            ),
            
            'Weather Analyst': AgentCapability(
                agent_name='Weather Analyst',
                tier=AgentTier.SPECIALIZED,
                specializations=['weather_data', 'climate_risk', 'forecasting'],
                complexity_threshold=TaskComplexity.MODERATE,
                credit_cost=5,
                estimated_duration=3,
                dependencies=['Dynamic Search Agent'],
                conflict_agents=[]
            ),
            
            # Advanced Tier - Complex analysis and investigation
            'Fraud Investigator': AgentCapability(
                agent_name='Fraud Investigator',
                tier=AgentTier.ADVANCED,
                specializations=['fraud_detection', 'pattern_analysis', 'investigation'],
                complexity_threshold=TaskComplexity.COMPLEX,
                credit_cost=8,
                estimated_duration=6,
                dependencies=['Claims Validation Agent', 'Data Analyst'],
                conflict_agents=[]
            ),
            
            'Data Analyst': AgentCapability(
                agent_name='Data Analyst',
                tier=AgentTier.ADVANCED,
                specializations=['data_analysis', 'pattern_recognition', 'statistics'],
                complexity_threshold=TaskComplexity.COMPLEX,
                credit_cost=7,
                estimated_duration=5,
                dependencies=[],
                conflict_agents=[]
            ),
            
            'ESG Specialist': AgentCapability(
                agent_name='ESG Specialist',
                tier=AgentTier.ADVANCED,
                specializations=['environmental_impact', 'sustainability', 'compliance'],
                complexity_threshold=TaskComplexity.COMPLEX,
                credit_cost=6,
                estimated_duration=4,
                dependencies=['Data Analyst'],
                conflict_agents=[]
            ),
            
            'Compliance Officer': AgentCapability(
                agent_name='Compliance Officer',
                tier=AgentTier.ADVANCED,
                specializations=['regulatory_compliance', 'legal_requirements', 'audit'],
                complexity_threshold=TaskComplexity.COMPLEX,
                credit_cost=7,
                estimated_duration=5,
                dependencies=['Policy Expert'],
                conflict_agents=[]
            ),
            
            # Support Tier - Auxiliary and coordination agents
            'Dynamic Search Agent': AgentCapability(
                agent_name='Dynamic Search Agent',
                tier=AgentTier.SUPPORT,
                specializations=['real_time_search', 'information_gathering', 'context'],
                complexity_threshold=TaskComplexity.SIMPLE,
                credit_cost=4,
                estimated_duration=2,
                dependencies=[],
                conflict_agents=[]
            ),
            
            'Workflow Coordinator': AgentCapability(
                agent_name='Workflow Coordinator',
                tier=AgentTier.SUPPORT,
                specializations=['coordination', 'optimization', 'monitoring'],
                complexity_threshold=TaskComplexity.MODERATE,
                credit_cost=5,
                estimated_duration=3,
                dependencies=[],
                conflict_agents=[]
            ),
            
            'Quality Assurance Agent': AgentCapability(
                agent_name='Quality Assurance Agent',
                tier=AgentTier.SUPPORT,
                specializations=['quality_control', 'validation', 'review'],
                complexity_threshold=TaskComplexity.COMPLEX,
                credit_cost=6,
                estimated_duration=4,
                dependencies=[],
                conflict_agents=[]
            ),
            
            'Emergency Response Agent': AgentCapability(
                agent_name='Emergency Response Agent',
                tier=AgentTier.SUPPORT,
                specializations=['emergency_handling', 'crisis_management', 'rapid_response'],
                complexity_threshold=TaskComplexity.CRITICAL,
                credit_cost=10,
                estimated_duration=2,
                dependencies=['Dynamic Search Agent'],
                conflict_agents=[]
            )
        }
        
        return agents
    
    def analyze_task_complexity(self, task: str, context: Dict[str, Any]) -> Tuple[TaskComplexity, Dict[str, Any]]:
        """
        Analyze task complexity using multiple factors
        """
        
        analysis = {
            'task': task,
            'context_factors': [],
            'complexity_indicators': [],
            'entity_count': 0,
            'keyword_matches': {},
            'ai_assessment': {},
            'final_complexity': TaskComplexity.MODERATE
        }
        
        task_lower = task.lower()
        
        # Count entities and complexity indicators
        entities = self._extract_entities(task, context)
        analysis['entity_count'] = len(entities)
        analysis['entities'] = entities
        
        # Check keyword matches for each complexity level
        for complexity, indicators in self.complexity_indicators.items():
            matches = [kw for kw in indicators['keywords'] if kw in task_lower]
            if matches:
                analysis['keyword_matches'][complexity.value] = matches
        
        # Context-based complexity factors
        context_factors = []
        if context.get('location'):
            context_factors.append('location_specific')
        if context.get('date') or context.get('time_sensitive'):
            context_factors.append('time_sensitive')
        if context.get('amount') or context.get('value'):
            context_factors.append('financial_impact')
        if context.get('multiple_parties'):
            context_factors.append('multi_party')
        
        analysis['context_factors'] = context_factors
        
        # AI-based complexity assessment
        ai_assessment = self._ai_assess_complexity(task, context, analysis)
        analysis['ai_assessment'] = ai_assessment
        
        # Determine final complexity
        final_complexity = self._determine_final_complexity(analysis)
        analysis['final_complexity'] = final_complexity
        
        return final_complexity, analysis
    
    def _extract_entities(self, task: str, context: Dict[str, Any]) -> List[str]:
        """Extract entities from task and context"""
        
        entities = []
        
        # Extract from context
        for key, value in context.items():
            if value and isinstance(value, str):
                entities.append(f"{key}:{value}")
        
        # Extract from task using patterns
        patterns = {
            'location': r'\b(?:in|at|near|from)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            'date': r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
            'amount': r'\$[\d,]+(?:\.\d{2})?',
            'person': r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\b'
        }
        
        for entity_type, pattern in patterns.items():
            matches = re.findall(pattern, task)
            for match in matches:
                entities.append(f"{entity_type}:{match}")
        
        return entities
    
    def _ai_assess_complexity(self, task: str, context: Dict[str, Any], analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Use AI to assess task complexity"""
        
        prompt = f"""
        Analyze the complexity of this insurance task:
        
        Task: "{task}"
        Context: {json.dumps(context, indent=2)}
        Entities found: {analysis.get('entities', [])}
        Context factors: {analysis.get('context_factors', [])}
        
        Assess complexity based on:
        1. Number of steps required
        2. Domain expertise needed
        3. External data requirements
        4. Risk level
        5. Time sensitivity
        6. Stakeholder involvement
        
        Return assessment in JSON format:
        {{
            "complexity_score": 1-10,
            "reasoning": "explanation of complexity assessment",
            "required_expertise": ["domain1", "domain2"],
            "external_data_needed": true/false,
            "estimated_steps": 1-15,
            "risk_level": "low/medium/high/critical",
            "recommended_complexity": "simple/moderate/complex/highly_complex/critical"
        }}
        """
        
        try:
            response = self.openai_client.get_chat_completion(prompt)
            assessment = json.loads(response.get('response', '{}'))
            return assessment
        except Exception as e:
            return {
                'complexity_score': 5,
                'reasoning': f'AI assessment failed: {str(e)}',
                'required_expertise': ['general'],
                'external_data_needed': False,
                'estimated_steps': 3,
                'risk_level': 'medium',
                'recommended_complexity': 'moderate'
            }
    
    def _determine_final_complexity(self, analysis: Dict[str, Any]) -> TaskComplexity:
        """Determine final complexity based on all factors"""
        
        # Start with AI recommendation
        ai_complexity = analysis.get('ai_assessment', {}).get('recommended_complexity', 'moderate')
        
        # Map AI recommendation to enum
        complexity_mapping = {
            'simple': TaskComplexity.SIMPLE,
            'moderate': TaskComplexity.MODERATE,
            'complex': TaskComplexity.COMPLEX,
            'highly_complex': TaskComplexity.HIGHLY_COMPLEX,
            'critical': TaskComplexity.CRITICAL
        }
        
        base_complexity = complexity_mapping.get(ai_complexity, TaskComplexity.MODERATE)
        
        # Adjust based on other factors
        entity_count = analysis.get('entity_count', 0)
        context_factors = len(analysis.get('context_factors', []))
        
        # Increase complexity based on entity count
        if entity_count > 5:
            if base_complexity.value in ['simple', 'moderate']:
                base_complexity = TaskComplexity.COMPLEX
        elif entity_count > 8:
            base_complexity = TaskComplexity.HIGHLY_COMPLEX
        
        # Increase complexity based on context factors
        if context_factors > 3:
            if base_complexity == TaskComplexity.SIMPLE:
                base_complexity = TaskComplexity.MODERATE
            elif base_complexity == TaskComplexity.MODERATE:
                base_complexity = TaskComplexity.COMPLEX
        
        # Check for critical keywords
        keyword_matches = analysis.get('keyword_matches', {})
        if 'critical' in keyword_matches:
            base_complexity = TaskComplexity.CRITICAL
        
        return base_complexity
    
    def select_agents_dynamically(self, task: str, context: Dict[str, Any], credit_budget: int) -> Dict[str, Any]:
        """
        Dynamically select agents based on task complexity and available resources
        """
        
        # Analyze task complexity
        complexity, complexity_analysis = self.analyze_task_complexity(task, context)
        
        # Get search context if needed
        search_context = None
        if complexity in [TaskComplexity.COMPLEX, TaskComplexity.HIGHLY_COMPLEX, TaskComplexity.CRITICAL]:
            search_context = self.search_agent.get_real_time_context(
                task, context.get('location')
            )
        
        # Select agents based on complexity and budget
        selected_agents = self._select_agents_by_complexity(
            complexity, task, context, credit_budget, search_context
        )
        
        # Optimize agent sequence
        optimized_sequence = self._optimize_agent_sequence(selected_agents, complexity)
        
        # Calculate resource allocation
        resource_allocation = self._calculate_resource_allocation(
            optimized_sequence, complexity, credit_budget
        )
        
        return {
            'task': task,
            'complexity': complexity.value,
            'complexity_analysis': complexity_analysis,
            'search_context': search_context,
            'selected_agents': selected_agents,
            'optimized_sequence': optimized_sequence,
            'resource_allocation': resource_allocation,
            'total_estimated_cost': sum(agent['credit_cost'] for agent in selected_agents),
            'total_estimated_duration': max(agent['estimated_duration'] for agent in selected_agents),
            'framework_version': '2.0_hierarchical'
        }
    
    def _select_agents_by_complexity(self, complexity: TaskComplexity, task: str, context: Dict[str, Any], 
                                   credit_budget: int, search_context: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """Select agents based on complexity level"""
        
        selected = []
        task_lower = task.lower()
        
        # Always include core agents for basic functionality
        core_agents = [agent for agent in self.agent_registry.values() 
                      if agent.tier == AgentTier.CORE]
        
        for agent in core_agents:
            selected.append(self._agent_to_dict(agent))
        
        # Add specialized agents based on task content and complexity
        specialized_agents = [agent for agent in self.agent_registry.values() 
                            if agent.tier == AgentTier.SPECIALIZED]
        
        for agent in specialized_agents:
            # For moderate+ complexity, be more inclusive
            if complexity in [TaskComplexity.MODERATE, TaskComplexity.COMPLEX, TaskComplexity.HIGHLY_COMPLEX, TaskComplexity.CRITICAL]:
                if self._is_agent_relevant(agent, task, context) or self._is_agent_useful_for_complexity(agent, complexity):
                    selected.append(self._agent_to_dict(agent))
            elif complexity == TaskComplexity.SIMPLE and self._is_agent_relevant(agent, task, context):
                selected.append(self._agent_to_dict(agent))
        
        # Add advanced agents for complex tasks
        if complexity in [TaskComplexity.COMPLEX, TaskComplexity.HIGHLY_COMPLEX, TaskComplexity.CRITICAL]:
            advanced_agents = [agent for agent in self.agent_registry.values() 
                             if agent.tier == AgentTier.ADVANCED]
            
            for agent in advanced_agents:
                # Include most advanced agents for complex tasks
                if self._is_agent_relevant(agent, task, context) or complexity in [TaskComplexity.HIGHLY_COMPLEX, TaskComplexity.CRITICAL]:
                    selected.append(self._agent_to_dict(agent))
        
        # Add support agents based on needs
        support_agents = [agent for agent in self.agent_registry.values() 
                         if agent.tier == AgentTier.SUPPORT]
        
        for agent in support_agents:
            # Always include search agent for moderate+ tasks
            if agent.agent_name == 'Dynamic Search Agent' and complexity != TaskComplexity.SIMPLE:
                selected.append(self._agent_to_dict(agent))
            # Include emergency agent for critical tasks
            elif agent.agent_name == 'Emergency Response Agent' and complexity == TaskComplexity.CRITICAL:
                selected.append(self._agent_to_dict(agent))
            # Include QA for complex+ tasks
            elif agent.agent_name == 'Quality Assurance Agent' and complexity in [TaskComplexity.COMPLEX, TaskComplexity.HIGHLY_COMPLEX, TaskComplexity.CRITICAL]:
                selected.append(self._agent_to_dict(agent))
            # Include coordinator for moderate+ tasks
            elif agent.agent_name == 'Workflow Coordinator' and complexity != TaskComplexity.SIMPLE:
                selected.append(self._agent_to_dict(agent))
        
        # Remove duplicates
        seen_agents = set()
        unique_selected = []
        for agent in selected:
            if agent['agent_name'] not in seen_agents:
                unique_selected.append(agent)
                seen_agents.add(agent['agent_name'])
        
        # Filter by budget constraints (but be more generous for complex tasks)
        filtered_agents = self._filter_by_budget(unique_selected, credit_budget, complexity)
        
        return filtered_agents
    
    def _is_agent_useful_for_complexity(self, agent: AgentCapability, complexity: TaskComplexity) -> bool:
        """Determine if an agent is useful for a given complexity level"""
        
        # For complex tasks, include more agents even if not directly relevant
        if complexity in [TaskComplexity.COMPLEX, TaskComplexity.HIGHLY_COMPLEX, TaskComplexity.CRITICAL]:
            # Include most specialized and advanced agents
            if agent.tier in [AgentTier.SPECIALIZED, AgentTier.ADVANCED]:
                return True
        
        # For highly complex and critical tasks, include almost all agents
        if complexity in [TaskComplexity.HIGHLY_COMPLEX, TaskComplexity.CRITICAL]:
            return True
        
        return False
    
    def _is_agent_relevant(self, agent: AgentCapability, task: str, context: Dict[str, Any]) -> bool:
        """Determine if an agent is relevant to the task"""
        
        task_lower = task.lower()
        
        # Check specialization relevance
        for specialization in agent.specializations:
            if any(keyword in task_lower for keyword in specialization.split('_')):
                return True
        
        # Specific agent relevance rules
        relevance_rules = {
            'Claims Processor': ['claim', 'filing', 'process', 'submit'],
            'Claims Validation Agent': ['claim', 'verify', 'validate', 'check'],
            'Risk Analyst': ['risk', 'danger', 'threat', 'safety', 'hazard'],
            'Fraud Investigator': ['fraud', 'suspicious', 'investigate', 'verify'],
            'Weather Analyst': ['weather', 'storm', 'flood', 'hurricane', 'climate'],
            'Underwriter': ['quote', 'pricing', 'premium', 'coverage', 'approve'],
            'ESG Specialist': ['environmental', 'sustainability', 'green', 'carbon'],
            'Compliance Officer': ['compliance', 'regulation', 'legal', 'audit'],
            'Data Analyst': ['analysis', 'data', 'pattern', 'trend', 'statistics']
        }
        
        keywords = relevance_rules.get(agent.agent_name, [])
        return any(keyword in task_lower for keyword in keywords)
    
    def _agent_to_dict(self, agent: AgentCapability) -> Dict[str, Any]:
        """Convert AgentCapability to dictionary"""
        return {
            'agent_name': agent.agent_name,
            'tier': agent.tier.value,
            'specializations': agent.specializations,
            'complexity_threshold': agent.complexity_threshold.value,
            'credit_cost': agent.credit_cost,
            'estimated_duration': agent.estimated_duration,
            'dependencies': agent.dependencies,
            'conflict_agents': agent.conflict_agents
        }
    
    def _filter_by_budget(self, agents: List[Dict[str, Any]], budget: int, complexity: TaskComplexity = TaskComplexity.MODERATE) -> List[Dict[str, Any]]:
        """Filter agents based on budget constraints"""
        
        # Sort by priority (core > specialized > advanced > support)
        tier_priority = {'core': 1, 'specialized': 2, 'advanced': 3, 'support': 4}
        agents.sort(key=lambda x: (tier_priority.get(x['tier'], 5), x['credit_cost']))
        
        selected = []
        total_cost = 0
        
        # For complex tasks, be more generous with budget allocation
        budget_multiplier = {
            TaskComplexity.SIMPLE: 1.0,
            TaskComplexity.MODERATE: 1.2,
            TaskComplexity.COMPLEX: 1.5,
            TaskComplexity.HIGHLY_COMPLEX: 1.8,
            TaskComplexity.CRITICAL: 2.0
        }
        
        effective_budget = int(budget * budget_multiplier.get(complexity, 1.0))
        
        # Always include core agents regardless of budget
        core_agents = [agent for agent in agents if agent['tier'] == 'core']
        for agent in core_agents:
            selected.append(agent)
            total_cost += agent['credit_cost']
        
        # Add other agents within budget
        remaining_agents = [agent for agent in agents if agent['tier'] != 'core']
        for agent in remaining_agents:
            if total_cost + agent['credit_cost'] <= effective_budget:
                selected.append(agent)
                total_cost += agent['credit_cost']
            elif complexity in [TaskComplexity.HIGHLY_COMPLEX, TaskComplexity.CRITICAL]:
                # For very complex tasks, include essential agents even if slightly over budget
                if agent['tier'] in ['specialized', 'advanced'] and total_cost + agent['credit_cost'] <= effective_budget * 1.2:
                    selected.append(agent)
                    total_cost += agent['credit_cost']
        
        return selected
    
    def _optimize_agent_sequence(self, agents: List[Dict[str, Any]], complexity: TaskComplexity) -> List[Dict[str, Any]]:
        """Optimize the sequence of agent execution"""
        
        # Create dependency graph
        agent_map = {agent['agent_name']: agent for agent in agents}
        
        # Topological sort based on dependencies
        sorted_agents = []
        remaining_agents = agents.copy()
        
        while remaining_agents:
            # Find agents with no unmet dependencies
            ready_agents = []
            for agent in remaining_agents:
                dependencies_met = all(
                    dep in [a['agent_name'] for a in sorted_agents] 
                    for dep in agent['dependencies']
                )
                if dependencies_met:
                    ready_agents.append(agent)
            
            if not ready_agents:
                # Break circular dependencies by adding remaining agents
                ready_agents = remaining_agents
            
            # Sort ready agents by tier priority
            tier_priority = {'core': 1, 'specialized': 2, 'advanced': 3, 'support': 4}
            ready_agents.sort(key=lambda x: tier_priority.get(x['tier'], 5))
            
            # Add the highest priority agent
            next_agent = ready_agents[0]
            sorted_agents.append(next_agent)
            remaining_agents.remove(next_agent)
        
        return sorted_agents
    
    def _calculate_resource_allocation(self, agents: List[Dict[str, Any]], complexity: TaskComplexity, budget: int) -> Dict[str, Any]:
        """Calculate resource allocation for agents"""
        
        total_cost = sum(agent['credit_cost'] for agent in agents)
        total_duration = sum(agent['estimated_duration'] for agent in agents)
        
        # Adjust based on complexity
        complexity_multipliers = {
            TaskComplexity.SIMPLE: 1.0,
            TaskComplexity.MODERATE: 1.2,
            TaskComplexity.COMPLEX: 1.5,
            TaskComplexity.HIGHLY_COMPLEX: 1.8,
            TaskComplexity.CRITICAL: 2.0
        }
        
        multiplier = complexity_multipliers[complexity]
        adjusted_cost = int(total_cost * multiplier)
        adjusted_duration = int(total_duration * multiplier)
        
        return {
            'total_agents': len(agents),
            'base_cost': total_cost,
            'adjusted_cost': adjusted_cost,
            'base_duration': total_duration,
            'adjusted_duration': adjusted_duration,
            'budget_utilization': adjusted_cost / budget if budget > 0 else 0,
            'complexity_multiplier': multiplier,
            'resource_efficiency': len(agents) / adjusted_cost if adjusted_cost > 0 else 0
        }

