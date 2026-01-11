# Deployment Instructions

## Step 1: Set up MongoDB Atlas (Free)

1. Go to https://www.mongodb.com/cloud/atlas
2. Sign up for free account
3. Create a free cluster (M0 tier)
4. Create a database user:
   - Database > Database Access > Add New Database User
   - Save username and password
5. Get connection string:
   - Database > Overview > Connect > Drivers
   - Copy the connection string: `mongodb+srv://username:password@cluster.mongodb.net/design_landscape?retryWrites=true`

## Step 2: Set up Netlify Deployment

1. Go to https://netlify.com
2. Sign up for free account
3. Connect your GitHub repo (or we can upload the folder)
4. Add environment variable:
   - Site settings > Build & Deploy > Environment
   - Add: `MONGO_URI` = your MongoDB connection string from Step 1

## Step 3: Deploy Frontend

```bash
cd 3d-landscape
netlify deploy --prod
```

## Step 4: Create MongoDB Collections

Before first use, create these indexes:
```javascript
// In MongoDB Atlas shell, run:
db.contributions.createIndex({ url: 1 }, { unique: true })
db.contributions.createIndex({ submittedAt: -1 })
```

## File Structure for Netlify

```
your-repo/
├── netlify/
│   └── functions/
│       ├── submit.js
│       ├── get-contributions.js
│       └── package.json
├── 3d-landscape/
│   ├── index.html
│   ├── data/
│   └── ...
├── netlify.toml
└── package.json
```

## Create netlify.toml

```toml
[build]
  functions = "netlify/functions"
  publish = "3d-landscape"

[dev]
  functions = "netlify/functions"
```

## Create netlify/functions/package.json

```json
{
  "name": "design-landscape-functions",
  "version": "1.0.0",
  "description": "Backend for design landscape contributions",
  "main": "submit.js",
  "dependencies": {
    "mongodb": "^5.0.0"
  }
}
```

## Testing Locally

```bash
npm install -g netlify-cli
netlify dev
```

Then your API will be at: http://localhost:8888/.netlify/functions/submit

## Frontend API Calls

The frontend should call:
- `POST /.netlify/functions/submit` - submit new page
- `GET /.netlify/functions/get-contributions` - fetch approved submissions

Example:
```javascript
const response = await fetch('/.netlify/functions/submit', {
  method: 'POST',
  body: JSON.stringify({
    url: 'https://example.com',
    sentence: 'Design text...',
    keywords: ['design', 'thinking']
  })
});
```
