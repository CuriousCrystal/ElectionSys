import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import StatsCards from '../components/dashboard/StatsCards';
import BoothCard from '../components/booths/BoothCard';
import { boothsAPI, analyticsAPI, alertsAPI } from '../api/apiService';

export default function DashboardPage() {
  const [metrics, setMetrics] = useState(null);
  const [booths, setBooths] = useState([]);
  const [recentAlerts, setRecentAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  const fetchData = async () => {
    try {
      const [metricsRes, boothsRes, alertsRes] = await Promise.all([
        analyticsAPI.getSystemMetrics(),
        boothsAPI.getAll(),
        alertsAPI.getRecent(5)
      ]);
      
      setMetrics(metricsRes.data);
      setBooths(boothsRes.data);
      setRecentAlerts(alertsRes.data);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 10000); // Refresh every 10 seconds
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return <div className="loading">Loading dashboard...</div>;
  }

  return (
    <div className="dashboard-page">
      <section className="dashboard-intro">
        <div>
          <h2>Learn the Election Process</h2>
          <p>Use the assistant and help center to understand registration, voting, and key election dates.</p>
        </div>
        <button className="btn-primary" onClick={() => navigate('/help')}>
          Explore voter guidance
        </button>
      </section>

      <StatsCards metrics={metrics} />
      
      <section className="dashboard-section">
        <div className="section-header">
          <h2>Polling Booths Status</h2>
          <button onClick={() => navigate('/booths')} className="btn-link">
            View All →
          </button>
        </div>
        
        {booths.length === 0 ? (
          <div className="empty-state">
            <p>No booths configured yet</p>
            <button onClick={() => navigate('/booths')} className="btn-primary">
              Add Your First Booth
            </button>
          </div>
        ) : (
          <div className="booths-grid">
            {booths.slice(0, 6).map(booth => (
              <BoothCard key={booth.booth_id} booth={booth} />
            ))}
          </div>
        )}
      </section>
      
      <section className="dashboard-section">
        <div className="section-header">
          <h2>Recent Alerts</h2>
          <button onClick={() => navigate('/alerts')} className="btn-link">
            View All →
          </button>
        </div>
        
        {recentAlerts.length === 0 ? (
          <div className="empty-state">
            <p>No alerts to display</p>
          </div>
        ) : (
          <div className="alerts-list">
            {recentAlerts.map(alert => (
              <div key={alert.id} className={`alert-item alert-${alert.severity}`}>
                <strong>{alert.severity.toUpperCase()}</strong>
                <p>{alert.message}</p>
                <span className="alert-time">
                  {new Date(alert.timestamp).toLocaleTimeString()}
                </span>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
