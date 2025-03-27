// App.js - Updated with Error Boundary
import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';

// Importing Application Components
import Home from './components/Home';
import Userprofile from './components/Userprofile';
import Login from './components/Login';
import Register from './components/Register';
import ForgotPassword from './components/ForgotPassword';
import ResetPassword from './components/ResetPassword';
import Leaderboard from './components/Leaderboard';
import Homeboard from './components/Homeboard';
import BingoBoard from './components/BingoBoard';
import Upload from './components/Upload';
import Scan from './components/Scan';

import PrivacyPolicy from './components/PrivacyPolicy';
import Overview from './components/Overview';
import BingoPatterns from './components/BingoPatterns';
import ErrorBoundary from './components/ErrorBoundary';

// Import Notification System
import NotificationManager from './components/NotificationManager';
import PopupManager from './components/PopupManager';
import GameKeeperNew from './components/GameKeeperNew';

const App = () => {
  return (
    <div>
      {/* Global Notification and Popup Managers */}
      <NotificationManager />
      <PopupManager />

      <Routes>
        {/* Home Route */}
        <Route path="/" element={<Home />} />

        {/* User Profile Page */}
        <Route path="/userprofile" element={<Userprofile />} />

        {/* Authentication Routes */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/reset-password/:token" element={<ResetPassword />} />

        {/* Leaderboard Routes */}
        <Route path="/leaderboard" element={<Leaderboard />} />
        
        {/* Other Game Features Routes */}
        <Route path="/homeboard" element={<Homeboard />} />
        <Route path="/privacy-policy" element={<PrivacyPolicy />} />
        <Route path="/bingo" element={<BingoBoard />} />
        <Route path="/upload" element={<Upload />} />
        
        <Route path="/gamekeeper" element={<GameKeeperNew />} />
        <Route path="/test-route" element={<div>Simple test route</div>} />
        
        {/* Alternative GameKeeper route with a different path */}
        <Route path="/gk" element={
  <ErrorBoundary>
    <GameKeeperNew />
  </ErrorBoundary>
} />
        
        <Route path="/scan" element={<Scan />} />
        <Route path="/overview" element={<Overview />} />
        <Route path="/patterns" element={<BingoPatterns />} />

        {/* Developer Dashboard - Restricted Access */}
        <Route
          path="/developer-dashboard"
          element={
            localStorage.getItem('userProfile') === 'Developer'
              ? <iframe
                  src="/developer-front.html"
                  title="Developer Dashboard"
                  style={{ width: '100%', height: '100vh', border: 'none' }}
                />
              : <Navigate to="/login" /> // Redirect to login if user is not a developer
          }
        />
      </Routes>
    </div>
  );
};

export default App;