// API Configuration
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const API_BASE_URL = API_URL;
export const AUTH_ENDPOINTS = {
  login: `${API_URL}/api/auth/login`,
  me: `${API_URL}/api/auth/me`,
  register: `${API_URL}/api/auth/register`,
};

export const ANALYTICS_ENDPOINTS = {
  zonesHistory: `${API_URL}/api/analytics/zones/history`,
  zonesReport: `${API_URL}/api/analytics/zones/report`,
  alertsSummary: `${API_URL}/api/analytics/alerts/summary`,
  alerts: `${API_URL}/api/analytics/alerts`,
  auditLogs: `${API_URL}/api/analytics/audit-logs`,
};

export const ALERTS_ENDPOINTS = {
  thresholds: `${API_URL}/api/alerts/thresholds`,
  unreadCount: `${API_URL}/api/alerts/unread-count`,
  recent: `${API_URL}/api/alerts/recent`,
};

export const ZONES_ENDPOINTS = {
  zones: `${API_URL}/api/zones`,
  recommendations: `${API_URL}/api/recommendations`,
};
