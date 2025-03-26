// components/GameKeeper.js
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
// Don't import the CSS yet to rule out CSS issues
// import './GameKeeper.css';

const GameKeeper = () => {
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    // Log to verify this component is actually being rendered
    console.log("GameKeeper component mounted");
    document.title = "GameKeeper Dashboard";
  }, []);

  // Simple logout function
  const handleLogout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('userProfile');
    navigate('/login');
  };

  return (
    <div style={{ 
      padding: '20px', 
      maxWidth: '1200px', 
      margin: '0 auto',
      fontFamily: 'Segoe UI, Tahoma, Geneva, Verdana, sans-serif'
    }}>
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center',
        marginBottom: '20px'
      }}>
        <h1 style={{ color: '#5E318A', fontWeight: 'bold' }}>BINGO Game - Game Keeper Dashboard</h1>
        <button 
          onClick={handleLogout}
          style={{
            backgroundColor: '#5E318A',
            color: 'white',
            border: 'none',
            padding: '8px 16px',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          Logout
        </button>
      </div>

      {error && <div style={{ color: 'red', marginBottom: '20px' }}>{error}</div>}
      
      {loading ? (
        <p>Loading dashboard...</p>
      ) : (
        <div style={{ marginTop: '20px', padding: '15px', border: '1px solid #ddd', borderRadius: '4px' }}>
          <h2 style={{ color: '#5E318A' }}>Dashboard Content</h2>
          <p>This is a simplified version of the GameKeeper dashboard.</p>
          <p>Once this renders correctly, we can add more functionality.</p>
        </div>
      )}
    </div>
  );
};

export default GameKeeper;