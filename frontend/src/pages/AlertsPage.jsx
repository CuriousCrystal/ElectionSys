import { useState, useEffect } from 'react';
import { alertsAPI } from '../api/apiService';
import { Check } from 'lucide-react';

export default function AlertsPage() {
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filterUnread, setFilterUnread] = useState(false);

  useEffect(() => {
    fetchAlerts();
  }, [filterUnread]);

  const fetchAlerts = async () => {
    try {
      const res = await alertsAPI.getAll({ unread_only: filterUnread, limit: 100 });
      setAlerts(res.data);
    } catch (error) {
      console.error('Error fetching alerts:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleMarkRead = async (alertId) => {
    try {
      await alertsAPI.markAsRead(alertId);
      fetchAlerts();
    } catch (error) {
      console.error('Error marking alert as read:', error);
    }
  };

  if (loading) {
    return <div className="loading">Loading alerts...</div>;
  }

  return (
    <div className="alerts-page">
      <div className="page-header">
        <h1>Alerts Management</h1>
        <label className="checkbox-label">
          <input
            type="checkbox"
            checked={filterUnread}
            onChange={(e) => setFilterUnread(e.target.checked)}
          />
          Show unread only
        </label>
      </div>
      
      {alerts.length === 0 ? (
        <div className="empty-state">
          <p>No alerts to display</p>
        </div>
      ) : (
        <div className="alerts-table">
          <table>
            <thead>
              <tr>
                <th>Severity</th>
                <th>Type</th>
                <th>Message</th>
                <th>Time</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {alerts.map(alert => (
                <tr key={alert.id} className={`alert-row alert-${alert.severity}`}>
                  <td>
                    <span className="severity-badge">{alert.severity.toUpperCase()}</span>
                  </td>
                  <td>{alert.alert_type.replace('_', ' ')}</td>
                  <td>{alert.message}</td>
                  <td>{new Date(alert.timestamp).toLocaleString()}</td>
                  <td>{alert.is_read ? 'Read' : 'Unread'}</td>
                  <td>
                    {!alert.is_read && (
                      <button onClick={() => handleMarkRead(alert.id)} className="btn-icon">
                        <Check size={16} />
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
