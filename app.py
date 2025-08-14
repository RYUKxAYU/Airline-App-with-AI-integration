from flask import Flask, render_template, request, jsonify
import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objs as go
import plotly.utils
import random
import time
from collections import defaultdict
import os

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-here'

class AirlineDataProcessor:
    """Handles data processing and analysis for airline market demand"""
    
    def __init__(self):
        self.routes_data = []
        self.price_trends = {}
        self.demand_patterns = {}
        
    def generate_sample_data(self):
        """Generate realistic sample airline data for demonstration"""
        # Australian cities and popular international destinations
        cities = [
            'Sydney', 'Melbourne', 'Brisbane', 'Perth', 'Adelaide', 
            'Gold Coast', 'Cairns', 'Darwin', 'Hobart', 'Canberra',
            'Singapore', 'Kuala Lumpur', 'Bangkok', 'Tokyo', 'Seoul',
            'Los Angeles', 'London', 'Dubai', 'Hong Kong', 'Bali'
        ]
        
        # Generate route data
        routes = []
        base_date = datetime.now()
        
        for _ in range(100):
            origin = random.choice(cities[:10])  # Australian cities as origins
            destination = random.choice(cities)
            while destination == origin:
                destination = random.choice(cities)
            
            # Generate realistic pricing based on route type
            is_domestic = destination in cities[:10]
            base_price = random.randint(150, 400) if is_domestic else random.randint(800, 2500)
            
            # Add seasonal and demand variations
            date_offset = random.randint(1, 90)
            flight_date = base_date + timedelta(days=date_offset)
            
            # Weekend and holiday premium
            weekend_multiplier = 1.2 if flight_date.weekday() >= 5 else 1.0
            
            routes.append({
                'origin': origin,
                'destination': destination,
                'price': int(base_price * weekend_multiplier),
                'date': flight_date.strftime('%Y-%m-%d'),
                'demand_score': random.randint(30, 100),
                'availability': random.randint(10, 200),
                'is_domestic': is_domestic,
                'airline': random.choice(['Qantas', 'Jetstar', 'Virgin Australia', 'Tiger Air', 'Singapore Airlines'])
            })
        
        return routes
    
    def analyze_popular_routes(self, data):
        """Analyze most popular routes based on demand and bookings"""
        route_demand = defaultdict(list)
        
        for flight in data:
            route_key = f"{flight['origin']} → {flight['destination']}"
            route_demand[route_key].append(flight['demand_score'])
        
        # Calculate average demand per route
        popular_routes = []
        for route, demands in route_demand.items():
            avg_demand = sum(demands) / len(demands)
            popular_routes.append({
                'route': route,
                'avg_demand': round(avg_demand, 1),
                'flight_count': len(demands)
            })
        
        return sorted(popular_routes, key=lambda x: x['avg_demand'], reverse=True)[:10]
    
    def analyze_price_trends(self, data):
        """Analyze price trends over time and by route type"""
        domestic_prices = []
        international_prices = []
        
        for flight in data:
            if flight['is_domestic']:
                domestic_prices.append(flight['price'])
            else:
                international_prices.append(flight['price'])
        
        return {
            'domestic_avg': round(sum(domestic_prices) / len(domestic_prices) if domestic_prices else 0, 2),
            'international_avg': round(sum(international_prices) / len(international_prices) if international_prices else 0, 2),
            'domestic_range': f"${min(domestic_prices)} - ${max(domestic_prices)}" if domestic_prices else "N/A",
            'international_range': f"${min(international_prices)} - ${max(international_prices)}" if international_prices else "N/A"
        }
    
    def get_demand_insights(self, data):
        """Generate AI-powered insights about demand patterns"""
        # Simulate API call to AI service for insights
        insights = []
        
        # Analyze by day of week
        weekday_demand = defaultdict(list)
        for flight in data:
            flight_date = datetime.strptime(flight['date'], '%Y-%m-%d')
            weekday = flight_date.strftime('%A')
            weekday_demand[weekday].append(flight['demand_score'])
        
        # Find peak demand days
        avg_demand_by_day = {}
        for day, demands in weekday_demand.items():
            avg_demand_by_day[day] = sum(demands) / len(demands)
        
        peak_day = max(avg_demand_by_day, key=avg_demand_by_day.get)
        
        insights.append(f"Peak demand occurs on {peak_day}s with an average demand score of {avg_demand_by_day[peak_day]:.1f}")
        
        # Domestic vs International insights
        domestic_flights = [f for f in data if f['is_domestic']]
        international_flights = [f for f in data if not f['is_domestic']]
        
        if domestic_flights and international_flights:
            dom_avg_demand = sum(f['demand_score'] for f in domestic_flights) / len(domestic_flights)
            intl_avg_demand = sum(f['demand_score'] for f in international_flights) / len(international_flights)
            
            if dom_avg_demand > intl_avg_demand:
                insights.append(f"Domestic routes show higher demand ({dom_avg_demand:.1f}) compared to international routes ({intl_avg_demand:.1f})")
            else:
                insights.append(f"International routes show higher demand ({intl_avg_demand:.1f}) compared to domestic routes ({dom_avg_demand:.1f})")
        
        return insights

