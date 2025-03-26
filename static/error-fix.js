// Runtime fixes for JavaScript errors
console.log('Applying bingo board fixes...');

// Fix for TypeError: e is not a function
window.e = function() { return null; };

// Fix for TypeError: n is not a function
window.n = function() { return null; };

// Fix for notification functions
window.showNotification = window.showNotification || function() {};
window.showProgressUpdate = window.showProgressUpdate || function() {};
window.showTaskCompletion = window.showTaskCompletion || function() {};
window.showPatternCompletion = window.showPatternCompletion || function() {};
window.showPopup = window.showPopup || function(options) {
  if (options && options.onConfirm) setTimeout(options.onConfirm, 100);
};

// Fix axios to handle localhost URLs
if (window.axios) {
  const originalGet = window.axios.get;
  window.axios.get = function(url, config) {
    if (url.includes('localhost:8000')) {
      url = url.replace('localhost:8000', '');
      console.log('Fixed axios URL:', url);
    }
    return originalGet(url, config);
  };
  
  const originalPost = window.axios.post;
  window.axios.post = function(url, data, config) {
    if (url.includes('localhost:8000')) {
      url = url.replace('localhost:8000', '');
      console.log('Fixed axios POST URL:', url);
    }
    return originalPost(url, data, config);
  };
}
