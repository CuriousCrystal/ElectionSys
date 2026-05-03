import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: { 'Content-Type': 'application/json' }
});

export const chatAPI = {
  sendMessage: (message, sessionId) => api.post('/api/chat', { message, session_id: sessionId })
};

export default api;
