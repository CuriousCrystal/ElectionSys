import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Vote, BarChart3, Bell, Settings, HelpCircle, ChevronLeft, ChevronRight } from 'lucide-react';
import { useState } from 'react';

const navItems = [
  { path: '/', icon: LayoutDashboard, label: 'Dashboard' },
  { path: '/booths', icon: Vote, label: 'Booths' },
  { path: '/analytics', icon: BarChart3, label: 'Analytics' },
  { path: '/alerts', icon: Bell, label: 'Alerts' },
  { path: '/help', icon: HelpCircle, label: 'Learn' },
  { path: '/settings', icon: Settings, label: 'Settings' }
];

export default function Sidebar() {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <aside className={`sidebar ${collapsed ? 'collapsed' : ''}`}>
      <button className="sidebar-toggle" onClick={() => setCollapsed(!collapsed)}>
        {collapsed ? <ChevronRight size={20} /> : <ChevronLeft size={20} />}
      </button>
      
      <nav className="sidebar-nav">
        {navItems.map(({ path, icon: Icon, label }) => (
          <NavLink
            key={path}
            to={path}
            className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
          >
            <Icon size={20} />
            {!collapsed && <span>{label}</span>}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
