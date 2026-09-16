/**
 * ResearchAtlas - Research Papers API Client
 * 
 * API client for research publication management.
 * Supports all 4 platforms: ORCID, Scopus, Google Scholar, Web of Science.
 */

import apiClient from './apiClient';

/**
 * Fetch publications from any platform for a faculty member
 * @param {string} facultyId - Faculty member ID
 * @param {string} platform - Platform name (ORCID, Scopus, Google Scholar, Web of Science)
 * @param {Object} identifiers - Platform-specific identifiers
 * @returns {Promise} Fetch result with publications
 */
export const fetchPublications = async (facultyId, platform, identifiers) => {
  const response = await apiClient.post(`/api/research-papers/faculty/${facultyId}/fetch`, {
    platform,
    identifiers
  });
  return response.data;
};

/**
 * Fetch publications from ORCID for a faculty member
 * @param {string} facultyId - Faculty member ID
 * @returns {Promise} Fetch result with publications
 */
export const fetchOrcidPublications = async (facultyId) => {
  const response = await apiClient.post(`/api/research-papers/faculty/${facultyId}/fetch/orcid`);
  return response.data;
};

/**
 * Get publications for a faculty member with optional filters
 * @param {string} facultyId - Faculty member ID
 * @param {Object} params - Query parameters (source, work_type, year, month, date, search)
 * @returns {Promise} Publications list
 */
export const getFacultyPublications = async (facultyId, params = {}) => {
  const response = await apiClient.get(`/api/research-papers/faculty/${facultyId}`, { params });
  return response.data;
};

/**
 * Get publication statistics for a faculty member
 * @param {string} facultyId - Faculty member ID
 * @returns {Promise} Statistics object
 */
export const getPublicationStatistics = async (facultyId) => {
  const response = await apiClient.get(`/api/research-papers/faculty/${facultyId}/statistics`);
  return response.data;
};

/**
 * Get available work types for a faculty member
 * @param {string} facultyId - Faculty member ID
 * @returns {Promise} Work types list
 */
export const getFacultyWorkTypes = async (facultyId) => {
  const response = await apiClient.get(`/api/research-papers/faculty/${facultyId}/work-types`);
  return response.data;
};

/**
 * Get available publication years for a faculty member
 * @param {string} facultyId - Faculty member ID
 * @returns {Promise} Years list
 */
export const getFacultyPublicationYears = async (facultyId) => {
  const response = await apiClient.get(`/api/research-papers/faculty/${facultyId}/years`);
  return response.data;
};
