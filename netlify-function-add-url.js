// Netlify Function to collect URLs
// Deploy this to your Netlify site

const { Octokit } = require("@octokit/rest");

exports.handler = async (event, context) => {
  // Enable CORS
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Content-Type': 'application/json'
  };

  // Handle OPTIONS request for CORS preflight
  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  }

  try {
    const data = JSON.parse(event.body);
    const { url, designKeywords, criticalKeywords } = data;

    if (!url) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ success: false, error: 'No URL provided' })
      };
    }

    // Option 1: Store in GitHub (you'll need to set up a GitHub token)
    // Uncomment and configure if you want to use GitHub storage
    /*
    const octokit = new Octokit({
      auth: process.env.GITHUB_TOKEN
    });

    const owner = 'your-username';
    const repo = 'your-repo';
    const path = 'data/all_urls.json';

    // Get current file
    const { data: fileData } = await octokit.repos.getContent({
      owner,
      repo,
      path,
    });

    const content = Buffer.from(fileData.content, 'base64').toString();
    const allData = JSON.parse(content);

    // Check if URL already exists
    if (allData.urls.includes(url)) {
      return {
        statusCode: 409,
        headers,
        body: JSON.stringify({
          success: false,
          error: 'URL already exists',
          totalUrls: allData.urls.length
        })
      };
    }

    // Add new URL
    allData.urls.push(url);

    // Update file in GitHub
    await octokit.repos.createOrUpdateFileContents({
      owner,
      repo,
      path,
      message: `Add URL: ${url}`,
      content: Buffer.from(JSON.stringify(allData, null, 2)).toString('base64'),
      sha: fileData.sha,
    });
    */

    // Option 2: Simple logging (for now)
    console.log('URL collected:', {
      url,
      designKeywords,
      criticalKeywords,
      timestamp: new Date().toISOString()
    });

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        message: 'URL received and logged',
        url: url
      })
    };

  } catch (error) {
    console.error('Error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        success: false,
        error: error.message
      })
    };
  }
};
