const { MongoClient } = require('mongodb');

const MONGO_URI = process.env.MONGODB_URI;
const DB_NAME = 'design_landscape';
const COLLECTION_NAME = 'contributions';

async function getDatabase() {
  const client = new MongoClient(MONGO_URI);
  await client.connect();
  return client.db(DB_NAME);
}

// Extract keywords from text using simple keyword matching
function extractKeywords(text, validKeywords) {
  if (!text) return [];
  const lowerText = text.toLowerCase();
  return validKeywords.filter(kw => 
    lowerText.includes(kw.toLowerCase())
  );
}

// Validate URL is reachable and extract keywords
async function validatePage(url, validKeywords) {
  try {
    const response = await fetch(url, { 
      method: 'HEAD',
      timeout: 5000 
    });
    
    if (!response.ok) {
      return { valid: false, error: 'Page not accessible' };
    }

    // For now, we'll accept the submission
    // In production, you could scrape the page to extract more keywords
    return { valid: true, error: null };
  } catch (error) {
    return { valid: false, error: 'Could not reach page: ' + error.message };
  }
}

exports.handler = async (event) => {
  // Only allow POST
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  }

  try {
    const { url, sentence, keywords } = JSON.parse(event.body);

    if (!url) {
      return {
        statusCode: 400,
        body: JSON.stringify({ error: 'URL is required' })
      };
    }

    // Get valid keywords from environment or hardcoded list
    const validKeywords = process.env.VALID_KEYWORDS 
      ? JSON.parse(process.env.VALID_KEYWORDS)
      : []; // Will be set from frontend

    // Check if URL already exists
    const db = await getDatabase();
    const existing = await db.collection(COLLECTION_NAME).findOne({ url });
    
    if (existing) {
      return {
        statusCode: 400,
        body: JSON.stringify({ error: 'URL already submitted' })
      };
    }

    // Validate page is reachable
    const validation = await validatePage(url, validKeywords);
    if (!validation.valid) {
      return {
        statusCode: 400,
        body: JSON.stringify({ error: validation.error })
      };
    }

    // Check if has at least 2 matching keywords
    const matchedKeywords = keywords.filter(kw => 
      validKeywords.some(vkw => vkw.toLowerCase() === kw.toLowerCase())
    );

    if (matchedKeywords.length < 2) {
      return {
        statusCode: 400,
        body: JSON.stringify({ 
          error: 'Page must contain at least 2 keywords from our list',
          foundKeywords: matchedKeywords.length,
          keywords: matchedKeywords
        })
      };
    }

    // Store in MongoDB
    const contribution = {
      url,
      sentence: sentence || '',
      keywords: matchedKeywords,
      submittedAt: new Date(),
      status: 'pending' // 'pending', 'approved', 'rejected'
    };

    const result = await db.collection(COLLECTION_NAME).insertOne(contribution);

    return {
      statusCode: 201,
      body: JSON.stringify({ 
        success: true, 
        id: result.insertedId,
        message: 'Submission received! Pending review.'
      })
    };

  } catch (error) {
    console.error('Error:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Server error: ' + error.message })
    };
  }
};
