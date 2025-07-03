"""
OpenAPI Client for Zurich Edge AI Insurance Platform
Integrates with real APIs for dynamic data retrieval
"""

import requests
import json
import sys
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging
from dataclasses import dataclass

# Add Manus API client path
sys.path.append('/opt/.manus/.sandbox-runtime')

try:
    from data_api import ApiClient as ManusApiClient
    MANUS_API_AVAILABLE = True
except ImportError:
    MANUS_API_AVAILABLE = False
    print("Manus API client not available, using fallback implementations")

@dataclass
class ApiResponse:
    """Standard API response format"""
    success: bool
    data: Dict[str, Any]
    error: Optional[str] = None
    source: str = "unknown"
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()

class WeatherApiClient:
    """Weather API client for risk assessment and claims processing"""
    
    def __init__(self):
        # Using Open-Meteo (free, no API key required)
        self.base_url = "https://api.open-meteo.com/v1"
        self.geocoding_url = "https://geocoding-api.open-meteo.com/v1"
        
    def get_current_weather(self, location: str) -> ApiResponse:
        """Get current weather data for a location"""
        try:
            # First, get coordinates for the location
            coords = self._get_coordinates(location)
            if not coords:
                return ApiResponse(
                    success=False,
                    data={},
                    error=f"Could not find coordinates for location: {location}",
                    source="open-meteo"
                )
            
            # Get current weather
            params = {
                'latitude': coords['lat'],
                'longitude': coords['lon'],
                'current': 'temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,rain,weather_code,cloud_cover,pressure_msl,surface_pressure,wind_speed_10m,wind_direction_10m,wind_gusts_10m',
                'timezone': 'auto'
            }
            
            response = requests.get(f"{self.base_url}/forecast", params=params, timeout=10)
            response.raise_for_status()
            
            weather_data = response.json()
            
            # Process and structure the data for insurance use
            processed_data = self._process_weather_data(weather_data, location)
            
            return ApiResponse(
                success=True,
                data=processed_data,
                source="open-meteo"
            )
            
        except Exception as e:
            return ApiResponse(
                success=False,
                data={},
                error=str(e),
                source="open-meteo"
            )
    
    def get_weather_forecast(self, location: str, days: int = 7) -> ApiResponse:
        """Get weather forecast for risk prediction"""
        try:
            coords = self._get_coordinates(location)
            if not coords:
                return ApiResponse(
                    success=False,
                    data={},
                    error=f"Could not find coordinates for location: {location}",
                    source="open-meteo"
                )
            
            params = {
                'latitude': coords['lat'],
                'longitude': coords['lon'],
                'daily': 'weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,rain_sum,precipitation_probability_max,wind_speed_10m_max,wind_gusts_10m_max',
                'timezone': 'auto',
                'forecast_days': min(days, 16)  # API limit
            }
            
            response = requests.get(f"{self.base_url}/forecast", params=params, timeout=10)
            response.raise_for_status()
            
            forecast_data = response.json()
            processed_data = self._process_forecast_data(forecast_data, location)
            
            return ApiResponse(
                success=True,
                data=processed_data,
                source="open-meteo"
            )
            
        except Exception as e:
            return ApiResponse(
                success=False,
                data={},
                error=str(e),
                source="open-meteo"
            )
    
    def get_historical_weather(self, location: str, start_date: str, end_date: str) -> ApiResponse:
        """Get historical weather data for claims analysis"""
        try:
            coords = self._get_coordinates(location)
            if not coords:
                return ApiResponse(
                    success=False,
                    data={},
                    error=f"Could not find coordinates for location: {location}",
                    source="open-meteo"
                )
            
            params = {
                'latitude': coords['lat'],
                'longitude': coords['lon'],
                'start_date': start_date,
                'end_date': end_date,
                'daily': 'weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,rain_sum,wind_speed_10m_max,wind_gusts_10m_max',
                'timezone': 'auto'
            }
            
            response = requests.get(f"{self.base_url}/historical", params=params, timeout=10)
            response.raise_for_status()
            
            historical_data = response.json()
            processed_data = self._process_historical_data(historical_data, location)
            
            return ApiResponse(
                success=True,
                data=processed_data,
                source="open-meteo"
            )
            
        except Exception as e:
            return ApiResponse(
                success=False,
                data={},
                error=str(e),
                source="open-meteo"
            )
    
    def _get_coordinates(self, location: str) -> Optional[Dict[str, float]]:
        """Get coordinates for a location using geocoding"""
        try:
            params = {'name': location, 'count': 1, 'language': 'en', 'format': 'json'}
            response = requests.get(f"{self.geocoding_url}/search", params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            if data.get('results') and len(data['results']) > 0:
                result = data['results'][0]
                return {
                    'lat': result['latitude'],
                    'lon': result['longitude'],
                    'name': result['name'],
                    'country': result.get('country', ''),
                    'admin1': result.get('admin1', '')
                }
            return None
            
        except Exception as e:
            print(f"Geocoding error: {e}")
            return None
    
    def _process_weather_data(self, weather_data: Dict, location: str) -> Dict[str, Any]:
        """Process current weather data for insurance analysis"""
        current = weather_data.get('current', {})
        
        # Calculate risk factors
        risk_factors = self._calculate_weather_risks(current)
        
        return {
            'location': location,
            'coordinates': {
                'latitude': weather_data.get('latitude'),
                'longitude': weather_data.get('longitude')
            },
            'current_conditions': {
                'temperature': current.get('temperature_2m'),
                'humidity': current.get('relative_humidity_2m'),
                'precipitation': current.get('precipitation', 0),
                'rain': current.get('rain', 0),
                'wind_speed': current.get('wind_speed_10m'),
                'wind_direction': current.get('wind_direction_10m'),
                'wind_gusts': current.get('wind_gusts_10m'),
                'pressure': current.get('pressure_msl'),
                'cloud_cover': current.get('cloud_cover'),
                'weather_code': current.get('weather_code')
            },
            'risk_assessment': risk_factors,
            'insurance_implications': self._get_insurance_implications(risk_factors),
            'timestamp': current.get('time', datetime.now().isoformat())
        }
    
    def _process_forecast_data(self, forecast_data: Dict, location: str) -> Dict[str, Any]:
        """Process forecast data for risk prediction"""
        daily = forecast_data.get('daily', {})
        
        # Analyze forecast for risk patterns
        risk_analysis = self._analyze_forecast_risks(daily)
        
        return {
            'location': location,
            'forecast_period': {
                'start': daily.get('time', [])[0] if daily.get('time') else None,
                'end': daily.get('time', [])[-1] if daily.get('time') else None,
                'days': len(daily.get('time', []))
            },
            'daily_forecast': self._structure_daily_forecast(daily),
            'risk_analysis': risk_analysis,
            'recommendations': self._generate_risk_recommendations(risk_analysis),
            'timestamp': datetime.now().isoformat()
        }
    
    def _process_historical_data(self, historical_data: Dict, location: str) -> Dict[str, Any]:
        """Process historical weather data for claims analysis"""
        daily = historical_data.get('daily', {})
        
        # Analyze historical patterns
        pattern_analysis = self._analyze_historical_patterns(daily)
        
        return {
            'location': location,
            'period': {
                'start': daily.get('time', [])[0] if daily.get('time') else None,
                'end': daily.get('time', [])[-1] if daily.get('time') else None,
                'days': len(daily.get('time', []))
            },
            'historical_data': self._structure_historical_data(daily),
            'pattern_analysis': pattern_analysis,
            'claims_correlation': self._analyze_claims_correlation(pattern_analysis),
            'timestamp': datetime.now().isoformat()
        }
    
    def _calculate_weather_risks(self, current: Dict) -> Dict[str, Any]:
        """Calculate weather-related insurance risks"""
        risks = {
            'flood_risk': 'low',
            'wind_damage_risk': 'low',
            'temperature_risk': 'low',
            'overall_risk_score': 0.0
        }
        
        # Precipitation risk
        precipitation = current.get('precipitation', 0)
        if precipitation > 10:
            risks['flood_risk'] = 'high'
            risks['overall_risk_score'] += 0.3
        elif precipitation > 5:
            risks['flood_risk'] = 'medium'
            risks['overall_risk_score'] += 0.15
        
        # Wind risk
        wind_speed = current.get('wind_speed_10m', 0)
        wind_gusts = current.get('wind_gusts_10m', 0)
        if wind_speed > 25 or wind_gusts > 35:
            risks['wind_damage_risk'] = 'high'
            risks['overall_risk_score'] += 0.4
        elif wind_speed > 15 or wind_gusts > 25:
            risks['wind_damage_risk'] = 'medium'
            risks['overall_risk_score'] += 0.2
        
        # Temperature extremes
        temperature = current.get('temperature_2m', 20)
        if temperature < -10 or temperature > 40:
            risks['temperature_risk'] = 'high'
            risks['overall_risk_score'] += 0.2
        elif temperature < 0 or temperature > 35:
            risks['temperature_risk'] = 'medium'
            risks['overall_risk_score'] += 0.1
        
        risks['overall_risk_score'] = min(1.0, risks['overall_risk_score'])
        
        return risks
    
    def _get_insurance_implications(self, risk_factors: Dict) -> Dict[str, Any]:
        """Get insurance implications based on weather risks"""
        implications = {
            'premium_adjustment': 'none',
            'coverage_recommendations': [],
            'immediate_actions': [],
            'risk_mitigation': []
        }
        
        overall_risk = risk_factors.get('overall_risk_score', 0)
        
        if overall_risk > 0.7:
            implications['premium_adjustment'] = 'increase_high'
            implications['immediate_actions'].extend([
                'Issue weather alert to policyholders',
                'Prepare claims processing team',
                'Review emergency response procedures'
            ])
        elif overall_risk > 0.4:
            implications['premium_adjustment'] = 'increase_moderate'
            implications['immediate_actions'].append('Monitor weather conditions closely')
        
        # Specific risk implications
        if risk_factors.get('flood_risk') == 'high':
            implications['coverage_recommendations'].append('Flood insurance upgrade')
            implications['risk_mitigation'].append('Install flood sensors')
        
        if risk_factors.get('wind_damage_risk') == 'high':
            implications['coverage_recommendations'].append('Wind damage coverage review')
            implications['risk_mitigation'].append('Secure outdoor property')
        
        return implications
    
    def _analyze_forecast_risks(self, daily: Dict) -> Dict[str, Any]:
        """Analyze forecast data for risk patterns"""
        precipitation_sum = daily.get('precipitation_sum', [])
        wind_max = daily.get('wind_speed_10m_max', [])
        temp_max = daily.get('temperature_2m_max', [])
        temp_min = daily.get('temperature_2m_min', [])
        
        analysis = {
            'high_risk_days': 0,
            'precipitation_trend': 'stable',
            'wind_trend': 'stable',
            'temperature_trend': 'stable',
            'extreme_weather_probability': 0.0
        }
        
        # Count high-risk days
        for i in range(len(precipitation_sum)):
            risk_score = 0
            if i < len(precipitation_sum) and precipitation_sum[i] > 10:
                risk_score += 0.4
            if i < len(wind_max) and wind_max[i] > 25:
                risk_score += 0.4
            if i < len(temp_max) and (temp_max[i] > 35 or (i < len(temp_min) and temp_min[i] < 0)):
                risk_score += 0.2
            
            if risk_score > 0.5:
                analysis['high_risk_days'] += 1
        
        # Calculate trends
        if len(precipitation_sum) > 3:
            if sum(precipitation_sum[-3:]) > sum(precipitation_sum[:3]):
                analysis['precipitation_trend'] = 'increasing'
            elif sum(precipitation_sum[-3:]) < sum(precipitation_sum[:3]):
                analysis['precipitation_trend'] = 'decreasing'
        
        analysis['extreme_weather_probability'] = min(1.0, analysis['high_risk_days'] / len(precipitation_sum))
        
        return analysis
    
    def _generate_risk_recommendations(self, risk_analysis: Dict) -> List[str]:
        """Generate recommendations based on risk analysis"""
        recommendations = []
        
        high_risk_days = risk_analysis.get('high_risk_days', 0)
        extreme_prob = risk_analysis.get('extreme_weather_probability', 0)
        
        if high_risk_days > 3:
            recommendations.append('Consider temporary policy adjustments for high-risk period')
            recommendations.append('Increase claims processing capacity')
        
        if extreme_prob > 0.6:
            recommendations.append('Issue proactive customer communications')
            recommendations.append('Review emergency response procedures')
        
        if risk_analysis.get('precipitation_trend') == 'increasing':
            recommendations.append('Monitor flood risk areas closely')
            recommendations.append('Consider flood insurance promotions')
        
        return recommendations
    
    def _structure_daily_forecast(self, daily: Dict) -> List[Dict]:
        """Structure daily forecast data"""
        forecast = []
        times = daily.get('time', [])
        
        for i, date in enumerate(times):
            day_data = {
                'date': date,
                'temperature_max': daily.get('temperature_2m_max', [])[i] if i < len(daily.get('temperature_2m_max', [])) else None,
                'temperature_min': daily.get('temperature_2m_min', [])[i] if i < len(daily.get('temperature_2m_min', [])) else None,
                'precipitation': daily.get('precipitation_sum', [])[i] if i < len(daily.get('precipitation_sum', [])) else None,
                'rain': daily.get('rain_sum', [])[i] if i < len(daily.get('rain_sum', [])) else None,
                'precipitation_probability': daily.get('precipitation_probability_max', [])[i] if i < len(daily.get('precipitation_probability_max', [])) else None,
                'wind_speed_max': daily.get('wind_speed_10m_max', [])[i] if i < len(daily.get('wind_speed_10m_max', [])) else None,
                'wind_gusts_max': daily.get('wind_gusts_10m_max', [])[i] if i < len(daily.get('wind_gusts_10m_max', [])) else None,
                'weather_code': daily.get('weather_code', [])[i] if i < len(daily.get('weather_code', [])) else None
            }
            forecast.append(day_data)
        
        return forecast
    
    def _structure_historical_data(self, daily: Dict) -> List[Dict]:
        """Structure historical weather data"""
        return self._structure_daily_forecast(daily)  # Same structure
    
    def _analyze_historical_patterns(self, daily: Dict) -> Dict[str, Any]:
        """Analyze historical weather patterns"""
        precipitation_sum = daily.get('precipitation_sum', [])
        wind_max = daily.get('wind_speed_10m_max', [])
        temp_max = daily.get('temperature_2m_max', [])
        temp_min = daily.get('temperature_2m_min', [])
        
        analysis = {
            'extreme_weather_events': 0,
            'average_precipitation': sum(precipitation_sum) / len(precipitation_sum) if precipitation_sum else 0,
            'max_wind_speed': max(wind_max) if wind_max else 0,
            'temperature_range': {
                'max': max(temp_max) if temp_max else 0,
                'min': min(temp_min) if temp_min else 0
            },
            'seasonal_patterns': self._identify_seasonal_patterns(daily)
        }
        
        # Count extreme weather events
        for i in range(len(precipitation_sum)):
            if (i < len(precipitation_sum) and precipitation_sum[i] > 20) or \
               (i < len(wind_max) and wind_max[i] > 30) or \
               (i < len(temp_max) and temp_max[i] > 40) or \
               (i < len(temp_min) and temp_min[i] < -15):
                analysis['extreme_weather_events'] += 1
        
        return analysis
    
    def _identify_seasonal_patterns(self, daily: Dict) -> Dict[str, Any]:
        """Identify seasonal weather patterns"""
        # Simplified seasonal analysis
        return {
            'high_precipitation_months': ['June', 'July', 'August'],
            'high_wind_months': ['March', 'April', 'November'],
            'extreme_temperature_months': ['January', 'February', 'July', 'August']
        }
    
    def _analyze_claims_correlation(self, pattern_analysis: Dict) -> Dict[str, Any]:
        """Analyze correlation between weather patterns and insurance claims"""
        extreme_events = pattern_analysis.get('extreme_weather_events', 0)
        avg_precipitation = pattern_analysis.get('average_precipitation', 0)
        max_wind = pattern_analysis.get('max_wind_speed', 0)
        
        correlation = {
            'claims_likelihood': 'low',
            'estimated_claims_increase': 0,
            'high_risk_factors': []
        }
        
        if extreme_events > 5:
            correlation['claims_likelihood'] = 'high'
            correlation['estimated_claims_increase'] = min(50, extreme_events * 5)
            correlation['high_risk_factors'].append('frequent_extreme_weather')
        
        if avg_precipitation > 15:
            correlation['high_risk_factors'].append('high_precipitation')
            correlation['estimated_claims_increase'] += 10
        
        if max_wind > 35:
            correlation['high_risk_factors'].append('high_wind_speeds')
            correlation['estimated_claims_increase'] += 15
        
        if correlation['estimated_claims_increase'] > 30:
            correlation['claims_likelihood'] = 'high'
        elif correlation['estimated_claims_increase'] > 15:
            correlation['claims_likelihood'] = 'medium'
        
        return correlation

class FinancialApiClient:
    """Financial API client for market data and economic indicators"""
    
    def __init__(self):
        self.manus_client = ManusApiClient() if MANUS_API_AVAILABLE else None
        
    def get_stock_data(self, symbol: str) -> ApiResponse:
        """Get stock market data for insurance company analysis"""
        try:
            if self.manus_client:
                # Use Manus API Hub
                stock_data = self.manus_client.call_api('YahooFinance/get_stock_chart', query={
                    'symbol': symbol,
                    'interval': '1d',
                    'range': '1mo'
                })
                
                processed_data = self._process_stock_data(stock_data, symbol)
                
                return ApiResponse(
                    success=True,
                    data=processed_data,
                    source="yahoo_finance_via_manus"
                )
            else:
                # Fallback to mock data
                return self._get_mock_stock_data(symbol)
                
        except Exception as e:
            return ApiResponse(
                success=False,
                data={},
                error=str(e),
                source="yahoo_finance_via_manus"
            )
    
    def get_stock_insights(self, symbol: str) -> ApiResponse:
        """Get stock insights and analysis"""
        try:
            if self.manus_client:
                insights_data = self.manus_client.call_api('YahooFinance/get_stock_insights', query={
                    'symbol': symbol
                })
                
                processed_data = self._process_stock_insights(insights_data, symbol)
                
                return ApiResponse(
                    success=True,
                    data=processed_data,
                    source="yahoo_finance_via_manus"
                )
            else:
                return self._get_mock_stock_insights(symbol)
                
        except Exception as e:
            return ApiResponse(
                success=False,
                data={},
                error=str(e),
                source="yahoo_finance_via_manus"
            )
    
    def get_economic_indicators(self, country: str = "USA") -> ApiResponse:
        """Get economic indicators for risk assessment"""
        try:
            if self.manus_client:
                # Get GDP data as an example
                gdp_data = self.manus_client.call_api('DataBank/indicator_data', query={
                    'indicator': 'NY.GDP.MKTP.CD',
                    'country': 'USA' if country == "USA" else 'EUU'
                })
                
                processed_data = self._process_economic_data(gdp_data, country)
                
                return ApiResponse(
                    success=True,
                    data=processed_data,
                    source="world_bank_via_manus"
                )
            else:
                return self._get_mock_economic_data(country)
                
        except Exception as e:
            return ApiResponse(
                success=False,
                data={},
                error=str(e),
                source="world_bank_via_manus"
            )
    
    def _process_stock_data(self, stock_data: Dict, symbol: str) -> Dict[str, Any]:
        """Process stock market data for insurance analysis"""
        chart = stock_data.get('chart', {})
        result = chart.get('result', [{}])[0] if chart.get('result') else {}
        meta = result.get('meta', {})
        indicators = result.get('indicators', {})
        quote = indicators.get('quote', [{}])[0] if indicators.get('quote') else {}
        
        return {
            'symbol': symbol,
            'meta': {
                'currency': meta.get('currency'),
                'exchange': meta.get('exchangeName'),
                'current_price': meta.get('regularMarketPrice'),
                'day_high': meta.get('regularMarketDayHigh'),
                'day_low': meta.get('regularMarketDayLow'),
                'volume': meta.get('regularMarketVolume'),
                '52_week_high': meta.get('fiftyTwoWeekHigh'),
                '52_week_low': meta.get('fiftyTwoWeekLow')
            },
            'price_data': {
                'open': quote.get('open', [])[-5:] if quote.get('open') else [],
                'close': quote.get('close', [])[-5:] if quote.get('close') else [],
                'high': quote.get('high', [])[-5:] if quote.get('high') else [],
                'low': quote.get('low', [])[-5:] if quote.get('low') else [],
                'volume': quote.get('volume', [])[-5:] if quote.get('volume') else []
            },
            'insurance_relevance': self._analyze_insurance_relevance(meta, symbol),
            'timestamp': datetime.now().isoformat()
        }
    
    def _process_stock_insights(self, insights_data: Dict, symbol: str) -> Dict[str, Any]:
        """Process stock insights for insurance analysis"""
        finance = insights_data.get('finance', {})
        result = finance.get('result', {})
        
        return {
            'symbol': symbol,
            'technical_analysis': result.get('instrumentInfo', {}).get('technicalEvents', {}),
            'valuation': result.get('instrumentInfo', {}).get('valuation', {}),
            'company_snapshot': result.get('companySnapshot', {}),
            'recommendation': result.get('recommendation', {}),
            'insurance_implications': self._analyze_insurance_implications(result),
            'timestamp': datetime.now().isoformat()
        }
    
    def _process_economic_data(self, economic_data: Dict, country: str) -> Dict[str, Any]:
        """Process economic indicators for insurance risk assessment"""
        data_points = economic_data.get('data', {})
        
        # Get recent years data
        recent_years = ['2020', '2021', '2022', '2023']
        recent_data = {year: data_points.get(year) for year in recent_years if data_points.get(year)}
        
        return {
            'country': country,
            'indicator': economic_data.get('indicatorName', 'GDP'),
            'recent_data': recent_data,
            'trend_analysis': self._analyze_economic_trends(recent_data),
            'insurance_impact': self._assess_economic_insurance_impact(recent_data),
            'timestamp': datetime.now().isoformat()
        }
    
    def _analyze_insurance_relevance(self, meta: Dict, symbol: str) -> Dict[str, Any]:
        """Analyze how stock data relates to insurance business"""
        current_price = meta.get('regularMarketPrice', 0)
        day_high = meta.get('regularMarketDayHigh', 0)
        day_low = meta.get('regularMarketDayLow', 0)
        
        volatility = ((day_high - day_low) / current_price * 100) if current_price > 0 else 0
        
        return {
            'volatility_percentage': round(volatility, 2),
            'market_stability': 'stable' if volatility < 2 else 'moderate' if volatility < 5 else 'volatile',
            'investment_risk': 'low' if volatility < 3 else 'medium' if volatility < 7 else 'high',
            'insurance_sector_relevance': 'high' if 'insurance' in symbol.lower() else 'medium'
        }
    
    def _analyze_insurance_implications(self, result: Dict) -> Dict[str, Any]:
        """Analyze insurance implications from stock insights"""
        technical = result.get('instrumentInfo', {}).get('technicalEvents', {})
        company = result.get('companySnapshot', {})
        
        return {
            'market_outlook': technical.get('shortTermOutlook', {}).get('direction', 'neutral'),
            'sector_performance': company.get('sectorInfo', 'unknown'),
            'risk_assessment': 'stable',  # Simplified
            'investment_recommendation': result.get('recommendation', {}).get('rating', 'hold')
        }
    
    def _analyze_economic_trends(self, recent_data: Dict) -> Dict[str, Any]:
        """Analyze economic trends from recent data"""
        values = [v for v in recent_data.values() if v is not None]
        
        if len(values) < 2:
            return {'trend': 'insufficient_data', 'growth_rate': 0}
        
        growth_rate = ((values[-1] - values[0]) / values[0] * 100) if values[0] != 0 else 0
        
        return {
            'trend': 'growing' if growth_rate > 2 else 'declining' if growth_rate < -2 else 'stable',
            'growth_rate': round(growth_rate, 2),
            'stability': 'stable' if abs(growth_rate) < 5 else 'volatile'
        }
    
    def _assess_economic_insurance_impact(self, recent_data: Dict) -> Dict[str, Any]:
        """Assess how economic indicators impact insurance business"""
        values = [v for v in recent_data.values() if v is not None]
        
        if not values:
            return {'impact': 'unknown', 'recommendations': []}
        
        latest_value = values[-1]
        growth_rate = ((values[-1] - values[0]) / values[0] * 100) if len(values) > 1 and values[0] != 0 else 0
        
        impact = {
            'economic_health': 'strong' if growth_rate > 3 else 'weak' if growth_rate < -2 else 'moderate',
            'insurance_demand_outlook': 'increasing' if growth_rate > 2 else 'decreasing' if growth_rate < -1 else 'stable',
            'premium_pricing_impact': 'increase' if growth_rate < -3 else 'stable',
            'recommendations': []
        }
        
        if growth_rate > 5:
            impact['recommendations'].append('Consider expanding coverage options')
        elif growth_rate < -3:
            impact['recommendations'].append('Review risk assessment models')
            impact['recommendations'].append('Consider premium adjustments')
        
        return impact
    
    def _get_mock_stock_data(self, symbol: str) -> ApiResponse:
        """Fallback mock stock data when API is unavailable"""
        import random
        
        base_price = 150 + random.uniform(-20, 20)
        
        mock_data = {
            'symbol': symbol,
            'meta': {
                'currency': 'USD',
                'exchange': 'NASDAQ',
                'current_price': round(base_price, 2),
                'day_high': round(base_price * 1.02, 2),
                'day_low': round(base_price * 0.98, 2),
                'volume': random.randint(1000000, 5000000),
                '52_week_high': round(base_price * 1.3, 2),
                '52_week_low': round(base_price * 0.7, 2)
            },
            'price_data': {
                'close': [round(base_price + random.uniform(-5, 5), 2) for _ in range(5)]
            },
            'insurance_relevance': {
                'volatility_percentage': round(random.uniform(1, 4), 2),
                'market_stability': 'stable',
                'investment_risk': 'medium',
                'insurance_sector_relevance': 'medium'
            },
            'timestamp': datetime.now().isoformat()
        }
        
        return ApiResponse(
            success=True,
            data=mock_data,
            source="mock_data"
        )
    
    def _get_mock_stock_insights(self, symbol: str) -> ApiResponse:
        """Fallback mock stock insights"""
        mock_data = {
            'symbol': symbol,
            'technical_analysis': {
                'shortTermOutlook': {'direction': 'bullish', 'score': 7.5}
            },
            'valuation': {'description': 'Fairly valued'},
            'company_snapshot': {'sectorInfo': 'Financial Services'},
            'recommendation': {'rating': 'buy', 'targetPrice': 165.0},
            'insurance_implications': {
                'market_outlook': 'positive',
                'sector_performance': 'Financial Services',
                'risk_assessment': 'stable',
                'investment_recommendation': 'buy'
            },
            'timestamp': datetime.now().isoformat()
        }
        
        return ApiResponse(
            success=True,
            data=mock_data,
            source="mock_data"
        )
    
    def _get_mock_economic_data(self, country: str) -> ApiResponse:
        """Fallback mock economic data"""
        import random
        
        base_gdp = 20000000000000  # 20 trillion
        
        mock_data = {
            'country': country,
            'indicator': 'GDP (current US$)',
            'recent_data': {
                '2020': base_gdp * (1 + random.uniform(-0.05, 0.05)),
                '2021': base_gdp * (1 + random.uniform(0.02, 0.08)),
                '2022': base_gdp * (1 + random.uniform(0.01, 0.06)),
                '2023': base_gdp * (1 + random.uniform(0.01, 0.05))
            },
            'trend_analysis': {
                'trend': 'growing',
                'growth_rate': round(random.uniform(2, 4), 2),
                'stability': 'stable'
            },
            'insurance_impact': {
                'economic_health': 'strong',
                'insurance_demand_outlook': 'increasing',
                'premium_pricing_impact': 'stable',
                'recommendations': ['Consider expanding coverage options']
            },
            'timestamp': datetime.now().isoformat()
        }
        
        return ApiResponse(
            success=True,
            data=mock_data,
            source="mock_data"
        )

class InsuranceApiClient:
    """Insurance-specific API client for industry data"""
    
    def __init__(self):
        self.weather_client = WeatherApiClient()
        self.financial_client = FinancialApiClient()
    
    def get_risk_assessment_data(self, location: str, asset_type: str = "property") -> ApiResponse:
        """Get comprehensive risk assessment data"""
        try:
            # Combine weather and financial data for risk assessment
            weather_response = self.weather_client.get_current_weather(location)
            
            risk_data = {
                'location': location,
                'asset_type': asset_type,
                'weather_risks': weather_response.data if weather_response.success else {},
                'assessment_timestamp': datetime.now().isoformat(),
                'comprehensive_risk_score': self._calculate_comprehensive_risk(
                    weather_response.data if weather_response.success else {},
                    asset_type
                )
            }
            
            return ApiResponse(
                success=True,
                data=risk_data,
                source="comprehensive_assessment"
            )
            
        except Exception as e:
            return ApiResponse(
                success=False,
                data={},
                error=str(e),
                source="comprehensive_assessment"
            )
    
    def get_claims_processing_data(self, claim_type: str, location: str) -> ApiResponse:
        """Get data for claims processing"""
        try:
            # Get historical weather data for claims correlation
            end_date = datetime.now().strftime('%Y-%m-%d')
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            
            historical_response = self.weather_client.get_historical_weather(location, start_date, end_date)
            
            claims_data = {
                'claim_type': claim_type,
                'location': location,
                'historical_weather': historical_response.data if historical_response.success else {},
                'processing_recommendations': self._generate_claims_recommendations(
                    claim_type,
                    historical_response.data if historical_response.success else {}
                ),
                'timestamp': datetime.now().isoformat()
            }
            
            return ApiResponse(
                success=True,
                data=claims_data,
                source="claims_processing"
            )
            
        except Exception as e:
            return ApiResponse(
                success=False,
                data={},
                error=str(e),
                source="claims_processing"
            )
    
    def get_pricing_data(self, customer_profile: Dict) -> ApiResponse:
        """Get data for dynamic pricing"""
        try:
            location = customer_profile.get('location', 'New York')
            
            # Get current weather and economic data
            weather_response = self.weather_client.get_current_weather(location)
            economic_response = self.financial_client.get_economic_indicators()
            
            pricing_data = {
                'customer_profile': customer_profile,
                'weather_factors': weather_response.data if weather_response.success else {},
                'economic_factors': economic_response.data if economic_response.success else {},
                'pricing_recommendations': self._calculate_dynamic_pricing(
                    customer_profile,
                    weather_response.data if weather_response.success else {},
                    economic_response.data if economic_response.success else {}
                ),
                'timestamp': datetime.now().isoformat()
            }
            
            return ApiResponse(
                success=True,
                data=pricing_data,
                source="dynamic_pricing"
            )
            
        except Exception as e:
            return ApiResponse(
                success=False,
                data={},
                error=str(e),
                source="dynamic_pricing"
            )
    
    def _calculate_comprehensive_risk(self, weather_data: Dict, asset_type: str) -> Dict[str, Any]:
        """Calculate comprehensive risk score"""
        base_risk = 0.3  # Base risk score
        
        # Weather risk factors
        weather_risk = weather_data.get('risk_assessment', {}).get('overall_risk_score', 0)
        
        # Asset type multipliers
        asset_multipliers = {
            'property': 1.0,
            'auto': 0.8,
            'business': 1.2,
            'marine': 1.5
        }
        
        multiplier = asset_multipliers.get(asset_type, 1.0)
        final_risk = min(1.0, (base_risk + weather_risk) * multiplier)
        
        return {
            'overall_risk_score': round(final_risk, 3),
            'risk_category': 'low' if final_risk < 0.3 else 'medium' if final_risk < 0.7 else 'high',
            'contributing_factors': {
                'base_risk': base_risk,
                'weather_risk': weather_risk,
                'asset_type_multiplier': multiplier
            },
            'confidence_level': 0.85
        }
    
    def _generate_claims_recommendations(self, claim_type: str, historical_data: Dict) -> List[str]:
        """Generate claims processing recommendations"""
        recommendations = []
        
        claims_correlation = historical_data.get('claims_correlation', {})
        claims_likelihood = claims_correlation.get('claims_likelihood', 'low')
        
        if claims_likelihood == 'high':
            recommendations.extend([
                'Expedite claims processing due to high weather correlation',
                'Assign senior adjuster for complex assessment',
                'Consider batch processing for similar claims'
            ])
        
        if claim_type.lower() in ['flood', 'water damage']:
            recommendations.append('Verify flood insurance coverage')
            recommendations.append('Check for water damage exclusions')
        
        if claim_type.lower() in ['wind', 'storm']:
            recommendations.append('Assess wind speed data correlation')
            recommendations.append('Review structural damage patterns')
        
        return recommendations
    
    def _calculate_dynamic_pricing(self, customer_profile: Dict, weather_data: Dict, economic_data: Dict) -> Dict[str, Any]:
        """Calculate dynamic pricing recommendations"""
        base_premium = customer_profile.get('base_premium', 1000)
        
        # Weather adjustment
        weather_risk = weather_data.get('risk_assessment', {}).get('overall_risk_score', 0)
        weather_adjustment = weather_risk * 0.2  # Max 20% adjustment
        
        # Economic adjustment
        economic_trend = economic_data.get('trend_analysis', {})
        economic_growth = economic_trend.get('growth_rate', 0) if economic_trend else 0
        economic_adjustment = -economic_growth * 0.01  # Inverse relationship
        
        # Customer risk factors
        age = customer_profile.get('age', 35)
        experience = customer_profile.get('driving_experience', 10)
        claims_history = customer_profile.get('claims_count', 0)
        
        customer_adjustment = 0
        if age < 25:
            customer_adjustment += 0.15
        elif age > 65:
            customer_adjustment += 0.1
        
        if experience < 5:
            customer_adjustment += 0.1
        
        customer_adjustment += claims_history * 0.05
        
        # Calculate final premium
        total_adjustment = weather_adjustment + economic_adjustment + customer_adjustment
        adjusted_premium = base_premium * (1 + total_adjustment)
        
        return {
            'base_premium': base_premium,
            'adjustments': {
                'weather_adjustment': round(weather_adjustment * 100, 2),
                'economic_adjustment': round(economic_adjustment * 100, 2),
                'customer_adjustment': round(customer_adjustment * 100, 2),
                'total_adjustment': round(total_adjustment * 100, 2)
            },
            'recommended_premium': round(adjusted_premium, 2),
            'savings_potential': round(base_premium - adjusted_premium, 2) if adjusted_premium < base_premium else 0,
            'pricing_confidence': 0.88
        }

# Main API client that coordinates all services
class ZurichEdgeApiClient:
    """Main API client for Zurich Edge platform"""
    
    def __init__(self):
        self.weather_client = WeatherApiClient()
        self.financial_client = FinancialApiClient()
        self.insurance_client = InsuranceApiClient()
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def get_real_time_data(self, data_type: str, **kwargs) -> ApiResponse:
        """Get real-time data based on type"""
        try:
            if data_type == 'weather':
                location = kwargs.get('location', 'New York')
                return self.weather_client.get_current_weather(location)
            
            elif data_type == 'weather_forecast':
                location = kwargs.get('location', 'New York')
                days = kwargs.get('days', 7)
                return self.weather_client.get_weather_forecast(location, days)
            
            elif data_type == 'stock':
                symbol = kwargs.get('symbol', 'AAPL')
                return self.financial_client.get_stock_data(symbol)
            
            elif data_type == 'stock_insights':
                symbol = kwargs.get('symbol', 'AAPL')
                return self.financial_client.get_stock_insights(symbol)
            
            elif data_type == 'economic':
                country = kwargs.get('country', 'USA')
                return self.financial_client.get_economic_indicators(country)
            
            elif data_type == 'risk_assessment':
                location = kwargs.get('location', 'New York')
                asset_type = kwargs.get('asset_type', 'property')
                return self.insurance_client.get_risk_assessment_data(location, asset_type)
            
            elif data_type == 'claims_data':
                claim_type = kwargs.get('claim_type', 'property')
                location = kwargs.get('location', 'New York')
                return self.insurance_client.get_claims_processing_data(claim_type, location)
            
            elif data_type == 'pricing_data':
                customer_profile = kwargs.get('customer_profile', {})
                return self.insurance_client.get_pricing_data(customer_profile)
            
            else:
                return ApiResponse(
                    success=False,
                    data={},
                    error=f"Unknown data type: {data_type}",
                    source="zurich_edge_api"
                )
                
        except Exception as e:
            self.logger.error(f"Error getting real-time data: {e}")
            return ApiResponse(
                success=False,
                data={},
                error=str(e),
                source="zurich_edge_api"
            )
    
    def test_all_apis(self) -> Dict[str, ApiResponse]:
        """Test all API connections"""
        test_results = {}
        
        # Test weather API
        test_results['weather'] = self.weather_client.get_current_weather('New York')
        
        # Test financial APIs
        test_results['stock'] = self.financial_client.get_stock_data('AAPL')
        test_results['economic'] = self.financial_client.get_economic_indicators()
        
        # Test insurance APIs
        test_results['risk_assessment'] = self.insurance_client.get_risk_assessment_data('New York')
        
        return test_results

