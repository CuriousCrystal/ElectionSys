import { useState, useEffect } from 'react';
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { analyticsAPI } from '../api/apiService';

const COLORS = ['#00f5d4', '#9b5de5', '#f15bb5', '#fee440', '#00bbf9'];

export default function AnalyticsPage() {
  const [alertsSummary, setAlertsSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [timeRange, setTimeRange] = useState(24);

  useEffect(() => {
    fetchAnalytics();
  }, [timeRange]);

  const fetchAnalytics = async () => {
    try {
      const res = await analyticsAPI.getAlertsSummary(timeRange);
      setAlertsSummary(res.data);
    } catch (error) {
      console.error('Error fetching analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading analytics...</div>;
  }

  const severityData = alertsSummary?.alerts_by_severity 
    ? Object.entries(alertsSummary.alerts_by_severity).map(([name, value]) => ({ name, value }))
    : [];

  const typeData = alertsSummary?.alerts_by_type
    ? Object.entries(alertsSummary.alerts_by_type).map(([name, value]) => ({ name, value }))
    : [];

  return (
    <div className="analytics-page">
      <div className="page-header">
        <h1>Analytics & Reports</h1>
        <select value={timeRange} onChange={(e) => setTimeRange(Number(e.target.value))}>
          <option value={6}>Last 6 hours</option>
          <option value={24}>Last 24 hours</option>
          <option value={168}>Last 7 days</option>
        </select>
      </div>
      
      <div className="charts-grid">
        <div className="chart-card">
          <h3>Alerts by Severity</h3>
          {severityData.length === 0 ? (
            <div className="empty-state">No data available</div>
          ) : (
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={severityData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {severityData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          )}
        </div>
        
        <div className="chart-card">
          <h3>Alerts by Type</h3>
          {typeData.length === 0 ? (
            <div className="empty-state">No data available</div>
          ) : (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={typeData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#9b5de5" />
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>
      </div>
      
      <div className="summary-stats">
        <div className="stat-box">
          <h3>Total Alerts</h3>
          <p className="stat-number">{alertsSummary?.total_alerts || 0}</p>
        </div>
        <div className="stat-box">
          <h3>Unread Alerts</h3>
          <p className="stat-number">{alertsSummary?.unread_alerts || 0}</p>
        </div>
      </div>
    </div>
  );
}
