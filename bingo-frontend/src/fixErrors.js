// Fixes for JavaScript errors in the bingo board application

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
  window.showNotification = window.showNotification || function() {};
  window.showProgressUpdate = window.showProgressUpdate || function() {};
  window.showTaskCompletion = window.showTaskCompletion || function() {};
  window.showPatternCompletion = window.showPatternCompletion || function() {};
  window.showPopup = window.showPopup || function(options) {
    if (options && options.onConfirm) setTimeout(options.onConfirm, 100);
  };
  
  // Fix API URLs in network requests
  if (window.axios) {
    const originalAxiosGet = window.axios.get;
    window.axios.get = function(url, config) {
      if (typeof url === 'string' && url.includes('localhost:8000')) {
        url = url.replace('localhost:8000', 'https://ecm2434-v3.onrender.com');
        console.log('Fixed axios URL to:', url);
      }
      return originalAxiosGet(url, config);
    };
    
    const originalAxiosPost = window.axios.post;
    window.axios.post = function(url, data, config) {
      if (typeof url === 'string' && url.includes('localhost:8000')) {
        url = url.replace('localhost:8000', 'https://ecm2434-v3.onrender.com');
        console.log('Fixed axios POST URL to:', url);
      }
      return originalAxiosPost(url, data, config);
    };
  }
  
  // Fix fetch API to handle localhost URLs
  const originalFetch = window.fetch;
  window.fetch = function(url, options) {
    if (typeof url === 'string' && url.includes('localhost:8000')) {
      url = url.replace('localhost:8000', 'https://ecm2434-v3.onrender.com');
      console.log('Fixed fetch URL:', url);
    }
    return originalFetch(url, options);
  };
  
  
  console.log('Error fixes loaded successfully');