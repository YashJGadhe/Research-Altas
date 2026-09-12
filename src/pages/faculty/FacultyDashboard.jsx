/**
 * ResearchAtlas - Faculty Dashboard (Phase 1 Placeholder)
 * 
 * Placeholder dashboard for faculty users.
 * Future prompts will build actual faculty dashboard functionality.
 */

import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { ROLE_LABELS, DEPARTMENT_LABELS } from '../../utils/constants';

const FacultyDashboard = () => {
  const { currentUser, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-emerald-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <span className="text-2xl mr-3">🌐</span>
              <span className="text-xl font-bold text-gray-900">ResearchAtlas</span>
              <span className="ml-4 px-2.5 py-0.5 bg-emerald-100 text-emerald-700 text-xs font-medium rounded-full">
                Faculty
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
          <h1 className="text-3xl font-bold text-gray-900">Faculty Dashboard</h1>
          <p className="text-gray-500 mt-2">Welcome back, {currentUser?.full_name}</p>
        </div>

        {/* Status Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="card">
            <div className="flex items-center">
              <div className="w-12 h-12 bg-emerald-100 rounded-xl flex items-center justify-center mr-4">
                <span className="text-2xl">📄</span>
              </div>
              <div>
                <p className="text-sm text-gray-500">My Publications</p>
                <p className="text-2xl font-bold text-gray-900">—</p>
              </div>
            </div>
          </div>
          <div className="card">
            <div className="flex items-center">
              <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center mr-4">
                <span className="text-2xl">🔬</span>
              </div>
              <div>
                <p className="text-sm text-gray-500">Research Activities</p>
                <p className="text-2xl font-bold text-gray-900">—</p>
              </div>
            </div>
          </div>
          <div className="card">
            <div className="flex items-center">
              <div className="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center mr-4">
                <span className="text-2xl">📊</span>
              </div>
              <div>
                <p className="text-sm text-gray-500">Citations</p>
                <p className="text-2xl font-bold text-gray-900">—</p>
              </div>
            </div>
          </div>
        </div>

        {/* Phase 1 Notice */}
        <div className="card border-emerald-200 bg-emerald-50">
          <div className="flex items-start">
            <div className="w-10 h-10 bg-emerald-100 rounded-lg flex items-center justify-center mr-4 flex-shrink-0">
              <span className="text-xl">ℹ️</span>
            </div>
            <div>
              <h3 className="text-lg font-semibold text-emerald-900 mb-1">Phase 1 — Authentication Foundation</h3>
              <p className="text-emerald-700 text-sm">
                You are authenticated as a Faculty member. Your personal research profile, publications,
                platform profiles, and notifications will be available in the next phase.
              </p>
              <div className="mt-4 grid grid-cols-2 gap-3">
                <div className="bg-white rounded-lg p-3 border border-emerald-100">
                  <p className="text-xs text-gray-500">Your Role</p>
                  <p className="font-medium text-gray-900">{ROLE_LABELS[currentUser?.role]}</p>
                </div>
                <div className="bg-white rounded-lg p-3 border border-emerald-100">
                  <p className="text-xs text-gray-500">Department</p>
                  <p className="font-medium text-gray-900">{DEPARTMENT_LABELS[currentUser?.department] || currentUser?.department}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default FacultyDashboard;
