import React, { useEffect, useRef, useState } from 'react';
import { getOwnershipGraph, checkOwnership } from '../services/api';
import cytoscape from 'cytoscape';
import dagre from 'cytoscape-dagre';

cytoscape.use(dagre);

function OwnershipGraphView() {
  const cyRef = useRef(null);
  const [ownerId, setOwnerId] = useState('');
  const [result, setResult] = useState(null);
  const [graphError, setGraphError] = useState(null);

  useEffect(() => {
    getOwnershipGraph()
      .then(res => {
        const graphData = res.data.data;
        if (!graphData || !graphData.nodes || !graphData.edges) {
          throw new Error('Invalid graph data: missing nodes or edges');
        }

        const elements = [];

        // Add nodes
        graphData.nodes.forEach(node => {
          elements.push({
            data: {
              id: node.id,
              label: node.id,
              type: node.node_type || 'unknown'
            }
          });
        });

        // Add edges (the backend returns "edges", not "links")
        graphData.edges.forEach(edge => {
          elements.push({
            data: {
              source: edge.source,
              target: edge.target,
              label: edge.relationship || 'edge'
            }
          });
        });

        if (!cyRef.current) {
          throw new Error('Graph container not ready');
        }

        const cy = cytoscape({
          container: cyRef.current,
          elements: elements,
          style: [
            {
              selector: 'node',
              style: {
                'background-color': ele => ele.data('type') === 'owner' ? '#2a5298' : '#4caf50',
                'label': 'data(label)',
                'color': '#fff',
                'font-size': '10px',
                'width': '40px',
                'height': '40px',
                'text-valign': 'center',
                'text-halign': 'center'
              }
            },
            {
              selector: 'edge',
              style: {
                'width': 2,
                'line-color': '#999',
                'target-arrow-color': '#999',
                'target-arrow-shape': 'triangle',
                'curve-style': 'bezier',
                'label': 'data(label)',
                'font-size': '8px'
              }
            }
          ],
          layout: {
            name: 'dagre',
            rankDir: 'TB',
            animate: true,
            spacingFactor: 1.5
          }
        });

        return () => cy.destroy();
      })
      .catch(err => {
        console.error('Graph error:', err);
        setGraphError(err.message);
      });
  }, []);

  const handleCheckOwnership = async () => {
    try {
      const res = await checkOwnership(ownerId);
      setResult(res.data.data);
    } catch (err) {
      console.error(err);
      alert('Error checking ownership. Check console for details.');
    }
  };

  return (
    <div>
      <h2>🕸️ Ownership Graph (BFS)</h2>
      {graphError && (
        <div style={{ color: 'red', marginBottom: '10px' }}>
          Error loading graph: {graphError}
        </div>
      )}
      <div
        ref={cyRef}
        style={{
          height: '500px',
          width: '100%',
          border: '1px solid #ccc',
          borderRadius: '8px',
          marginBottom: '20px',
          backgroundColor: '#fafafa'
        }}
      />
      <div className="card">
        <h3>Check Owner Suspiciousness</h3>
        <input
          type="text"
          placeholder="Owner ID (e.g., OWN1234)"
          value={ownerId}
          onChange={(e) => setOwnerId(e.target.value)}
        />
        <button onClick={handleCheckOwnership}>Analyze</button>
        {result && (
          <div style={{ marginTop: '10px' }}>
            <p>
              <strong>Connected Vehicles:</strong>{' '}
              {result.connected_vehicles.length
                ? result.connected_vehicles.join(', ')
                : 'None'}
            </p>
            <p>
              <strong>Suspicious:</strong>{' '}
              {result.suspicious.length
                ? result.suspicious.map((s) => s.reason).join(', ')
                : 'No'}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default OwnershipGraphView;