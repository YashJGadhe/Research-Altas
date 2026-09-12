/**
 * ResearchAtlas - User Management API Module
 * 
 * Admin-only user management operations.
 * All endpoints require admin authorization.
 */

import apiClient from './apiClient';

/**
 * Get all users (Admin only)
 * @returns {Promise} List of all users
 */
export const getAllUsers = async () => {
  const response = await apiClient.get('/api/users/');
  return response.data;
};

/**
 * Get a single user by ID (Admin only)
 * @param {string} userId - User ID
 * @returns {Promise} User data
 */
export const getUserById = async (userId) => {
  const response = await apiClient.get(`/api/users/${userId}`);
  return response.data;
};

/**
 * Update a user (Admin only)
 * @param {string} userId - User ID
 * @param {Object} userData - Updated user data
 * @returns {Promise} Updated user
 */
export const updateUser = async (userId, userData) => {
  const response = await apiClient.put(`/api/users/${userId}`, userData);
  return response.data;
};

/**
 * Delete a user (Admin only)
 * @param {string} userId - User ID
 * @returns {Promise} Deletion confirmation
 */
export const deleteUser = async (userId) => {
  const response = await apiClient.delete(`/api/users/${userId}`);
  return response.data;
};
