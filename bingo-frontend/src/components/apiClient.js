// apiClient.js
import axios from 'axios';

// ✅ Set your deployed backend base URL
const apiClient = axios.create({
  baseURL: 'https://ecm2434-v3.onrender.com',
  timeout: 15000,
});

// ✅ Intercept requests to fix any localhost references
apiClient.interceptors.request.use(
  config => {
    if (config.url && config.url.includes('localhost:8000')) {
      config.url = config.url.replace('localhost:8000', 'https://ecm2434-v3.onrender.com');
      console.log('Rewriting localhost URL to:', config.url);
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

export default apiClient;
