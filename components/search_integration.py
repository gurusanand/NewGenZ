"""
Search Integration Component for Dynamic Agent Framework

This module provides real-time search capabilities for agents to gather
current information and make informed decisions.
"""

import requests
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import re
from .openai_client import OpenAIClient

class SearchIntegration:
    """
    Provides search capabilities for agents to gather real-time information
    """
    
    def __init__(self):
        self.openai_client = OpenAIClient()
        
        # Search endpoints and configurations
        self.search_configs = {
            'news': {
                'priority': 'high',
                'timeout': 10,
                'max_results': 5
            },
            'general': {
                'priority': 'medium', 
                'timeout': 8,
                'max_results': 3
            },
            'technical': {
                'priority': 'medium',
                'timeout': 12,
                'max_results': 4
            }
        }
    
    def search_for_context(self, query: str, search_type: str = 'general') -> Dict[str, Any]:
        """
        Search for information to provide context for agent decisions
        
        Args:
            query: Search query
            search_type: Type of search (news, general, technical)
            
        Returns:
            Dict containing search results and analysis
        """
        
        search_result = {
            'query': query,
            'search_type': search_type,
            'timestamp': datetime.now().isoformat(),
            'results': [],
            'summary': '',
            'key_insights': [],
            'confidence': 0.0,
            'sources_count': 0
        }
        
        try:
            # Simulate search results (in real implementation, this would call actual search APIs)
            simulated_results = self._simulate_search_results(query, search_type)
            search_result['results'] = simulated_results
            search_result['sources_count'] = len(simulated_results)
            
            # Use AI to analyze and summarize results
            analysis = self._analyze_search_results(query, simulated_results)
            search_result.update(analysis)
            
        except Exception as e:
            search_result['error'] = str(e)
            search_result['summary'] = f"Search failed: {str(e)}"
        
        return search_result
    
    def _simulate_search_results(self, query: str, search_type: str) -> List[Dict]:
        """
        Simulate search results (replace with actual search API calls)
        """
        
        # This would be replaced with actual search API calls
        # For now, we'll generate realistic simulated results
        
        base_results = []
        
        if 'earthquake' in query.lower():
            base_results = [
                {
                    'title': 'Recent Earthquake Activity - USGS',
                    'url': 'https://earthquake.usgs.gov/earthquakes/browse/',
                    'snippet': 'Real-time earthquake monitoring and historical seismic data',
                    'source': 'USGS',
                    'relevance': 0.95
                },
                {
                    'title': 'Earthquake Insurance Claims Process',
                    'url': 'https://insurance.gov/earthquake-claims',
                    'snippet': 'Guidelines for filing earthquake damage claims',
                    'source': 'Insurance Authority',
                    'relevance': 0.88
                }
            ]
        elif 'flood' in query.lower():
            base_results = [
                {
                    'title': 'Flood Risk Assessment Tools',
                    'url': 'https://floodrisk.gov/assessment',
                    'snippet': 'Current flood risk levels and historical data',
                    'source': 'NOAA',
                    'relevance': 0.92
                },
                {
                    'title': 'Flood Insurance Coverage Guidelines',
                    'url': 'https://fema.gov/flood-insurance',
                    'snippet': 'Federal flood insurance program information',
                    'source': 'FEMA',
                    'relevance': 0.85
                }
            ]
        elif 'market' in query.lower() or 'economic' in query.lower():
            base_results = [
                {
                    'title': 'Current Market Conditions',
                    'url': 'https://marketdata.com/current',
                    'snippet': 'Real-time market analysis and economic indicators',
                    'source': 'Market Data Inc',
                    'relevance': 0.90
                },
                {
                    'title': 'Insurance Industry Trends',
                    'url': 'https://insurancejournal.com/trends',
                    'snippet': 'Latest trends affecting insurance markets',
                    'source': 'Insurance Journal',
                    'relevance': 0.82
                }
            ]
        else:
            # Generic results
            base_results = [
                {
                    'title': f'Information about {query}',
                    'url': f'https://example.com/search?q={query}',
                    'snippet': f'Comprehensive information and analysis about {query}',
                    'source': 'General Database',
                    'relevance': 0.75
                }
            ]
        
        return base_results
    
    def _analyze_search_results(self, query: str, results: List[Dict]) -> Dict[str, Any]:
        """
        Use AI to analyze search results and extract insights
        """
        
        if not results:
            return {
                'summary': 'No search results found',
                'key_insights': [],
                'confidence': 0.0
            }
        
        # Prepare results for AI analysis
        results_text = "\n".join([
            f"Title: {r['title']}\nSource: {r['source']}\nSnippet: {r['snippet']}\nRelevance: {r['relevance']}"
            for r in results
        ])
        
        prompt = f"""
        Analyze these search results for the query: "{query}"
        
        Search Results:
        {results_text}
        
        Provide analysis in JSON format:
        {{
            "summary": "brief summary of key findings",
            "key_insights": ["insight1", "insight2", "insight3"],
            "confidence": 0.0-1.0,
            "risk_factors": ["factor1", "factor2"],
            "recommendations": ["rec1", "rec2"],
            "data_quality": "high/medium/low"
        }}
        """
        
        try:
            response = self.openai_client.get_chat_completion(prompt)
            analysis = json.loads(response.get('response', '{}'))
            return analysis
        except Exception as e:
            return {
                'summary': f'Analysis failed: {str(e)}',
                'key_insights': ['Unable to analyze results'],
                'confidence': 0.3,
                'risk_factors': [],
                'recommendations': ['Manual review recommended'],
                'data_quality': 'low'
            }
    
    def search_for_agent_context(self, agent_type: str, task: str, context: Dict) -> Dict[str, Any]:
        """
        Search for specific information relevant to an agent type
        """
        
        # Define agent-specific search strategies
        search_strategies = {
            'Risk Analyst': {
                'queries': [
                    f"risk assessment {task}",
                    f"safety concerns {context.get('location', '')}",
                    f"historical incidents {task}"
                ],
                'search_type': 'technical'
            },
            'Claims Validation Agent': {
                'queries': [
                    f"recent events {context.get('location', '')}",
                    f"news {task}",
                    f"verification {task}"
                ],
                'search_type': 'news'
            },
            'Weather Analyst': {
                'queries': [
                    f"weather conditions {context.get('location', '')}",
                    f"climate risks {context.get('location', '')}",
                    f"weather forecast {context.get('location', '')}"
                ],
                'search_type': 'technical'
            },
            'Fraud Investigator': {
                'queries': [
                    f"fraud patterns {task}",
                    f"suspicious indicators {task}",
                    f"verification methods {task}"
                ],
                'search_type': 'technical'
            },
            'Policy Expert': {
                'queries': [
                    f"insurance policy {task}",
                    f"coverage guidelines {task}",
                    f"regulatory requirements {task}"
                ],
                'search_type': 'general'
            }
        }
        
        strategy = search_strategies.get(agent_type, {
            'queries': [task],
            'search_type': 'general'
        })
        
        # Perform searches for each query
        all_results = []
        for query in strategy['queries']:
            search_result = self.search_for_context(query, strategy['search_type'])
            all_results.extend(search_result.get('results', []))
        
        # Combine and analyze all results
        combined_analysis = self._combine_search_analyses(all_results, agent_type, task)
        
        return {
            'agent_type': agent_type,
            'task': task,
            'search_strategy': strategy,
            'total_sources': len(all_results),
            'analysis': combined_analysis,
            'timestamp': datetime.now().isoformat()
        }
    
    def _combine_search_analyses(self, results: List[Dict], agent_type: str, task: str) -> Dict[str, Any]:
        """
        Combine multiple search results into a comprehensive analysis
        """
        
        if not results:
            return {
                'summary': 'No relevant information found',
                'confidence': 0.0,
                'recommendations': ['Proceed with standard protocols']
            }
        
        # Prepare combined results for analysis
        combined_text = "\n".join([
            f"Source: {r.get('source', 'Unknown')}\nContent: {r.get('snippet', '')}"
            for r in results
        ])
        
        prompt = f"""
        As a {agent_type}, analyze this information for the task: "{task}"
        
        Available Information:
        {combined_text}
        
        Provide your analysis in JSON format:
        {{
            "summary": "key findings relevant to {agent_type}",
            "confidence": 0.0-1.0,
            "risk_level": "low/medium/high/critical",
            "recommendations": ["specific actions for {agent_type}"],
            "additional_data_needed": ["what else to investigate"],
            "priority_level": "low/medium/high/urgent"
        }}
        """
        
        try:
            response = self.openai_client.get_chat_completion(prompt)
            analysis = json.loads(response.get('response', '{}'))
            return analysis
        except Exception as e:
            return {
                'summary': f'Analysis failed: {str(e)}',
                'confidence': 0.3,
                'risk_level': 'medium',
                'recommendations': ['Proceed with caution', 'Manual review recommended'],
                'additional_data_needed': ['More specific information'],
                'priority_level': 'medium'
            }

