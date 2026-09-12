/**
 * ResearchAtlas - Citation Management Page (Phase 2 Placeholder)
 * 
 * Route: /admin/citations
 * Admin-only page for citation management.
 * Will include WoS, Scopus, Google Scholar, ResearchGate, ORCID citations.
 */

import React from 'react';
import AdminPageHeader from '../../components/admin/AdminPageHeader';
import EmptyState from '../../components/admin/EmptyState';

const CitationManagement = () => {
  return (
    <div>
      <AdminPageHeader
        title="Citation Management"
        description="Track and manage research citations across multiple platforms"
        icon={
          <svg className="w-6 h-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
          </svg>
        }
      />

      <div className="bg-white rounded-xl border border-gray-200 shadow-sm">
        <EmptyState
          title="Citation Management"
          description="Citation tracking across Web of Science, Scopus, Google Scholar, ResearchGate, and ORCID will be available in the next phase. Features will include h-index, i10-index, and platform-wise comparison."
          icon={
            <svg className="w-10 h-10 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          }
        />
      </div>
    </div>
  );
};

export default CitationManagement;
