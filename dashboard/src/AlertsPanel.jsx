import { useState, useEffect } from 'react';
import { Bell, AlertTriangle, AlertCircle, Info } from 'lucide-react';

function AlertsPanel({ token }) {
  const [alerts, setAlerts] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [showPanel, setShowPanel] = useState(false);

  const fetchAlerts = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/alerts/recent?limit=10');
      const data = await response.json();
      setAlerts(data.alerts);
    } catch (error) {
      console.error('Error fetching alerts:', error);
    }

    try {
      const response = await fetch('http://localhost:8000/api/alerts/unread-count');
      const data = await response.json();
      setUnreadCount(data.unread_count);
    } catch (error) {
      console.error('Error fetching unread count:', error);
    }
  };

  useEffect(() => {
    fetchAlerts();
    const interval = setInterval(fetchAlerts, 5000);
    return () => clearInterval(interval);
  }, []);

  const markAsRead = async (alertId) => {
    try {
      await fetch(`http://localhost:8000/api/alerts/${alertId}/read`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      fetchAlerts();
    } catch (error) {
      console.error('Error marking alert as read:', error);
    }
  };

  const getSeverityIcon = (severity) => {
    switch (severity) {
      case 'critical':
        return <AlertCircle size={18} style={{ color: '#ff3b30' }} />;
      case 'high':
        return <AlertTriangle size={18} style={{ color: '#ff9500' }} />;
      case 'medium':
        return <Info size={18} style={{ color: '#ffcc00' }} />;
      default:
        return <Info size={18} style={{ color: 'var(--text-secondary)' }} />;
    }
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical':
        return 'rgba(255, 59, 48, 0.1)';
      case 'high':
        return 'rgba(255, 149, 0, 0.1)';
      case 'medium':
        return 'rgba(255, 204, 0, 0.1)';
      default:
        return 'var(--bg-primary)';
    }
  };

  return (
    <div style={{ position: 'relative' }}>
      <button
        onClick={() => setShowPanel(!showPanel)}
        style={{
          position: 'relative',
          padding: '8px',
          borderRadius: '8px',
          border: '1px solid var(--border-color)',
          background: 'var(--bg-secondary)',
          cursor: 'pointer',
          color: 'var(--text-primary)'
        }}
      >
        <Bell size={20} />
        {unreadCount > 0 && (
          <span style={{
            position: 'absolute',
            top: '-5px',
            right: '-5px',
            background: '#ff3b30',
            color: 'white',
            borderRadius: '50%',
            width: '20px',
            height: '20px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '12px',
            fontWeight: 'bold'
          }}>
            {unreadCount}
          </span>
        )}
      </button>

      {showPanel && (
        <div style={{
          position: 'absolute',
          top: '50px',
          right: '0',
          width: '400px',
          maxHeight: '500px',
          overflowY: 'auto',
          background: 'var(--bg-secondary)',
          border: '1px solid var(--border-color)',
          borderRadius: '12px',
          boxShadow: '0 4px 12px rgba(0, 0, 0, 0.3)',
          zIndex: 1000
        }}>
          <div style={{
            padding: '20px',
            borderBottom: '1px solid var(--border-color)',
            fontWeight: '600',
            fontSize: '16px'
          }}>
            Alerts & Notifications
          </div>

          {alerts.length === 0 ? (
            <div style={{
              padding: '40px 20px',
              textAlign: 'center',
              color: 'var(--text-secondary)'
            }}>
              No alerts at this time
            </div>
          ) : (
            alerts.map((alert) => (
              <div
                key={alert.id}
                onClick={() => !alert.is_read && markAsRead(alert.id)}
                style={{
                  padding: '15px 20px',
                  borderBottom: '1px solid var(--border-color)',
                  background: alert.is_read ? 'transparent' : getSeverityColor(alert.severity),
                  cursor: alert.is_read ? 'default' : 'pointer',
                  opacity: alert.is_read ? 0.7 : 1,
                  transition: 'opacity 0.2s'
                }}
              >
                <div style={{ display: 'flex', alignItems: 'flex-start', gap: '10px' }}>
                  {getSeverityIcon(alert.severity)}
                  <div style={{ flex: 1 }}>
                    <div style={{
                      fontWeight: '600',
                      fontSize: '14px',
                      marginBottom: '5px',
                      textTransform: 'capitalize'
                    }}>
                      {alert.severity} - {alert.alert_type}
                    </div>
                    <div style={{
                      fontSize: '13px',
                      color: 'var(--text-secondary)',
                      marginBottom: '5px'
                    }}>
                      {alert.message}
                    </div>
                    <div style={{
                      fontSize: '11px',
                      color: 'var(--text-secondary)'
                    }}>
                      {new Date(alert.timestamp).toLocaleString()}
                    </div>
                  </div>
                  {!alert.is_read && (
                    <div style={{
                      width: '8px',
                      height: '8px',
                      borderRadius: '50%',
                      background: 'var(--accent-primary)',
                      flexShrink: 0
                    }}></div>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}

export default AlertsPanel;
