/**
 * ResearchAtlas - Research Papers API Client
 * 
 * API client for research publication management.
 */

import apiClient from './apiClient';

/**
 * Fetch publications from ORCID for a faculty member
 */
export const fetchOrcidPublications = async (facultyId) => {
  const response = await apiClient.post(`/api/research-papers/faculty/${facultyId}/fetch/orcid`);
  return response.data;
};

/**
 * Get publications for a faculty member with optional filters
 */
export const getFacultyPublications = async (facultyId, params = {}) => {
  const response = await apiClient.get(`/api/research-papers/faculty/${facultyId}`, { params });
  return response.data;
};

/**
 * Get publication statistics for a faculty member
 */
export const getPublicationStatistics = async (facultyId) => {
  const response = await apiClient.get(`/api/research-papers/faculty/${facultyId}/statistics`);
  return response.data;
};

/**
 * Get available work types for a faculty member
 */
export const getFacultyWorkTypes = async (facultyId) => {
  const response = await apiClient.get(`/api/research-papers/faculty/${facultyId}/work-types`);
  return response.data;
};

/**
 * Get available publication years for a faculty member
 */
export const getFacultyPublicationYears = async (facultyId) => {
  const response = await apiClient.get(`/api/research-papers/faculty/${facultyId}/years`);
  return response.data;
};
