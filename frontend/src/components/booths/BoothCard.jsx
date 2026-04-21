import { MapPin, Users, Clock } from 'lucide-react';

export default function BoothCard({ booth }) {
  const getStatusColor = (status) => {
    switch(status) {
      case 'smooth': return 'var(--status-smooth)';
      case 'busy': return 'var(--status-busy)';
      case 'critical': return 'var(--status-critical)';
      default: return 'var(--text-secondary)';
    }
  };

  return (
    <div className="booth-card">
      <div className="booth-header">
        <h3 className="booth-name">
          <div className="status-dot" style={{ background: getStatusColor(booth.status) }}></div>
          {booth.name}
        </h3>
        <span className="booth-status" style={{ color: getStatusColor(booth.status) }}>
          {booth.status.toUpperCase()}
        </span>
      </div>
      
      <div className="booth-details">
        <div className="booth-detail">
          <MapPin size={16} />
          <span>{booth.constituency}</span>
        </div>
        <div className="booth-detail">
          <Users size={16} />
          <span>{booth.current_voters} / {booth.capacity} voters</span>
        </div>
        <div className="booth-detail">
          <Clock size={16} />
          <span>Queue: {booth.queue_length} | Wait: {booth.wait_time_minutes} min</span>
        </div>
      </div>
      
      <div className="capacity-bar">
        <div 
          className="capacity-fill" 
          style={{ 
            width: `${(booth.current_voters / booth.capacity) * 100}%`,
            background: getStatusColor(booth.status)
          }}
        ></div>
      </div>
    </div>
  );
}
