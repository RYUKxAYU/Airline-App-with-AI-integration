# Airline Market Demand Analytics - Complete Setup Guide

## 📁 Project File Structure

Create the following directory structure and files:

```
airline-demand-app/
│
├── app.py                    # Main Flask application
├── api_integrations.py       # Gemini AI integration module  
├── scraper.py               # Web scraping module
├── requirements.txt         # Python dependencies
├── run.py                   # Application launcher script
├── README.md                # Main documentation
├── SETUP.md                 # This setup guide
├── .env                     # Environment variables (optional)
├── .gitignore               # Git ignore file
│
├── templates/               # HTML templates
│   └── index.html          # Main dashboard template
│
├── static/                 # Static assets
│   ├── css/               # Custom CSS files
│   ├── js/                # Custom JavaScript files
│   └── images/            # Image assets
│
└── data/                   # Data storage (optional)
    ├── flight_data.csv     # Scraped flight data
    └── market_analysis.json # Analysis results
```

## 🚀 Quick Start (5 Minutes)

### Step 1: Create Project Directory
```bash
mkdir airline-demand-app
cd airline-demand-app
```

### Step 2: Create Python Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### Step 3: Create and Save All Files

**Save each of the provided code artifacts as:**
- `app.py` - Main Flask application  
- `api_integrations.py` - API integration module
- `scraper.py` - Web scraping module
- `requirements.txt` - Dependencies list
- `run.py` - Launcher script

### Step 4: Create Directory Structure
```bash
mkdir templates static static/css static/js static/images data
```

### Step 5: Save HTML Template
Save the provided HTML code as `templates/index.html`

### Step 6: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 7: Run the Application
```bash
# Using the launcher script (recommended)
python run.py

# OR directly
python app.py
```

### Step 8: Access the Application
Open your browser and go to: `http://localhost:5000`

## 🔧 Detailed Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Modern web browser
- Internet connection (for AI features)

### Environment Setup

#### 1. Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv airline_env

# Activate virtual environment
# Windows:
airline_env\Scripts\activate
# macOS/Linux:
source airline_env/bin/activate

# Verify activation
which python  # Should show path to venv
```

#### 2. Install Dependencies
```bash
# Install all required packages
pip install -r requirements.txt

# Verify installation
pip list
```

### Configuration

#### 1. Environment Variables (Optional)
Create a `.env` file for advanced configuration:

```bash
# .env file
GEMINI_API_KEY=AIzaSyAWKJAemUaM6FTLl0BKuORQ8naxb4S3mF4
FLASK_ENV=development
FLASK_DEBUG=True

