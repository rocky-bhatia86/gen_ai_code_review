# 🚀 Azure VM Deployment Guide for AI Code Review System

## Phase 1: Create Azure VM

### 1.1 Create VM in Azure Portal
```bash
# VM Specifications (Recommended)
- Size: Standard B2s (2 vCPUs, 4 GB RAM) - Minimum
- Size: Standard D2s_v3 (2 vCPUs, 8 GB RAM) - Recommended
- OS: Ubuntu 22.04 LTS
- Authentication: SSH public key
- Ports: 22 (SSH), 80 (HTTP), 443 (HTTPS), 8001 (API)
```

### 1.2 Connect to VM
```bash
# SSH into your VM
ssh azureuser@your-vm-ip-address

# Update system
sudo apt update && sudo apt upgrade -y
```

## Phase 2: Install Dependencies

### 2.1 Install Python and Node.js
```bash
# Install Python 3.11
sudo apt install -y python3.11 python3.11-venv python3.11-dev python3-pip

# Install Node.js 18
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install Git
sudo apt install -y git curl wget nginx

# Verify installations
python3.11 --version
node --version
npm --version
```

### 2.2 Install Process Manager
```bash
# Install PM2 for process management
sudo npm install -g pm2

# Install Python packages system-wide
sudo apt install -y python3-pip
```

## Phase 3: Deploy Application

### 3.1 Clone Repository
```bash
# Clone your code
cd /home/azureuser
git clone https://github.com/your-username/ai_code_review_project.git
cd ai_code_review_project

# Or upload your local code
# scp -r ./ai_code_review_project azureuser@your-vm-ip:/home/azureuser/
```

### 3.2 Setup Backend
```bash
# Create Python virtual environment
cd backend
python3.11 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Test backend locally
python -c "from main import app; print('✅ Backend imports successful')"
```

### 3.3 Setup Frontend
```bash
# Install frontend dependencies
cd ../frontend
npm install

# Build production version
npm run build

# The build folder contains the static files
ls -la build/
```

## Phase 4: Environment Variables

### 4.1 Create Environment File
```bash
# Create .env file in project root
cd /home/azureuser/ai_code_review_project
cat > .env << 'EOF'
# AI Code Review System - Production Configuration

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# GitHub Integration
GITHUB_TOKEN=your_github_token_here
GITHUB_WEBHOOK_SECRET=your_webhook_secret_here

# Server Configuration
HOST=0.0.0.0
PORT=8001
ENVIRONMENT=production

# Security
SECRET_KEY=your_secret_key_here
EOF

# Set proper permissions
chmod 600 .env
```

### 4.2 Load Environment Variables
```bash
# Create a script to load environment variables
cat > start_backend.sh << 'EOF'
#!/bin/bash
cd /home/azureuser/ai_code_review_project/backend
source venv/bin/activate
source ../.env
export OPENAI_API_KEY
export GITHUB_TOKEN
export GITHUB_WEBHOOK_SECRET
uvicorn main:app --host 0.0.0.0 --port 8001 --workers 2
EOF

chmod +x start_backend.sh
```

## Phase 5: Configure Nginx (Reverse Proxy)

### 5.1 Create Nginx Configuration
```bash
# Create Nginx config for the app
sudo tee /etc/nginx/sites-available/ai-code-review << 'EOF'
server {
    listen 80;
    server_name your-domain.com your-vm-ip-address;

    # Frontend (React build)
    location / {
        root /home/azureuser/ai_code_review_project/frontend/build;
        index index.html index.htm;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8001/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # Direct backend access (for webhooks)
    location /webhook/ {
        proxy_pass http://localhost:8001/webhook/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Enable the site
sudo ln -s /etc/nginx/sites-available/ai-code-review /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default

# Test and restart Nginx
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl enable nginx
```

## Phase 6: Configure Services with PM2

### 6.1 Create PM2 Ecosystem File
```bash
# Create PM2 configuration
cd /home/azureuser/ai_code_review_project
cat > ecosystem.config.js << 'EOF'
module.exports = {
  apps: [{
    name: 'ai-code-review-backend',
    script: '/home/azureuser/ai_code_review_project/start_backend.sh',
    cwd: '/home/azureuser/ai_code_review_project/backend',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    env: {
      NODE_ENV: 'production'
    },
    error_file: '/home/azureuser/logs/backend-error.log',
    out_file: '/home/azureuser/logs/backend-out.log',
    log_file: '/home/azureuser/logs/backend-combined.log',
    time: true
  }]
};
EOF

# Create logs directory
mkdir -p /home/azureuser/logs
```

