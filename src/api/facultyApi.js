/**
 * ResearchAtlas - Faculty Management API Module
 * 
 * Admin faculty management operations.
 * Future prompts will extend this with research profiles, publications, etc.
 */

import apiClient from './apiClient';

/**
 * Get all faculty members (Admin only)
 * @returns {Promise} List of all faculty
 */
export const getAllFaculty = async () => {
  const response = await apiClient.get('/api/faculty/');
  return response.data;
};

/**
 * Get a single faculty member by ID (Admin only)
 * @param {string} facultyId - Faculty user ID
 * @returns {Promise} Faculty data
 */
export const getFacultyById = async (facultyId) => {
  const response = await apiClient.get(`/api/faculty/${facultyId}`);
  return response.data;
};

/**
 * Create a new faculty member (Admin only)
 * @param {Object} facultyData - Faculty data
 * @returns {Promise} Created faculty
 */
export const createFaculty = async (facultyData) => {
  const response = await apiClient.post('/api/faculty/', facultyData);
  return response.data;
};

/**
 * Update a faculty member (Admin only)
 * @param {string} facultyId - Faculty user ID
 * @param {Object} facultyData - Updated data
 * @returns {Promise} Updated faculty
 */
export const updateFaculty = async (facultyId, facultyData) => {
  const response = await apiClient.put(`/api/faculty/${facultyId}`, facultyData);
  return response.data;
};

/**
 * Activate/deactivate a faculty member (Admin only)
 * @param {string} facultyId - Faculty user ID
 * @param {boolean} isActive - Active status
 * @returns {Promise} Updated faculty
 */
export const toggleFacultyStatus = async (facultyId, isActive) => {
  const response = await apiClient.patch(`/api/faculty/${facultyId}/status`, {
    is_active: isActive,
  });
  return response.data;
};

/**
 * Delete a faculty member (Admin only)
 * @param {string} facultyId - Faculty user ID
 * @returns {Promise} Deletion confirmation
 */
export const deleteFaculty = async (facultyId) => {
  const response = await apiClient.delete(`/api/faculty/${facultyId}`);
  return response.data;
};
