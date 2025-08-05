# 🤖 AI Code Review System

An intelligent code review system that integrates with GitHub to automatically review pull requests and provides a web interface for manual code reviews.

## ✨ Features

### 🔄 **Dual Workflow Support**
- **Manual Review**: Paste code or upload files through the web UI
- **Automatic Review**: GitHub webhook integration for PR reviews

### 🎯 **Smart AI Reviews**
- Powered by OpenAI GPT-4o-mini
- Analyzes code quality, security, and best practices
- Supports all major programming languages
- Fallback mock mode when API keys aren't configured

### 🎨 **Modern UI**
- Clean, responsive design with Tailwind CSS
- Drag & drop file upload
- Real-time status indicators
- Mobile-friendly interface

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   GitHub/GitLab │────│   Webhook        │────│  Review Engine  │
│   Pull Request  │    │   Handler        │    │  (OpenAI)       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Web UI        │────│   FastAPI        │────│  Configuration  │
│   (React)       │    │   Backend        │    │  (Environment)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Clone the repository
git clone <your-repo-url>
cd ai_code_review_project

# Copy environment template
cp .env.example .env

# Edit .env with your API keys (see Configuration section)
```

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm start
```

### 4. Access the Application
- Web UI: http://localhost:3000
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/

## ⚙️ Configuration

### Required Environment Variables

```bash
# .env file
OPENAI_API_KEY=your_openai_api_key_here
GITHUB_TOKEN=your_github_personal_access_token_here
GITHUB_WEBHOOK_SECRET=your_webhook_secret_for_security
```

### Getting API Keys

1. **OpenAI API Key**:
   - Visit [OpenAI API Keys](https://platform.openai.com/api-keys)
   - Create a new secret key
   - Add billing information (required for usage)

2. **GitHub Personal Access Token**:
   - Go to GitHub Settings → Developer settings → Personal access tokens
   - Generate new token with `repo` permissions
   - For webhook integration, also need `write:repo_hook`

3. **Webhook Secret**:
   - Any random string (e.g., `mysecretwebhookkey123`)
   - Used to verify webhook authenticity

## 🔗 GitHub Integration

### Setting Up Webhooks

1. Go to your GitHub repository settings
2. Navigate to **Webhooks** → **Add webhook**
3. Configure:
   ```
   Payload URL: https://your-domain.com/webhook/github
   Content type: application/json
   Secret: [your GITHUB_WEBHOOK_SECRET]
   Events: Pull requests
   ```

### Supported Events
- Pull request opened
- Pull request synchronized (updated)

The system automatically:
1. Fetches PR diff when webhook is triggered
2. Reviews changes using AI
3. Posts review as a comment on the PR

## 🖥️ Usage

### Web Interface

1. **Code Review Tab**: 
   - Paste code directly for instant review
   - Supports any programming language

2. **File Upload Tab**:
   - Drag & drop or click to upload code files
   - Supports: `.py`, `.js`, `.ts`, `.java`, `.cpp`, etc.

3. **PR Review Tab**:
   - Enter GitHub PR URL for manual review
   - Fetches and analyzes PR diff

### API Endpoints

- `POST /review` - Review pasted code
- `POST /review/file` - Review uploaded file  
- `POST /review/pr` - Review GitHub PR by URL
- `POST /webhook/github` - GitHub webhook handler
- `GET /status` - System configuration status

## 🛠️ Development

### Backend Structure
```
backend/
├── main.py              # FastAPI application & routes
├── config.py            # Configuration management
├── models.py            # Pydantic data models
└── services/
    ├── review_service.py # AI review logic
    └── git_service.py   # GitHub integration
```

### Frontend Structure
```
frontend/src/
├── App.js              # Main application component
├── services/
│   └── api.js         # Backend API calls
└── components/
    ├── CodeInput.js    # Code textarea component
    ├── FileUpload.js   # File upload component
    ├── PRInput.js      # PR URL input component
    └── ReviewOutput.js # Review results display
```

### Running in Development

```bash
# Terminal 1 - Backend
cd backend
uvicorn main:app --reload --port 8000

# Terminal 2 - Frontend  
cd frontend
npm start
```

## 📋 API Documentation

FastAPI automatically generates interactive API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔧 Troubleshooting

### Common Issues

1. **"Mock Mode" Status**: 
   - Check if `OPENAI_API_KEY` is set correctly
   - Verify OpenAI account has billing enabled

2. **GitHub Integration Not Working**:
   - Ensure `GITHUB_TOKEN` has proper permissions
   - Check webhook URL is accessible from internet
   - Verify webhook secret matches `GITHUB_WEBHOOK_SECRET`

3. **Frontend Build Errors**:
   - Try deleting `node_modules` and running `npm install` again
   - Check Node.js version (recommended: 16+)

### Checking System Status

Visit http://localhost:8000/status to see:
- OpenAI configuration status
- GitHub integration status  
- Current model and server info

## 🚦 System Status Indicators

The web UI shows real-time status:
- 🟢 **AI: Ready** - OpenAI configured and working
- 🟡 **AI: Mock Mode** - Running without OpenAI (testing only)
- 🟢 **GitHub: Connected** - GitHub token configured
- ⚫ **GitHub: Not Configured** - No GitHub token set

## 📝 Notes

- The system works in "mock mode" without API keys for testing
- Real AI reviews require OpenAI API key and billing
- GitHub integration is optional - manual reviews work independently
- All code processing happens server-side for security
