import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
import random
from datetime import datetime, timedelta
from urllib.parse import urljoin, urlparse
import re

class AirlineDataScraper:
    """
    Web scraper for airline booking data from public sources
    Note: This is a demonstration implementation. In production, ensure compliance 
    with websites' robots.txt and terms of service.
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.base_urls = {
            'kayak': 'https://www.kayak.com.au/flights',
            'skyscanner': 'https://www.skyscanner.com.au/flights',
            'expedia': 'https://www.expedia.com.au/Flights'
        }
        
    def scrape_flight_data(self, origin='SYD', destination='MEL', date=None):
        """
        Scrape flight data from multiple sources
        Note: This is a simplified demonstration. Real implementation would
        require handling dynamic content, CAPTCHAs, and rate limiting.
        """
        if not date:
            date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
            
        # For demonstration, we'll generate realistic sample data
        # In production, this would make actual HTTP requests to flight booking sites
        return self._generate_realistic_flight_data(origin, destination, date)
    
    def _generate_realistic_flight_data(self, origin, destination, date):
        """Generate realistic flight data for demonstration"""
        
        # Australian airports and major international destinations
        airport_codes = {
            'Sydney': 'SYD', 'Melbourne': 'MEL', 'Brisbane': 'BNE',
            'Perth': 'PER', 'Adelaide': 'ADL', 'Gold Coast': 'OOL',
            'Cairns': 'CNS', 'Darwin': 'DRW', 'Hobart': 'HBA',
            'Canberra': 'CBR', 'Singapore': 'SIN', 'Bangkok': 'BKK',
            'Tokyo': 'NRT', 'Seoul': 'ICN', 'Hong Kong': 'HKG',
            'Los Angeles': 'LAX', 'London': 'LHR', 'Dubai': 'DXB'
        }
        
        airlines = [
            'Qantas', 'Virgin Australia', 'Jetstar', 'Tiger Air',
            'Singapore Airlines', 'Cathay Pacific', 'Emirates',
            'Thai Airways', 'ANA', 'Korean Air'
        ]
        
        flights = []
        
        # Generate multiple flights for the route
        for i in range(random.randint(5, 15)):
            # Base pricing logic
            route_distance = self._estimate_distance(origin, destination)
            base_price = max(200, route_distance * 0.15)  # Rough pricing model
            
            # Add variations
            price_variation = random.uniform(0.8, 1.4)
            final_price = int(base_price * price_variation)
            
            # Generate flight times
            departure_hour = random.randint(6, 22)
            flight_duration = max(1, route_distance // 800)  # Rough duration estimate
            arrival_hour = (departure_hour + flight_duration) % 24
            
            flight = {
                'origin': origin,
                'destination': destination,
                'airline': random.choice(airlines),
                'price': final_price,
                'currency': 'AUD',
                'departure_time': f"{departure_hour:02d}:{random.randint(0,59):02d}",
                'arrival_time': f"{arrival_hour:02d}:{random.randint(0,59):02d}",
                'duration': f"{flight_duration}h {random.randint(0,59)}m",
                'stops': random.choice([0, 0, 0, 1]),  # Mostly direct flights
                'date': date,
                'available_seats': random.randint(5, 200),
                'booking_class': random.choice(['Economy', 'Premium Economy', 'Business', 'First']),
                'scraped_at': datetime.now().isoformat(),
                'demand_indicator': random.uniform(0.3, 1.0)  # 0-1 scale
            }
            
            flights.append(flight)
            
        return flights
    
    def _estimate_distance(self, origin, destination):
        """Rough distance estimation for pricing"""
        # Simplified distance matrix (in km)
        domestic_routes = {
            ('SYD', 'MEL'): 880, ('SYD', 'BNE'): 920, ('MEL', 'BNE'): 1370,
            ('SYD', 'PER'): 3290, ('MEL', 'PER'): 2840, ('SYD', 'ADL'): 1160
        }
        
        # Check if it's a known domestic route
        route_key = (origin, destination)
        if route_key in domestic_routes:
            return domestic_routes[route_key]
        elif (destination, origin) in domestic_routes:
            return domestic_routes[(destination, origin)]
        
        # International routes (rough estimates)
        if origin in ['SYD', 'MEL', 'BNE'] and destination in ['SIN', 'BKK', 'NRT']:
            return random.randint(6000, 9000)
        elif destination in ['LAX', 'LHR']:
            return random.randint(15000, 20000)
        else:
            return random.randint(1000, 5000)  # Default range
    
    def scrape_multiple_routes(self, routes, date=None):
        """Scrape data for multiple routes"""
        all_flights = []
        
        for origin, destination in routes:
            print(f"Scraping data for {origin} -> {destination}")
            
            try:
                flights = self.scrape_flight_data(origin, destination, date)
                all_flights.extend(flights)
                
                # Polite delay between requests
                time.sleep(random.uniform(1, 3))
                
            except Exception as e:
                print(f"Error scraping {origin}-{destination}: {e}")
                continue
                
        return all_flights
    
    def get_popular_australian_routes(self):
        """Return list of popular Australian flight routes"""
        return [
            ('SYD', 'MEL'), ('MEL', 'SYD'), ('SYD', 'BNE'), ('BNE', 'SYD'),
            ('MEL', 'BNE'), ('BNE', 'MEL'), ('SYD', 'PER'), ('PER', 'SYD'),
            ('MEL', 'PER'), ('PER', 'MEL'), ('SYD', 'ADL'), ('ADL', 'SYD'),
            ('SYD', 'OOL'), ('OOL', 'SYD'), ('MEL', 'OOL'), ('OOL', 'MEL'),
            ('SYD', 'CNS'), ('CNS', 'SYD'), ('SYD', 'SIN'), ('MEL', 'SIN'),
            ('SYD', 'BKK'), ('MEL', 'BKK'), ('SYD', 'NRT'), ('MEL', 'NRT')
        ]
    
    def save_to_csv(self, flights_data, filename='flight_data.csv'):
        """Save scraped data to CSV file"""
        df = pd.DataFrame(flights_data)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
        return filename
    
    def get_market_trends(self, flights_data):
        """Analyze market trends from scraped data"""
        df = pd.DataFrame(flights_data)
        
        if df.empty:
            return {}
        
        trends = {
            'total_flights': len(df),
            'avg_price': df['price'].mean(),
            'price_range': {
                'min': df['price'].min(),
                'max': df['price'].max()
            },
            'most_expensive_route': df.loc[df['price'].idxmax()][['origin', 'destination', 'price']].to_dict(),
            'cheapest_route': df.loc[df['price'].idxmin()][['origin', 'destination', 'price']].to_dict(),
            'airlines_count': df['airline'].nunique(),
            'popular_airlines': df['airline'].value_counts().head().to_dict(),
            'route_popularity': df.groupby(['origin', 'destination']).size().sort_values(ascending=False).head().to_dict(),
            'average_demand': df['demand_indicator'].mean() if 'demand_indicator' in df.columns else 0
        }
        
        return trends

# Example usage and testing
if __name__ == "__main__":
    scraper = AirlineDataScraper()
    
    # Test single route
    print("Testing single route scraping...")
    flights = scraper.scrape_flight_data('SYD', 'MEL')
    print(f"Found {len(flights)} flights")
    
    # Test multiple routes
    print("\nTesting multiple routes...")
    popular_routes = scraper.get_popular_australian_routes()[:5]  # Test first 5
    all_flights = scraper.scrape_multiple_routes(popular_routes)
    
    print(f"\nTotal flights scraped: {len(all_flights)}")
    
    # Analyze trends
    trends = scraper.get_market_trends(all_flights)
    print("\nMarket Trends:")
    for key, value in trends.items():
        print(f"{key}: {value}")
    
    # Save to CSV
    scraper.save_to_csv(all_flights)
  
