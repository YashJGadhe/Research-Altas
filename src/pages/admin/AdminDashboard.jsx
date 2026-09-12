/**
 * ResearchAtlas - Admin Dashboard (Phase 1 Placeholder)
 */

import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { ROLE_LABELS, DEPARTMENT_LABELS } from '../../utils/constants';

const AdminDashboard = () => {
  const { currentUser, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <span className="text-2xl mr-3">🌐</span>
              <span className="text-xl font-bold text-gray-900">ResearchAtlas</span>
              <span className="ml-4 px-2.5 py-0.5 bg-purple-100 text-purple-700 text-xs font-medium rounded-full">
                Admin
              </span>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600">
                {currentUser?.full_name}
              </span>
              <button onClick={handleLogout} className="btn-secondary text-sm py-2 px-4">
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Dashboard Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
          <p className="text-gray-500 mt-2">Welcome back, {currentUser?.full_name}</p>
        </div>

        {/* User Profile Card */}
        <div className="card mb-8">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Your Profile</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="bg-gray-50 rounded-lg p-3">
              <p className="text-xs text-gray-500">Name</p>
              <p className="font-medium text-gray-900">{currentUser?.full_name}</p>
            </div>
            <div className="bg-gray-50 rounded-lg p-3">
              <p className="text-xs text-gray-500">Email</p>
              <p className="font-medium text-gray-900">{currentUser?.email}</p>
            </div>
            <div className="bg-gray-50 rounded-lg p-3">
              <p className="text-xs text-gray-500">Department</p>
              <p className="font-medium text-gray-900">{DEPARTMENT_LABELS[currentUser?.department] || currentUser?.department}</p>
            </div>
            <div className="bg-gray-50 rounded-lg p-3">
              <p className="text-xs text-gray-500">Role</p>
              <p className="font-medium text-gray-900">{ROLE_LABELS[currentUser?.role]}</p>
            </div>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
            <div className="bg-blue-50 rounded-lg p-3 border border-blue-100">
              <p className="text-xs text-blue-600">ORCID ID</p>
              <p className="font-medium text-blue-900 font-mono text-sm">{currentUser?.orcid_id || '—'}</p>
            </div>
            <div className="bg-blue-50 rounded-lg p-3 border border-blue-100">
              <p className="text-xs text-blue-600">Scopus ID</p>
              <p className="font-medium text-blue-900 font-mono text-sm">{currentUser?.scopus_id || '—'}</p>
            </div>
            <div className="bg-blue-50 rounded-lg p-3 border border-blue-100">
              <p className="text-xs text-blue-600">WoS ID</p>
              <p className="font-medium text-blue-900 font-mono text-sm">{currentUser?.wos_id || '—'}</p>
            </div>
          </div>
        </div>

        {/* Status Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="card">
            <div className="flex items-center">
              <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center mr-4">
                <span className="text-2xl">👥</span>
              </div>
              <div>
                <p className="text-sm text-gray-500">Total Users</p>
                <p className="text-2xl font-bold text-gray-900">—</p>
              </div>
            </div>
          </div>
          <div className="card">
            <div className="flex items-center">
              <div className="w-12 h-12 bg-emerald-100 rounded-xl flex items-center justify-center mr-4">
                <span className="text-2xl">🎓</span>
              </div>
              <div>
                <p className="text-sm text-gray-500">Faculty Members</p>
                <p className="text-2xl font-bold text-gray-900">—</p>
              </div>
            </div>
          </div>
          <div className="card">
            <div className="flex items-center">
              <div className="w-12 h-12 bg-amber-100 rounded-xl flex items-center justify-center mr-4">
                <span className="text-2xl">📚</span>
              </div>
              <div>
                <p className="text-sm text-gray-500">Publications</p>
                <p className="text-2xl font-bold text-gray-900">—</p>
              </div>
            </div>
          </div>
        </div>

        {/* Phase 1 Notice */}
        <div className="card border-purple-200 bg-purple-50">
          <div className="flex items-start">
            <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center mr-4 flex-shrink-0">
              <span className="text-xl">ℹ️</span>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-purple-900 mb-1">Phase 1 — Authentication Foundation</h3>
              <p className="text-purple-700 text-sm">
                The authentication and authorization system is fully operational. Dashboard functionality,
                user management, faculty management, and research modules will be implemented in subsequent phases.
              </p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default AdminDashboard;
