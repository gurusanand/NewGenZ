"""
ESG Framework Integration for Climate Risk Modeling
Integrates Environmental, Social, and Governance factors for comprehensive risk assessment
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import streamlit as st
from typing import Dict, List, Any, Tuple
from datetime import datetime, timedelta
import numpy as np

class ESGClimateRiskFramework:
    """ESG framework for climate risk modeling in insurance"""
    
    def __init__(self):
        self.esg_weights = {
            'environmental': 0.5,  # Climate and environmental factors
            'social': 0.3,         # Social impact and community factors
            'governance': 0.2      # Regulatory and governance factors
        }
        
        self.climate_risk_categories = {
            'physical_risks': ['extreme_weather', 'sea_level_rise', 'temperature_change', 'precipitation_change'],
            'transition_risks': ['policy_changes', 'technology_shifts', 'market_changes', 'reputation_risks'],
            'liability_risks': ['litigation', 'regulatory_compliance', 'stranded_assets']
        }
        
        self.esg_metrics = {
            'environmental': {
                'carbon_footprint': 'CO2 emissions and carbon intensity',
                'climate_adaptation': 'Adaptation measures and resilience',
                'biodiversity_impact': 'Impact on ecosystems and biodiversity',
                'resource_efficiency': 'Water and energy efficiency'
            },
            'social': {
                'community_resilience': 'Community preparedness and social cohesion',
                'vulnerable_populations': 'Impact on vulnerable groups',
                'health_safety': 'Public health and safety considerations',
                'economic_inequality': 'Economic disparities and access'
            },
            'governance': {
                'climate_governance': 'Climate risk management frameworks',
                'regulatory_compliance': 'Adherence to environmental regulations',
                'transparency': 'ESG reporting and disclosure quality',
                'stakeholder_engagement': 'Engagement with stakeholders on climate issues'
            }
        }
    
    def calculate_esg_climate_risk_score(self, location_data: Dict, weather_data: Dict, economic_data: Dict) -> Dict[str, Any]:
        """Calculate comprehensive ESG climate risk score"""
        
        # Environmental risk assessment
        environmental_score = self._assess_environmental_risks(location_data, weather_data)
        
        # Social risk assessment
        social_score = self._assess_social_risks(location_data, economic_data)
        
        # Governance risk assessment
        governance_score = self._assess_governance_risks(location_data)
        
        # Calculate weighted overall score
        overall_score = (
            environmental_score['score'] * self.esg_weights['environmental'] +
            social_score['score'] * self.esg_weights['social'] +
            governance_score['score'] * self.esg_weights['governance']
        )
        
        return {
            'overall_esg_risk_score': overall_score,
            'risk_category': self._categorize_risk(overall_score),
            'environmental': environmental_score,
            'social': social_score,
            'governance': governance_score,
            'climate_scenarios': self._generate_climate_scenarios(location_data, weather_data),
            'recommendations': self._generate_esg_recommendations(environmental_score, social_score, governance_score),
            'compliance_status': self._assess_regulatory_compliance(location_data)
        }
    
    def _assess_environmental_risks(self, location_data: Dict, weather_data: Dict) -> Dict[str, Any]:
        """Assess environmental climate risks"""
        
        # Physical climate risks
        extreme_weather_risk = self._calculate_extreme_weather_risk(weather_data)
        temperature_risk = self._calculate_temperature_risk(weather_data)
        precipitation_risk = self._calculate_precipitation_risk(weather_data)
        
        # Transition risks
        carbon_transition_risk = self._calculate_carbon_transition_risk(location_data)
        
        environmental_factors = {
            'extreme_weather': extreme_weather_risk,
            'temperature_change': temperature_risk,
            'precipitation_change': precipitation_risk,
            'carbon_transition': carbon_transition_risk
        }
        
        # Calculate weighted environmental score
        environmental_score = np.mean(list(environmental_factors.values()))
        
        return {
            'score': environmental_score,
            'factors': environmental_factors,
            'key_risks': self._identify_key_environmental_risks(environmental_factors),
            'adaptation_measures': self._suggest_adaptation_measures(environmental_factors)
        }
    
    def _assess_social_risks(self, location_data: Dict, economic_data: Dict) -> Dict[str, Any]:
        """Assess social climate risks"""
        
        # Community vulnerability
        community_vulnerability = self._calculate_community_vulnerability(location_data)
        
        # Economic inequality impact
        inequality_impact = self._calculate_inequality_impact(economic_data)
        
        # Health and safety risks
        health_safety_risk = self._calculate_health_safety_risk(location_data)
        
        social_factors = {
            'community_vulnerability': community_vulnerability,
            'economic_inequality': inequality_impact,
            'health_safety': health_safety_risk
        }
        
        social_score = np.mean(list(social_factors.values()))
        
        return {
            'score': social_score,
            'factors': social_factors,
            'vulnerable_groups': self._identify_vulnerable_groups(location_data),
            'social_interventions': self._suggest_social_interventions(social_factors)
        }
    
    def _assess_governance_risks(self, location_data: Dict) -> Dict[str, Any]:
        """Assess governance climate risks"""
        
        # Regulatory framework strength
        regulatory_strength = self._assess_regulatory_framework(location_data)
        
        # Climate governance quality
        governance_quality = self._assess_climate_governance(location_data)
        
        # Transparency and reporting
        transparency_score = self._assess_transparency(location_data)
        
        governance_factors = {
            'regulatory_framework': regulatory_strength,
            'climate_governance': governance_quality,
            'transparency': transparency_score
        }
        
        governance_score = np.mean(list(governance_factors.values()))
        
        return {
            'score': governance_score,
            'factors': governance_factors,
            'regulatory_gaps': self._identify_regulatory_gaps(governance_factors),
            'governance_improvements': self._suggest_governance_improvements(governance_factors)
        }
    
    def _calculate_extreme_weather_risk(self, weather_data: Dict) -> float:
        """Calculate extreme weather risk score"""
        base_risk = weather_data.get('risk_assessment', {}).get('overall_risk_score', 0.3)
        
        # Adjust for climate change projections
        climate_multiplier = 1.2  # 20% increase due to climate change
        
        return min(base_risk * climate_multiplier, 1.0)
    
    def _calculate_temperature_risk(self, weather_data: Dict) -> float:
        """Calculate temperature change risk"""
        current_temp = weather_data.get('current_conditions', {}).get('temperature', 70)
        
        # Risk increases with extreme temperatures
        if current_temp > 90 or current_temp < 32:
            return 0.7
        elif current_temp > 85 or current_temp < 40:
            return 0.5
        else:
            return 0.3
    
    def _calculate_precipitation_risk(self, weather_data: Dict) -> float:
        """Calculate precipitation change risk"""
        precipitation = weather_data.get('current_conditions', {}).get('precipitation', 0)
        
        # Risk based on precipitation levels
        if precipitation > 2.0:
            return 0.8
        elif precipitation > 1.0:
            return 0.6
        elif precipitation > 0.5:
            return 0.4
        else:
            return 0.2
    
    def _calculate_carbon_transition_risk(self, location_data: Dict) -> float:
        """Calculate carbon transition risk"""
        # Simulated based on location's carbon intensity
        location = location_data.get('location', 'Unknown')
        
        # High carbon regions face higher transition risks
        high_carbon_regions = ['Texas', 'West Virginia', 'Wyoming']
        if any(region in location for region in high_carbon_regions):
            return 0.7
        else:
            return 0.4
    
    def _calculate_community_vulnerability(self, location_data: Dict) -> float:
        """Calculate community vulnerability score"""
        # Simulated vulnerability based on location characteristics
        location = location_data.get('location', 'Unknown')
        
        # Coastal areas and urban centers may have higher vulnerability
        if 'coast' in location.lower() or 'beach' in location.lower():
            return 0.6
        elif 'city' in location.lower() or 'urban' in location.lower():
            return 0.5
        else:
            return 0.3
    
    def _calculate_inequality_impact(self, economic_data: Dict) -> float:
        """Calculate economic inequality impact"""
        economic_health = economic_data.get('insurance_impact', {}).get('economic_health', 'moderate')
        
        if economic_health == 'weak':
            return 0.7
        elif economic_health == 'moderate':
            return 0.5
        else:
            return 0.3
    
    def _calculate_health_safety_risk(self, location_data: Dict) -> float:
        """Calculate health and safety risk"""
        # Simulated based on location and population density
        return 0.4  # Base health safety risk
    
    def _assess_regulatory_framework(self, location_data: Dict) -> float:
        """Assess regulatory framework strength"""
        # Simulated regulatory strength score
        return 0.7  # Moderate regulatory framework
    
    def _assess_climate_governance(self, location_data: Dict) -> float:
        """Assess climate governance quality"""
        # Simulated governance quality score
        return 0.6  # Moderate climate governance
    
    def _assess_transparency(self, location_data: Dict) -> float:
        """Assess transparency and reporting quality"""
        # Simulated transparency score
        return 0.8  # Good transparency
    
    def _categorize_risk(self, risk_score: float) -> str:
        """Categorize overall ESG climate risk"""
        if risk_score >= 0.7:
            return "HIGH"
        elif risk_score >= 0.5:
            return "MEDIUM"
        elif risk_score >= 0.3:
            return "LOW"
        else:
            return "VERY LOW"
    
    def _generate_climate_scenarios(self, location_data: Dict, weather_data: Dict) -> Dict[str, Any]:
        """Generate climate scenarios for risk modeling"""
        
        scenarios = {
            'current': {
                'description': 'Current climate conditions',
                'risk_multiplier': 1.0,
                'timeframe': 'Present'
            },
            'rcp45': {
                'description': 'Moderate climate change scenario (RCP 4.5)',
                'risk_multiplier': 1.3,
                'timeframe': '2030-2050'
            },
            'rcp85': {
                'description': 'High climate change scenario (RCP 8.5)',
                'risk_multiplier': 1.8,
                'timeframe': '2050-2100'
            }
        }
        
        return scenarios
    
    def _generate_esg_recommendations(self, env_score: Dict, social_score: Dict, gov_score: Dict) -> List[str]:
        """Generate ESG-based recommendations"""
        
        recommendations = []
        
        # Environmental recommendations
        if env_score['score'] > 0.6:
            recommendations.extend([
                "Implement climate adaptation measures",
                "Invest in renewable energy infrastructure",
                "Develop flood and extreme weather resilience plans"
            ])
        
        # Social recommendations
        if social_score['score'] > 0.6:
            recommendations.extend([
                "Strengthen community emergency preparedness",
                "Support vulnerable population protection programs",
                "Invest in social infrastructure resilience"
            ])
        
        # Governance recommendations
        if gov_score['score'] > 0.6:
            recommendations.extend([
                "Enhance climate risk governance frameworks",
                "Improve ESG reporting and transparency",
                "Strengthen regulatory compliance programs"
            ])
        
        return recommendations
    
    def _assess_regulatory_compliance(self, location_data: Dict) -> Dict[str, Any]:
        """Assess regulatory compliance status"""
        
        return {
            'tcfd_compliance': 'Partial',  # Task Force on Climate-related Financial Disclosures
            'eu_taxonomy': 'Not Applicable',
            'sec_climate_disclosure': 'In Progress',
            'local_regulations': 'Compliant',
            'overall_status': 'Good'
        }
    
    def _identify_key_environmental_risks(self, factors: Dict) -> List[str]:
        """Identify key environmental risks"""
        key_risks = []
        
        for factor, score in factors.items():
            if score > 0.6:
                key_risks.append(factor.replace('_', ' ').title())
        
        return key_risks if key_risks else ['Low environmental risk exposure']
    
    def _suggest_adaptation_measures(self, factors: Dict) -> List[str]:
        """Suggest climate adaptation measures"""
        
        measures = [
            "Implement early warning systems",
            "Develop climate-resilient infrastructure",
            "Create emergency response protocols",
            "Invest in natural disaster preparedness"
        ]
        
        return measures
    
    def _identify_vulnerable_groups(self, location_data: Dict) -> List[str]:
        """Identify vulnerable population groups"""
        
        return [
            "Elderly populations",
            "Low-income communities",
            "Coastal residents",
            "Outdoor workers"
        ]
    
    def _suggest_social_interventions(self, factors: Dict) -> List[str]:
        """Suggest social interventions"""
        
        return [
            "Community resilience building programs",
            "Vulnerable population support systems",
            "Public health preparedness initiatives",
            "Economic support for climate adaptation"
        ]
    
    def _identify_regulatory_gaps(self, factors: Dict) -> List[str]:
        """Identify regulatory gaps"""
        
        gaps = []
        
        if factors['regulatory_framework'] < 0.7:
            gaps.append("Climate risk disclosure requirements")
        
        if factors['climate_governance'] < 0.7:
            gaps.append("Climate governance standards")
        
        return gaps if gaps else ['No significant regulatory gaps identified']
    
    def _suggest_governance_improvements(self, factors: Dict) -> List[str]:
        """Suggest governance improvements"""
        
        return [
            "Establish climate risk committees",
            "Implement ESG reporting frameworks",
            "Develop climate scenario planning",
            "Enhance stakeholder engagement"
        ]

class ESGDashboard:
    """Dashboard for ESG climate risk visualization"""
    
    def __init__(self):
        self.esg_framework = ESGClimateRiskFramework()
    
    def display_esg_climate_dashboard(self, location_data: Dict, weather_data: Dict, economic_data: Dict):
        """Display comprehensive ESG climate risk dashboard"""
        
        st.subheader("🌍 ESG Climate Risk Assessment")
        st.markdown("*Environmental, Social, and Governance climate risk analysis*")
        
        # Calculate ESG risk scores
        esg_results = self.esg_framework.calculate_esg_climate_risk_score(
            location_data, weather_data, economic_data
        )
        
        # Overall ESG risk summary
        self._display_esg_summary(esg_results)
        
        # Detailed ESG analysis
        col1, col2 = st.columns(2)
        
        with col1:
            self._display_esg_breakdown(esg_results)
        
        with col2:
            self._display_climate_scenarios(esg_results['climate_scenarios'])
        
        # ESG recommendations
        self._display_esg_recommendations(esg_results)
        
        # Regulatory compliance
        self._display_compliance_status(esg_results['compliance_status'])
    
    def _display_esg_summary(self, esg_results: Dict):
        """Display ESG risk summary"""
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            overall_score = esg_results['overall_esg_risk_score']
            risk_category = esg_results['risk_category']
            
            st.metric(
                "Overall ESG Risk",
                f"{overall_score:.2f}",
                delta=f"{risk_category} Risk",
                delta_color="inverse"
            )
        
        with col2:
            env_score = esg_results['environmental']['score']
            st.metric(
                "Environmental",
                f"{env_score:.2f}",
                delta="Climate Impact"
            )
        
        with col3:
            social_score = esg_results['social']['score']
            st.metric(
                "Social",
                f"{social_score:.2f}",
                delta="Community Impact"
            )
        
        with col4:
            gov_score = esg_results['governance']['score']
            st.metric(
                "Governance",
                f"{gov_score:.2f}",
                delta="Regulatory Framework"
            )
    
    def _display_esg_breakdown(self, esg_results: Dict):
        """Display detailed ESG breakdown"""
        
        st.markdown("### 📊 ESG Risk Breakdown")
        
        # Create ESG breakdown chart
        esg_data = {
            'ESG Factor': ['Environmental', 'Social', 'Governance'],
            'Risk Score': [
                esg_results['environmental']['score'],
                esg_results['social']['score'],
                esg_results['governance']['score']
            ],
            'Weight': [0.5, 0.3, 0.2]
        }
        
        fig = px.bar(
            esg_data,
            x='ESG Factor',
            y='Risk Score',
            color='Risk Score',
            color_continuous_scale='RdYlGn_r',
            title="ESG Risk Scores by Factor"
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        # Environmental factors detail
        with st.expander("🌱 Environmental Factors", expanded=False):
            env_factors = esg_results['environmental']['factors']
            for factor, score in env_factors.items():
                st.progress(score, text=f"{factor.replace('_', ' ').title()}: {score:.2f}")
        
        # Social factors detail
        with st.expander("👥 Social Factors", expanded=False):
            social_factors = esg_results['social']['factors']
            for factor, score in social_factors.items():
                st.progress(score, text=f"{factor.replace('_', ' ').title()}: {score:.2f}")
        
        # Governance factors detail
        with st.expander("⚖️ Governance Factors", expanded=False):
            gov_factors = esg_results['governance']['factors']
            for factor, score in gov_factors.items():
                st.progress(score, text=f"{factor.replace('_', ' ').title()}: {score:.2f}")
    
    def _display_climate_scenarios(self, scenarios: Dict):
        """Display climate scenarios"""
        
        st.markdown("### 🌡️ Climate Scenarios")
        
        scenario_data = []
        for scenario_name, scenario_info in scenarios.items():
            scenario_data.append({
                'Scenario': scenario_name.upper(),
                'Risk Multiplier': scenario_info['risk_multiplier'],
                'Timeframe': scenario_info['timeframe'],
                'Description': scenario_info['description']
            })
        
        df = pd.DataFrame(scenario_data)
        st.dataframe(df, use_container_width=True)
        
        # Scenario impact visualization
        fig = px.bar(
            df,
            x='Scenario',
            y='Risk Multiplier',
            color='Risk Multiplier',
            color_continuous_scale='Reds',
            title="Climate Scenario Risk Multipliers"
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    def _display_esg_recommendations(self, esg_results: Dict):
        """Display ESG recommendations"""
        
        st.markdown("### 💡 ESG Recommendations")
        
        recommendations = esg_results['recommendations']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🎯 Priority Actions")
            for i, rec in enumerate(recommendations[:3], 1):
                st.markdown(f"{i}. {rec}")
        
        with col2:
            st.markdown("#### 📈 Long-term Strategies")
            for i, rec in enumerate(recommendations[3:], 4):
                st.markdown(f"{i}. {rec}")
    
    def _display_compliance_status(self, compliance: Dict):
        """Display regulatory compliance status"""
        
        with st.expander("📋 Regulatory Compliance Status", expanded=False):
            st.markdown("### Compliance Framework Status")
            
            compliance_data = []
            for framework, status in compliance.items():
                if framework != 'overall_status':
                    compliance_data.append({
                        'Framework': framework.replace('_', ' ').upper(),
                        'Status': status
                    })
            
            df = pd.DataFrame(compliance_data)
            st.dataframe(df, use_container_width=True)
            
            overall_status = compliance.get('overall_status', 'Unknown')
            st.success(f"Overall Compliance Status: {overall_status}")

def create_esg_demo():
    """Create ESG climate risk demo"""
    
    # Sample data
    sample_location = {
        'location': 'Miami, FL',
        'coordinates': {'lat': 25.7617, 'lon': -80.1918},
        'population': 470000,
        'coastal': True
    }
    
    sample_weather = {
        'current_conditions': {
            'temperature': 85,
            'humidity': 78,
            'precipitation': 0.5
        },
        'risk_assessment': {
            'overall_risk_score': 0.6,
            'flood_risk': 'high',
            'hurricane_risk': 'high'
        }
    }
    
    sample_economic = {
        'insurance_impact': {
            'economic_health': 'moderate',
            'growth_rate': 2.1
        }
    }
    
    # Create and display dashboard
    esg_dashboard = ESGDashboard()
    esg_dashboard.display_esg_climate_dashboard(sample_location, sample_weather, sample_economic)
    
    return esg_dashboard

