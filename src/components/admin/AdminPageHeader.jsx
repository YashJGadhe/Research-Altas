/**
 * ResearchAtlas - Admin Page Header Component
 * 
 * Reusable page header for all admin module pages.
 * Shows page title, description, and optional action buttons.
 */

import React from 'react';

const AdminPageHeader = ({ title, description, icon, actions }) => {
  return (
    <div className="mb-8">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div className="flex items-start gap-4">
          {icon && (
            <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center flex-shrink-0">
              {icon}
            </div>
          )}
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{title}</h1>
            {description && (
              <p className="text-gray-500 mt-1 text-sm">{description}</p>
            )}
          </div>
        </div>
        
        {actions && (
          <div className="flex items-center gap-3">
            {actions}
          </div>
        )}
      </div>
    </div>
  );
};

export default AdminPageHeader;
