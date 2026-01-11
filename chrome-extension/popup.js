document.addEventListener('DOMContentLoaded', () => {
  const reloadBtn = document.getElementById('reload');
  if (reloadBtn) {
    reloadBtn.addEventListener('click', () => {
      chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
        chrome.tabs.reload(tabs[0].id);
      });
    });
  }

  const downloadBtn = document.getElementById('download-urls');
  if (downloadBtn) {
    downloadBtn.addEventListener('click', () => {
      chrome.runtime.sendMessage({ action: 'downloadAllUrls' }, (response) => {
        if (response && response.success) {
          console.log('Download started:', response.downloadId);
        } else {
          console.error('Download failed:', response?.error);
        }
      });
    });
  }
});
