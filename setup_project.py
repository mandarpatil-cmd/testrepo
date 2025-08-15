import os
import json
import pandas as pd
from datetime import datetime, timedelta
import random

def create_project_structure():
    """Create the complete project directory structure"""
    
    directories = [
        "aioptima",
        "aioptima/backend",
        "aioptima/backend/models",
        "aioptima/backend/api",
        "aioptima/backend/services",
        "aioptima/frontend",
        "aioptima/database",
        "aioptima/config",
        "aioptima/tests",
        "aioptima/docs",
        "aioptima/scripts"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    # Create __init__.py files
    init_files = [
        "aioptima/__init__.py",
        "aioptima/backend/__init__.py",
        "aioptima/backend/models/__init__.py",
        "aioptima/backend/api/__init__.py",
        "aioptima/backend/services/__init__.py",
        "aioptima/tests/__init__.py"
    ]
    
    for init_file in init_files:
        with open(init_file, 'w') as f:
            f.write('"""AIOptima package"""\n')
        print(f"✅ Created: {init_file}")

def generate_sample_data():
    """Generate comprehensive sample data for testing"""
    
    # AI Providers and their models
    providers_data = {
        'OpenAI': {
            'models': ['gpt-4', 'gpt-4-turbo', 'gpt-3.5-turbo', 'gpt-3.5-turbo-16k'],
            'cost_input': 0.00001,
            'cost_output': 0.00003,
            'energy_factor': 1.0
        },
        'Anthropic': {
            'models': ['claude-3-opus', 'claude-3-sonnet', 'claude-3-haiku', 'claude-instant'],
            'cost_input': 0.000015,
            'cost_output': 0.000075,
            'energy_factor': 1.2
        },
        'Google': {
            'models': ['gemini-pro', 'gemini-pro-vision', 'palm-2', 'codey'],
            'cost_input': 0.0000125,
            'cost_output': 0.0000375,
            'energy_factor': 0.8
        },
        'Cohere': {
            'models': ['command', 'command-light', 'embed-english', 'embed-multilingual'],
            'cost_input': 0.000001,
            'cost_output': 0.000002,
            'energy_factor': 0.6
        }
    }
    
    # Generate sample API usage data
    sample_data = []
    start_date = datetime.now() - timedelta(days=30)
    
    for day in range(30):
        current_date = start_date + timedelta(days=day)
        
        # Generate 5-50 calls per day with realistic patterns
        daily_calls = random.randint(5, 50)
        
        # More calls during business hours
        for _ in range(daily_calls):
            # Bias towards business hours (9 AM - 6 PM)
            hour = random.choices(
                range(24),
                weights=[1, 1, 1, 1, 1, 1, 2, 4, 6, 8, 8, 8, 8, 8, 8, 8, 8, 6, 4, 2, 1, 1, 1, 1]
            )[0]
            
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            
            timestamp = current_date.replace(hour=hour, minute=minute, second=second)
            
            # Select provider and model
            provider = random.choice(list(providers_data.keys()))
            model = random.choice(providers_data[provider]['models'])
            
            # Generate realistic token usage
            input_tokens = random.randint(50, 2000)
            output_tokens = random.randint(20, 800)
            
            # Response time varies by provider and model complexity
            base_response_time = random.uniform(0.5, 3.0)
            if 'gpt-4' in model or 'claude-3-opus' in model:
                response_time = base_response_time * random.uniform(1.5, 2.5)
            else:
                response_time = base_response_time * random.uniform(0.8, 1.2)
            
            sample_data.append({
                'provider_name': provider,
                'model_name': model,
                'input_tokens': input_tokens,
                'output_tokens': output_tokens,
                'response_time': round(response_time, 2),
                'timestamp': timestamp.isoformat()
            })
    
    # Save sample data
    sample_df = pd.DataFrame(sample_data)
    sample_df.to_csv('aioptima/database/sample_data.csv', index=False)
    print(f"✅ Generated {len(sample_data)} sample API calls")
    
    # Generate different usage scenarios
    scenarios = {
        'heavy_usage': sample_df.sample(frac=2, replace=True),  # 2x the data
        'light_usage': sample_df.sample(frac=0.3),  # 30% of the data
        'burst_usage': generate_burst_pattern(sample_df),
        'cost_focused': generate_cost_focused_data(sample_df, providers_data)
    }
    
    for scenario_name, scenario_data in scenarios.items():
        scenario_data.to_csv(f'aioptima/database/{scenario_name}_sample.csv', index=False)
        print(f"✅ Generated {scenario_name} scenario with {len(scenario_data)} records")
    
    return sample_df

def generate_burst_pattern(base_df):
    """Generate data with burst usage patterns"""
    burst_data = base_df.copy()
    
    # Add burst periods (5x normal usage for 2-hour windows)
    burst_times = pd.date_range(
        start=datetime.now() - timedelta(days=30),
        end=datetime.now(),
        freq='3D'  # Every 3 days
    )
    
    additional_data = []
    for burst_time in burst_times:
        burst_end = burst_time + timedelta(hours=2)
        
        # Generate 5x more calls during burst
        for _ in range(random.randint(50, 100)):
            timestamp = burst_time + timedelta(
                minutes=random.randint(0, 120)
            )
            
            provider = random.choice(['OpenAI', 'Anthropic'])
            model = random.choice(['gpt-4', 'claude-3-opus'])  # Heavy models during bursts
            
            additional_data.append({
                'provider_name': provider,
                'model_name': model,
                'input_tokens': random.randint(500, 3000),  # Larger requests
                'output_tokens': random.randint(200, 1500),
                'response_time': round(random.uniform(2.0, 8.0), 2),  # Slower responses
                'timestamp': timestamp.isoformat()
            })
    
    burst_df = pd.DataFrame(additional_data)
    return pd.concat([burst_data, burst_df], ignore_index=True)

def generate_cost_focused_data(base_df, providers_data):
    """Generate data focusing on cost optimization scenarios"""
    cost_data = base_df.copy()
    
    # Add expensive usage patterns
    expensive_data = []
    
    # Heavy GPT-4 usage (most expensive)
    for _ in range(200):
        timestamp = datetime.now() - timedelta(
            days=random.randint(1, 30),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        
        expensive_data.append({
            'provider_name': 'OpenAI',
            'model_name': 'gpt-4',
            'input_tokens': random.randint(1000, 4000),  # Large inputs
            'output_tokens': random.randint(500, 2000),   # Large outputs
            'response_time': round(random.uniform(3.0, 10.0), 2),
            'timestamp': timestamp.isoformat()
        })
    
    # Mix in some efficient usage
    for _ in range(300):
        timestamp = datetime.now() - timedelta(
            days=random.randint(1, 30),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        
        expensive_data.append({
            'provider_name': random.choice(['Google', 'Cohere']),
            'model_name': random.choice(['gemini-pro', 'command-light']),
            'input_tokens': random.randint(100, 800),
            'output_tokens': random.randint(50, 300),
            'response_time': round(random.uniform(0.5, 2.0), 2),
            'timestamp': timestamp.isoformat()
        })
    
    cost_df = pd.DataFrame(expensive_data)
    return pd.concat([cost_data, cost_df], ignore_index=True)

def create_config_files():
    """Create configuration files"""
    
    # Environment configuration
    env_config = """# AIOptima Environment Configuration
# Database
DATABASE_URL=sqlite:///./database/aioptima.db

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
SECRET_KEY=your-secret-key-change-this-in-production

# Dashboard Configuration
DASHBOARD_PORT=8501

# Energy Calculation
CARBON_INTENSITY=0.5  # kg CO2 per kWh
ENERGY_EFFICIENCY_FACTOR=1.0

# Provider API Keys (optional - for real-time monitoring)
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
GOOGLE_API_KEY=your-google-key
"""
    
    with open('aioptima/.env', 'w') as f:
        f.write(env_config)
    print("✅ Created .env configuration file")
    
    # Docker configuration
    dockerfile = """FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000 8501

# Create startup script
RUN echo '#!/bin/bash\\n\\
uvicorn backend.main:app --host 0.0.0.0 --port 8000 &\\n\\
streamlit run frontend/dashboard.py --server.port 8501 --server.address 0.0.0.0\\n\\
wait' > start.sh && chmod +x start.sh

CMD ["./start.sh"]
"""
    
    with open('aioptima/Dockerfile', 'w') as f:
        f.write(dockerfile)
    print("✅ Created Dockerfile")
    
    # Docker Compose
    docker_compose = """version: '3.8'

services:
  aioptima:
    build: .
    ports:
      - "8000:8000"  # Backend API
      - "8501:8501"  # Streamlit Dashboard
    volumes:
      - ./database:/app/database
      - ./.env:/app/.env
    environment:
      - PYTHONPATH=/app
"""
    
    with open('aioptima/docker-compose.yml', 'w') as f:
        f.write(docker_compose)
    print("✅ Created docker-compose.yml")

def create_startup_scripts():
    """Create startup scripts for easy development"""
    
    # Start backend script
    start_backend = """#!/bin/bash
echo "🚀 Starting AIOptima Backend..."
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
"""
    
    with open('aioptima/start_backend.sh', 'w') as f:
        f.write(start_backend)
    os.chmod('aioptima/start_backend.sh', 0o755)
    print("✅ Created start_backend.sh")
    
    # Start dashboard script
    start_dashboard = """#!/bin/bash
echo "📊 Starting AIOptima Dashboard..."
cd frontend
streamlit run dashboard.py --server.port 8501
"""
    
    with open('aioptima/start_dashboard.sh', 'w') as f:
        f.write(start_dashboard)
    os.chmod('aioptima/start_dashboard.sh', 0o755)
    print("✅ Created start_dashboard.sh")
    
    # Combined startup script
    start_all = """#!/bin/bash
echo "🤖 Starting AIOptima Complete System..."

# Start backend in background
echo "Starting backend..."
cd backend && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 5

# Start dashboard
echo "Starting dashboard..."
cd ../frontend && streamlit run dashboard.py --server.port 8501 &
DASHBOARD_PID=$!

echo "✅ AIOptima is running!"
echo "   Backend API: http://localhost:8000"
echo "   Dashboard: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for interrupt
trap "kill $BACKEND_PID $DASHBOARD_PID; exit" INT
wait
"""
    
    with open('aioptima/start_all.sh', 'w') as f:
        f.write(start_all)
    os.chmod('aioptima/start_all.sh', 0o755)
    print("✅ Created start_all.sh")

def create_documentation():
    """Create project documentation"""
    
    readme = ""