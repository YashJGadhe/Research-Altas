/**
 * ResearchAtlas - Admin Layout Component
 * 
 * Main layout wrapper for all Admin pages.
 * Features:
 * - Persistent sidebar
 * - Responsive design
 * - Sidebar state persistence
 * - Mobile drawer support
 */

import React, { useState, useEffect } from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import AdminHeader from './AdminHeader';

const AdminLayout = () => {
  const [isCollapsed, setIsCollapsed] = useState(() => {
    // Persist sidebar state in localStorage
    const saved = localStorage.getItem('adminSidebarCollapsed');
    return saved === 'true';
  });

  const [isMobileOpen, setIsMobileOpen] = useState(false);

  // Save sidebar state to localStorage
  useEffect(() => {
    localStorage.setItem('adminSidebarCollapsed', isCollapsed.toString());
  }, [isCollapsed]);

  // Prevent body scroll when mobile menu is open
  useEffect(() => {
    if (isMobileOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => {
      document.body.style.overflow = '';
    };
  }, [isMobileOpen]);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Sidebar */}
      <Sidebar
        isCollapsed={isCollapsed}
        setIsCollapsed={setIsCollapsed}
        isMobileOpen={isMobileOpen}
        setIsMobileOpen={setIsMobileOpen}
      />

      {/* Main Content Area */}
      <div
        className={`transition-all duration-300 ${
          isCollapsed ? 'lg:ml-20' : 'lg:ml-64'
        }`}
      >
        {/* Header */}
        <AdminHeader
          setIsCollapsed={setIsCollapsed}
          isCollapsed={isCollapsed}
          setIsMobileOpen={setIsMobileOpen}
        />

        {/* Page Content */}
        <main className="p-4 sm:p-6 lg:p-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default AdminLayout;
