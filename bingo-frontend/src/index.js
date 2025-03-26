import './fix';
import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import './index.css';
import App from './App';
// import reportWebVitals from './reportWebVitals';
// Add these fallbacks for functions that might be missing
window.showNotification = window.showNotification || function(id, message) {
  console.log('Notification:', message);
};

window.showProgressUpdate = window.showProgressUpdate || function() {};
window.showPatternCompletion = window.showPatternCompletion || function() {};
window.showPopup = window.showPopup || function(options) {
  if (options && options.onConfirm) setTimeout(options.onConfirm, 100);
};

window.addEventListener('error', function(event) {
  console.log('Detailed error information:', {
    message: event.message,
    filename: event.filename,
    lineno: event.lineno,
    colno: event.colno,
    error: event.error
  });
});

// Fix image loading errors
document.addEventListener('error', function(e) {
  if (e.target.tagName.toLowerCase() === 'img') {
    console.log('Image failed to load:', e.target.src);
    e.target.src = '/static/default_image.png';
  }
}, true);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>
);
