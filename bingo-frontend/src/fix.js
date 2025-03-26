// Fallback functions for error handling
window.showNotification = window.showNotification || function() {};
window.showProgressUpdate = window.showProgressUpdate || function() {};
window.showTaskCompletion = window.showTaskCompletion || function() {};
window.showPatternCompletion = window.showPatternCompletion || function() {};
window.showPopup = window.showPopup || function(opts) {
  if (opts && opts.onConfirm) setTimeout(opts.onConfirm, 100);
};

// Override fetch to fix localhost URLs
const originalFetch = window.fetch;
window.fetch = function(url, options) {
  if (typeof url === 'string' && url.includes('localhost:8000')) {
    url = url.replace('localhost:8000', '');
    console.log('Fixed URL:', url);
  }
  return originalFetch(url, options);
};

// Add error handler for image loading
window.addEventListener('error', function(e) {
  if (e.target.tagName === 'IMG') {
    console.log('Image load error, using fallback for:', e.target.src);
    e.target.src = '/static/images/placeholder.png';
    e.preventDefault();
  }
}, true);
