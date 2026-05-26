import React, { useState, useEffect } from 'react';
import { getVehicles, getChallans } from '../services/api';

function DataTables() {
  const [vehicles, setVehicles] = useState([]);
  const [challans, setChallans] = useState([]);
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([getVehicles(page), getChallans(page)])
      .then(([vRes, cRes]) => {
        setVehicles(vRes.data.data);
        setChallans(cRes.data.data);
        setLoading(false);
      })
      .catch(console.error);
  }, [page]);

  if (loading) return <div>Loading data...</div>;

  return (
    <div>
      <h2>📋 Registered Vehicles</h2>
      <table border="1" cellPadding="8" style={{ width: '100%', borderCollapse: 'collapse', marginBottom: '30px' }}>
        <thead><tr><th>Plate</th><th>Owner</th><th>Owner ID</th><th>Type</th><th>Reg Date</th></tr></thead>
        <tbody>
          {vehicles.map(v => (
            <tr key={v.plate_number}>
              <td>{v.plate_number}</td><td>{v.owner_name}</td><td>{v.owner_id}</td><td>{v.vehicle_type}</td><td>{v.registration_date}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <h2>📄 Challan History</h2>
      <table border="1" cellPadding="8" style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead><tr><th>ID</th><th>Plate</th><th>Amount</th><th>Violation</th><th>Date</th><th>Paid</th></tr></thead>
        <tbody>
          {challans.map(c => (
            <tr key={c.challan_id}>
              <td>{c.challan_id}</td><td>{c.plate_number}</td><td>₹{c.amount}</td><td>{c.violation_type}</td><td>{c.date}</td>
              <td>{c.paid_status ? '✅' : '❌'}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <div style={{ marginTop: '20px' }}>
        <button onClick={() => setPage(p => Math.max(1, p-1))}>Previous</button>
        <span style={{ margin: '0 10px' }}>Page {page}</span>
        <button onClick={() => setPage(p => p+1)}>Next</button>
      </div>
    </div>
  );
}

export default DataTables;