/**
 * ResearchAtlas - Citation API Client
 * 
 * API client for citation management operations.
 */

import apiClient from './apiClient';

/**
 * Get all citation records
 */
export const getAllCitations = async () => {
  const response = await apiClient.get('/api/citations/');
  return response.data;
};

/**
 * Get citation record by ID
 */
export const getCitationById = async (recordId) => {
  const response = await apiClient.get(`/api/citations/${recordId}`);
  return response.data;
};

/**
 * Get citation record by faculty ID
 */
export const getCitationByFacultyId = async (facultyId) => {
  const response = await apiClient.get(`/api/citations/faculty/${facultyId}`);
  return response.data;
};

/**
 * Update citation record manually
 */
export const updateCitation = async (recordId, updateData) => {
  const response = await apiClient.put(`/api/citations/${recordId}`, updateData);
  return response.data;
};

/**
 * Get citation history for a record
 */
export const getCitationHistory = async (recordId) => {
  const response = await apiClient.get(`/api/citations/${recordId}/history`);
  return response.data;
};

/**
 * Fetch ORCID data for a faculty member
 */
export const fetchOrcidData = async (recordId) => {
  const response = await apiClient.post(`/api/citations/${recordId}/fetch/orcid`);
  return response.data;
};

/**
 * Get fetch logs
 */
export const getFetchLogs = async (facultyId = null, limit = 50) => {
  const params = { limit };
  if (facultyId) {
    params.faculty_id = facultyId;
  }
  const response = await apiClient.get('/api/citations/logs/fetch', { params });
  return response.data;
};
