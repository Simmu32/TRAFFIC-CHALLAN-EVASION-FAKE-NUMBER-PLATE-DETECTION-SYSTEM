import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import { getCameraOptimization, getCameraCostBenefit } from '../services/api';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

function CameraOptimization() {
  const [optData, setOptData] = useState(null);
  const [costBenefit, setCostBenefit] = useState(null);

  useEffect(() => {
    getCameraOptimization().then(res => setOptData(res.data.data));
    getCameraCostBenefit().then(res => setCostBenefit(res.data.data));
  }, []);

  if (!optData) return <div>Loading camera optimization...</div>;

  return (
    <div>
      <h2>📷 Greedy Set Cover – Camera Placement</h2>
      <div className="card">
        <p><strong>Optimal Cameras:</strong> {optData.num_cameras}</p>
        <p><strong>Coverage:</strong> {optData.coverage_percentage.toFixed(2)}% of intersections</p>
        <p><strong>Uncovered Intersections:</strong> {optData.uncovered_intersections.length}</p>
      </div>
      {costBenefit && (
        <div className="card">
          <h3>💰 Cost-Benefit Analysis</h3>
          <p>Total Cost: ₹{costBenefit.total_cost.toLocaleString()}</p>
          <p>Estimated Benefit: ₹{costBenefit.estimated_benefit.toLocaleString()}</p>
          <p>ROI: {costBenefit.roi.toFixed(2)}</p>
        </div>
      )}
      <div style={{ height: '500px', marginTop: '20px' }}>
        <MapContainer center={[12.935, 77.617]} zoom={12} style={{ height: '100%', width: '100%' }}>
          <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
          {optData.selected_cameras?.map(cam => (
            <Marker key={cam.camera_id} position={[cam.latitude, cam.longitude]}>
              <Popup>Camera {cam.camera_id}<br />Radius: {cam.radius}km</Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>
    </div>
  );
}

export default CameraOptimization;