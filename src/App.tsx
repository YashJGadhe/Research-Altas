/**
 * ResearchAtlas - Main Application Component
 * 
 * Entry point that sets up providers and routing.
 * AuthProvider wraps the entire application for global auth state.
 * BrowserRouter handles client-side routing.
 */

import React from 'react';
import { BrowserRouter } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import AppRoutes from './routes/AppRoutes';

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
