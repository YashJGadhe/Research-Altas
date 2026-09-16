/**
 * ResearchAtlas - Empty State Component
 * 
 * Reusable empty state for all admin module pages.
 * Shows a placeholder message indicating the module will be implemented in the next phase.
 */

import React from 'react';

const EmptyState = ({ title, description, icon }) => {
  return (
    <div className="flex flex-col items-center justify-center py-16 px-4">
      <div className="w-20 h-20 bg-blue-50 rounded-2xl flex items-center justify-center mb-6">
        {icon || (
          <svg className="w-10 h-10 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
          </svg>
        )}
      </div>
      <h3 className="text-xl font-semibold text-gray-900 mb-2">{title}</h3>
      <p className="text-gray-500 text-center max-w-md text-sm leading-relaxed">
        {description || 'Module functionality will be implemented in the next phase.'}
      </p>
      <div className="mt-6 px-4 py-2 bg-blue-50 border border-blue-100 rounded-lg">
        <p className="text-xs text-blue-600 font-medium">
          🚀 Coming in Phase 3+
        </p>
      </div>
    </div>
  );
};

export default EmptyState;
