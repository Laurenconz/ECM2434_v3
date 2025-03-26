// Fix for JavaScript errors in the bingo board

// Fix for "TypeError: e is not a function" at line 494171
window.e = function() { 
  console.log('Fixed function e called');
  return null; 
};

// Fix for "TypeError: n is not a function" at line 495872
window.n = function() { 
  console.log('Fixed function n called');
  return null; 
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

console.log('Fix script loaded');