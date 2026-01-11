const express = require('express');
const cors = require('cors');
const { MongoClient } = require('mongodb');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// CORS configuration - very explicit
const corsOptions = {
  origin: '*', // Allow all origins
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: false
};

// Custom CORS middleware that ALWAYS sets headers
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  
  // Handle preflight OPTIONS requests
  if (req.method === 'OPTIONS') {
    return res.sendStatus(200);
  }
  next();
});

// Middleware
app.use(express.json());

// MongoDB connection
const MONGO_URI = process.env.MONGODB_URI;
let db;

async function connectDB() {
  try {
    const client = new MongoClient(MONGO_URI);
    await client.connect();
    db = client.db('designpages');
    console.log('✓ Connected to MongoDB');
  } catch (error) {
    console.error('✗ MongoDB connection failed:', error.message);
    process.exit(1);
  }
}

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Get all submitted URLs
app.get('/urls', async (req, res) => {
  try {
    const urlsCollection = db.collection('urls');
    const urls = await urlsCollection.find({}).sort({ addedAt: -1 }).toArray();
    res.json({ 
      success: true, 
      count: urls.length,
      urls 
    });
  } catch (error) {
    console.error('Error fetching URLs:', error);
    res.status(500).json({ error: 'Failed to fetch URLs' });
  }
});

// Add URL endpoint
app.post('/add-url', async (req, res) => {
  try {
    const { url, title, description } = req.body;

    // Validate input
    if (!url || typeof url !== 'string') {
      return res.status(400).json({ error: 'URL is required and must be a string' });
    }

    // Validate URL format
    try {
      new URL(url);
    } catch (e) {
      return res.status(400).json({ error: 'Invalid URL format' });
    }

    const urlsCollection = db.collection('urls');

    // Check if URL already exists
    const existing = await urlsCollection.findOne({ url });
    if (existing) {
      return res.status(409).json({ error: 'URL already exists', existingId: existing._id });
    }

    // Insert new URL
    const result = await urlsCollection.insertOne({
      url,
      title: title || 'Untitled',
      description: description || '',
      addedAt: new Date(),
      source: 'chrome-extension'
    });

    res.status(201).json({
      success: true,
      message: 'URL added successfully',
      id: result.insertedId
    });
  } catch (error) {
    console.error('Error adding URL:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('Error:', err.message);
  res.status(500).json({ error: 'Internal server error' });
});

// Start server
connectDB().then(() => {
  app.listen(PORT, () => {
    console.log(`✓ Server running on port ${PORT}`);
  });
});
