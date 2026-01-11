const { MongoClient } = require('mongodb');

const MONGO_URI = process.env.MONGODB_URI;

exports.handler = async (event, context) => {
  // Always add CORS headers to response
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Content-Type': 'application/json'
  };

  // Netlify context allows CORS bypass in newer versions
  if (context && context.clientContext) {
    context.clientContext.allowCors = true;
  }

  // Handle preflight
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 204,
      headers,
      body: null
    };
  }

  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({ error: 'Method Not Allowed' })
    };
  }

  let client;
  try {
    const body = JSON.parse(event.body || '{}');
    const { url, designKeywords, criticalKeywords } = body;

    if (!url) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ 
          error: 'URL is required',
          success: false 
        })
      };
    }

    client = new MongoClient(MONGO_URI, { 
      serverSelectionTimeoutMS: 5000 
    });
    
    await client.connect();
    const db = client.db('designpages');
    const collection = db.collection('urls');

    // Check if URL already exists
    const existing = await collection.findOne({ url });
    if (existing) {
      await client.close();
      return {
        statusCode: 409,
        headers,
        body: JSON.stringify({ 
          error: 'URL already exists',
          success: false
        })
      };
    }

    // Insert new URL
    const result = await collection.insertOne({
      url,
      designKeywords: designKeywords || [],
      criticalKeywords: criticalKeywords || [],
      addedAt: new Date(),
      source: 'chrome-extension'
    });

    const count = await collection.countDocuments();

    await client.close();

    return {
      statusCode: 201,
      headers,
      body: JSON.stringify({
        success: true,
        insertedId: result.insertedId.toString(),
        totalUrls: count,
        message: 'URL added successfully'
      })
    };

  } catch (error) {
    console.error('Error:', error);
    if (client) {
      try {
        await client.close();
      } catch (e) {}
    }
    
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        error: error.message,
        success: false
      })
    };
  }
};
