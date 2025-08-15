#!/usr/bin/env python3
"""
Airline Market Demand Analytics Web App Launcher
Run this script to start the Flask web application
"""

import os
import sys
from pathlib import Path

def setup_environment():
    """Set up environment variables and paths"""
    # Set Gemini API key if not already set
    if not os.getenv('GEMINI_API_KEY'):
        os.environ['GEMINI_API_KEY'] = 'AIzaSyAWKJAemUaM6FTLl0BKuORQ8naxb4S3mF4'
    
    # Add current directory to Python path
    current_dir = Path(__file__).parent.absolute()
    if str(current_dir) not in sys.path:
        sys.path.insert(0, str(current_dir))

def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = [
        'flask', 'requests', 'pandas', 'plotly', 'beautifulsoup4'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n💡 Install missing packages with:")
        print(f"   pip install {' '.join(missing_packages)}")
        print("\n   Or install all requirements:")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def create_directories():
    """Create required directories if they don't exist"""
    directories = ['templates', 'static', 'static/css', 'static/js', 'static/images']
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ Directory '{directory}' ready")

def check_template_file():
    """Check if the HTML template exists"""
    template_path = Path('templates/index.html')
    if not template_path.exists():
        print(f"❌ Template file missing: {template_path}")
        print("💡 Make sure to save the HTML template as 'templates/index.html'")
        return False
    
    print("✓ HTML template found")
    return True

def main():
    """Main launcher function"""
    print("🚀 Airline Market Demand Analytics - Starting Application")
    print("=" * 60)
    
    # Setup environment
    setup_environment()
    print("✓ Environment configured")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    print("✓ All dependencies satisfied")
    
    # Create directories
    create_directories()
    
    # Check template
    if not check_template_file():
        print("\n⚠️  Warning: Template file missing. Create templates/index.html with the provided HTML code.")
        print("The app will still start but may show template errors.")
        input("Press Enter to continue anyway, or Ctrl+C to exit...")
    
    print("\n" + "=" * 60)
    print("🎯 Application Configuration:")
    print(f"   • Flask Debug Mode: Enabled")
    print(f"   • Host: 0.0.0.0 (accessible from network)")
    print(f"   • Port: 5000")
    print(f"   • Gemini AI: {'Enabled' if os.getenv('GEMINI_API_KEY') else 'Disabled (using mock data)'}")
    print("=" * 60)
    
    try:
        # Import and run the Flask app
        from app import app
        
        print("\n✅ Starting Flask development server...")
        print("🌐 Access the application at: http://localhost:5000")
        print("📊 Dashboard will load with sample airline market data")
        print("\n💡 Press Ctrl+C to stop the server\n")
        
        # Run the Flask app
        app.run(
            debug=True,
            host='0.0.0.0',
            port=5000,
            use_reloader=True
        )
        
    except ImportError as e:
        print(f"❌ Error importing Flask app: {e}")
        print("💡 Make sure app.py exists in the current directory")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
