const { MongoClient } = require('mongodb');

const MONGO_URI = process.env.MONGODB_URI;

// CORS headers for all responses
const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization',
  'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
  'Content-Type': 'application/json'
};

exports.handler = async (event) => {
  // Handle preflight requests
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers: corsHeaders,
      body: ''
    };
  }

  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers: corsHeaders,
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  }

  const client = new MongoClient(MONGO_URI);

  try {
    const { url, designKeywords, criticalKeywords } = JSON.parse(event.body);

    if (!url) {
      return {
        statusCode: 400,
        headers: corsHeaders,
        body: JSON.stringify({ error: 'URL is required' })
      };
    }

    await client.connect();
    const db = client.db('designpages');
    const urlsCollection = db.collection('urls');

    // Check if URL already exists
    const existingUrl = await urlsCollection.findOne({ url });
    if (existingUrl) {
      await client.close();
      return {
        statusCode: 400,
        headers: corsHeaders,
        body: JSON.stringify({ 
          error: 'URL already in database',
          success: false
        })
      };
    }

    // Add new URL
    const result = await urlsCollection.insertOne({
      url,
      designKeywords: designKeywords || [],
      criticalKeywords: criticalKeywords || [],
      addedAt: new Date(),
      source: 'chrome-extension'
    });

    // Get total count
    const totalUrls = await urlsCollection.countDocuments();

    await client.close();

    return {
      statusCode: 200,
      headers: corsHeaders,
      body: JSON.stringify({
        success: true,
        message: 'URL added successfully',
        insertedId: result.insertedId,
        totalUrls
      })
    };
  } catch (error) {
    console.error('Error adding URL:', error);
    return {
      statusCode: 500,
      headers: corsHeaders,
      body: JSON.stringify({
        error: error.message,
        success: false
      })
    };
  } finally {
    await client.close();
  }
};
