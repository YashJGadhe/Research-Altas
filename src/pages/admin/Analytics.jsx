/**
 * ResearchAtlas - Analytics Page (Phase 2 Placeholder)
 * 
 * Route: /admin/analytics
 * Admin-only page for research analytics.
 */

import React from 'react';
import AdminPageHeader from '../../components/admin/AdminPageHeader';
import EmptyState from '../../components/admin/EmptyState';

const Analytics = () => {
  return (
    <div>
      <AdminPageHeader
        title="Analytics"
        description="Research analytics, trends, and insights across the institution"
        icon={
          <svg className="w-6 h-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
        }
      />

      <div className="bg-white rounded-xl border border-gray-200 shadow-sm">
        <EmptyState
          title="Analytics"
          description="Research analytics with citation counts, publication trends, year-wise and month-wise analysis, faculty productivity, research areas, and collaboration analysis will be available in the next phase."
          icon={
            <svg className="w-10 h-10 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          }
        />
      </div>
    </div>
  );
};

export default Analytics;
