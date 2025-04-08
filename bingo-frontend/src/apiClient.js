// apiClient.js
import axios from 'axios';

// Create an axios instance with the correct defaults
const apiClient = axios.create({
  baseURL: 'https://ecm2434-v3.onrender.com/api',
  timeout: 15000,
});

// Unified request interceptor
apiClient.interceptors.request.use((config) => {
  // Fix URLs that might still use localhost
  if (config.url && config.url.includes('localhost:8000')) {
    config.url = config.url.replace('localhost:8000', '');
  }

  // Attach token if available
  const token = localStorage.getItem('accessToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

// Export the client for use in components
export default apiClient;
