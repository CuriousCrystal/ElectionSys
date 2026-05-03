import axios from 'axios';

// When deploying to Netlify, we use a relative path if VITE_API_URL is not set
// This allows the Netlify redirect to handle the routing to the function
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '',
  headers: { 'Content-Type': 'application/json' }
});

export const chatAPI = {
  sendMessage: (message, sessionId) => api.post('/api/chat', { message, session_id: sessionId })
};

export default api;
