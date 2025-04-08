// bingo-frontend/src/apiClient.js

import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'https://ecm2434-v3.onrender.com/api', // ✅ use your deployed backend
  timeout: 15000,
});

// Optional interceptor for adding token
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('accessToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default apiClient;
