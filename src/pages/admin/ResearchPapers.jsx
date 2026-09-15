/**
 * ResearchAtlas - Research Papers Page
 * 
 * Admin page for viewing and managing faculty research publications.
 */

import React, { useState, useEffect } from 'react';
import { useAuth } from '../../hooks/useAuth';
import { getAllCitations } from '../../api/citationApi';
import {
  fetchOrcidPublications,
  getFacultyPublications,
  getPublicationStatistics,
  getFacultyWorkTypes
} from '../../api/researchPaperApi';
import AdminPageHeader from '../../components/admin/AdminPageHeader';
import { isDemoMode } from '../../api/mockApi';
import { MOCK_RESEARCH_PAPERS, MOCK_FETCH_RESULT, MOCK_STATISTICS } from '../../api/mockResearchPapers';

const ResearchPapers = () => {
  const { currentUser } = useAuth();
  
  // State management
  const [facultyList, setFacultyList] = useState([]);
  const [selectedFaculty, setSelectedFaculty] = useState('');
  const [selectedPlatform, setSelectedPlatform] = useState('ORCID');
  const [publications, setPublications] = useState([]);
  const [statistics, setStatistics] = useState(null);
  const [workTypes, setWorkTypes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [fetching, setFetching] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  
  // Filter state
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedWorkType, setSelectedWorkType] = useState('');
  const [sortBy, setSortBy] = useState('year_desc');
  
  // Fetch status
  const [fetchStatus, setFetchStatus] = useState(null);

  // Load faculty list on mount
  useEffect(() => {
    loadFacultyList();
  }, []);

  // Load publications when faculty changes
  useEffect(() => {
    if (selectedFaculty) {
      loadPublications();
      loadStatistics();
      loadWorkTypes();
    } else {
      setPublications([]);
      setStatistics(null);
      setWorkTypes([]);
    }
  }, [selectedFaculty]);

  // Reload publications when filters change
  useEffect(() => {
    if (selectedFaculty) {
      loadPublications();
    }
  }, [searchQuery, selectedWorkType, sortBy]);

  const loadFacultyList = async () => {
    try {
      setLoading(true);
      
      // Check if in demo mode
      if (isDemoMode()) {
        // Use mock faculty data
        const mockFaculty = Object.keys(MOCK_RESEARCH_PAPERS).map(facultyId => {
          const papers = MOCK_RESEARCH_PAPERS[facultyId];
          const firstPaper = papers[0];
          return {
            id: facultyId,
            name: firstPaper.faculty_name,
            orcid_id: '0000-0000-0000-0000' // Mock ORCID ID
          };
        });
        setFacultyList(mockFaculty);
        setLoading(false);
        return;
      }
      
      // Import faculty API to get actual faculty members
      const { getAllFaculty } = await import('../../api/facultyApi');
      const data = await getAllFaculty();
      
      // Map faculty data to the format needed
      const faculty = data.faculty.map(f => ({
        id: f.id,  // This is the actual MongoDB ObjectId
        name: f.full_name,
        orcid_id: f.orcid_id || ''
      }));
      
      setFacultyList(faculty);
    } catch (err) {
      setError('Failed to load faculty list');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const loadPublications = async () => {
    if (!selectedFaculty) return;

    try {
      setLoading(true);
      
      // Check if in demo mode
      if (isDemoMode()) {
        // Use mock publications data
        const mockPapers = MOCK_RESEARCH_PAPERS[selectedFaculty] || [];
        
        // Apply filters
        let filteredPapers = [...mockPapers];
        
        if (searchQuery) {
          const query = searchQuery.toLowerCase();
          filteredPapers = filteredPapers.filter(paper => 
            paper.title.toLowerCase().includes(query) ||
            paper.authors.some(author => author.toLowerCase().includes(query)) ||
            paper.publication_venue.toLowerCase().includes(query) ||
            (paper.doi && paper.doi.toLowerCase().includes(query))
          );
        }
        
        if (selectedWorkType) {
          filteredPapers = filteredPapers.filter(paper => 
            paper.work_type === selectedWorkType
          );
        }
        
        // Apply sorting
        if (sortBy === 'year_desc') {
          filteredPapers.sort((a, b) => b.year - a.year);
        } else if (sortBy === 'year_asc') {
          filteredPapers.sort((a, b) => a.year - b.year);
        }
        
        setPublications(filteredPapers);
        setLoading(false);
        return;
      }
      
      const params = {};
      
      if (searchQuery) params.search = searchQuery;
      if (selectedWorkType) params.work_type = selectedWorkType;
      if (sortBy) params.sort_by = sortBy;
      
      const data = await getFacultyPublications(selectedFaculty, params);
      setPublications(data.publications);
    } catch (err) {
      setError('Failed to load publications');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const loadStatistics = async () => {
    if (!selectedFaculty) return;

    try {
      // Check if in demo mode
      if (isDemoMode()) {
        // Calculate statistics from mock data
        const mockPapers = MOCK_RESEARCH_PAPERS[selectedFaculty] || [];
        const stats = {
          total_publications: mockPapers.length,
          by_source: { 'ORCID': mockPapers.length },
          by_work_type: {},
          year_range: { min: null, max: null },
          last_fetched: new Date().toISOString()
        };
        
        // Calculate work type counts
        mockPapers.forEach(paper => {
          const workType = paper.work_type;
          stats.by_work_type[workType] = (stats.by_work_type[workType] || 0) + 1;
        });
        
        // Calculate year range
        const years = mockPapers.map(p => p.year).filter(y => y);
        if (years.length > 0) {
          stats.year_range.min = Math.min(...years);
          stats.year_range.max = Math.max(...years);
        }
        
        setStatistics(stats);
        return;
      }
      
      const data = await getPublicationStatistics(selectedFaculty);
      setStatistics(data.statistics);
    } catch (err) {
      console.error('Failed to load statistics:', err);
    }
  };

  const loadWorkTypes = async () => {
    if (!selectedFaculty) return;

    try {
      // Check if in demo mode
      if (isDemoMode()) {
        // Extract unique work types from mock data
        const mockPapers = MOCK_RESEARCH_PAPERS[selectedFaculty] || [];
        const uniqueWorkTypes = [...new Set(mockPapers.map(paper => paper.work_type))];
        setWorkTypes(uniqueWorkTypes);
        return;
      }
      
      const data = await getFacultyWorkTypes(selectedFaculty);
      setWorkTypes(data.work_types);
    } catch (err) {
      console.error('Failed to load work types:', err);
    }
  };

  const handleFetchPublications = async () => {
    if (!selectedFaculty) {
      setError('Please select a faculty member');
      return;
    }

    if (selectedPlatform !== 'ORCID') {
      setError('Only ORCID integration is currently available');
      return;
    }

    try {
      setFetching(true);
      setError('');
      setSuccess('');
      
      // Check if in demo mode
      if (isDemoMode()) {
        // Simulate API delay
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        // Use mock data
        const mockPapers = MOCK_RESEARCH_PAPERS[selectedFaculty] || [];
        const result = {
          ...MOCK_FETCH_RESULT,
          faculty_id: selectedFaculty,
          faculty_name: mockPapers[0]?.faculty_name || 'Unknown',
          fetched_count: mockPapers.length,
          duplicates_removed: 0,
          unique_count: mockPapers.length,
          stored_count: mockPapers.length,
          status: 'success',
          success: true
        };
        
        setFetchStatus({
          fetched_count: result.fetched_count,
          duplicates_removed: result.duplicates_removed,
          unique_count: result.unique_count,
          stored_count: result.stored_count,
          status: result.status
        });
        
        setSuccess(`Successfully fetched ${result.unique_count} publications from ORCID (Demo Mode)`);
        
        // Reload publications and statistics
        await loadPublications();
        await loadStatistics();
        await loadWorkTypes();
        
        setFetching(false);
        return;
      }
      
      const result = await fetchOrcidPublications(selectedFaculty);
      
      setFetchStatus({
        fetched_count: result.fetched_count,
        duplicates_removed: result.duplicates_removed,
        unique_count: result.unique_count,
        stored_count: result.stored_count,
        status: result.status
      });
      
      if (result.success) {
        setSuccess(`Successfully fetched ${result.unique_count} publications from ORCID`);
        // Reload publications and statistics
        await loadPublications();
        await loadStatistics();
        await loadWorkTypes();
      } else {
        setError(result.error || 'Failed to fetch publications');
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to fetch publications from ORCID');
      console.error(err);
    } finally {
      setFetching(false);
    }
  };

  const getSelectedFacultyName = () => {
    const faculty = facultyList.find(f => f.id === selectedFaculty);
    return faculty ? faculty.name : '';
  };

  const hasOrcidId = () => {
    // In demo mode, always return true to enable fetch button
    if (isDemoMode()) {
      return true;
    }
    const faculty = facultyList.find(f => f.id === selectedFaculty);
    return faculty && faculty.orcid_id;
  };

  return (
    <div className="space-y-6">
      <AdminPageHeader
        title="Research Papers"
        description="View and manage research publications for faculty members."
        icon={
          <svg className="w-6 h-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
          </svg>
        }
      />

      {/* Selection Controls */}
      <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Faculty Selection */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Select a Faculty
            </label>
            <select
              value={selectedFaculty}
              onChange={(e) => setSelectedFaculty(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              disabled={loading}
            >
              <option value="">-- Select Faculty --</option>
              {facultyList.map(faculty => (
                <option key={faculty.id} value={faculty.id}>
                  {faculty.name}
                </option>
              ))}
            </select>
          </div>

          {/* Platform Selection */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Select Platform
            </label>
            <select
              value={selectedPlatform}
              onChange={(e) => setSelectedPlatform(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              disabled={!selectedFaculty}
            >
              <option value="ORCID">ORCID</option>
              <option value="Scopus" disabled>Scopus (Coming Soon)</option>
              <option value="Web of Science" disabled>Web of Science (Coming Soon)</option>
              <option value="Google Scholar" disabled>Google Scholar (Coming Soon)</option>
              <option value="OpenAlex" disabled>OpenAlex (Coming Soon)</option>
            </select>
          </div>

          {/* Fetch Button */}
          <div className="flex items-end">
            <button
              onClick={handleFetchPublications}
              disabled={fetching || !selectedFaculty || !hasOrcidId()}
              className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              {fetching ? (
                <>
                  <svg className="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                  </svg>
                  Fetching...
                </>
              ) : (
                <>
                  <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                  </svg>
                  Fetch Research Papers
                </>
              )}
            </button>
          </div>
        </div>

        {!hasOrcidId() && selectedFaculty && (
          <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg text-yellow-800 text-sm">
            ⚠️ ORCID is not configured for this faculty member. Please add ORCID ID in Citation Management first.
          </div>
        )}
      </div>

      {/* Error/Success Messages */}
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
          {error}
        </div>
      )}
      {success && (
        <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg">
          {success}
        </div>
      )}

      {/* Fetch Status Summary */}
      {fetchStatus && selectedFaculty && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <p className="text-xs text-blue-600 font-medium">Faculty</p>
              <p className="text-sm font-semibold text-blue-900">{getSelectedFacultyName()}</p>
            </div>
            <div>
              <p className="text-xs text-blue-600 font-medium">Platform</p>
              <p className="text-sm font-semibold text-blue-900">{selectedPlatform}</p>
            </div>
            <div>
              <p className="text-xs text-blue-600 font-medium">Fetch Status</p>
              <p className="text-sm font-semibold text-blue-900 capitalize">{fetchStatus.status}</p>
            </div>
            <div>
              <p className="text-xs text-blue-600 font-medium">Last Fetched</p>
              <p className="text-sm font-semibold text-blue-900">
                {statistics?.last_fetched ? new Date(statistics.last_fetched).toLocaleDateString() : 'N/A'}
              </p>
            </div>
          </div>
          <div className="grid grid-cols-3 gap-4 mt-4 pt-4 border-t border-blue-200">
            <div>
              <p className="text-xs text-blue-600 font-medium">Fetched</p>
              <p className="text-2xl font-bold text-blue-900">{fetchStatus.fetched_count}</p>
            </div>
            <div>
              <p className="text-xs text-blue-600 font-medium">Duplicates Removed</p>
              <p className="text-2xl font-bold text-blue-900">{fetchStatus.duplicates_removed}</p>
            </div>
            <div>
              <p className="text-xs text-blue-600 font-medium">Unique Publications</p>
              <p className="text-2xl font-bold text-blue-900">{fetchStatus.unique_count}</p>
            </div>
          </div>
        </div>
      )}

      {/* Filters */}
      {selectedFaculty && publications.length > 0 && (
        <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-6">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {/* Search */}
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Search Research Papers
              </label>
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search by title, author, venue, DOI..."
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            {/* Work Type Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Work Type
              </label>
              <select
                value={selectedWorkType}
                onChange={(e) => setSelectedWorkType(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">All Types</option>
                {workTypes.map(type => (
                  <option key={type} value={type}>{type}</option>
                ))}
              </select>
            </div>

            {/* Sort */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Sort by Year
              </label>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="year_desc">Newest First</option>
                <option value="year_asc">Oldest First</option>
              </select>
            </div>
          </div>
        </div>
      )}

      {/* Publications Table */}
      {selectedFaculty ? (
        <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
          {loading ? (
            <div className="flex items-center justify-center h-64">
              <div className="text-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                <p className="mt-4 text-gray-600">Loading publications...</p>
              </div>
            </div>
          ) : publications.length === 0 ? (
            <div className="flex items-center justify-center h-64">
              <div className="text-center text-gray-500">
                <svg className="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <p className="text-lg font-medium">No research publications found</p>
                <p className="text-sm mt-2">Click "Fetch Research Papers" to retrieve publications from {selectedPlatform}</p>
              </div>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50 border-b border-gray-200">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">Sr.</th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider min-w-[300px]">Title</th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">Authors</th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">Publication</th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">Year</th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">Work Type</th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">DOI</th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">Source</th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">View</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {publications.map((pub, index) => (
                    <tr key={pub.id} className="hover:bg-gray-50">
                      <td className="px-4 py-3 text-sm text-gray-900">{index + 1}</td>
                      <td className="px-4 py-3 text-sm text-gray-900">
                        <div className="max-w-md">
                          <p className="font-medium">{pub.title}</p>
                        </div>
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-600">
                        <div className="max-w-xs">
                          {pub.authors && pub.authors.length > 0 ? (
                            pub.authors.length > 2 ? (
                              <span title={pub.authors.join(', ')}>
                                {pub.authors.slice(0, 2).join(', ')} et al.
                              </span>
                            ) : (
                              pub.authors.join(', ')
                            )
                          ) : (
                            'Not Available'
                          )}
                        </div>
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-600">
                        <div className="max-w-xs truncate" title={pub.publication_venue}>
                          {pub.publication_venue || 'Not Available'}
                        </div>
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-900 font-medium">
                        {pub.year || 'N/A'}
                      </td>
                      <td className="px-4 py-3 text-sm">
                        <span className="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded">
                          {pub.work_type || 'Other'}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-sm">
                        {pub.doi ? (
                          <a
                            href={`https://doi.org/${pub.doi}`}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-blue-600 hover:text-blue-800 hover:underline"
                            title={pub.doi}
                          >
                            View DOI
                          </a>
                        ) : (
                          <span className="text-gray-400">N/A</span>
                        )}
                      </td>
                      <td className="px-4 py-3 text-sm">
                        <span className="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded">
                          {pub.source}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-sm">
                        {pub.url ? (
                          <a
                            href={pub.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-blue-600 hover:text-blue-800 hover:underline"
                          >
                            View
                          </a>
                        ) : (
                          <span className="text-gray-400 text-xs">No URL</span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      ) : (
        <div className="bg-white rounded-xl border border-gray-200 shadow-sm p-12">
          <div className="text-center text-gray-500">
            <svg className="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            <p className="text-lg font-medium">Select a faculty member to view research papers</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default ResearchPapers;
