/**
 * ResearchAtlas - Admin Header Component
 * 
 * Top header bar for Admin module.
 * Features:
 * - Sidebar toggle (mobile)
 * - Current page title
 * - Admin info (name, role badge)
 * - Logout button
 */

import React from 'react';
import { useLocation } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { ROUTES, ROLE_LABELS } from '../../utils/constants';

const AdminHeader = ({ setIsCollapsed, isCollapsed, setIsMobileOpen }) => {
  const { currentUser, logout } = useAuth();
  const location = useLocation();

  // Map routes to page titles
  const pageTitles = {
    [ROUTES.ADMIN_DASHBOARD]: 'Dashboard',
    [ROUTES.ADMIN_FACULTY]: 'View Faculty',
    [ROUTES.ADMIN_CITATIONS]: 'Citation Management',
    [ROUTES.ADMIN_RESEARCH_PAPERS]: 'Research Papers',
    [ROUTES.ADMIN_NOTIFICATIONS]: 'Notifications',
    [ROUTES.ADMIN_ANALYTICS]: 'Analytics',
    [ROUTES.ADMIN_REPORTS]: 'Reports',
    [ROUTES.ADMIN_MANAGE_FACULTY]: 'Manage Faculty',
  };

  const currentPageTitle = pageTitles[location.pathname] || 'Admin';

  const handleLogout = () => {
    logout();
  };

  return (
    <header className="sticky top-0 z-30 bg-white border-b border-gray-200 shadow-sm">
      <div className="flex items-center justify-between h-16 px-4 sm:px-6">
        {/* Left side - Mobile toggle + Page title */}
        <div className="flex items-center gap-4">
          {/* Mobile sidebar toggle */}
          <button
            onClick={() => setIsMobileOpen(true)}
            className="lg:hidden p-2 rounded-lg text-gray-500 hover:text-gray-700 hover:bg-gray-100 transition-colors"
            aria-label="Open sidebar"
          >
            <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>

          {/* Desktop sidebar toggle */}
          <button
            onClick={() => setIsCollapsed(!isCollapsed)}
            className="hidden lg:flex p-2 rounded-lg text-gray-500 hover:text-gray-700 hover:bg-gray-100 transition-colors"
            aria-label="Toggle sidebar"
          >
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h7" />
            </svg>
          </button>

          {/* Page title */}
          <div>
            <h2 className="text-lg font-semibold text-gray-900">{currentPageTitle}</h2>
            <p className="text-xs text-gray-500 hidden sm:block">
              Research & Development Management
            </p>
          </div>
        </div>

        {/* Right side - Admin info + Logout */}
        <div className="flex items-center gap-3">
          {/* Admin info */}
          <div className="hidden sm:flex items-center gap-3">
            <div className="text-right">
              <p className="text-sm font-medium text-gray-900 leading-tight">
                {currentUser?.full_name || 'Admin'}
              </p>
              <p className="text-xs text-gray-500">{ROLE_LABELS[currentUser?.role]}</p>
            </div>
            <div className="w-9 h-9 bg-blue-100 rounded-full flex items-center justify-center">
              <span className="text-blue-700 font-semibold text-sm">
                {currentUser?.full_name?.charAt(0)?.toUpperCase() || 'A'}
              </span>
            </div>
          </div>

          {/* Logout button */}
          <button
            onClick={handleLogout}
            className="flex items-center gap-2 px-3 py-2 text-sm text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
            title="Logout"
          >
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
            <span className="hidden md:inline">Logout</span>
          </button>
        </div>
      </div>
    </header>
  );
};

export default AdminHeader;
