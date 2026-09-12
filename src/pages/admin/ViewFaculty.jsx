/**
 * ResearchAtlas - View Faculty Page (Phase 2 Placeholder)
 * 
 * Route: /admin/faculty
 * Admin-only page to view all faculty members.
 * Faculty table and data retrieval will be implemented in Phase 3.
 */

import React from 'react';
import AdminPageHeader from '../../components/admin/AdminPageHeader';
import EmptyState from '../../components/admin/EmptyState';

const ViewFaculty = () => {
  return (
    <div>
      <AdminPageHeader
        title="View Faculty"
        description="Browse and view all faculty members and their research profiles"
        icon={
          <svg className="w-6 h-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
        }
      />

      <div className="bg-white rounded-xl border border-gray-200 shadow-sm">
        <EmptyState
          title="View Faculty"
          description="Faculty listing with search, filters, and detailed profiles will be available in the next phase. You will be able to view faculty research profiles, publications, and platform IDs."
          icon={
            <svg className="w-10 h-10 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          }
        />
      </div>
    </div>
  );
};

export default ViewFaculty;
