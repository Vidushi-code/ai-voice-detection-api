# Deployment Guide - Railway.app

## Quick Deploy to Railway

Railway.app is recommended for hackathon demos - it's free, fast, and simple.

### Prerequisites
- GitHub account
- Railway.app account (sign up at railway.app)

### Step 1: Prepare Repository

```bash
# Ensure all files are committed
git add .
git commit -m "Ready for deployment"
git push origin main
```

### Step 2: Deploy on Railway

1. Go to [railway.app](https://railway.app)
2. Click "Start a New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Railway will auto-detect Python and deploy

### Step 3: Configure Environment

In Railway dashboard:
1. Go to Variables tab
2. Add environment variables:

```
API_KEY=your_secure_production_key_here
ENVIRONMENT=production
PORT=8000
```

### Step 4: Add Start Command

Railway should auto-detect, but if needed, set start command:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Step 5: Upload Model

Since model files are large, you need to:

**Option A: Train on Railway (if data is small)**
```bash
# Add to railway.toml
[build]
buildCommand = "pip install -r requirements.txt && python train.py"
```

**Option B: Upload pre-trained model**
1. Train locally: `python train.py`
2. Upload `model/voice_model.pkl` via Railway CLI or commit to Git LFS

### Step 6: Test Deployment

```bash
# Replace with your Railway URL
RAILWAY_URL="https://your-app.railway.app"

curl -X POST "$RAILWAY_URL/predict" \
  -H "Authorization: Bearer your_api_key" \
  -H "Content-Type: application/json" \
  -d '{"audio_url": "https://example.com/test.mp3"}'
```

### Railway Configuration File

Create `railway.toml`:

```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/health"
healthcheckTimeout = 30
restartPolicyType = "on-failure"
restartPolicyMaxRetries = 3
```

### Costs

- **Free tier**: 500 hours/month, $5 credit
- **Hobby plan**: $5/month
- Perfect for hackathon demos!

### Monitoring

Railway provides:
- Real-time logs
- Metrics dashboard
- Deployment history
- Auto-scaling

---

## Alternative: Fly.io

### Step 1: Install Fly CLI

```bash
# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex

# Mac/Linux
curl -L https://fly.io/install.sh | sh
```

### Step 2: Login and Launch

```bash
fly auth login
fly launch
```

### Step 3: Configure

Edit `fly.toml`:

```toml
app = "ai-voice-detection"

[build]
  builder = "paketobuildpacks/builder:base"

[env]
  PORT = "8000"
  ENVIRONMENT = "production"

[[services]]
  internal_port = 8000
  protocol = "tcp"

  [[services.ports]]
    port = 80
    handlers = ["http"]

  [[services.ports]]
    port = 443
    handlers = ["tls", "http"]
```

### Step 4: Set Secrets

```bash
fly secrets set API_KEY=your_production_key_here
```

### Step 5: Deploy

```bash
fly deploy
```

### Step 6: Open Application

```bash
fly open
```

---

## Alternative: Heroku

### Step 1: Create Procfile

```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Step 2: Deploy

```bash
heroku login
heroku create ai-voice-detection
git push heroku main
```

### Step 3: Set Environment Variables

```bash
heroku config:set API_KEY=your_key_here
heroku config:set ENVIRONMENT=production
```

---

## Alternative: AWS EC2

### Step 1: Launch EC2 Instance

- Ubuntu 22.04 LTS
- t2.medium or larger
- Open port 8000 in security group

### Step 2: Connect and Setup

```bash
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3-pip python3-venv -y

# Clone repository
git clone <your-repo-url>
cd ai-impact

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Train model (if not included)
python train.py
```

### Step 3: Create Systemd Service

Create `/etc/systemd/system/ai-voice-api.service`:

```ini
[Unit]
Description=AI Voice Detection API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/ai-impact
Environment="PATH=/home/ubuntu/ai-impact/venv/bin"
Environment="API_KEY=your_key_here"
Environment="ENVIRONMENT=production"
ExecStart=/home/ubuntu/ai-impact/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable ai-voice-api
sudo systemctl start ai-voice-api
sudo systemctl status ai-voice-api
```

### Step 4: Setup Nginx (Optional)

```bash
sudo apt install nginx -y
```

Create `/etc/nginx/sites-available/ai-voice-api`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable:

```bash
sudo ln -s /etc/nginx/sites-available/ai-voice-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Build and Run

```bash
# Build image
docker build -t ai-voice-detection .

# Run container
docker run -d \
  -p 8000:8000 \
  -e API_KEY=your_key_here \
  -e ENVIRONMENT=production \
  --name voice-detection \
  ai-voice-detection

# Check logs
docker logs -f voice-detection
```

### Docker Compose

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - API_KEY=your_key_here
      - ENVIRONMENT=production
    restart: unless-stopped
    volumes:
      - ./model:/app/model
```

Run with:
```bash
docker-compose up -d
```

---

## Buildathon Demo Tips

### For Live Demo

1. **Use Railway** - Fastest deployment, live in 5 minutes
2. **Pre-train model** - Don't train during demo
3. **Prepare test URLs** - Have 3-4 audio URLs ready
4. **Show docs** - Open `/docs` endpoint to show Swagger UI

### Fallback Plan

If deployment fails during demo:
1. Run locally: `python main.py`
2. Use ngrok for public URL: `ngrok http 8000`
3. Share ngrok URL with judges

### What Judges Look For

✅ **Working demo** - Actually deployed and accessible  
✅ **Fast response** - < 2 second predictions  
✅ **Good UI** - Show Swagger docs at /docs  
✅ **Error handling** - Demonstrate with bad URLs  
✅ **Security** - Show API key authentication  

### Presentation URL

After deployment, your API will be at:
```
https://your-app-name.railway.app/docs
```

Show this during presentation - judges can test live!
