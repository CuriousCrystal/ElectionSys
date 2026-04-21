import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: { 'Content-Type': 'application/json' }
});

// Request interceptor - attach JWT token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor - handle 401
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API functions grouped by domain
export const authAPI = {
  login: (credentials) => api.post('/api/auth/login', credentials),
  register: (userData) => api.post('/api/auth/register', userData),
  getMe: () => api.get('/api/auth/me')
};

export const boothsAPI = {
  getAll: (filters) => api.get('/api/booths', { params: filters }),
  getById: (id) => api.get(`/api/booths/${id}`),
  create: (data) => api.post('/api/booths', data),
  update: (id, data) => api.put(`/api/booths/${id}`, data),
  delete: (id) => api.delete(`/api/booths/${id}`),
  getRecommendations: () => api.get('/api/booths/recommendations')
};

export const alertsAPI = {
  getRecent: (limit) => api.get('/api/alerts/recent', { params: { limit } }),
  getUnreadCount: () => api.get('/api/alerts/unread-count'),
  getAll: (params) => api.get('/api/alerts', { params }),
  markAsRead: (id) => api.post(`/api/alerts/${id}/read`)
};

export const analyticsAPI = {
  getSystemMetrics: () => api.get('/api/analytics/system'),
  getAlertsSummary: (hours) => api.get('/api/analytics/alerts/summary', { params: { hours } }),
  getBoothHistory: (params) => api.get('/api/analytics/booths/history', { params })
};

export const chatAPI = {
  sendMessage: (message, sessionId) => api.post('/api/chat', { message, session_id: sessionId })
};

export default api;
