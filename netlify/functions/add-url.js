const { MongoClient } = require('mongodb');

const MONGO_URI = process.env.MONGODB_URI;

exports.handler = async (event, context) => {
  // CORS headers - must be present on every response
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Content-Type': 'application/json'
  };

  // Handle preflight requests immediately
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 204,
      headers: headers,
      body: null
    };
  }

  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers: headers,
      body: JSON.stringify({ error: 'Method not allowed', success: false })
    };
  }

  const client = new MongoClient(MONGO_URI);

  try {
    let body = {};
    if (event.body) {
      body = JSON.parse(event.body);
    }
    
    const { url, designKeywords, criticalKeywords } = body;

    if (!url) {
      return {
        statusCode: 400,
        headers: headers,
        body: JSON.stringify({ error: 'URL is required', success: false })
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
        statusCode: 409,
        headers: headers,
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
      headers: headers,
      body: JSON.stringify({
        success: true,
        message: 'URL added successfully',
        insertedId: result.insertedId,
        totalUrls
      })
    };
  } catch (error) {
    console.error('Error adding URL:', error);
    await client.close();
    return {
      statusCode: 500,
      headers: headers,
      body: JSON.stringify({
        error: error.message,
        success: false
      })
    };
  }
};
