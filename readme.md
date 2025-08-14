# Airline Market Demand Analytics Web App

A comprehensive Python Flask web application for analyzing airline booking market demand trends across Australia. This application scrapes public flight data, integrates with AI APIs for intelligent insights, and provides an intuitive web interface for visualizing market trends.

## 🚀 Features

### Core Functionality
- **Data Scraping**: Automated collection of airline booking data from public sources
- **AI Integration**: OpenAI-powered analysis for market insights and trend identification
- **Interactive Dashboard**: Real-time visualization of demand patterns and price trends
- **Route Analysis**: Popular routes, pricing trends, and demand forecasting
- **Filtering System**: Advanced filters for origin, destination, dates, and more

### Key Insights Provided
- Popular flight routes and destinations
- Price trend analysis and forecasting
- High-demand periods identification
- Airline market share analysis
- Seasonal demand patterns
- Best booking time recommendations

## 🏗️ Project Structure

```
airline-demand-app/
│
├── app.py                 # Main Flask application
├── scraper.py            # Web scraping module
├── api_integrations.py   # AI and API integration module
├── requirements.txt      # Python dependencies
├── templates/
│   └── index.html        # Main web interface template
├── static/
│   ├── css/
│   ├── js/
│   └── images/
└── README.md
```

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Optional: OpenAI API key for AI-powered insights

## 🛠️ Installation & Setup

### 1. Clone or Download the Project

Create a new directory and save all the provided files:

```bash
mkdir airline-demand-app
cd airline-demand-app
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv airline_env

# Activate virtual environment
# On Windows:
airline_env\Scripts\activate
# On macOS/Linux:
source airline_env/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create Required Directories

```bash
mkdir templates static
mkdir static/css static/js static/images
```

### 5. Set Up Template Files

Save the `index.html` content in `templates/index.html`

### 6. Environment Configuration (Optional)

For enhanced AI features, create a `.env` file:

```bash
# Optional: Add your OpenAI API key for enhanced insights
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Other API keys
AMADEUS_API_KEY=your_amadeus_key
AMADEUS_API_SECRET=your_amadeus_secret
SKYSCANNER
