from app_merged import *

def process_enhanced_claim(self, claim_type, location, description, date, damage, policy):
    """Process claim with enhanced real-time data integration"""
    st.subheader("⚡ Real-Time Claims Processing")
    # Create progress indicators
    progress_bar = st.progress(0)
    status_text = st.empty()
    # Step 1: Initialize Enhanced Claims Agent
    status_text.text("🤖 Initializing Enhanced Claims Specialist Agent...")
    progress_bar.progress(10)
    time.sleep(1)
    claims_agent = st.session_state.claims_agent
    # Step 2: Gather Real-Time Data
    status_text.text("📡 Gathering Real-Time Weather and Claims Data...")
    progress_bar.progress(30)
    # Display real-time data gathering
    with st.expander("🌐 Real-Time Data Sources", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Weather Data API:**")
            weather_data = st.session_state.api_client.get_real_time_data('weather', location=location)
            if weather_data.success:
                st.success("✅ Weather data retrieved successfully")
                weather_info = weather_data.data.get('current_conditions', {})
                st.json({
                    'temperature': weather_info.get('temperature', 'N/A'),
                    'precipitation': weather_info.get('precipitation', 'N/A'),
                    'wind_speed': weather_info.get('wind_speed', 'N/A'),
                    'risk_score': weather_data.data.get('risk_assessment', {}).get('overall_risk_score', 'N/A')
                })
            else:
                st.error("❌ Weather data unavailable - using fallback")
        with col2:
            st.markdown("**Claims Data API:**")
            claims_data = st.session_state.api_client.get_real_time_data(
                'claims_data', 
                claim_type=claim_type.lower().replace(' ', '_'),
                location=location
            )
            if claims_data.success:
                st.success("✅ Historical claims data retrieved")
                historical_info = claims_data.data.get('historical_weather', {})
                st.json({
                    'similar_claims': historical_info.get('similar_claims_count', 'N/A'),
                    'claims_correlation': historical_info.get('claims_correlation', {}),
                    'pattern_analysis': historical_info.get('pattern_analysis', {})
                })
            else:
                st.error("❌ Claims data unavailable - using fallback")
    time.sleep(2)
    # Step 3: Enhanced Processing
    status_text.text("🧠 Processing with Enhanced AI Analysis...")
    progress_bar.progress(60)
    # Prepare context for enhanced processing
    context = {
        'location': location,
        'incident_location': location,
        'claim_date': date.strftime('%Y-%m-%d'),
        'estimated_damage': damage,
        'policy_number': policy,
        'deductible': 500,
        'policy_limit': 50000
    }
    # Enhanced reasoning and action
    task = f"Process {claim_type.lower()} claim: {description}"
    reasoning = claims_agent.reason(task, context)
    result = claims_agent.act(reasoning, task, context)
    time.sleep(2)
    # Step 4: Display Enhanced Results
    status_text.text("✅ Enhanced Processing Complete!")
    progress_bar.progress(100)
    st.success("🎉 Claim processed successfully with real-time data integration!")
    # Display comprehensive results
    self.display_enhanced_claim_results(result, weather_data, claims_data)

def display_enhanced_claim_results(self, result, weather_data, claims_data):
    """Display enhanced claim processing results"""
    st.subheader("📋 Enhanced Claim Processing Results")
    # Claim summary
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🆔 Claim Information")
        st.markdown(f"**Claim ID:** {result['claim_id']}")
        st.markdown(f"**Processing Time:** {result['processing_time']} minutes")
        st.markdown(f"**Confidence Score:** {result['confidence_score']:.2%}")
        # Approval status with enhanced details
        approval = result['approval_status']
        status_color = {
            'auto_approved': '🟢',
            'pre_approved': '🟡',
            'manual_review_required': '🔴'
        }.get(approval['status'], '⚪')
        st.markdown(f"**Status:** {status_color} {approval['status'].replace('_', ' ').title()}")
        st.markdown(f"**Review Required:** {'Yes' if approval['review_required'] else 'No'}")
        st.markdown(f"**Approval Authority:** {approval['approval_authority'].replace('_', ' ').title()}")
    with col2:
        st.markdown("### 💰 Payout Calculation")
        payout = result['payout_calculation']
        st.metric("Base Amount", f"${payout['base_amount']:,}")
        if payout.get('weather_adjustment', 0) > 0:
            st.metric("Weather Adjustment", f"+${payout['weather_adjustment']:,.0f}")
        st.metric("Final Payout", f"${payout['final_payout']:,}")
        # Weather factor indicator
        if payout.get('weather_factor_applied'):
            st.info("🌦️ Weather factor applied to payout calculation")
    # Real-time data integration summary
    st.markdown("### 🌐 Real-Time Data Integration")
    integration_data = result['real_time_data_integration']
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Weather Correlation:**")
        weather_corr = integration_data['weather_correlation']
        st.markdown(f"- Correlation: {weather_corr['correlation']}")
        st.markdown(f"- Risk Score: {weather_corr['risk_score']:.2f}")
        st.markdown(f"- Confidence: {weather_corr['confidence']:.2%}")
    with col2:
        st.markdown("**Historical Analysis:**")
        historical = integration_data['historical_analysis']
        if historical:
            st.markdown(f"- Pattern Match: {historical.get('pattern_match', 'N/A')}")
            st.markdown(f"- Similar Claims: {historical.get('similar_claims', 'N/A')}")
        else:
            st.markdown("- No historical data available")
    with col3:
        st.markdown("**API Data Quality:**")
        api_quality = integration_data['api_data_quality']
        st.markdown(f"- Overall Quality: {api_quality['overall_quality']}")
        st.markdown(f"- Completeness: {api_quality['data_completeness']:.1%}")
    # Damage assessment with real-time factors
    st.markdown("### 🔍 Enhanced Damage Assessment")
    damage_assessment = result['damage_assessment']
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Assessment Details:**")
        st.markdown(f"- Damage Level: {damage_assessment['damage_level'].replace('_', ' ').title()}")
        st.markdown(f"- Repair Complexity: {damage_assessment['repair_complexity']}")
        st.markdown(f"- Estimated Repair Time: {damage_assessment['estimated_repair_time']}")
        st.markdown(f"- AI Confidence: {damage_assessment['ai_confidence']:.2%}")
    with col2:
        st.markdown("**Weather Contribution:**")
        weather_contrib = damage_assessment['weather_contribution']
        st.markdown(f"- Contribution Level: {weather_contrib['contribution_level']}")
        st.markdown(f"- Risk Score: {weather_contrib['risk_score']:.2f}")
        st.markdown(f"- Specific Factors: {', '.join(weather_contrib['specific_factors'])}")
    # Next steps with real-time considerations
    st.markdown("### 📋 Next Steps")
    next_steps = result['next_steps']
    for i, step in enumerate(next_steps, 1):
        st.markdown(f"{i}. {step.replace('_', ' ').title()}")
    # Real-time monitoring alert
    if weather_data.success:
        weather_risk = weather_data.data.get('risk_assessment', {}).get('overall_risk_score', 0)
        if weather_risk > 0.6:
            st.warning("⚠️ High weather risk detected. Ongoing monitoring recommended.")

def display_enhanced_risk_analysis(self):
    """Display enhanced risk analysis with comprehensive real-time data"""
    st.header("📊 Enhanced Risk Analysis")
    st.markdown("*Powered by Multi-Source Real-Time Data Integration*")
    # Risk analysis input form
    with st.form("enhanced_risk_form"):
        st.subheader("🎯 Risk Assessment Parameters")
        col1, col2 = st.columns(2)
        with col1:
            asset_type = st.selectbox(
                "Asset Type",
                ["Property", "Auto", "Business", "Marine", "Aviation"]
            )
            location = st.text_input("Location", value="New York, NY")
            risk_type = st.selectbox(
                "Primary Risk Focus",
                ["Comprehensive", "Weather-Related", "Economic", "Security", "Natural Disasters"]
            )
        with col2:
            assessment_period = st.selectbox(
                "Assessment Period",
                ["30 days", "6 months", "1 year", "5 years"]
            )
            coverage_amount = st.number_input("Coverage Amount ($)", min_value=0, value=100000)
            include_predictive = st.checkbox("Include Predictive Analytics", value=True)
        submitted = st.form_submit_button("🚀 Perform Enhanced Risk Analysis")
    if submitted:
        self.perform_enhanced_risk_analysis(asset_type, location, risk_type, 
                                     assessment_period, coverage_amount, include_predictive)

def perform_enhanced_risk_analysis(self, asset_type, location, risk_type, period, coverage, predictive):
    """Perform enhanced risk analysis with comprehensive real-time data"""
    st.subheader("⚡ Real-Time Risk Analysis")
    # Create progress indicators
    progress_bar = st.progress(0)
    status_text = st.empty()
    # Step 1: Initialize Enhanced Risk Analyst
    status_text.text("🤖 Initializing Enhanced Risk Analyst Agent...")
    progress_bar.progress(10)
    time.sleep(1)
    risk_agent = st.session_state.risk_agent
    # Step 2: Comprehensive Data Gathering
    status_text.text("📡 Gathering Comprehensive Real-Time Data...")
    progress_bar.progress(30)
    # Display comprehensive data gathering
    with st.expander("🌐 Multi-Source Data Integration", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Weather Data:**")
            weather_data = st.session_state.api_client.get_real_time_data('weather', location=location)
            if weather_data.success:
                st.success("✅ Current weather data")
                weather_risk = weather_data.data.get('risk_assessment', {}).get('overall_risk_score', 0)
                st.metric("Weather Risk", f"{weather_risk:.2%}")
            else:
                st.error("❌ Weather data unavailable")
            # Forecast data
            forecast_data = st.session_state.api_client.get_real_time_data('weather_forecast', location=location, days=14)
            if forecast_data.success:
                st.success("✅ 14-day forecast data")
                extreme_prob = forecast_data.data.get('risk_analysis', {}).get('extreme_weather_probability', 0)
                st.metric("Extreme Weather Prob", f"{extreme_prob:.2%}")
            else:
                st.error("❌ Forecast data unavailable")
        with col2:
            st.markdown("**Economic Data:**")
            economic_data = st.session_state.api_client.get_real_time_data('economic', country='USA')
            if economic_data.success:
                st.success("✅ Economic indicators")
                economic_health = economic_data.data.get('insurance_impact', {}).get('economic_health', 'moderate')
                growth_rate = economic_data.data.get('trend_analysis', {}).get('growth_rate', 0)
                st.metric("Economic Health", economic_health.title())
                st.metric("Growth Rate", f"{growth_rate:.1f}%")
            else:
                st.error("❌ Economic data unavailable")
        with col3:
            st.markdown("**Risk Assessment Data:**")
            risk_data = st.session_state.api_client.get_real_time_data(
                'risk_assessment', 
                location=location, 
                asset_type=asset_type.lower()
            )
            if risk_data.success:
                st.success("✅ Historical risk data")
                historical_incidents = risk_data.data.get('historical_incidents', 0)
                st.metric("Historical Incidents", historical_incidents)
            else:
                st.error("❌ Risk data unavailable")
    time.sleep(2)
    # Step 3: Enhanced Analysis Processing
    status_text.text("🧠 Performing Enhanced Multi-Factor Analysis...")
    progress_bar.progress(70)
    # Prepare context for enhanced analysis
    context = {
        'location': location,
        'property_location': location,
        'asset_type': asset_type.lower(),
        'coverage_amount': coverage,
        'assessment_period': period,
        'include_predictive': predictive
    }
    # Enhanced reasoning and action
    task = f"Perform comprehensive {risk_type.lower()} risk analysis for {asset_type.lower()} in {location}"
    reasoning = risk_agent.reason(task, context)
    result = risk_agent.act(reasoning, task, context)
    time.sleep(2)
    # Step 4: Display Enhanced Results
    status_text.text("✅ Enhanced Analysis Complete!")
    progress_bar.progress(100)
    st.success("🎉 Risk analysis completed with comprehensive real-time data integration!")
    # Display comprehensive results
    self.display_enhanced_risk_results(result, weather_data, forecast_data, economic_data, risk_data)

def display_enhanced_risk_results(self, result, weather_data, forecast_data, economic_data, risk_data):
    """Display enhanced risk analysis results"""
    st.subheader("📊 Enhanced Risk Analysis Results")
    # Overall risk score with real-time factors
    overall_risk = result['overall_risk_score']
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Overall Risk Score",
            f"{overall_risk['overall_score']}/10",
            delta=f"Category: {overall_risk['risk_category']}"
        )
    with col2:
        confidence_level = result['confidence_level']
        st.metric(
            "Analysis Confidence",
            f"{confidence_level:.1%}",
            delta="Multi-source data"
        )
    with col3:
        api_metrics = result['api_integration_metrics']
        st.metric(
            "Data Integration",
            f"{api_metrics['success_rate']:.1%}",
            delta=f"{api_metrics['successful_calls']}/{api_metrics['total_api_calls']} APIs"
        )
    # Risk score components breakdown
    st.markdown("### 🔍 Risk Score Components")
    score_components = overall_risk['score_components']
    # Create visualization of score components
    components_df = pd.DataFrame([
        {'Component': 'Base Risk Factor', 'Value': score_components['base_risk_factor']},
        {'Component': 'Weather Adjustment', 'Value': score_components['weather_adjustment']},
        {'Component': 'Economic Adjustment', 'Value': score_components['economic_adjustment']},
        {'Component': 'Final Adjustment', 'Value': score_components['final_adjustment_factor']}
    ])
    fig = px.bar(
        components_df, 
        x='Component', 
        y='Value',
        title="Risk Score Component Analysis",
        color='Value',
        color_continuous_scale='RdYlGn_r'
    )
    st.plotly_chart(fig, use_container_width=True)
    # Real-time data integration summary
    st.markdown("### 🌐 Real-Time Data Integration Analysis")
    integration_data = result['real_time_data_integration']
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Weather Analysis:**")
        weather_analysis = integration_data['weather_analysis']
        st.markdown(f"- Current Risk Level: {weather_analysis.get('current_risk_level', 'N/A'):.2%}")
        st.markdown(f"- Forecast Trend: {weather_analysis.get('forecast_risk_trend', 'N/A'):.2%}")
        st.markdown(f"- High Risk Days Ahead: {weather_analysis.get('high_risk_days_ahead', 'N/A')}")
        st.markdown(f"- Analysis Quality: {weather_analysis.get('analysis_quality', 'N/A').title()}")
    with col2:
        st.markdown("**Economic Analysis:**")
        economic_analysis = integration_data['economic_analysis']
        st.markdown(f"- Economic Health: {economic_analysis.get('economic_health', 'N/A').title()}")
        st.markdown(f"- Growth Trend: {economic_analysis.get('growth_trend', 'N/A').title()}")
        st.markdown(f"- Growth Rate: {economic_analysis.get('growth_rate', 'N/A'):.1f}%")
        st.markdown(f"- Insurance Outlook: {economic_analysis.get('insurance_demand_outlook', 'N/A').title()}")
    # Enhanced predictions with real-time data
    st.markdown("### 🔮 Enhanced Predictions")
    predictions = result['predictions']
    # Create tabs for different prediction timeframes
    pred_tab1, pred_tab2, pred_tab3 = st.tabs(["Short-term (30 days)", "Medium-term (6 months)", "Long-term (5 years)"])
    with pred_tab1:
        short_term = predictions['short_term']
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Probability Increase", f"{short_term['probability_increase']:.1%}")
            st.metric("Expected Events", short_term['expected_events'])
        with col2:
            st.metric("Confidence", f"{short_term['confidence']:.1%}")
            st.markdown("**Key Factors:**")
            for factor in short_term['key_factors']:
                st.markdown(f"- {factor.replace('_', ' ').title()}")
    with pred_tab2:
        medium_term = predictions['medium_term']
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Probability Change", f"{medium_term['probability_change']:+.1%}")
            st.metric("Trend Direction", medium_term['trend_direction'].title())
        with col2:
            st.metric("Confidence", f"{medium_term['confidence']:.1%}")
            st.markdown("**Influencing Factors:**")
            for factor in medium_term['influencing_factors']:
                st.markdown(f"- {factor.replace('_', ' ').title()}")
    with pred_tab3:
        long_term = predictions['long_term']
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Risk Evolution", long_term['risk_evolution'].replace('_', ' ').title())
            st.metric("Confidence", f"{long_term['confidence']:.1%}")
        with col2:
            st.markdown("**Emerging Risks:**")
            for risk in long_term['emerging_risks']:
                st.markdown(f"- {risk.replace('_', ' ').title()}")
    # Enhanced recommendations with real-time adjustments
    st.markdown("### 💡 Enhanced Recommendations")
    recommendations = result['recommendations']
    # Priority ranking with real-time factors
    st.markdown("**Priority Recommendations:**")
    priority_recs = recommendations['priority_ranking']
    for i, rec in enumerate(priority_recs[:5], 1):  # Show top 5
        priority_color = {
            'critical': '🔴',
            'high': '🟡',
            'medium': '🟠',
            'standard': '🟢'
        }.get(rec['priority'], '⚪')
        st.markdown(f"{i}. {priority_color} **{rec['recommendation'].replace('_', ' ').title()}**")
        st.markdown(f"   - Priority: {rec['priority'].title()}")
        st.markdown(f"   - Impact Score: {rec['impact_score']:.2f}")
        st.markdown(f"   - Difficulty: {rec['implementation_difficulty'].title()}")
        if rec.get('weather_urgency_factor'):
            st.markdown("   - ⚠️ Weather urgency factor applied")
    # Real-time adjustments
    real_time_adjustments = recommendations['real_time_adjustments']
    if real_time_adjustments['urgency_level'] != 'standard':
        st.warning(f"⚡ Urgency Level: {real_time_adjustments['urgency_level'].title()}")
    if real_time_adjustments['budget_considerations'] != 'standard':
        budget_color = '🟢' if real_time_adjustments['budget_considerations'] == 'expanded' else '🟡'
        st.info(f"{budget_color} Budget Considerations: {real_time_adjustments['budget_considerations'].title()}")
    # Cost-benefit analysis with real-time economic factors
    st.markdown("### 💰 Enhanced Cost-Benefit Analysis")
    cost_benefit = recommendations['cost_benefit_analysis']
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Implementation Cost", f"${cost_benefit['total_implementation_cost']:,}")
        st.metric("Annual Savings", f"${cost_benefit['annual_savings_potential']:,}")
    with col2:
        st.metric("Payback Period", f"{cost_benefit['payback_period']:.1f} years")
        st.metric("ROI", f"{cost_benefit['roi_percentage']:.1f}%")
    with col3:
        if 'risk_reduction_value' in cost_benefit:
            st.metric("Risk Reduction Value", f"${cost_benefit['risk_reduction_value']:,}")
        estimated_reduction = recommendations['estimated_risk_reduction']
        st.metric("Risk Reduction", f"{estimated_reduction:.1%}")

# From app.py - Agent Dashboard functionality
def render_agent_dashboard(self):
    """Render the agent management dashboard"""
    st.header("🤖 Agent Management Dashboard")
    
    # Agent status overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🏗️ Hierarchy Overview")
        for level, agents in st.session_state.agent_hierarchy.hierarchy_levels.items():
            st.write(f"**Level {level}:**")
            for agent in agents:
                agent_info = st.session_state.agent_hierarchy.agents[agent]
                status = "🟢 Active" if agent in st.session_state.active_agents else "⚪ Idle"
                st.write(f"  {status} {agent_info.name}")
    
    with col2:
        st.subheader("📊 Agent Performance")
        # Create mock performance data
        performance_data = {
            'Agent': [info.name for info in st.session_state.agent_hierarchy.agents.values()],
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
        for agent_type, agent_info in st.session_state.agent_hierarchy.agents.items():
            efficiency_data.append({
                'Agent': agent_info.name,
                'Cost per Task': agent_info.credit_cost,
                'Max Concurrent': agent_info.max_concurrent_tasks,
                'Efficiency Score': round(agent_info.max_concurrent_tasks / agent_info.credit_cost, 2)
            })
        
        df_efficiency = pd.DataFrame(efficiency_data)
        st.dataframe(df_efficiency, use_container_width=True)

# From app_final_enhanced.py - Dashboard Overview
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

# From app_final_enhanced.py - Model Explainability
def display_model_explainability(self):
    """Display model explainability features"""
    st.markdown("## 🔍 Model Explainability Dashboard")
    st.markdown("*Transparent AI decision-making for customer trust and regulatory compliance*")
    # Feature overview
    st.info("🎯 **Customer Transparency**: Our AI provides clear explanations of every decision, ensuring customers understand how their insurance decisions are made.")
    # Demo selection
    demo_type = st.selectbox(
        "Select Explanation Demo",
        ["Claims Processing Decision", "Risk Assessment Explanation", "Premium Calculation Breakdown"]
    )
    # Only one selectbox for this label in this context
    # Display customer explanation demo
    if demo_type == "Claims Processing Decision":
        st.markdown("### 📋 Claims Processing Explanation Demo")
        create_customer_explanation_demo()
    
    elif demo_type == "Risk Assessment Explanation":
        st.markdown("### 🎯 Risk Assessment Explanation")
        
        # Create sample risk assessment data
        risk_data = {
            'risk_score': 0.65,
            'confidence_score': 0.88,
            'data_quality_score': 0.92,
            'weather_contribution': {'risk_score': 0.4, 'contribution_level': 'high'},
            'historical_analysis': {'similar_cases': 25, 'pattern_match': 'strong'},
            'data_sources_used': ['Weather API', 'Historical Database', 'Economic Indicators']
        }
        
        explainability = ModelExplainabilityDashboard()
        explainability.display_customer_explanation('risk_assessment', risk_data)
    
    else:  # Premium Calculation
        st.markdown("### 💰 Premium Calculation Explanation")
        
        premium_data = {
            'base_premium': 1200,
            'risk_adjustments': 180,
            'confidence_score': 0.91,
            'data_quality_score': 0.89,
            'data_sources_used': ['Market Data', 'Risk Models', 'Regulatory Database']
        }
        
        explainability = ModelExplainabilityDashboard()
        explainability.display_customer_explanation('pricing', premium_data)

# From app_final_enhanced.py - ESG Climate Risk
def display_esg_climate_risk(self):
    """Display ESG climate risk features"""
    
    st.markdown("## 🌍 ESG Climate Risk Framework")
    st.markdown("*Environmental, Social, and Governance climate risk modeling for sustainable insurance*")
    
    # ESG overview
    st.info("🌱 **ESG Integration**: Our platform incorporates Environmental, Social, and Governance factors to provide comprehensive climate risk assessment aligned with sustainability goals.")
    
    # ESG demo
    st.markdown("### 📊 ESG Climate Risk Analysis")
    create_esg_demo()

# From app_final_enhanced.py - Credit Optimization
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

# From app_enhanced.py - API Status Dashboard and Credit Management
def display_api_status_dashboard(self):
    """Display real-time API status dashboard"""
    
    st.markdown("### API Connection Status")
    
    # Test API connections
    api_client = st.session_state.api_client
    
    # Weather API Status
    weather_status = api_client.get_real_time_data('weather', location='New York')
    status_class = "api-success" if weather_status.success else "api-error"
    status_text = "✅ Connected" if weather_status.success else "❌ Disconnected"
    st.markdown(f"""
    <div class="api-status {status_class}">
        <strong>Weather API:</strong> {status_text}
        <br><small>Last Updated: {datetime.now().strftime('%H:%M:%S')}</small>
    </div>
    """, unsafe_allow_html=True)
    # Economic API Status
    economic_status = api_client.get_real_time_data('economic', country='USA')
    status_class = "api-success" if economic_status.success else "api-error"
    status_text = "✅ Connected" if economic_status.success else "❌ Disconnected"
    
    st.markdown(f"""
    <div class="api-status {status_class}">
        <strong>Economic API:</strong> {status_text}
        <br><small>Last Updated: {datetime.now().strftime('%H:%M:%S')}</small>
    </div>
    """, unsafe_allow_html=True)
    
    # Claims Data API Status
    claims_status = api_client.get_real_time_data('claims_data', claim_type='auto', location='New York')
    status_class = "api-success" if claims_status.success else "api-error"
    status_text = "✅ Connected" if claims_status.success else "❌ Disconnected"
    
    st.markdown(f"""
    <div class="api-status {status_class}">
        <strong>Claims API:</strong> {status_text}
        <br><small>Last Updated: {datetime.now().strftime('%H:%M:%S')}</small>
    </div>
    """, unsafe_allow_html=True)
    
    # Overall API Health
    total_apis = 3
    successful_apis = sum([weather_status.success, economic_status.success, claims_status.success])
    health_percentage = (successful_apis / total_apis) * 100
    
    st.metric[
        {'Policy Type': 'Home Insurance', 'Active Policies': 67, 'Total Premium': '$234,500', 'Avg Premium': '$3,500'},
        {'Policy Type': 'Business Insurance', 'Active Policies': 34, 'Total Premium': '$189,600', 'Avg Premium': '$5,576'},
        {'Policy Type': 'Travel Insurance', 'Active Policies': 57, 'Total Premium': '$28,500', 'Avg Premium': '$500'}
    ]
    
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

def display_create_policy_form(self):
    """Display create new policy form"""
    
    with st.form("create_policy"):
        st.subheader("📝 Create New Policy")
        
        col1, col2 = st.columns(2)
        
        with col1:
            client_name = st.selectbox("Select Client", ["John Smith", "Sarah Johnson", "Mike Davis", "New Client"])
            policy_type = st.selectbox("Policy Type", ["Auto", "Home", "Business", "Travel", "Life"])
            coverage_amount = st.number_input("Coverage Amount ($)", min_value=1000, value=100000)
            
        with col2:
            effective_date = st.date_input("Effective Date", value=datetime.now().date())
            term_length = st.selectbox("Term Length", ["6 months", "1 year", "2 years"])
            payment_frequency = st.selectbox("Payment Frequency", ["Monthly", "Quarterly", "Semi-Annual", "Annual"])
        
        # Additional details based on policy type
        if policy_type == "Auto":
            st.markdown("**Vehicle Information:**")
            col1, col2 = st.columns(2)
            with col1:
                vehicle_year = st.number_input("Year", min_value=1990, max_value=2025, value=2020)
                vehicle_make = st.text_input("Make", value="Toyota")
            with col2:
                vehicle_model = st.text_input("Model", value="Camry")
                vin = st.text_input("VIN")
        
        submitted = st.form_submit_button("🚀 Create Policy")
        
        if submitted:
            policy_number = f"{policy_type.upper()}-{datetime.now().year}-{random.randint(1000, 9999)}"
            st.success(f"✅ Policy {policy_number} created successfully!")

def display_commission_tracking(self):
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
    
    # Payment history
    st.markdown("**Recent Commission Payments:**")
    
    payments = [
        {'Date': '2024-12-01', 'Period': 'November 2024', 'Amount': '$7,250', 'Status': 'Paid', 'Method': 'Direct Deposit'},
        {'Date': '2024-11-01', 'Period': 'October 2024', 'Amount': '$6,890', 'Status': 'Paid', 'Method': 'Direct Deposit'},
        {'Date': '2024-10-01', 'Period': 'September 2024', 'Amount': '$8,120', 'Status': 'Paid', 'Method': 'Direct Deposit'}
    ]
    
    df_payments = pd.DataFrame(payments)
    st.dataframe(df_payments, use_container_width=True)

def display_broker_api_access(self):
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
    
    # API documentation
    st.markdown("**Available Endpoints:**")
    
    endpoints = [
        {'Endpoint': '/api/v1/quotes', 'Method': 'POST', 'Description': 'Generate insurance quotes'},
        {'Endpoint': '/api/v1/policies', 'Method': 'GET/POST', 'Description': 'Manage policies'},
        {'Endpoint': '/api/v1/claims', 'Method': 'GET/POST', 'Description': 'Submit and track claims'},
        {'Endpoint': '/api/v1/clients', 'Method': 'GET/POST/PUT', 'Description': 'Manage client data'},
        {'Endpoint': '/api/v1/commissions', 'Method': 'GET', 'Description': 'Retrieve commission data'}
    ]
    
    df_endpoints = pd.DataFrame(endpoints)
    st.dataframe(df_endpoints, use_container_width=True)
    
    # API testing
    st.markdown("**Test API Endpoints:**")
    
    test_endpoint = st.selectbox("Select Endpoint", [ep['Endpoint'] for ep in endpoints])
    test_method = st.selectbox("HTTP Method", ["GET", "POST", "PUT", "DELETE"])
    
    test_payload = st.text_area(
        "Request Payload (JSON)",
        value='{\n  "client_id": "12345",\n  "policy_type": "auto",\n  "coverage_amount": 100000\n}',
        height=100
    )
    
    if st.button("🧪 Test API Call"):
        with st.spinner("Making API call..."):
            time.sleep(2)
            st.success("✅ API call successful!")
            st.json({
                "status": "success",
                "quote_id": "QT-" + str(random.randint(100000, 999999)),
                "premium": random.randint(500, 2000),
                "valid_until": (datetime.now() + timedelta(days=30)).isoformat()
            })

def display_partner_network(self):
    """Display partner network and ecosystem integrations"""
    
    st.subheader("🤝 Partner Network & Ecosystem")
    
    # Partner categories
    partner_tabs = st.tabs(["🏢 Insurance Carriers", "🔧 Technology Partners", "📊 Data Providers", "🌐 Distribution Partners"])
    
    with partner_tabs[0]:
        st.markdown("**Connected Insurance Carriers:**")
        
        carriers = [
            {'Name': 'Zurich Insurance', 'Status': 'Connected', 'Products': 'Auto, Home, Business', 'Commission': '8-12%'},
            {'Name': 'AIG', 'Status': 'Connected', 'Products': 'Commercial, Specialty', 'Commission': '10-15%'},
            {'Name': 'Travelers', 'Status': 'Pending', 'Products': 'Auto, Home', 'Commission': '7-10%'},
            {'Name': 'Liberty Mutual', 'Status': 'Available', 'Products': 'Auto, Home, Business', 'Commission': '8-11%'}
        ]
        
        for carrier in carriers:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                status_color = {"Connected": "🟢", "Pending": "🟡", "Available": "⚪"}
                st.markdown(f"{status_color[carrier['Status']]} **{carrier['Name']}**")
            
            with col2:
                st.markdown(f"Products: {carrier['Products']}")
            
            with col3:
                st.markdown(f"Commission: {carrier['Commission']}")
            
            with col4:
                if carrier['Status'] == 'Available':
                    if st.button(f"Connect", key=f"connect_{carrier['Name']}"):
                        st.success(f"Connection request sent to {carrier['Name']}")
                elif carrier['Status'] == 'Connected':
                    if st.button(f"Manage", key=f"manage_{carrier['Name']}"):
                        st.info(f"Managing {carrier['Name']} integration")
        
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
    
    with partner_tabs[3]:
        st.markdown("**Distribution Channel Partners:**")
        
        distribution = [
            {'Channel': 'Online Marketplace', 'Type': 'Digital Platform', 'Reach': '50K+ users', 'Commission': '5%'},
            {'Channel': 'Bank Partnerships', 'Type': 'Financial Institution', 'Reach': '100K+ customers', 'Commission': '3%'},
            {'Channel': 'Automotive Dealers', 'Type': 'Point of Sale', 'Reach': '25K+ transactions', 'Commission': '8%'},
            {'Channel': 'Real Estate Agents', 'Type': 'Professional Network', 'Reach': '15K+ agents', 'Commission': '6%'}
        ]
        
        df_distribution = pd.DataFrame(distribution)
        st.dataframe(df_distribution, use_container_width=True)