// Background service worker for handling URL storage

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'addUrlToList') {
    addUrlToAllUrlsJson(message.url, message.designKeywords, message.criticalKeywords)
      .then(result => sendResponse(result))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true; // Keep message channel open for async response
  }
});

async function addUrlToAllUrlsJson(url, designKeywords, criticalKeywords) {
  try {
    // Get current list from storage
    const result = await chrome.storage.local.get('all_urls_data');
    const currentData = result.all_urls_data || { urls: [] };
    
    // Add new URL if not already present
    if (!currentData.urls.includes(url)) {
      currentData.urls.push(url);
      
      // Save back to storage
      await chrome.storage.local.set({ all_urls_data: currentData });
      
      console.log('✓ Background: Added URL to all_urls list');
      console.log('  Total URLs:', currentData.urls.length);
      
      return { 
        success: true, 
        totalUrls: currentData.urls.length,
        message: 'URL added successfully' 
      };
    } else {
      return { 
        success: false, 
        error: 'URL already in list',
        totalUrls: currentData.urls.length 
      };
    }
  } catch (error) {
    console.error('❌ Background: Error adding URL:', error);
    return { success: false, error: error.message };
  }
}

// Export function to download all_urls.json
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'downloadAllUrls') {
    chrome.storage.local.get('all_urls_data', (result) => {
      const data = result.all_urls_data || { urls: [] };
      const jsonString = JSON.stringify(data, null, 2);
      const blob = new Blob([jsonString], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      
      chrome.downloads.download({
        url: url,
        filename: 'all_urls.json',
        saveAs: true
      }, (downloadId) => {
        if (downloadId) {
          sendResponse({ success: true, downloadId: downloadId });
        } else {
          sendResponse({ success: false, error: chrome.runtime.lastError?.message });
        }
      });
    });
    return true;
  }
});
