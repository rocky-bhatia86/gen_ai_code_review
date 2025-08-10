# 🔷 Azure OpenAI Integration Guide

This guide explains how to configure the AI Code Review System to use **Azure OpenAI** instead of regular OpenAI.

## 🚀 Quick Setup

### 1. Environment Variables

Set these environment variables in your `.env` file or system environment:

```bash
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
OPENAI_API_TYPE=azure
OPENAI_API_VERSION=2024-02-01

# GitHub Configuration (same as regular setup)
GITHUB_TOKEN=your_github_personal_access_token_here
GITHUB_WEBHOOK_SECRET=your_webhook_secret_for_security
```

### 2. Using the Template

Copy the Azure OpenAI environment template:
```bash
cp env.azure.example .env
```

Then edit `.env` with your actual Azure OpenAI credentials.

## 🔧 Configuration Details

### Azure OpenAI Settings

| Variable | Description | Example Value |
|----------|-------------|---------------|
| `AZURE_OPENAI_API_KEY` | Your Azure OpenAI API key | `your_azure_openai_api_key_here` |
| `AZURE_OPENAI_ENDPOINT` | Your Azure OpenAI endpoint URL | `https://your-resource-name.openai.azure.com` |
| `AZURE_OPENAI_DEPLOYMENT_NAME` | Your model deployment name | `gpt-4o` |
| `OPENAI_API_TYPE` | Set to "azure" for Azure OpenAI | `azure` |
| `OPENAI_API_VERSION` | Azure OpenAI API version | `2024-02-01` |

### Finding Your Azure OpenAI Credentials

1. **API Key**: Go to Azure Portal → Your OpenAI Resource → Keys and Endpoint
2. **Endpoint**: Found in the same location as the API key
3. **Deployment Name**: Go to Azure OpenAI Studio → Deployments → Your model deployment name

## 🧪 Testing the Integration

Run the test script to verify everything is working:

```bash
cd backend
python3 azure_openai_setup.py
```

Expected output:
```
🚀 Azure OpenAI Setup and Test
========================================
✅ Azure OpenAI environment variables set:
   - API Type: azure
   - Endpoint: https://datadocpoc.openai.azure.com
   - Deployment: gpt-4o
   - API Version: 2024-02-01

🔍 Testing Azure OpenAI Integration...
   - Is Azure OpenAI: True
   - OpenAI Enabled: True
   - Model/Deployment: gpt-4o

✅ Azure OpenAI integration test completed successfully!
```

## 🔄 Switching Between OpenAI and Azure OpenAI

The system automatically detects which service to use based on the `OPENAI_API_TYPE` environment variable:

### Use Regular OpenAI:
```bash
OPENAI_API_TYPE=openai
OPENAI_API_KEY=your_openai_api_key
```

### Use Azure OpenAI:
```bash
OPENAI_API_TYPE=azure
AZURE_OPENAI_API_KEY=your_azure_key
AZURE_OPENAI_ENDPOINT=your_azure_endpoint
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment
```

## 📊 System Status

Check the system status to verify Azure OpenAI configuration:

```bash
curl http://localhost:8000/status
```

Response with Azure OpenAI:
```json
{
  "openai_configured": true,
  "github_configured": true,
  "openai_type": "azure",
  "is_azure_openai": true,
  "model_or_deployment": "gpt-4o",
  "azure_endpoint": "https://datadocpoc.openai.azure.com",
  "server": "localhost:8000"
}
```

## 🚦 Running the Application

Start the backend server:
```bash
cd backend
uvicorn main:app --reload --port 8000
```

The system will automatically use Azure OpenAI for all code reviews when configured correctly.

## 🔍 Features with Azure OpenAI

All existing features work identically with Azure OpenAI:

- ✅ **Manual Code Review** - Paste code in web UI
- ✅ **File Upload Review** - Upload files for review  
- ✅ **PR Review** - Automatic GitHub webhook reviews
- ✅ **Inline Comments** - Line-specific technical feedback
- ✅ **Technical Focus** - Syntax, best practices, security, performance

## 🛠️ Troubleshooting

### Common Issues

1. **"Azure OpenAI not configured"**
   - Verify all required environment variables are set
   - Check that `OPENAI_API_TYPE=azure`

2. **Authentication errors**
   - Verify your Azure OpenAI API key is correct
   - Check that your endpoint URL is correct

3. **Deployment not found**
   - Verify your deployment name matches exactly
   - Check that the deployment is active in Azure OpenAI Studio

### Debug Mode

Run the test script to diagnose issues:
```bash
python3 azure_openai_setup.py
```

This will show detailed configuration and test the connection.

## 📝 Notes

- Azure OpenAI typically has better reliability and compliance features
- The technical review prompt and functionality remain identical
- All GitHub integration features work the same way
- Mock mode still works when Azure OpenAI is not available 