/**
 * ResearchAtlas - Authentication Context
 * 
 * Central authentication state management.
 * All future pages and components use this context.
 * Manages: currentUser, token, role, isAuthenticated, loading state.
 */

import React, { createContext, useState, useEffect, useCallback } from 'react';
import { getCurrentUser as fetchCurrentUser, logout as apiLogout } from '../api/authApi';

export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [token, setToken] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  /**
   * Initialize auth state from localStorage on mount
   */
  useEffect(() => {
    const initializeAuth = async () => {
      const storedToken = localStorage.getItem('token');
      const storedUser = localStorage.getItem('user');

      if (storedToken && storedUser) {
        try {
          setToken(storedToken);
          const parsedUser = JSON.parse(storedUser);
          setCurrentUser(parsedUser);
          setIsAuthenticated(true);

          // Verify token is still valid by fetching current user
          try {
            const userData = await fetchCurrentUser();
            setCurrentUser(userData);
            localStorage.setItem('user', JSON.stringify(userData));
          } catch (error) {
            // Token invalid - clear everything
            handleLogout();
          }
        } catch (error) {
          handleLogout();
        }
      }
      setLoading(false);
    };

    initializeAuth();
  }, []);

  /**
   * Login handler - stores token and user data
   */
  const handleLogin = useCallback((loginData) => {
    const { access_token, user } = loginData;
    
    localStorage.setItem('token', access_token);
    localStorage.setItem('user', JSON.stringify(user));
    
    setToken(access_token);
    setCurrentUser(user);
    setIsAuthenticated(true);
  }, []);

  /**
   * Logout handler - clears all auth state
   */
  const handleLogout = useCallback(() => {
    apiLogout();
    setToken(null);
    setCurrentUser(null);
    setIsAuthenticated(false);
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  }, []);

  /**
   * Update current user data (e.g., after profile update)
   */
  const updateUser = useCallback((userData) => {
    setCurrentUser(userData);
    localStorage.setItem('user', JSON.stringify(userData));
  }, []);

  const value = {
    currentUser,
    token,
    role: currentUser?.role || null,
    isAuthenticated,
    loading,
    login: handleLogin,
    logout: handleLogout,
    updateUser,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
