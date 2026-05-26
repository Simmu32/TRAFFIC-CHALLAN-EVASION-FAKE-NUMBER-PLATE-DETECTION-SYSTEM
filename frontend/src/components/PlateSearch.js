import React, { useState } from 'react';
import { searchPlate } from '../services/api';

function PlateSearch() {
  const [partial, setPartial] = useState('');
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    setLoading(true);
    try {
      const res = await searchPlate(partial);
      setMatches(res.data.data.matches);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>🔎 KMP Partial Plate Search</h2>
      <div>
        <input 
          type="text" 
          placeholder="Enter partial plate (e.g., MH12)"
          value={partial}
          onChange={(e) => setPartial(e.target.value.toUpperCase())}
        />
        <button onClick={handleSearch}>Search</button>
      </div>
      {loading && <p>Searching...</p>}
      {matches.length > 0 && (
        <div className="card">
          <p><strong>{matches.length}</strong> matching plate(s):</p>
          <ul>
            {matches.map(m => <li key={m}>{m}</li>)}
          </ul>
        </div>
      )}
      {matches.length === 0 && !loading && partial && <p>No matches found.</p>}
    </div>
  );
}

export default PlateSearch;