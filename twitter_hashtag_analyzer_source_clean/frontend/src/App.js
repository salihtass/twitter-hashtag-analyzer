import React, { useState, useEffect } from 'react';
import axios from 'axios';

// Import components
import Dashboard from './components/Dashboard';

function App() {
  const [isBackendConnected, setIsBackendConnected] = useState(false);
  const [backendStatus, setBackendStatus] = useState('Checking connection...');

  // This would be used in a real implementation to check backend connectivity
  // For now, we'll simulate a successful connection after a delay
  useEffect(() => {
    const checkBackendConnection = async () => {
      try {
        // In a real implementation, this would be an actual API endpoint
        // await axios.get('/api/status');
        
        // Simulate API call delay
        setTimeout(() => {
          setIsBackendConnected(true);
          setBackendStatus('Connected to backend successfully');
        }, 1500);
      } catch (error) {
        setIsBackendConnected(false);
        setBackendStatus('Failed to connect to backend. Using mock data.');
        console.error('Backend connection error:', error);
      }
    };

    checkBackendConnection();
  }, []);

  return (
    <div className="App">
      {!isBackendConnected && (
        <div className="backend-status-banner">
          {backendStatus}
        </div>
      )}
      <Dashboard />
    </div>
  );
}

export default App;
