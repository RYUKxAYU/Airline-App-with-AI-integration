import requests
import json
import os
from datetime import datetime, timedelta
import pandas as pd
from typing import List, Dict, Any, Optional

class OpenAIAnalyzer:
    """
    Integration with OpenAI API for intelligent analysis of flight data
    Note: Requires OpenAI API key in environment variables
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.base_url = "https://api.openai.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}" if self.api_key else "",
            "Content-Type": "application/json"
        }
    
    def analyze_flight_trends(self, flight_data: List[Dict]) -> Dict[str, Any]:
        """Analyze flight data using AI to extract insights"""
        
        if not self.api_key:
            # Return mock insights if no API key available
            return self._generate_mock_insights(flight_data)
        
        # Prepare data summary for AI analysis
        data_summary = self._prepare_data_summary(flight_data)
        
        prompt = f"""
        Analyze the following airline booking data and provide insights about:
        1. Market demand patterns
        2. Price trends and anomalies  
        3. Popular routes and destinations
        4. Best booking recommendations
        5. Seasonal or temporal patterns
        
        Data Summary:
        {data_summary}
        
        Please provide clear, actionable insights in JSON format with the following structure:
        {{
            "demand_insights": ["insight1", "insight2", ...],
            "price_insights": ["insight1", "insight2", ...],
            "route_insights": ["insight1", "insight2", ...],
            "recommendations": ["rec1", "rec2", ...],
            "summary": "Overall market summary"
        }}
        """
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json={
                    "model": "gpt-3.5-turbo",
                    "messages": [
                        {"role": "system", "content": "You are an airline industry analyst expert at interpreting market data and trends."},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 1000,
                    "temperature": 0.7
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                # Try to parse JSON response
                try:
                    insights = json.loads(content)
                    return insights
                except json.JSONDecodeError:
                    # If not JSON, return content as text insights
                    return {
                        "demand_insights": [content],
                        "price_insights": [],
                        "route_insights": [],
                        "recommendations": [],
                        "summary": "AI analysis completed"
                    }
            else:
                print(f"OpenAI API error: {response.status_code}")
                return self._generate_mock_insights(flight_data)
                
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return self._generate_mock_insights(flight_data)
    
    def _prepare_data_summary(self, flight_data: List[Dict]) -> str:
        """Prepare a concise summary of flight data for AI analysis"""
        
        if not flight_data:
            return "No flight data available"
        
        df = pd.DataFrame(flight_data)
        
        summary = {
            "total_flights": len(df),
            "date_range": f"{df['date'].min()} to {df['date'].max()}" if 'date' in df.columns else "Not specified",
            "price_stats": {
                "average": round(df['price'].mean(), 2) if 'price' in df.columns else 0,
                "min": df['price'].min() if 'price' in df.columns else 0,
                "max": df['price'].max() if 'price' in df.columns else 0
            },
            "top_routes": df.groupby(['origin', 'destination']).size().head(5).to_dict() if 'origin' in df.columns else {},
            "airlines": df['airline'].value_counts().head(5).to_dict() if 'airline' in df.columns else {},
            "demand_avg": round(df['demand_indicator'].mean(), 2) if 'demand_indicator' in df.columns else 0
        }
        
        return json.dumps(summary, indent=2)
    
    def _generate_mock_insights(self, flight_data: List[Dict]) -> Dict[str, Any]:
        """Generate mock insights when API is not available"""
        
        if not flight_data:
            return {
                "demand_insights": ["No flight data available for analysis"],
                "price_insights": [],
                "route_insights": [],
                "recommendations": [],
                "summary": "Insufficient data for analysis"
            }
        
        df = pd.DataFrame(flight_data)
        avg_price = df['price'].mean() if 'price' in df.columns else 0
        
        mock_insights = {
            "demand_insights": [
                f"Analyzed {len(df)} flights across multiple routes",
                f"Average flight price is ${avg_price:.0f} AUD",
                "Weekend flights show higher demand patterns",
                "Morning flights (6-9 AM) are most popular for business routes"
            ],
            "price_insights": [
                f"Price range varies from ${df['price'].min():.0f} to ${df['price'].max():.0f}" if 'price' in df.columns else "Price data unavailable",
                "International flights average 60% higher than domestic",
                "Booking 3-4 weeks in advance offers best value"
            ],
            "route_insights": [
                "Sydney-Melbourne remains the busiest route",
                "International routes to Asia show strong demand",
                "Regional routes have limited but stable demand"
            ],
            "recommendations": [
                "Book domestic flights 2-3 weeks in advance",
                "Consider Tuesday/Wednesday departures for lower prices",
                "Morning flights offer better on-time performance"
            ],
            "summary": "Market shows healthy demand with price stability across major routes"
        }
        
        return mock_insights

class FlightAPIIntegrator:
    """
    Integration with various flight data APIs
    Note: This is a demonstration class. Real implementation would require API keys
    """
    
    def __init__(self):
        self.apis = {
            'amadeus': {
                'base_url': 'https://api.amadeus.com/v2',
                'key': os.getenv('AMADEUS_API_KEY'),
                'secret': os.getenv('AMADEUS_API_SECRET')
            },
            'skyscanner': {
                'base_url': 'https://partners.api.skyscanner.net/apiservices',
                'key': os.getenv('SKYSCANNER_API_KEY')
            }
        }
    
    def get_flight_offers(self, origin: str, destination: str, departure_date: str) -> List[Dict]:
        """Get flight offers from multiple APIs"""
        
        # For demonstration, return sample data
        # Real implementation would make actual API calls
        
        sample_offers = [
            {
                'id': f'offer_{i}',
                'origin': origin,
                'destination': destination,
                'departure_date': departure_date,
                'price': 450 + (i * 50),
                'currency': 'AUD',
                'airline': ['Qantas', 'Virgin Australia', 'Jetstar'][i % 3],
                'duration': f'{2 + i}h 30m',
                'stops': 0 if i < 2 else 1,
                'booking_link': f'https://example.com/book/{i}',
                'last_updated': datetime.now().isoformat()
            }
            for i in range(5)
        ]
        
        return sample_offers
    
    def get_price_history(self, route: str, days: int = 30) -> List[Dict]:
        """Get historical price data for a route"""
        
        # Generate sample historical data
        base_date = datetime.now() - timedelta(days=days)
        history = []
        
        base_price = 400
        
        for i in range(days):
            date = base_date + timedelta(days=i)
            # Add some realistic price variation
            price_variation = 1 + (0.2 * (i % 7 - 3.5) / 3.5)  # Weekly pattern
            daily_price = base_price * price_variation
            
            history.append({
                'date': date.strftime('%Y-%m-%d'),
                'price': round(daily_price, 2),
                'currency': 'AUD',
                'route': route
            })
        
        return history
    
    def get_destination_insights(self, destination: str) -> Dict[str, Any]:
        """Get insights about a specific destination"""
        
        # Mock destination data
        destinations_data = {
            'Melbourne': {
                'peak_season': 'December - February',
                'weather': 'Temperate oceanic climate',
                'events': ['Australian Open (Jan)', 'Melbourne Cup (Nov)'],
                'avg_stay': '3-4 days',
                'popular_from': ['Sydney', 'Brisbane', 'Adelaide']
            },
            'Sydney': {
                'peak_season': 'September - November, March - May',
                'weather': 'Humid subtropical climate',
                'events': ['New Year\'s Eve', 'Sydney Festival (Jan)'],
                'avg_stay': '4-5 days',
                'popular_from': ['Melbourne', 'Brisbane', 'Perth']
            }
        }
        
        return destinations_data.get(destination, {
            'peak_season': 'Varies',
            'weather': 'Information not available',
            'events': [],
            'avg_stay': 'Unknown',
            'popular_from': []
        })

class MarketDataAggregator:
    """Aggregates data from multiple sources for comprehensive market analysis"""
    
    def __init__(self):
        self.openai_analyzer = OpenAIAnalyzer()
        self.flight_api = FlightAPIIntegrator()
    
    def get_comprehensive_analysis(self, flight_data: List[Dict]) -> Dict[str, Any]:
        """Get comprehensive market analysis combining multiple data sources"""
        
        # AI-powered insights
        ai_insights = self.openai_analyzer.analyze_flight_trends(flight_data)
        
        # Statistical analysis
        stats = self._calculate_market_stats(flight_data)
        
        # Combine all insights
        comprehensive_analysis = {
            'ai_insights': ai_insights,
            'market_statistics': stats,
            'data_quality': self._assess_data_quality(flight_data),
            'timestamp': datetime.now().isoformat(),
            'total_data_points': len(flight_data)
        }
        
        return comprehensive_analysis
    
    def _calculate_market_stats(self, flight_data: List[Dict]) -> Dict[str, Any]:
        """Calculate detailed market statistics"""
        
        if not flight_data:
            return {}
        
        df = pd.DataFrame(flight_data)
        
        stats = {
            'price_distribution': {
                'mean': df['price'].mean() if 'price' in df.columns else 0,
                'median': df['price'].median() if 'price' in df.columns else 0,
                'std': df['price'].std() if 'price' in df.columns else 0,
                'percentiles': {
                    '25th': df['price'].quantile(0.25) if 'price' in df.columns else 0,
                    '75th': df['price'].quantile(0.75) if 'price' in df.columns else 0,
                    '90th': df['price'].quantile(0.90) if 'price' in df.columns else 0
                }
            },
            'route_analysis': {
                'total_routes': len(df.groupby(['origin', 'destination'])) if 'origin' in df.columns else 0,
                'most_frequent': df.groupby(['origin', 'destination']).size().idxmax() if 'origin' in df.columns else None
            },
            'temporal_patterns': {
                'data_span_days': (pd.to_datetime(df['date']).max() - pd.to_datetime(df['date']).min()).days if 'date' in df.columns else 0
            }
        }
        
        return stats
    
    def _assess_data_quality(self, flight_data: List[Dict]) -> Dict[str, Any]:
        """Assess the quality and completeness of the data"""
        
        if not flight_data:
            return {'quality_score': 0, 'issues': ['No data available']}
        
        df = pd.DataFrame(flight_data)
        
        required_fields = ['origin', 'destination', 'price', 'date']
        missing_fields = [field for field in required_fields if field not in df.columns]
        
        quality_score = max(0, 100 - (len(missing_fields) * 25))  # Deduct 25 points per missing field
        
        issues = []
        if missing_fields:
            issues.append(f"Missing required fields: {missing_fields}")
        
        # Check for null values
        null_counts = df.isnull().sum()
        if null_counts.sum() > 0:
            issues.append(f"Null values found in: {null_counts[null_counts > 0].to_dict()}")
            quality_score -= min(20, null_counts.sum())
        
        return {
            'quality_score': max(0, quality_score),
            'issues': issues if issues else ['No major issues detected'],
            'completeness': (1 - df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
        }

# Example usage
if __name__ == "__main__":
    # Test AI analyzer
    analyzer = OpenAIAnalyzer()
    
    # Sample flight data
    sample_data = [
        {'origin': 'SYD', 'destination': 'MEL', 'price': 299, 'date': '2024-03-15', 'airline': 'Qantas'},
        {'origin': 'MEL', 'destination': 'BNE', 'price': 189, 'date': '2024-03-16', 'airline': 'Virgin'},
        {'origin': 'SYD', 'destination': 'PER', 'price': 449, 'date': '2024-03-17', 'airline': 'Jetstar'}
    ]
    
    insights = analyzer.analyze_flight_trends(sample_data)
    print("AI Insights:", json.dumps(insights, indent=2))
    
    # Test comprehensive analysis
    aggregator = MarketDataAggregator()
    analysis = aggregator.get_comprehensive_analysis(sample_data)
    print("\nComprehensive Analysis:", json.dumps(analysis, indent=2))
