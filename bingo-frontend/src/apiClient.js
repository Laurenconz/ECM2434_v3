// apiClient.js
import axios from 'axios';

// Create an axios instance with the correct defaults
const apiClient = axios.create({
  baseURL: '',  // Empty string for relative URLs
  timeout: 15000,
});

// Override any requests that still use localhost:8000
apiClient.interceptors.request.use(config => {
  // Fix URLs that might still use localhost
  if (config.url && config.url.includes('localhost:8000')) {
    config.url = config.url.replace('localhost:8000', '');
  }
  return config;
});

// Export the client for use in components
export default apiClient;
