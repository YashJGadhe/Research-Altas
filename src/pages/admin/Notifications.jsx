/**
 * ResearchAtlas - Notifications Page (Phase 2 Placeholder)
 * 
 * Route: /admin/notifications
 * Admin-only page for viewing system notifications.
 */

import React from 'react';
import AdminPageHeader from '../../components/admin/AdminPageHeader';
import EmptyState from '../../components/admin/EmptyState';

const Notifications = () => {
  return (
    <div>
      <AdminPageHeader
        title="Notifications"
        description="System notifications for publications, updates, and research activities"
        icon={
          <svg className="w-6 h-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
          </svg>
        }
      />

      <div className="bg-white rounded-xl border border-gray-200 shadow-sm">
        <EmptyState
          title="Notifications"
          description="Notification system for new publications, updated publications, research data updates, data harvesting alerts, and faculty-specific updates will be available in the next phase."
          icon={
            <svg className="w-10 h-10 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
            </svg>
          }
        />
      </div>
    </div>
  );
};

export default Notifications;
