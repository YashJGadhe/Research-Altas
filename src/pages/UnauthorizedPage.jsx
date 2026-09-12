/**
 * ResearchAtlas - Unauthorized Page
 * 
 * Displayed when a user tries to access a route they don't have permission for.
 */

import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { ROLE_DASHBOARD_MAP, ROUTES } from '../utils/constants';

const UnauthorizedPage = () => {
  const navigate = useNavigate();
  const { isAuthenticated, role } = useAuth();

  const handleGoBack = () => {
    if (isAuthenticated && role) {
      navigate(ROLE_DASHBOARD_MAP[role] || ROUTES.LOGIN);
    } else {
      navigate(ROUTES.LOGIN);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 to-red-50 px-4">
      <div className="text-center max-w-md">
        <div className="inline-flex items-center justify-center w-20 h-20 bg-red-100 rounded-full mb-6">
          <svg className="w-10 h-10 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
        </div>
        <h1 className="text-3xl font-bold text-gray-900 mb-3">Access Denied</h1>
        <p className="text-gray-600 mb-8">
          You don't have permission to access this page. Please contact an administrator if you believe this is an error.
        </p>
        <button onClick={handleGoBack} className="btn-primary">
          Go to Dashboard
        </button>
      </div>
    </div>
  );
};

export default UnauthorizedPage;
