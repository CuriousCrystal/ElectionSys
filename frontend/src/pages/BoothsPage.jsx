import { useState, useEffect } from 'react';
import BoothCard from '../components/booths/BoothCard';
import { boothsAPI } from '../api/apiService';
import { Search } from 'lucide-react';

export default function BoothsPage() {
  const [booths, setBooths] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('');

  useEffect(() => {
    fetchBooths();
  }, []);

  const fetchBooths = async () => {
    try {
      const res = await boothsAPI.getAll();
      setBooths(res.data);
    } catch (error) {
      console.error('Error fetching booths:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredBooths = booths.filter(booth => {
    const matchesSearch = booth.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         booth.constituency.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = !filterStatus || booth.status === filterStatus;
    return matchesSearch && matchesStatus;
  });

  if (loading) {
    return <div className="loading">Loading booths...</div>;
  }

  return (
    <div className="booths-page">
      <div className="page-header">
        <h1>Polling Booths</h1>
      </div>
      
      <div className="filters">
        <div className="search-box">
          <Search size={18} />
          <input
            type="text"
            placeholder="Search by name or constituency..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        
        <select value={filterStatus} onChange={(e) => setFilterStatus(e.target.value)}>
          <option value="">All Status</option>
          <option value="smooth">Smooth</option>
          <option value="busy">Busy</option>
          <option value="critical">Critical</option>
        </select>
      </div>
      
      {filteredBooths.length === 0 ? (
        <div className="empty-state">
          <p>No booths found</p>
          {booths.length === 0 && (
            <button className="btn-primary">Add Your First Booth</button>
          )}
        </div>
      ) : (
        <div className="booths-grid">
          {filteredBooths.map(booth => (
            <BoothCard key={booth.booth_id} booth={booth} />
          ))}
        </div>
      )}
    </div>
  );
}