# Initialize data processor
data_processor = AirlineDataProcessor()

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    """API endpoint to fetch and process airline data"""
    try:
        # Generate sample data (in real implementation, this would scrape actual data)
        raw_data = data_processor.generate_sample_data()
        
        # Process data for insights
        popular_routes = data_processor.analyze_popular_routes(raw_data)
        price_trends = data_processor.analyze_price_trends(raw_data)
        demand_insights = data_processor.get_demand_insights(raw_data)
        
        return jsonify({
            'success': True,
            'data': {
                'popular_routes': popular_routes,
                'price_trends': price_trends,
                'demand_insights': demand_insights,
                'total_flights': len(raw_data),
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/charts/demand')
def demand_chart():
    """Generate demand visualization data"""
    try:
        raw_data = data_processor.generate_sample_data()
        
        # Group by destination for demand chart
        dest_demand = defaultdict(list)
        for flight in raw_data:
            dest_demand[flight['destination']].append(flight['demand_score'])
        
        destinations = []
        avg_demands = []
        
        for dest, demands in dest_demand.items():
            destinations.append(dest)
            avg_demands.append(sum(demands) / len(demands))
        
        # Sort by demand
        sorted_data = sorted(zip(destinations, avg_demands), key=lambda x: x[1], reverse=True)[:15]
        destinations, avg_demands = zip(*sorted_data)
        
        fig = go.Figure(data=[
            go.Bar(x=list(destinations), y=list(avg_demands), 
                   marker_color='lightblue',
                   text=[f'{d:.1f}' for d in avg_demands],
                   textposition='auto')
        ])
        
        fig.update_layout(
            title='Average Demand Score by Destination',
            xaxis_title='Destination',
            yaxis_title='Average Demand Score',
            template='plotly_white'
        )
        
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return jsonify({'chart': graphJSON})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/charts/prices')
def price_chart():
    """Generate price trend visualization"""
    try:
        raw_data = data_processor.generate_sample_data()
        
        # Group prices by date
        date_prices = defaultdict(list)
        for flight in raw_data:
            date_prices[flight['date']].append(flight['price'])
        
        dates = sorted(date_prices.keys())
        avg_prices = [sum(date_prices[date]) / len(date_prices[date]) for date in dates]
        
        fig = go.Figure(data=[
            go.Scatter(x=dates, y=avg_prices, mode='lines+markers',
                      line=dict(color='orange', width=3),
                      marker=dict(size=6))
        ])
        
        fig.update_layout(
            title='Average Flight Prices Over Time',
            xaxis_title='Date',
            yaxis_title='Average Price (AUD)',
            template='plotly_white'
        )
        
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return jsonify({'chart': graphJSON})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/filter')
def filter_data():
    """Filter data based on user inputs"""
    origin = request.args.get('origin', '')
    destination = request.args.get('destination', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    
    try:
        raw_data = data_processor.generate_sample_data()
        
        # Apply filters
        filtered_data = raw_data
        
        if origin:
            filtered_data = [f for f in filtered_data if f['origin'].lower() == origin.lower()]
        
        if destination:
            filtered_data = [f for f in filtered_data if f['destination'].lower() == destination.lower()]
        
        if date_from:
            filtered_data = [f for f in filtered_data if f['date'] >= date_from]
        
        if date_to:
            filtered_data = [f for f in filtered_data if f['date'] <= date_to]
        
        # Process filtered data
        popular_routes = data_processor.analyze_popular_routes(filtered_data)
        price_trends = data_processor.analyze_price_trends(filtered_data)
        
        return jsonify({
            'success': True,
            'data': {
                'popular_routes': popular_routes,
                'price_trends': price_trends,
                'total_flights': len(filtered_data),
                'filters_applied': {
                    'origin': origin,
                    'destination': destination,
                    'date_from': date_from,
                    'date_to': date_to
                }
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
