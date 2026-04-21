import { Users, Clock, AlertTriangle, Activity } from 'lucide-react';

const StatCard = ({ title, value, icon: Icon, color, subtitle }) => (
  <div className="stat-card">
    <div className="stat-icon" style={{ background: `${color}20`, color }}>
      <Icon size={24} />
    </div>
    <div className="stat-content">
      <h3 className="stat-title">{title}</h3>
      <p className="stat-value">{value}</p>
      {subtitle && <p className="stat-subtitle">{subtitle}</p>}
    </div>
  </div>
);

export default function StatsCards({ metrics }) {
  const stats = [
    {
      title: 'Active Booths',
      value: metrics?.active_booths || 0,
      icon: Activity,
      color: '#00f5d4',
      subtitle: 'Running smoothly'
    },
    {
      title: 'Total Voters',
      value: metrics?.total_voters || 0,
      icon: Users,
      color: '#9b5de5',
      subtitle: 'Across all booths'
    },
    {
      title: 'Critical Alerts',
      value: metrics?.critical_alerts || 0,
      icon: AlertTriangle,
      color: '#f15bb5',
      subtitle: 'Requires attention'
    },
    {
      title: 'Avg Wait Time',
      value: `${metrics?.avg_wait_time || 0} min`,
      icon: Clock,
      color: '#fee440',
      subtitle: 'Per booth'
    }
  ];

  return (
    <div className="stats-grid">
      {stats.map((stat, index) => (
        <StatCard key={index} {...stat} />
      ))}
    </div>
  );
}
