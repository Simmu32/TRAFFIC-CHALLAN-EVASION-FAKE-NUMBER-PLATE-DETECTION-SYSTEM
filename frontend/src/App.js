import React, { useState, useEffect } from 'react';
import './App.css';
import Dashboard from './components/Dashboard';
import PlateValidation from './components/PlateValidation';
import PlateSearch from './components/PlateSearch';
import OwnershipGraphView from './components/OwnershipGraphView';
import CameraOptimization from './components/CameraOptimization';
import Statistics from './components/Statistics';
import DataTables from './components/DataTables';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');

  return (
    <div className="App">
      <header className="app-header">
        <h1>🚦 Traffic Challan System</h1>
        <p>Indian Vehicle Number Plate Analysis & Enforcement</p>
      </header>
      <div className="tabs">
        <button className={activeTab === 'dashboard' ? 'active' : ''} onClick={() => setActiveTab('dashboard')}>Dashboard</button>
        <button className={activeTab === 'validate' ? 'active' : ''} onClick={() => setActiveTab('validate')}>Plate Validation</button>
        <button className={activeTab === 'search' ? 'active' : ''} onClick={() => setActiveTab('search')}>KMP Search</button>
        <button className={activeTab === 'ownership' ? 'active' : ''} onClick={() => setActiveTab('ownership')}>Ownership Graph</button>
        <button className={activeTab === 'cameras' ? 'active' : ''} onClick={() => setActiveTab('cameras')}>Camera Optimization</button>
        <button className={activeTab === 'stats' ? 'active' : ''} onClick={() => setActiveTab('stats')}>Statistics</button>
        <button className={activeTab === 'data' ? 'active' : ''} onClick={() => setActiveTab('data')}>Data Tables</button>
      </div>
      <div className="content">
        {activeTab === 'dashboard' && <Dashboard />}
        {activeTab === 'validate' && <PlateValidation />}
        {activeTab === 'search' && <PlateSearch />}
        {activeTab === 'ownership' && <OwnershipGraphView />}
        {activeTab === 'cameras' && <CameraOptimization />}
        {activeTab === 'stats' && <Statistics />}
        {activeTab === 'data' && <DataTables />}
      </div>
    </div>
  );
}

export default App;