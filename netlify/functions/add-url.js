const { MongoClient } = require('mongodb');

const MONGO_URI = process.env.MONGODB_URI;
const client = new MongoClient(MONGO_URI);

exports.handler = async (event) => {
  // CORS headers
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Content-Type': 'application/json'
  };

  // Handle preflight requests
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({ message: 'OK' })
    };
  }

  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  }

  try {
    const { url, designKeywords, criticalKeywords } = JSON.parse(event.body);

    if (!url) {
      return {
        statusCode: 400,
        headers,
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
        headers,
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
      headers,
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
      headers,
      body: JSON.stringify({
        error: error.message,
        success: false
      })
    };
  } finally {
    await client.close();
  }
};
