#!/usr/bin/env python3
"""
Production startup script for AI Code Review System
Loads environment variables and starts the server
"""

import os
import sys
from pathlib import Path

def load_env_file(env_file_path):
    """Load environment variables from .env file"""
    if not os.path.exists(env_file_path):
        print(f"❌ Environment file not found: {env_file_path}")
        return False
    
    with open(env_file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value
    
    return True

def check_configuration():
    """Check if all required configuration is present"""
    required_vars = [
        'AZURE_OPENAI_API_KEY',
        'AZURE_OPENAI_ENDPOINT', 
        'AZURE_OPENAI_DEPLOYMENT_NAME'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        return False
    
    print("✅ Azure OpenAI configuration verified")
    
    # Check optional GitHub configuration
    if os.getenv('GITHUB_TOKEN'):
        print("✅ GitHub integration enabled")
    else:
        print("⚠️  GitHub token not configured - webhook functionality disabled")
    
    return True

def main():
    """Start the production server"""
    print("🚀 Starting AI Code Review System - Production Mode")
    print("=" * 60)
    
    # Load environment variables
    env_file = Path(__file__).parent.parent / '.env'
    if load_env_file(env_file):
        print(f"✅ Loaded environment from: {env_file}")
    else:
        print("⚠️  Using system environment variables")
    
    # Check configuration
    if not check_configuration():
        print("❌ Configuration check failed. Please fix the issues above.")
        sys.exit(1)
    
    # Import and start the application
    try:
        import uvicorn
        from main import app
        
        host = os.getenv('HOST', '0.0.0.0')
        port = int(os.getenv('PORT', 8001))
        
        print(f"🌐 Starting server on {host}:{port}")
        print("📡 Webhook endpoint: /webhook/github")
        print("🔍 Status endpoint: /status")
        print("=" * 60)
        
        uvicorn.run(app, host=host, port=port)
        
    except ImportError:
        print("❌ uvicorn not installed. Run: pip install uvicorn")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 