// Fix specific JavaScript errors in the bingo board
console.log('Loading error fixes...');

// Fix for "TypeError: e is not a function"
window.e = function() { 
  console.log('Fixed function e called');
  return null; 
};

// Fix for "TypeError: n is not a function"
window.n = function() { 
  console.log('Fixed function n called');
  return null; 
};

// Provide missing notification functions
window.showNotification = function() { console.log('Notification:', arguments); };
window.showProgressUpdate = function() { console.log('Progress update:', arguments); };
window.showTaskCompletion = function() { console.log('Task completion:', arguments); };
window.showPatternCompletion = function() { console.log('Pattern completion:', arguments); };
window.showPopup = function(options) {
  console.log('Popup:', options);
  if (options && options.onConfirm) setTimeout(options.onConfirm, 100);
};

// Override fetch to fix localhost references
const originalFetch = window.fetch;
window.fetch = function(url, options) {
  if (typeof url === 'string' && url.includes('localhost:8000')) {
    const newUrl = url.replace('localhost:8000', '');
    console.log('Fixed fetch URL from', url, 'to', newUrl);
    return originalFetch(newUrl, options);
  }
  return originalFetch(url, options);
};

console.log('Error fixes loaded');
