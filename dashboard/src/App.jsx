import { useState, useEffect } from 'react';
import { Users, Clock, MapPin, Activity, LogOut, BarChart3 } from 'lucide-react';
import Login from './Login';
import AlertsPanel from './AlertsPanel';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [user, setUser] = useState(null);
  const [data, setData] = useState({ zones: {} });
  const [lastUpdated, setLastUpdated] = useState('');
  const [showAnalytics, setShowAnalytics] = useState(false);

  // Fetch user info
  useEffect(() => {
    if (token) {
      fetch('http://localhost:8000/api/auth/me', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      })
        .then(res => res.json())
        .then(data => setUser(data))
        .catch(() => {
          localStorage.removeItem('token');
          setToken(null);
        });
    }
  }, [token]);

  // Fetch real-time simulation data
  useEffect(() => {
    if (!token) return;

    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/zones', {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });
        const result = await response.json();
        setData(result);
        
        const date = new Date(result.timestamp);
        setLastUpdated(date.toLocaleTimeString());
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData(); // Initial load
    const interval = setInterval(fetchData, 3000); // Poll every 3 seconds
    return () => clearInterval(interval);
  }, [token]);

  const handleLogin = (newToken) => {
    setToken(newToken);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
  };

  if (!token) {
    return <Login onLogin={handleLogin} />;
  }

  const getDensityColor = (density) => {
    if (density < 40) return 'var(--status-smooth)';
    if (density < 80) return 'var(--status-crowded)';
    return 'var(--status-full)';
  };

  const zones = Object.entries(data.zones);

  return (
    <div className="dashboard-container">
      <header style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1>Event Command Center</h1>
        <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-secondary)' }}>
            <Activity size={18} className="glow-dot Smooth" style={{ background: 'transparent', boxShadow: 'none' }}/>
            <span>Live • Last updated: {lastUpdated}</span>
          </div>
          
          <AlertsPanel token={token} />
          
          <button
            onClick={() => setShowAnalytics(!showAnalytics)}
            style={{
              padding: '8px',
              borderRadius: '8px',
              border: '1px solid var(--border-color)',
              background: showAnalytics ? 'var(--accent-primary)' : 'var(--bg-secondary)',
              cursor: 'pointer',
              color: 'var(--text-primary)'
            }}
          >
            <BarChart3 size={20} />
          </button>

          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', paddingLeft: '15px', borderLeft: '1px solid var(--border-color)' }}>
            <span style={{ fontSize: '14px', color: 'var(--text-secondary)' }}>
              {user?.full_name} ({user?.role})
            </span>
            <button
              onClick={handleLogout}
              style={{
                padding: '8px 12px',
                borderRadius: '8px',
                border: '1px solid var(--border-color)',
                background: 'var(--bg-secondary)',
                cursor: 'pointer',
                color: 'var(--text-primary)',
                display: 'flex',
                alignItems: 'center',
                gap: '5px'
              }}
            >
              <LogOut size={16} />
              Logout
            </button>
          </div>
        </div>
      </header>

      {showAnalytics && (
        <div style={{
          marginTop: '20px',
          padding: '20px',
          background: 'var(--bg-secondary)',
          borderRadius: '12px',
          border: '1px solid var(--border-color)'
        }}>
          <h2 style={{ marginBottom: '15px' }}>Analytics & Reports</h2>
          <p style={{ color: 'var(--text-secondary)' }}>
            Historical analytics and reporting features are available via the API endpoints.
            Check the API documentation at http://localhost:8000/docs for details.
          </p>
        </div>
      )}

      <div className="grid-layout">
        {zones.map(([name, info]) => (
          <div key={name} className="zone-card">
            <div className="zone-header">
              <h2 className="zone-title">
                <div className={`glow-dot ${info.status}`}></div>
                {name}
              </h2>
              <span className={`status-badge status-${info.status}`}>
                {info.status}
              </span>
            </div>

            <div className="metrics-container">
              <div>
                <div className="metric-row">
                  <span className="metric-label" style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <Users size={16} /> Crowd Density
                  </span>
                  <span className="metric-value">{info.density}%</span>
                </div>
                <div className="density-bar-bg">
                  <div 
                    className="density-bar-fill" 
                    style={{ 
                      width: `${info.density}%`,
                      backgroundColor: getDensityColor(info.density)
                    }}
                  ></div>
                </div>
              </div>

              <div className="metric-row">
                <span className="metric-label" style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <Clock size={16} /> Wait Time
                </span>
                <span className={`metric-value ${info.wait_time > 12 ? 'wait-time-critical' : ''}`}>
                  {info.wait_time} min
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
