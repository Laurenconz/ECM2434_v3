// apiClient.js
import axios from 'axios';

// Create a configured axios instance
const apiClient = axios.create({
  baseURL: '/api',  // Change from empty string to '/api'
  timeout: 15000,
});

// Add request interceptor to fix any remaining localhost:8000 URLs
apiClient.interceptors.request.use(
  config => {
    // Fix URLs that still use localhost
    if (config.url && config.url.includes('localhost:8000')) {
      config.url = config.url.replace('localhost:8000', '');
      console.log('Fixed URL in interceptor:', config.url);
    }
    
    // Fix any hardcoded URLs to other domains
    if (config.url && config.url.includes('https://ecm2434-v3.onrender.com')) {
      config.url = config.url.replace('https://ecm2434-v3.onrender.com', '');
      console.log('Fixed URL in interceptor:', config.url);
    }
    
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

export default apiClient;