class DynamicSearchAgent:
    """
    An agent that can perform dynamic searches and provide context to other agents
    """
    
    def __init__(self):
        self.search_integration = SearchIntegration()
        self.agent_id = "SEARCH_AGENT_001"
        self.name = "Dynamic Search Agent"
    
    def search_and_analyze(self, query: str, context: Dict, requesting_agent: str = None) -> Dict[str, Any]:
        """
        Perform search and provide analysis for other agents
        """
        
        # Determine search strategy based on requesting agent
        if requesting_agent:
            search_result = self.search_integration.search_for_agent_context(
                requesting_agent, query, context
            )
        else:
            search_result = self.search_integration.search_for_context(query)
        
        # Add metadata
        search_result.update({
            'search_agent_id': self.agent_id,
            'requesting_agent': requesting_agent,
            'search_timestamp': datetime.now().isoformat()
        })
        
        return search_result
    
    def get_real_time_context(self, task: str, location: str = None) -> Dict[str, Any]:
        """
        Get comprehensive real-time context for a task
        """
        
        context_searches = []
        
        # Location-based searches
        if location:
            location_context = self.search_integration.search_for_context(
                f"current conditions {location}", 'news'
            )
            context_searches.append(('location', location_context))
        
        # Task-specific searches
        task_context = self.search_integration.search_for_context(task, 'general')
        context_searches.append(('task', task_context))
        
        # Industry context
        industry_context = self.search_integration.search_for_context(
            f"insurance industry {task}", 'technical'
        )
        context_searches.append(('industry', industry_context))
        
        return {
            'task': task,
            'location': location,
            'context_searches': context_searches,
            'timestamp': datetime.now().isoformat(),
            'total_sources': sum(len(search[1].get('results', [])) for search in context_searches)
        }

