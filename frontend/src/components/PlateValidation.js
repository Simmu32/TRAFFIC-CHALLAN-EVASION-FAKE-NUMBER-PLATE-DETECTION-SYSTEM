import React, { useState } from 'react';
import { validatePlate } from '../services/api';

function PlateValidation() {
  const [plate, setPlate] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleValidate = async () => {
    setError('');
    try {
      const res = await validatePlate(plate);
      setResult(res.data.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Validation failed');
    }
  };

  return (
    <div>
      <h2>🔍 Indian Plate Validation (Pattern Matching)</h2>
      <div>
        <input 
          type="text" 
          placeholder="Enter plate number e.g., MH12AB1234"
          value={plate}
          onChange={(e) => setPlate(e.target.value.toUpperCase())}
        />
        <button onClick={handleValidate}>Validate</button>
      </div>
      {error && <div className="error">{error}</div>}
      {result && (
        <div className="card">
          <p><strong>Format Valid:</strong> {result.format_valid ? '✅ Yes' : '❌ No'}</p>
          <p><strong>Character Valid:</strong> {result.character_valid ? '✅ Yes' : '❌ No'} - {result.character_message}</p>
          <p><strong>Fake Patterns:</strong> {result.fake_patterns.length ? result.fake_patterns.join(', ') : 'None detected'}</p>
        </div>
      )}
    </div>
  );
}

export default PlateValidation;