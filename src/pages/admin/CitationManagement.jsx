/**
 * ResearchAtlas - Citation Management Page (Phase 6)
 * 
 * Route: /admin/citations
 * Admin-only page for citation management with:
 * - Table view of all faculty citations
 * - Manual editing with validation
 * - ORCID API integration
 * - Historical data tracking
 * - Previous values display
 */

import React, { useState, useEffect } from 'react';
import AdminPageHeader from '../../components/admin/AdminPageHeader';
import { useAuth } from '../../hooks/useAuth';
import {
  getAllCitations,
  updateCitation,
  getCitationHistory,
  fetchOrcidData
} from '../../api/citationApi';

const CitationManagement = () => {
  const { currentUser } = useAuth();
  const [citations, setCitations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  
  // Modal states
  const [editModal, setEditModal] = useState({ open: false, record: null });
  const [historyModal, setHistoryModal] = useState({ open: false, record: null, history: [] });
  const [fetchResultModal, setFetchResultModal] = useState({ open: false, result: null });
  
  // Edit form state
  const [editForm, setEditForm] = useState({});
  const [editLoading, setEditLoading] = useState(false);

  useEffect(() => {
    loadCitations();
  }, []);

  const loadCitations = async () => {
    try {
      setLoading(true);
      const data = await getAllCitations();
      setCitations(data.records);
      setError('');
    } catch (err) {
      setError('Failed to load citation data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (record) => {
    setEditForm({
      web_of_science: { ...record.web_of_science },
      scopus: { ...record.scopus },
      google_scholar: { ...record.google_scholar },
      publons_url: record.publons_url || '',
      scopus_url: record.scopus_url || '',
      google_scholar_url: record.google_scholar_url || '',
      researchgate_url: record.researchgate_url || '',
      orcid: { ...record.orcid },
      openalex: { ...record.openalex }
    });
    setEditModal({ open: true, record });
  };

  const handleEditSubmit = async () => {
    try {
      setEditLoading(true);
      await updateCitation(editModal.record.id, editForm);
      setSuccess('Citation data updated successfully');
      setEditModal({ open: false, record: null });
      await loadCitations();
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError('Failed to update citation data');
      console.error(err);
    } finally {
      setEditLoading(false);
    }
  };

  const handleViewHistory = async (record) => {
    try {
      const historyData = await getCitationHistory(record.id);
      setHistoryModal({ open: true, record, history: historyData.history });
    } catch (err) {
      setError('Failed to load history');
      console.error(err);
    }
  };

  const handleFetchOrcid = async (record) => {
    try {
      setLoading(true);
      const result = await fetchOrcidData(record.id);
      setFetchResultModal({ open: true, result });
      await loadCitations();
    } catch (err) {
      setError('Failed to fetch ORCID data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleFetchAll = async () => {
    try {
      setLoading(true);
      let totalUpdated = 0;
      let totalFound = 0;
      
      for (const record of citations) {
        if (record.orcid?.id) {
          try {
            const result = await fetchOrcidData(record.id);
            if (result.success) {
              totalUpdated += result.records_updated;
              totalFound += result.records_found;
            }
          } catch (err) {
            console.error(`Failed to fetch ORCID for ${record.faculty_name}:`, err);
          }
        }
      }
      
      setSuccess(`Fetch complete. Found ${totalFound} works, updated ${totalUpdated} records.`);
      await loadCitations();
      setTimeout(() => setSuccess(''), 5000);
    } catch (err) {
      setError('Failed to fetch data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading && citations.length === 0) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading citation data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <AdminPageHeader
        title="Citation Management"
        description="Manage, fetch and monitor faculty research metrics from supported scholarly sources."
        icon={
          <svg className="w-6 h-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
          </svg>
        }
      />

      {/* Action Buttons */}
      <div className="flex gap-3">
        <button
          onClick={handleFetchAll}
          disabled={loading}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center gap-2"
        >
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Fetch All Data
        </button>
        <button
          onClick={loadCitations}
          disabled={loading}
          className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 disabled:opacity-50 flex items-center gap-2"
        >
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          Refresh
        </button>
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

      {/* Citation Table */}
      <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-gray-50 border-b border-gray-200">
              <tr>
                <th className="px-4 py-3 text-left font-semibold text-gray-700 sticky left-0 bg-gray-50 z-10">Sr.</th>
                <th className="px-4 py-3 text-left font-semibold text-gray-700 sticky left-16 bg-gray-50 z-10 min-w-[200px]">Faculty Name</th>
                
                {/* Web of Science */}
                <th colSpan={3} className="px-4 py-3 text-center font-semibold text-gray-700 bg-blue-50 border-l border-gray-200">
                  Web of Science
                </th>
                
                {/* Scopus */}
                <th colSpan={3} className="px-4 py-3 text-center font-semibold text-gray-700 bg-green-50 border-l border-gray-200">
                  Scopus
                </th>
                
                {/* Google Scholar */}
                <th colSpan={4} className="px-4 py-3 text-center font-semibold text-gray-700 bg-purple-50 border-l border-gray-200">
                  Google Scholar
                </th>
                
                {/* Links */}
                <th className="px-4 py-3 text-center font-semibold text-gray-700 bg-gray-50 border-l border-gray-200">Publons</th>
                <th className="px-4 py-3 text-center font-semibold text-gray-700 bg-gray-50">Scopus Link</th>
                <th className="px-4 py-3 text-center font-semibold text-gray-700 bg-gray-50">GS Link</th>
                <th className="px-4 py-3 text-center font-semibold text-gray-700 bg-gray-50">ResearchGate</th>
                <th className="px-4 py-3 text-center font-semibold text-gray-700 bg-gray-50">ORCID</th>
                <th className="px-4 py-3 text-center font-semibold text-gray-700 bg-gray-50">OpenAlex</th>
                
                {/* Actions */}
                <th className="px-4 py-3 text-center font-semibold text-gray-700 bg-gray-50 border-l border-gray-200 sticky right-0 z-10">Actions</th>
              </tr>
              <tr className="bg-gray-25 text-xs text-gray-600">
                <th className="px-4 py-2 sticky left-0 bg-gray-25 z-10"></th>
                <th className="px-4 py-2 sticky left-16 bg-gray-25 z-10"></th>
                <th className="px-4 py-2 text-center bg-blue-50 border-l border-gray-200">Papers</th>
                <th className="px-4 py-2 text-center bg-blue-50">Citations</th>
                <th className="px-4 py-2 text-center bg-blue-50">h-index</th>
                <th className="px-4 py-2 text-center bg-green-50 border-l border-gray-200">Papers</th>
                <th className="px-4 py-2 text-center bg-green-50">Citations</th>
                <th className="px-4 py-2 text-center bg-green-50">h-index</th>
                <th className="px-4 py-2 text-center bg-purple-50 border-l border-gray-200">Papers</th>
                <th className="px-4 py-2 text-center bg-purple-50">Citations</th>
                <th className="px-4 py-2 text-center bg-purple-50">h-index</th>
                <th className="px-4 py-2 text-center bg-purple-50">i10-index</th>
                <th className="px-4 py-2 text-center bg-gray-50 border-l border-gray-200">Link</th>
                <th className="px-4 py-2 text-center bg-gray-50">Link</th>
                <th className="px-4 py-2 text-center bg-gray-50">Link</th>
                <th className="px-4 py-2 text-center bg-gray-50">ID</th>
                <th className="px-4 py-2 text-center bg-gray-50">ID</th>
                <th className="px-4 py-2 text-center bg-gray-50">ID</th>
                <th className="px-4 py-2 text-center bg-gray-50 border-l border-gray-200 sticky right-0 z-10"></th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {citations.map((record, index) => (
                <tr key={record.id} className="hover:bg-gray-50">
                  <td className="px-4 py-3 sticky left-0 bg-white z-10">{index + 1}</td>
                  <td className="px-4 py-3 font-medium text-gray-900 sticky left-16 bg-white z-10">
                    {record.faculty_name}
                  </td>
                  
                  {/* Web of Science */}
                  <td className="px-4 py-3 text-center border-l border-gray-200">{record.web_of_science?.papers || 0}</td>
                  <td className="px-4 py-3 text-center">{record.web_of_science?.citations || 0}</td>
                  <td className="px-4 py-3 text-center">{record.web_of_science?.h_index || 0}</td>
                  
                  {/* Scopus */}
                  <td className="px-4 py-3 text-center border-l border-gray-200">{record.scopus?.papers || 0}</td>
                  <td className="px-4 py-3 text-center">{record.scopus?.citations || 0}</td>
                  <td className="px-4 py-3 text-center">{record.scopus?.h_index || 0}</td>
                  
                  {/* Google Scholar */}
                  <td className="px-4 py-3 text-center border-l border-gray-200">{record.google_scholar?.papers || 0}</td>
                  <td className="px-4 py-3 text-center">{record.google_scholar?.citations || 0}</td>
                  <td className="px-4 py-3 text-center">{record.google_scholar?.h_index || 0}</td>
                  <td className="px-4 py-3 text-center">{record.google_scholar?.i10_index || 0}</td>
                  
                  {/* Links */}
                  <td className="px-4 py-3 text-center border-l border-gray-200">
                    {record.publons_url ? (
                      <a href={record.publons_url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
                        Link
                      </a>
                    ) : 'NIL'}
                  </td>
                  <td className="px-4 py-3 text-center">
                    {record.scopus_url ? (
                      <a href={record.scopus_url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
                        Link
                      </a>
                    ) : 'NIL'}
                  </td>
                  <td className="px-4 py-3 text-center">
                    {record.google_scholar_url ? (
                      <a href={record.google_scholar_url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
                        Link
                      </a>
                    ) : 'NIL'}
                  </td>
                  <td className="px-4 py-3 text-center">
                    {record.researchgate_url ? (
                      <a href={record.researchgate_url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
                        Link
                      </a>
                    ) : 'NIL'}
                  </td>
                  <td className="px-4 py-3 text-center">
                    {record.orcid?.id || 'NIL'}
                  </td>
                  <td className="px-4 py-3 text-center">
                    {record.openalex?.id || 'NIL'}
                  </td>
                  
                  {/* Actions */}
                  <td className="px-4 py-3 text-center border-l border-gray-200 sticky right-0 bg-white z-10">
                    <div className="flex gap-2 justify-center">
                      <button
                        onClick={() => handleEdit(record)}
                        className="px-3 py-1 text-xs bg-blue-600 text-white rounded hover:bg-blue-700"
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => handleFetchOrcid(record)}
                        disabled={!record.orcid?.id}
                        className="px-3 py-1 text-xs bg-green-600 text-white rounded hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
                        title={!record.orcid?.id ? 'ORCID ID not configured' : 'Fetch ORCID data'}
                      >
                        Fetch
                      </button>
                      <button
                        onClick={() => handleViewHistory(record)}
                        className="px-3 py-1 text-xs bg-gray-600 text-white rounded hover:bg-gray-700"
                      >
                        History
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Edit Modal */}
      {editModal.open && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <h3 className="text-xl font-semibold mb-4">Edit Citation Data - {editModal.record.faculty_name}</h3>
              
              <div className="space-y-6">
                {/* Web of Science */}
                <div className="border border-gray-200 rounded-lg p-4">
                  <h4 className="font-semibold text-blue-700 mb-3">Web of Science</h4>
                  <div className="grid grid-cols-3 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Papers</label>
                      <input
                        type="number"
                        min="0"
                        value={editForm.web_of_science?.papers || 0}
                        onChange={(e) => setEditForm({
                          ...editForm,
                          web_of_science: { ...editForm.web_of_science, papers: parseInt(e.target.value) || 0 }
                        })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Citations</label>
                      <input
                        type="number"
                        min="0"
                        value={editForm.web_of_science?.citations || 0}
                        onChange={(e) => setEditForm({
                          ...editForm,
                          web_of_science: { ...editForm.web_of_science, citations: parseInt(e.target.value) || 0 }
                        })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">h-index</label>
                      <input
                        type="number"
                        min="0"
                        value={editForm.web_of_science?.h_index || 0}
                        onChange={(e) => setEditForm({
                          ...editForm,
                          web_of_science: { ...editForm.web_of_science, h_index: parseInt(e.target.value) || 0 }
                        })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                      />
                    </div>
                  </div>
                </div>

                {/* Scopus */}
                <div className="border border-gray-200 rounded-lg p-4">
                  <h4 className="font-semibold text-green-700 mb-3">Scopus</h4>
                  <div className="grid grid-cols-3 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Papers</label>
                      <input
                        type="number"
                        min="0"
                        value={editForm.scopus?.papers || 0}
                        onChange={(e) => setEditForm({
                          ...editForm,
                          scopus: { ...editForm.scopus, papers: parseInt(e.target.value) || 0 }
                        })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Citations</label>
                      <input
                        type="number"
                        min="0"
                        value={editForm.scopus?.citations || 0}
                        onChange={(e) => setEditForm({
                          ...editForm,
                          scopus: { ...editForm.scopus, citations: parseInt(e.target.value) || 0 }
                        })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">h-index</label>
                      <input
                        type="number"
                        min="0"
                        value={editForm.scopus?.h_index || 0}
                        onChange={(e) => setEditForm({
                          ...editForm,
                          scopus: { ...editForm.scopus, h_index: parseInt(e.target.value) || 0 }
                        })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                      />
                    </div>
                  </div>
                </div>

                {/* Google Scholar */}
                <div className="border border-gray-200 rounded-lg p-4">
                  <h4 className="font-semibold text-purple-700 mb-3">Google Scholar</h4>
                  <div className="grid grid-cols-4 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Papers</label>
                      <input
                        type="number"
                        min="0"
                        value={editForm.google_scholar?.papers || 0}
                        onChange={(e) => setEditForm({
                          ...editForm,
                          google_scholar: { ...editForm.google_scholar, papers: parseInt(e.target.value) || 0 }
                        })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Citations</label>
                      <input
                        type="number"
                        min="0"
                        value={editForm.google_scholar?.citations || 0}
                        onChange={(e) => setEditForm({
                          ...editForm,
                          google_scholar: { ...editForm.google_scholar, citations: parseInt(e.target.value) || 0 }
                        })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">h-index</label>
                      <input
                        type="number"
                        min="0"
                        value={editForm.google_scholar?.h_index || 0}
                        onChange={(e) => setEditForm({
                          ...editForm,
                          google_scholar: { ...editForm.google_scholar, h_index: parseInt(e.target.value) || 0 }
                        })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">i10-index</label>
                      <input
                        type="number"
                        min="0"
                        value={editForm.google_scholar?.i10_index || 0}
                        onChange={(e) => setEditForm({
                          ...editForm,
                          google_scholar: { ...editForm.google_scholar, i10_index: parseInt(e.target.value) || 0 }
                        })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                      />
                    </div>
                  </div>
                </div>

                {/* URLs */}
                <div className="border border-gray-200 rounded-lg p-4">
                  <h4 className="font-semibold text-gray-700 mb-3">Profile URLs</h4>
                  <div className="space-y-3">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Publons URL</label>
                      <input
                        type="url"
                        value={editForm.publons_url || ''}
                        onChange={(e) => setEditForm({ ...editForm, publons_url: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                        placeholder="https://publons.com/researcher/..."
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Scopus URL</label>
                      <input
                        type="url"
                        value={editForm.scopus_url || ''}
                        onChange={(e) => setEditForm({ ...editForm, scopus_url: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                        placeholder="https://www.scopus.com/authid/..."
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Google Scholar URL</label>
                      <input
                        type="url"
                        value={editForm.google_scholar_url || ''}
                        onChange={(e) => setEditForm({ ...editForm, google_scholar_url: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                        placeholder="https://scholar.google.com/citations?user=..."
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">ResearchGate URL</label>
                      <input
                        type="url"
                        value={editForm.researchgate_url || ''}
                        onChange={(e) => setEditForm({ ...editForm, researchgate_url: e.target.value })}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                        placeholder="https://www.researchgate.net/profile/..."
                      />
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">ORCID ID</label>
                        <input
                          type="text"
                          value={editForm.orcid?.id || ''}
                          onChange={(e) => setEditForm({
                            ...editForm,
                            orcid: { ...editForm.orcid, id: e.target.value }
                          })}
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                          placeholder="0000-0000-0000-0000"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">OpenAlex ID</label>
                        <input
                          type="text"
                          value={editForm.openalex?.id || ''}
                          onChange={(e) => setEditForm({
                            ...editForm,
                            openalex: { ...editForm.openalex, id: e.target.value }
                          })}
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                          placeholder="A1234567890"
                        />
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex gap-3 mt-6">
                <button
                  onClick={handleEditSubmit}
                  disabled={editLoading}
                  className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
                >
                  {editLoading ? 'Saving...' : 'Save Changes'}
                </button>
                <button
                  onClick={() => setEditModal({ open: false, record: null })}
                  className="px-6 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* History Modal */}
      {historyModal.open && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl max-w-3xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              <h3 className="text-xl font-semibold mb-4">
                Citation History - {historyModal.record.faculty_name}
              </h3>
              
              {historyModal.history.length === 0 ? (
                <p className="text-gray-500 text-center py-8">No history records found.</p>
              ) : (
                <div className="space-y-4">
                  {historyModal.history.map((entry, index) => (
                    <div key={entry.id} className="border border-gray-200 rounded-lg p-4">
                      <div className="flex justify-between items-start mb-2">
                        <div>
                          <span className="text-xs font-semibold text-gray-500">
                            {new Date(entry.created_at).toLocaleString()}
                          </span>
                          <span className="ml-2 px-2 py-1 text-xs bg-blue-100 text-blue-700 rounded">
                            {entry.change_source}
                          </span>
                          <span className="ml-2 px-2 py-1 text-xs bg-green-100 text-green-700 rounded">
                            {entry.source_platform}
                          </span>
                        </div>
                        {entry.created_by && (
                          <span className="text-xs text-gray-500">By: {entry.created_by}</span>
                        )}
                      </div>
                      <div className="text-sm">
                        <p className="font-medium text-gray-700 mb-1">Changed Fields:</p>
                        <ul className="list-disc list-inside text-gray-600">
                          {entry.changed_fields.map((field, i) => (
                            <li key={i}>{field}</li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              <div className="mt-6">
                <button
                  onClick={() => setHistoryModal({ open: false, record: null, history: [] })}
                  className="px-6 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Fetch Result Modal */}
      {fetchResultModal.open && fetchResultModal.result && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl max-w-2xl w-full">
            <div className="p-6">
              <h3 className="text-xl font-semibold mb-4">ORCID Fetch Result</h3>
              
              <div className="space-y-3">
                <div className={`p-4 rounded-lg ${fetchResultModal.result.success ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'}`}>
                  <p className={`font-semibold ${fetchResultModal.result.success ? 'text-green-700' : 'text-red-700'}`}>
                    Status: {fetchResultModal.result.success ? 'SUCCESS' : 'FAILED'}
                  </p>
                  <p className="text-sm text-gray-700 mt-1">{fetchResultModal.result.message}</p>
                </div>

                {fetchResultModal.result.success && (
                  <>
                    <div className="grid grid-cols-2 gap-4">
                      <div className="bg-gray-50 p-3 rounded-lg">
                        <p className="text-xs text-gray-500">Records Found</p>
                        <p className="text-2xl font-semibold text-gray-900">{fetchResultModal.result.records_found}</p>
                      </div>
                      <div className="bg-gray-50 p-3 rounded-lg">
                        <p className="text-xs text-gray-500">Records Updated</p>
                        <p className="text-2xl font-semibold text-gray-900">{fetchResultModal.result.records_updated}</p>
                      </div>
                    </div>

                    {fetchResultModal.result.data && (
                      <div className="border border-gray-200 rounded-lg p-4">
                        <h4 className="font-semibold text-gray-700 mb-2">ORCID Data Retrieved</h4>
                        <div className="text-sm space-y-1">
                          <p><span className="font-medium">Name:</span> {fetchResultModal.result.data.name}</p>
                          <p><span className="font-medium">ORCID:</span> {fetchResultModal.result.data.orcid_id}</p>
                          <p><span className="font-medium">Works Count:</span> {fetchResultModal.result.data.works_count}</p>
                        </div>
                      </div>
                    )}
                  </>
                )}
              </div>

              <div className="mt-6">
                <button
                  onClick={() => setFetchResultModal({ open: false, result: null })}
                  className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CitationManagement;