### 6.2 Start Services
```bash
# Start the backend with PM2
pm2 start ecosystem.config.js

# Save PM2 configuration
pm2 save

# Setup PM2 to start on boot
pm2 startup
# Follow the instructions shown by the command above

# Check status
pm2 status
pm2 logs
```

## Phase 7: Configure Firewall

### 7.1 Azure Network Security Group
```bash
# In Azure Portal, configure NSG rules:
# - Allow SSH (22) from your IP
# - Allow HTTP (80) from anywhere
# - Allow HTTPS (443) from anywhere
# - Allow Custom (8001) from anywhere (for direct API access)
```

### 7.2 Ubuntu Firewall (UFW)
```bash
# Configure local firewall
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw allow 8001
sudo ufw --force enable
sudo ufw status
```

## Phase 8: SSL Certificate (Optional but Recommended)

### 8.1 Install Certbot
```bash
# Install Certbot for Let's Encrypt SSL
sudo apt install -y certbot python3-certbot-nginx

# Get SSL certificate (replace with your domain)
sudo certbot --nginx -d your-domain.com

# Test auto-renewal
sudo certbot renew --dry-run
```

## Phase 9: Testing Deployment

### 9.1 Test Backend API
```bash
# Test from VM
curl http://localhost:8001/status

# Test from outside
curl http://your-vm-ip:8001/status
curl http://your-domain.com/api/status
```

### 9.2 Test Frontend
```bash
# Visit in browser
http://your-vm-ip
http://your-domain.com
```

### 9.3 Test Full Workflow
```bash
# Test code review
curl -X POST http://your-vm-ip/api/review \
  -H "Content-Type: application/json" \
  -d '{"code": "def hello(): print(\"Hello World\")"}'
```

## Phase 10: Monitoring and Maintenance

### 10.1 Setup Monitoring
```bash
# View logs
pm2 logs
tail -f /home/azureuser/logs/backend-combined.log

# Monitor system resources
htop
df -h
free -h
```

### 10.2 Auto-deployment Script
```bash
# Create update script
cat > update_app.sh << 'EOF'
#!/bin/bash
cd /home/azureuser/ai_code_review_project

# Pull latest changes
git pull origin main

# Update backend
cd backend
source venv/bin/activate
pip install -r requirements.txt

# Update frontend
cd ../frontend
npm install
npm run build

# Restart services
pm2 restart ai-code-review-backend

echo "✅ Application updated successfully!"
EOF

chmod +x update_app.sh
```

## Phase 11: GitHub Webhook Configuration

### 11.1 Configure Webhook in GitHub
```bash
# In your GitHub repository settings:
# Webhooks → Add webhook

# Payload URL: https://your-domain.com/webhook/github
# Content type: application/json
# Secret: your_webhook_secret_from_env
# Events: Pull requests
```

### 11.2 Test Webhook
```bash
# Create a test PR and check logs
pm2 logs ai-code-review-backend
```

## 🎯 Final Checklist

- [ ] VM created and configured
- [ ] Dependencies installed
- [ ] Code deployed
- [ ] Environment variables set
- [ ] Nginx configured
- [ ] PM2 services running
- [ ] Firewall configured
- [ ] SSL certificate installed (optional)
- [ ] Frontend accessible
- [ ] Backend API working
- [ ] GitHub webhook configured
- [ ] Monitoring setup

## 🚨 Troubleshooting

### Common Issues:
1. **Port 8001 blocked**: Check Azure NSG and UFW
2. **PM2 not starting**: Check logs and environment variables
3. **Nginx 502 error**: Backend not running or wrong proxy config
4. **API keys not working**: Check .env file permissions and loading

### Debug Commands:
```bash
# Check processes
pm2 status
sudo systemctl status nginx

# Check logs
pm2 logs
sudo tail -f /var/log/nginx/error.log

# Check ports
sudo netstat -tlnp | grep :8001
sudo netstat -tlnp | grep :80
```

## 🎉 Success!

Your AI Code Review System is now deployed on Azure VM with:
- ✅ Production-ready setup
- ✅ Auto-restart on failure
- ✅ Reverse proxy with Nginx
- ✅ SSL support
- ✅ GitHub webhook integration
- ✅ Monitoring and logging 