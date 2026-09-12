/**
 * ResearchAtlas - Authentication API Module
 * 
 * Handles all authentication-related API calls.
 * Uses the centralized apiClient for all requests.
 */

import apiClient from './apiClient';

/**
 * Register a new user
 * @param {Object} userData - { full_name, email, password, confirm_password, role, department }
 * @returns {Promise} Registration response
 */
export const register = async (userData) => {
  const response = await apiClient.post('/api/auth/register', {
    full_name: userData.full_name,
    email: userData.email,
    password: userData.password,
    confirm_password: userData.confirm_password,
    role: userData.role,
    department: userData.department,
  });
  return response.data;
};

/**
 * Login user
 * @param {Object} credentials - { email, password }
 * @returns {Promise} Login response with token and user info
 */
export const login = async (credentials) => {
  const response = await apiClient.post('/api/auth/login', {
    email: credentials.email,
    password: credentials.password,
  });
  return response.data;
};

/**
 * Get current authenticated user
 * @returns {Promise} Current user data
 */
export const getCurrentUser = async () => {
  const response = await apiClient.get('/api/auth/me');
  return response.data;
};

/**
 * Logout - handled client-side by clearing tokens
 * Backend can optionally blacklist tokens in the future
 */
export const logout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
};