# Optional: Additional API keys
AMADEUS_API_KEY=your_amadeus_key
AMADEUS_API_SECRET=your_amadeus_secret
SKYSCANNER_API_KEY=your_skyscanner_key
```

#### 2. Git Configuration (Optional)
Create a `.gitignore` file:

```bash
# .gitignore
__pycache__/
*.pyc
*.pyo
*.pyd
.env
.venv/
venv/
airline_env/
.DS_Store
*.log
data/*.csv
.pytest_cache/
```

### File Contents

#### Complete requirements.txt
```txt
Flask==2.3.3
requests==2.31.0
pandas==2.1.0
plotly==5.15.0
beautifulsoup4==4.12.2
numpy==1.24.3
python-dateutil==2.8.2
Werkzeug==2.3.7
Jinja2==3.1.2
MarkupSafe==2.1.3
itsdangerous==2.1.2
click==8.1.7
blinker==1.6.2
pytz==2023.3
six==1.16.0
urllib3==2.0.4
certifi==2023.7.22
charset-normalizer==3.2.0
idna==3.4
soupsieve==2.4.1
tenacity==8.2.3
packaging==23.1
python-dotenv==1.0.0
```

## 🧪 Testing the Installation

### 1. Test Individual Modules

#### Test the Scraper
```bash
python scraper.py
```
Expected output:
```
Testing single route scraping...
Found X flights
Testing multiple routes...
Total flights scraped: Y
Market Trends:
...
Data saved to flight_data.csv
```

#### Test API Integration
```bash
python api_integrations.py
```
Expected output:
```
Gemini AI Insights: {
  "demand_insights": [...],
  "price_insights": [...],
  ...
}
```

#### Test Flask App
```bash
python app.py
```
Expected output:
```
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://[your-ip]:5000
```

### 2. Test Web Interface

1. **Access Dashboard**: Open `http://localhost:5000`
2. **Check Data Loading**: Verify metrics display numbers
3. **Test Filters**: Try filtering by city names
4. **Verify Charts**: Ensure charts load and display data
5. **Check Insights**: Verify AI insights appear

### 3. API Endpoints Testing

```bash
# Test data endpoint
curl http://localhost:5000/api/data

# Test chart endpoints
curl http://localhost:5000/api/charts/demand
curl http://localhost:5000/api/charts/prices

# Test filtering
curl "http://localhost:5000/filter?origin=Sydney&destination=Melbourne"
```

## 🔍 Troubleshooting Guide

### Common Issues and Solutions

#### Issue: "Module not found" errors
**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall requirements
pip install -r requirements.txt
```

#### Issue: "Port 5000 already in use"
**Solution:**
```bash
# Check what's using port 5000
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Kill the process or change port in app.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

#### Issue: "Template not found"
**Solution:**
```bash
# Ensure directory structure exists
mkdir -p templates

# Verify template file exists
ls -la templates/index.html

# Check Flask template directory
echo "Templates should be in: $(pwd)/templates/"
```

#### Issue: Charts not loading
**Solution:**
1. Check browser console for JavaScript errors
2. Verify Plotly.js CDN is accessible
3. Ensure API endpoints return valid JSON
4. Check browser network tab for failed requests

#### Issue: AI insights not working
**Solution:**
1. Verify Gemini API key is set correctly
2. Check internet connection
3. Review API response in server logs
4. App will fall back to mock insights if API fails

### Debug Mode

Enable detailed debugging:

```python
# In app.py, add:
import logging
logging.basicConfig(level=logging.DEBUG)

# Run with debug mode
app.run(debug=True, host='0.0.0.0', port=5000)
```

### Performance Monitoring

For basic performance logging add the following code:

```python
import time
from functools import wraps

def timing_decorator(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        print(f"{f.__name__} took {end-start:.2f} seconds")
        return result
    return wrapper
```

## Deployment Options

### Local Development
- Use the included Flask development server
- Perfect for testing and development

### Production Deployment options

#### Heroku
```bash
# Install Heroku CLI and login
pip install gunicorn

# Create Procfile
echo "web: gunicorn app:app" > Procfile

# Deploy
git init
git add .
git commit -m "Initial commit"
heroku create your-app-name
git push heroku main
```

#### DigitalOcean Droplet
```bash
# On Ubuntu server
sudo apt update
sudo apt install python3-pip python3-venv nginx

# Clone your code
git clone your-repo
cd airline-demand-app

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Install and configure Gunicorn
pip install gunicorn
gunicorn --bind 0.0.0.0:8000 app:app
```

#### Option 3: Docker Deployment
Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

CMD ["python", "app.py"]
```

Build and run:
```bash
docker build -t airline-app .
docker run -p 5000:5000 airline-app
```

## Data Integration 

### Real Data Sources

#### Option 1: Amadeus GDS API
1. Register at https://developers.amadeus.com/
2. Get API credentials
3. Update `api_integrations.py` with real API calls

#### Option 2: Skyscanner API
1. Apply for Skyscanner partner access
2. Implement actual scraping with rate limiting
3. Add CAPTCHA handling

#### Option 3: Custom Scraping
1. Identify target websites
2. Implement respectful scraping
3. Add data validation and cleaning

### Database Integration

#### SQLite for development
```python
import sqlite3

def create_tables():
    conn = sqlite3.connect('airline_data.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS flights (
        id INTEGER PRIMARY KEY,
        origin TEXT,
        destination TEXT,
        price REAL,
        date TEXT,
        airline TEXT,
        demand_score INTEGER
    )
    ''')
    
    conn.commit()
    conn.close()
```

#### PostgreSQL for Prodcution Level app
```python
import psycopg2
from sqlalchemy import create_engine

DATABASE_URL = "postgresql://user:password@localhost/airline_db"
engine = create_engine(DATABASE_URL)
```
