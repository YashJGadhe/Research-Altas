/**
 * ResearchAtlas - Authentication API Module
 * 
 * Handles all authentication-related API calls.
 * Uses the centralized apiClient for all requests.
 * Falls back to mock API in demo mode or when backend is unavailable.
 */

import apiClient from './apiClient';
import { mockLogin, mockRegister, mockGetCurrentUser, isDemoMode, enableDemoMode } from './mockApi';

/**
 * Register a new user
 * @param {Object} userData - { full_name, email, password, confirm_password, role, department, orcid_id, scopus_id, wos_id }
 * @returns {Promise} Registration response
 */
export const register = async (userData) => {
  // Use mock API in demo mode
  if (isDemoMode()) {
    return await mockRegister(userData);
  }

  try {
    const response = await apiClient.post('/api/auth/register', {
      full_name: userData.full_name,
      email: userData.email,
      password: userData.password,
      confirm_password: userData.confirm_password,
      role: userData.role,
      department: userData.department,
      orcid_id: userData.orcid_id,
      scopus_id: userData.scopus_id,
      wos_id: userData.wos_id,
    });
    return response.data;
  } catch (error) {
    // If backend is not available, fall back to mock
    if (error.code === 'ERR_NETWORK' || !error.response || error.message.includes('Network Error')) {
      console.log('Backend not available, enabling demo mode');
      enableDemoMode();
      return await mockRegister(userData);
    }
    throw error;
  }
};

/**
 * Login user
 * @param {Object} credentials - { email, password }
 * @returns {Promise} Login response with token and user info
 */
export const login = async (credentials) => {
  // Use mock API in demo mode
  if (isDemoMode()) {
    console.log('Using demo mode for login');
    return await mockLogin(credentials.email, credentials.password);
  }

  try {
    const response = await apiClient.post('/api/auth/login', {
      email: credentials.email,
      password: credentials.password,
    });
    return response.data;
  } catch (error) {
    // If backend is not available, fall back to mock
    if (error.code === 'ERR_NETWORK' || !error.response || error.message.includes('Network Error')) {
      console.log('Backend not available, enabling demo mode');
      enableDemoMode();
      return await mockLogin(credentials.email, credentials.password);
    }
    throw error;
  }
};

/**
 * Get current authenticated user
 * @returns {Promise} Current user data
 */
export const getCurrentUser = async () => {
  // Use mock API in demo mode
  if (isDemoMode()) {
    return await mockGetCurrentUser();
  }

  try {
    const response = await apiClient.get('/api/auth/me');
    return response.data;
  } catch (error) {
    // If backend is not available, fall back to mock
    if (error.code === 'ERR_NETWORK' || !error.response || error.message.includes('Network Error')) {
      console.log('Backend not available, using demo mode');
      enableDemoMode();
      return await mockGetCurrentUser();
    }
    throw error;
  }
};

/**
 * Logout - handled client-side by clearing tokens
 * Backend can optionally blacklist tokens in the future
 */
export const logout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
  // Keep demo mode enabled for next login
};
