import { Bell, LogOut, User } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { useState, useEffect } from 'react';
import { alertsAPI } from '../../api/apiService';

export default function Header() {
  const { user, logout } = useAuth();
  const [unreadCount, setUnreadCount] = useState(0);

  useEffect(() => {
    alertsAPI.getUnreadCount()
      .then(res => setUnreadCount(res.data.unread_count))
      .catch(() => {});
  }, []);

  return (
    <header className="header">
      <div className="header-left">
        <h1 className="header-title">Election Command Center</h1>
      </div>
      
      <div className="header-right">
        <button className="header-icon-btn">
          <Bell size={20} />
          {unreadCount > 0 && <span className="notification-badge">{unreadCount}</span>}
        </button>
        
        <div className="user-info">
          <User size={20} />
          <span>{user?.full_name}</span>
          <span className="user-role">{user?.role}</span>
        </div>
        
        <button className="logout-btn" onClick={logout}>
          <LogOut size={18} />
          Logout
        </button>
      </div>
    </header>
  );
}
