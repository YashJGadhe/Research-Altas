/**
 * ResearchAtlas - useAuth Hook
 * 
 * Reusable hook for accessing authentication state and actions.
 * All future pages should use this hook instead of directly accessing AuthContext.
 * 
 * Usage:
 *   const { currentUser, role, isAuthenticated, login, logout } = useAuth();
 */

import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';

export const useAuth = () => {
  const context = useContext(AuthContext);
  
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  
  return context;
};

export default useAuth;
