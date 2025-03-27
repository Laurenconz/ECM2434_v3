// components/GameKeeper.js - Simplified test version
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
// Import the CSS only after you confirm basic rendering works
// import './GameKeeper.css';

const GameKeeper = () => {
  const navigate = useNavigate();

  useEffect(() => {
    console.log("GameKeeper component mounted successfully");
    document.title = "GameKeeper Dashboard";
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('userProfile');
    navigate('/login');
  };

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center', 
        marginBottom: '20px' 
      }}>
        <h1 style={{ color: '#5E318A' }}>BINGO Game - Game Keeper Dashboard</h1>
        <button onClick={handleLogout} style={{ 
          backgroundColor: '#5E318A',
          color: 'white',
          border: 'none',
          padding: '8px 16px',
          borderRadius: '4px',
          cursor: 'pointer'
        }}>
          Logout
        </button>
      </div>
      
      <div style={{ 
        padding: '15px', 
        border: '1px solid #ddd', 
        borderRadius: '4px',
        backgroundColor: 'white',
        marginBottom: '20px'
      }}>
        <h2 style={{ color: '#5E318A' }}>React Component Test</h2>
        <p>If you can see this message, the React component is rendering correctly.</p>
      </div>
    </div>
  );
};

export default GameKeeper;