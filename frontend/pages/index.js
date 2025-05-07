import { useState, useEffect } from 'react';
import axios from 'axios';

export default function Home() {
  const [status, setStatus] = useState('Loading...');
  const [syncStatus, setSyncStatus] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [emails, setEmails] = useState([]);
  const [emailLimit, setEmailLimit] = useState(10);
  const [darkMode, setDarkMode] = useState(false);

  const API_BASE = 'http://localhost:8000';

  useEffect(() => {
    checkHealth();
    // Load dark mode preference from localStorage if available
    const savedMode = localStorage.getItem('darkMode');
    if (savedMode !== null) {
      setDarkMode(savedMode === 'true');
    }
  }, []);

  // Update document body when dark mode changes
  useEffect(() => {
    if (darkMode) {
      document.body.classList.add('dark-mode');
    } else {
      document.body.classList.remove('dark-mode');
    }
    // Save preference
    localStorage.setItem('darkMode', darkMode.toString());
  }, [darkMode]);

  const checkHealth = async () => {
    try {
      const response = await axios.get(`${API_BASE}/health`);
      setStatus(response.data.status);
      setError('');
    } catch (error) {
      console.error('Backend connection error:', error);
      setStatus('Error connecting to backend');
      setError('Make sure your backend is running on http://localhost:8000');
    }
  };

  const handleSync = async () => {
    setIsLoading(true);
    setSyncStatus('Syncing emails...');
    setEmails([]);
    
    try {
      // Using the correct endpoint from the backend with the limit parameter
      const response = await axios.get(`${API_BASE}/sync/emails`, {
        params: { limit: emailLimit }
      });
      
      if (response.data.emails && response.data.emails.length > 0) {
        setEmails(response.data.emails);
        setSyncStatus(`Success! Synced ${response.data.emails.length} emails`);
      } else {
        setSyncStatus('No emails found or returned');
      }
      setError('');
    } catch (error) {
      console.error('Sync error:', error);
      setSyncStatus('Failed to sync emails');
      setError(error.response?.data?.detail || 'Error communicating with backend');
    } finally {
      setIsLoading(false);
    }
  };

  // Dark mode styles
  const styles = {
    container: {
      padding: '40px', 
      maxWidth: '800px', 
      margin: '0 auto',
      transition: 'all 0.2s ease',
      backgroundColor: darkMode ? '#1a1a1a' : '#ffffff',
      minHeight: '100vh',
    },
    card: {
      marginTop: '20px', 
      padding: '15px', 
      backgroundColor: darkMode ? '#333333' : '#f4f4f4', 
      borderRadius: '5px',
      transition: 'all 0.2s ease',
    },
    button: {
      padding: '10px 15px',
      backgroundColor: status === 'healthy' ? (darkMode ? '#2196f3' : '#0070f3') : '#555',
      color: 'white',
      border: 'none',
      borderRadius: '5px',
      cursor: status === 'healthy' ? 'pointer' : 'not-allowed',
      transition: 'all 0.2s ease',
    },
    input: {
      padding: '8px',
      borderRadius: '4px',
      border: darkMode ? '1px solid #555' : '1px solid #ccc',
      backgroundColor: darkMode ? '#444' : '#fff',
      color: darkMode ? '#f0f0f0' : '#333',
      width: '70px',
      transition: 'all 0.2s ease',
    },
    emailCard: {
      border: darkMode ? '1px solid #444' : '1px solid #eaeaea',
      padding: '15px',
      marginBottom: '10px',
      borderRadius: '5px',
      backgroundColor: darkMode ? '#2d2d2d' : '#fff',
      transition: 'all 0.2s ease',
    },
    toggleBtn: {
      position: 'absolute',
      top: '20px',
      right: '20px',
      padding: '8px 12px',
      backgroundColor: darkMode ? '#f0f0f0' : '#333',
      color: darkMode ? '#333' : '#f0f0f0',
      border: 'none',
      borderRadius: '5px',
      cursor: 'pointer',
      display: 'flex',
      alignItems: 'center',
      gap: '6px',
      transition: 'all 0.2s ease',
    }
  };

  return (
    <div style={{...styles.container, position: 'relative'}}>
      <button 
        style={styles.toggleBtn}
        onClick={() => setDarkMode(!darkMode)}
      >
        {darkMode ? '☀️ Light' : '🌙 Dark'}
      </button>

      <h1>ME-RU - AI Email Agent</h1>
      <p>An AI-powered email assistant that fetches and analyzes your emails</p>
      
      <div style={styles.card}>
        <h2>Backend Status</h2>
        <p>Status: {status}</p>
        {error && <p style={{ color: darkMode ? '#ff6b6b' : 'red' }}>{error}</p>}
      </div>
      
      <div style={styles.card}>
        <h2>Actions</h2>
        
        <div style={{ marginBottom: '15px', display: 'flex', alignItems: 'center' }}>
          <label htmlFor="emailLimit" style={{ marginRight: '10px' }}>Number of emails to fetch:</label>
          <input
            id="emailLimit"
            type="number"
            min="1"
            max="50"
            value={emailLimit}
            onChange={(e) => setEmailLimit(Math.min(50, Math.max(1, parseInt(e.target.value) || 1)))}
            style={styles.input}
          />
        </div>
        
        <button 
          onClick={handleSync}
          disabled={isLoading || status !== 'healthy'}
          style={styles.button}
        >
          {isLoading ? 'Syncing...' : 'Sync Emails'}
        </button>
        
        {syncStatus && (
          <p style={{ marginTop: '10px' }}>{syncStatus}</p>
        )}
      </div>

      {emails.length > 0 && (
        <div style={{ marginTop: '30px' }}>
          <h2>Recent Emails</h2>
          <div style={{ maxHeight: '400px', overflowY: 'auto' }}>
            {emails.map((email, index) => (
              <div key={index} style={styles.emailCard}>
                <h3>{email.subject || 'No Subject'}</h3>
                <p><strong>From:</strong> {email.from}</p>
                <p><strong>Date:</strong> {email.date}</p>
                <p>{email.snippet || 'No preview available'}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
} 