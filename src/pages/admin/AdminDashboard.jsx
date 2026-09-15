/**
 * ResearchAtlas - Admin Dashboard (Phase 2)
 * 
 * Main dashboard page for Admin users.
 * Shows welcome message, admin identity, and basic empty state.
 * Statistics will be connected to real MongoDB data in future phases.
 */

import React from 'react';
import { useAuth } from '../../hooks/useAuth';
import { ROLE_LABELS, DEPARTMENT_LABELS } from '../../utils/constants';
import AdminPageHeader from '../../components/admin/AdminPageHeader';

const AdminDashboard = () => {
  const { currentUser } = useAuth();

  const quickLinks = [
    {
      title: 'View Faculty',
      description: 'Browse all faculty members and their research profiles',
      icon: (
        <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
      ),
      color: 'blue',
    },
    {
      title: 'Citation Management',
      description: 'Track and manage research citations across platforms',
      icon: (
        <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
        </svg>
      ),
      color: 'emerald',
    },
    {
      title: 'Research Papers',
      description: 'View and manage faculty research publications',
      icon: (
        <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
        </svg>
      ),
      color: 'purple',
    },
    {
      title: 'Analytics',
      description: 'Research analytics and insights dashboard',
      icon: (
        <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
        </svg>
      ),
      color: 'amber',
    },
  ];

  const colorMap = {
    blue: { bg: 'bg-blue-50', text: 'text-blue-600', border: 'border-blue-100' },
    emerald: { bg: 'bg-emerald-50', text: 'text-emerald-600', border: 'border-emerald-100' },
    purple: { bg: 'bg-purple-50', text: 'text-purple-600', border: 'border-purple-100' },
    amber: { bg: 'bg-amber-50', text: 'text-amber-600', border: 'border-amber-100' },
  };

  return (
    <div>
      {/* Page Header */}
      <AdminPageHeader
        title="Admin Dashboard"
        description={`Welcome back, ${currentUser?.full_name}`}
        icon={
          <svg className="w-6 h-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
          </svg>
        }
      />

      {/* Admin Profile Card */}
      <div className="bg-white rounded-xl border border-gray-200 p-6 mb-8 shadow-sm">
        <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wide mb-4">Your Profile</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-xs text-gray-500 mb-1">Name</p>
            <p className="font-semibold text-gray-900">{currentUser?.full_name}</p>
          </div>
          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-xs text-gray-500 mb-1">Email</p>
            <p className="font-semibold text-gray-900 text-sm">{currentUser?.email}</p>
          </div>
          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-xs text-gray-500 mb-1">Role</p>
            <p className="font-semibold text-gray-900">{ROLE_LABELS[currentUser?.role]}</p>
          </div>
          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-xs text-gray-500 mb-1">Department</p>
            <p className="font-semibold text-gray-900">{DEPARTMENT_LABELS[currentUser?.department] || currentUser?.department}</p>
          </div>
        </div>
        
        {/* Research IDs */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-4">
          <div className="bg-blue-50 rounded-lg p-3 border border-blue-100">
            <p className="text-xs text-blue-600 font-medium">ORCID ID</p>
            <p className="font-mono text-sm text-blue-900 mt-1">{currentUser?.orcid_id || '—'}</p>
          </div>
          <div className="bg-blue-50 rounded-lg p-3 border border-blue-100">
            <p className="text-xs text-blue-600 font-medium">Scopus ID</p>
            <p className="font-mono text-sm text-blue-900 mt-1">{currentUser?.scopus_id || '—'}</p>
          </div>
          <div className="bg-blue-50 rounded-lg p-3 border border-blue-100">
            <p className="text-xs text-blue-600 font-medium">WoS ID</p>
            <p className="font-mono text-sm text-blue-900 mt-1">{currentUser?.wos_id || '—'}</p>
          </div>
        </div>
      </div>

      {/* Quick Links */}
      <div className="mb-8">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Access</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {quickLinks.map((link) => {
            const colors = colorMap[link.color];
            return (
              <div
                key={link.title}
                className={`bg-white rounded-xl border border-gray-200 p-5 hover:shadow-md transition-shadow cursor-pointer`}
              >
                <div className={`w-10 h-10 ${colors.bg} rounded-lg flex items-center justify-center mb-3 ${colors.text}`}>
                  {link.icon}
                </div>
                <h4 className="font-semibold text-gray-900 text-sm">{link.title}</h4>
                <p className="text-xs text-gray-500 mt-1">{link.description}</p>
              </div>
            );
          })}
        </div>
      </div>

      {/* Demo Mode Notice */}
      {localStorage.getItem('demoMode') === 'true' && (
        <div className="bg-gradient-to-r from-purple-50 to-blue-50 border border-purple-200 rounded-xl p-4 mb-6">
          <div className="flex items-center gap-3">
            <span className="text-2xl">🎮</span>
            <div>
              <h3 className="text-sm font-semibold text-purple-900">Demo Mode Active</h3>
              <p className="text-xs text-purple-700">
                You are viewing a demo preview. Connect to the backend for full functionality.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Phase 2 Notice */}
      <div className="bg-blue-50 border border-blue-200 rounded-xl p-6">
        <div className="flex items-start gap-4">
          <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center flex-shrink-0">
            <span className="text-xl">ℹ️</span>
          </div>
          <div>
            <h3 className="text-base font-semibold text-blue-900 mb-1">Phase 2 — Admin Module Structure</h3>
            <p className="text-blue-700 text-sm leading-relaxed">
              The Admin module structure is complete with sidebar navigation, role-based routing,
              and all module pages. Real data, statistics, and functionality will be connected
              in subsequent phases. The authentication foundation from Phase 1 is fully integrated.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
