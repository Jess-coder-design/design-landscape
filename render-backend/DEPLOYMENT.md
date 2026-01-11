# Render.com Deployment Guide

## Quick Start

### 1. Create Render Account
- Go to [render.com](https://render.com)
- Sign up with GitHub

### 2. Connect the Repository
- Click **"New +"** → **"Web Service"**
- Connect your GitHub repo (Jess-coder-design/design-landscape)
- Root directory: `render-backend`
- Build command: `npm install`
- Start command: `npm start`

### 3. Set Environment Variables
- In Render dashboard, go to **Environment** tab
- Add: `MONGODB_URI` = your MongoDB connection string

### 4. Deploy
- Render auto-deploys when you push to GitHub
- Your backend URL will be something like: `https://design-landscape-backend.onrender.com`

## Update Chrome Extension

Update [chrome-extension/content.js](chrome-extension/content.js) line ~751:

Replace:
```javascript
const response = await fetch('https://classy-genie-854a0e.netlify.app/.netlify/functions/add-url', {
```

With:
```javascript
const response = await fetch('https://design-landscape-backend.onrender.com/add-url', {
```

## Testing

After deployment, test the endpoint:
```bash
curl -X POST https://design-landscape-backend.onrender.com/add-url \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com","title":"Example"}'
```

Expected response:
```json
{"success": true, "message": "URL added successfully", "id": "..."}
```

## Local Development (Optional)

```bash
cd render-backend
npm install
node server.js
```

Server runs at `http://localhost:3000`
