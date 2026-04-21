import { useAuth } from '../context/AuthContext';

export default function SettingsPage() {
  const { user } = useAuth();

  return (
    <div className="settings-page">
      <div className="page-header">
        <h1>Settings</h1>
      </div>
      
      <div className="settings-section">
        <h2>User Profile</h2>
        <div className="profile-card">
          <div className="profile-field">
            <label>Full Name</label>
            <p>{user?.full_name}</p>
          </div>
          <div className="profile-field">
            <label>Username</label>
            <p>{user?.username}</p>
          </div>
          <div className="profile-field">
            <label>Email</label>
            <p>{user?.email}</p>
          </div>
          <div className="profile-field">
            <label>Role</label>
            <p className="role-badge">{user?.role}</p>
          </div>
        </div>
      </div>
      
      <div className="settings-section">
        <h2>System Information</h2>
        <div className="info-card">
          <p>Election Assistant System v2.0.0</p>
          <p>Built with FastAPI + React + MongoDB</p>
        </div>
      </div>
    </div>
  );
}
