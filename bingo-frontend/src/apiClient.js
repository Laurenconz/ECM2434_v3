import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'https://ecm2434-v3.onrender.com/api',
  timeout: 15000,
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('accessToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default apiClient;