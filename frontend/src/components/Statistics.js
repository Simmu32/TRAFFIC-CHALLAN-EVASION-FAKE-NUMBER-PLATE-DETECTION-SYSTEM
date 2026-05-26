import React, { useEffect, useState } from 'react';
import { Bar, Pie, Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement } from 'chart.js';
import { getStatsViolations, getStatsPayment, getStatsStates } from '../services/api';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement);

function Statistics() {
  const [violations, setViolations] = useState([]);
  const [payment, setPayment] = useState([]);
  const [states, setStates] = useState([]);

  useEffect(() => {
    Promise.all([getStatsViolations(), getStatsPayment(), getStatsStates()])
      .then(([vRes, pRes, sRes]) => {
        setViolations(vRes.data.data);
        setPayment(pRes.data.data);
        setStates(sRes.data.data);
      });
  }, []);

  const violationChart = {
    labels: violations.map(v => v.violation_type),
    datasets: [{ label: 'Count', data: violations.map(v => v.cnt), backgroundColor: '#2a5298' }]
  };

  const paymentChart = {
    labels: payment.map(p => p.paid_status ? 'Paid' : 'Unpaid'),
    datasets: [{ data: payment.map(p => p['COUNT(*)']), backgroundColor: ['#4caf50', '#f44336'] }]
  };

  const stateChart = {
    labels: states.slice(0, 10).map(s => s.state),
    datasets: [{ label: 'Vehicles', data: states.slice(0,10).map(s => s['COUNT(*)']), backgroundColor: '#ff9800' }]
  };

  return (
    <div>
      <h2>📈 Statistics & Hypothesis Testing</h2>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '20px' }}>
        <div className="card" style={{ flex: 1 }}>
          <h3>Violation Types</h3>
          <Bar data={violationChart} />
        </div>
        <div className="card" style={{ flex: 1 }}>
          <h3>Payment Status</h3>
          <Pie data={paymentChart} />
        </div>
      </div>
      <div className="card">
        <h3>Top 10 States by Registered Vehicles</h3>
        <Bar data={stateChart} />
      </div>
    </div>
  );
}

export default Statistics;