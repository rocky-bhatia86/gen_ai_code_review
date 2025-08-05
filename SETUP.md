# 🚀 Quick Setup Guide

## Prerequisites
- Python 3.8+
- Node.js 16+
- OpenAI API Key (for AI reviews)
- GitHub Personal Access Token (optional, for PR reviews)

## 1. Clone and Setup Backend

```bash
# Clone the repository
git clone https://github.com/rocky-bhatia86/ai-code-review-system.git
cd ai-code-review-system

# Create Python virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
cd backend
pip install -r requirements.txt
```

## 2. Configure Environment Variables

```bash
# Copy the example environment file
cp env.example .env

# Edit .env with your actual values:
# OPENAI_API_KEY=your_openai_api_key_here
# GITHUB_TOKEN=your_github_token_here (optional)
```

## 3. Start Backend Server

```bash
# From the backend directory
uvicorn main:app --reload --port 8001 --host localhost
```

## 4. Setup Frontend

```bash
# Open a new terminal and navigate to frontend
cd frontend

# Install Node.js dependencies
npm install

# Start the React development server
npm start
```

## 5. Access the Application

- **Web UI**: http://localhost:3000
- **API Documentation**: http://localhost:8001/docs
- **API Status**: http://localhost:8001/status

## 🎉 You're Ready!

The system will work in "Mock Mode" without an OpenAI API key, or in "Real AI Mode" with your API key configured.

For detailed documentation, see [README.md](README.md)
For deployment instructions, see [azure-deployment-guide.md](azure-deployment-guide.md) 