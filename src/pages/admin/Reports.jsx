/**
 * ResearchAtlas - Reports Page (Phase 2 Placeholder)
 * 
 * Route: /admin/reports
 * Admin-only page for generating reports.
 */

import React from 'react';
import AdminPageHeader from '../../components/admin/AdminPageHeader';
import EmptyState from '../../components/admin/EmptyState';

const Reports = () => {
  return (
    <div>
      <AdminPageHeader
        title="Reports"
        description="Generate and export research reports in various formats"
        icon={
          <svg className="w-6 h-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        }
      />

      <div className="bg-white rounded-xl border border-gray-200 shadow-sm">
        <EmptyState
          title="Reports"
          description="Excel and PDF report generation for research data, faculty publications, citations, and analytics will be available in the next phase."
          icon={
            <svg className="w-10 h-10 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          }
        />
      </div>
    </div>
  );
};

export default Reports;
