import React, { useEffect, useState } from 'react';
import { getStatsOverview } from '../services/api';

function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getStatsOverview().then(res => {
      setStats(res.data.data);
      setLoading(false);
    }).catch(err => console.error(err));
  }, []);

  if (loading) return <div>Loading dashboard...</div>;

  return (
    <div>
      <h2>📊 System Overview</h2>
      <div style={{ display: 'flex', gap: '20px', marginTop: '20px' }}>
        <div className="card" style={{ flex: 1, textAlign: 'center' }}>
          <h3>Total Vehicles</h3>
          <p style={{ fontSize: '2rem' }}>{stats.total_vehicles}</p>
        </div>
        <div className="card" style={{ flex: 1, textAlign: 'center' }}>
          <h3>Total Challans</h3>
          <p style={{ fontSize: '2rem' }}>{stats.total_challans}</p>
        </div>
        <div className="card" style={{ flex: 1, textAlign: 'center' }}>
          <h3>Amount Collected</h3>
          <p style={{ fontSize: '2rem' }}>₹{stats.total_amount_collected.toLocaleString()}</p>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;