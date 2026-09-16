/**
 * ResearchAtlas - Login Page
 * 
 * Handles user authentication.
 * On success, stores token/user and redirects based on role.
 */

import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { login as loginApi } from '../../api/authApi';
import { useAuth } from '../../hooks/useAuth';
import { ROLE_DASHBOARD_MAP, ROUTES, EMAIL_REGEX, ROLE_EMAIL_DOMAINS, ROLES, ROLE_LABELS } from '../../utils/constants';

const LoginPage = () => {
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  // If already authenticated, redirect to dashboard
  React.useEffect(() => {
    if (isAuthenticated) {
      const from = location.state?.from?.pathname;
      navigate(from || ROUTES.LOGIN, { replace: true });
    }
  }, [isAuthenticated, navigate, location]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    // Client-side validation
    if (!formData.email || !formData.password) {
      setError('Please fill in all fields.');
      return;
    }

    if (!EMAIL_REGEX.test(formData.email)) {
      setError('Please enter a valid email address.');
      return;
    }

    setLoading(true);

    try {
      const response = await loginApi(formData);
      
      // Store auth data via context
      login(response);

      // Redirect based on role
      const dashboardRoute = ROLE_DASHBOARD_MAP[response.user.role];
      const redirectTo = location.state?.from?.pathname || dashboardRoute;
      navigate(redirectTo, { replace: true });
    } catch (err) {
      if (err.response?.data?.detail) {
        setError(err.response.data.detail);
      } else if (err.response?.status === 401) {
        setError('Invalid email or password.');
      } else if (err.response?.status === 403) {
        setError('Your account has been deactivated. Please contact an administrator.');
      } else {
        setError('Login failed. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 px-4 py-8">
      <div className="w-full max-w-md">
        {/* Demo Banner */}
        <div className="mb-4 p-3 bg-gradient-to-r from-purple-600 to-blue-600 rounded-xl text-white text-center shadow-lg">
          <p className="text-sm font-semibold flex items-center justify-center gap-2">
            <span>🎮</span> Preview Demo Mode <span>🎮</span>
          </p>
          <p className="text-xs opacity-90 mt-0.5">Click "Login as Admin" below to explore</p>
        </div>

        {/* Header */}
        <div className="text-center mb-6">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-600 rounded-2xl shadow-lg mb-4">
            <span className="text-3xl">🌐</span>
          </div>
          <h1 className="text-3xl font-bold text-gray-900">ResearchAtlas</h1>
          <p className="text-gray-500 mt-2">Research & Development Information Management</p>
        </div>

        {/* Login Card */}
        <div className="bg-white rounded-2xl shadow-xl border border-gray-100 p-8">
          <h2 className="text-2xl font-semibold text-gray-900 mb-6">Sign In</h2>

          {error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1.5">
                Email Address
              </label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className="input-field"
                placeholder="you@raisoni.net"
                autoComplete="email"
                required
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1.5">
                Password
              </label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                className="input-field"
                placeholder="••••••••"
                autoComplete="current-password"
                required
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="btn-primary w-full py-3 text-base"
            >
              {loading ? (
                <span className="flex items-center justify-center">
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                  </svg>
                  Signing in...
                </span>
              ) : (
                'Sign In'
              )}
            </button>
          </form>

          {/* Email Domain Info */}
          <div className="mt-6 p-3 bg-blue-50 border border-blue-100 rounded-lg">
            <p className="text-xs text-blue-700 font-medium mb-1">Accepted Email Domains:</p>
            <ul className="text-xs text-blue-600 space-y-0.5">
              <li>• Admin & Faculty: <strong>@raisoni.net</strong></li>
              <li>• Students: <strong>@ghrce.raisoni.net</strong></li>
            </ul>
          </div>

          {/* Demo Mode Quick Login */}
          <div className="mt-4 p-4 bg-gradient-to-r from-purple-50 to-blue-50 border border-purple-200 rounded-lg">
            <p className="text-xs text-purple-700 font-semibold mb-3 flex items-center gap-1">
              <span>🎮</span> Demo Mode - Quick Login
            </p>
            
            {/* One-click Admin Login */}
            <button
              type="button"
              onClick={async () => {
                setError('');
                setLoading(true);
                try {
                  // Enable demo mode first
                  localStorage.setItem('demoMode', 'true');
                  
                  // Import mock API directly
                  const { mockLogin } = await import('../../api/mockApi');
                  const response = await mockLogin('admin@test.com', 'Admin@123');
                  
                  // Use the login function from AuthContext
                  login(response);
                  
                  // Navigate to admin dashboard
                  navigate(ROUTES.ADMIN_DASHBOARD, { replace: true });
                } catch (err) {
                  console.error('Demo login error:', err);
                  setError('Demo login failed. Please try again.');
                } finally {
                  setLoading(false);
                }
              }}
              disabled={loading}
              className="w-full mb-3 py-2.5 px-4 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white font-semibold rounded-lg text-sm transition-all shadow-md hover:shadow-lg flex items-center justify-center gap-2"
            >
              <span>👑</span>
              <span>Login as Admin (Demo)</span>
            </button>

            <div className="space-y-2">
              <button
                type="button"
                onClick={async () => {
                  setError('');
                  setLoading(true);
                  try {
                    localStorage.setItem('demoMode', 'true');
                    const { mockLogin } = await import('../../api/mockApi');
                    const response = await mockLogin('admin@test.com', 'Admin@123');
                    login(response);
                    navigate(ROUTES.ADMIN_DASHBOARD, { replace: true });
                  } catch (err) {
                    console.error('Demo login error:', err);
                    setError('Demo login failed. Please try again.');
                  } finally {
                    setLoading(false);
                  }
                }}
                disabled={loading}
                className="w-full text-left px-3 py-2 bg-white hover:bg-purple-50 border border-purple-200 rounded-md text-xs transition-colors"
              >
                <span className="font-semibold text-purple-700">👑 Admin:</span>
                <span className="text-gray-600 ml-1">admin@test.com / Admin@123</span>
              </button>
              <button
                type="button"
                onClick={async () => {
                  setError('');
                  setLoading(true);
                  try {
                    localStorage.setItem('demoMode', 'true');
                    const { mockLogin } = await import('../../api/mockApi');
                    const response = await mockLogin('faculty@test.com', 'Faculty@123');
                    login(response);
                    navigate(ROUTES.FACULTY_DASHBOARD, { replace: true });
                  } catch (err) {
                    console.error('Demo login error:', err);
                    setError('Demo login failed. Please try again.');
                  } finally {
                    setLoading(false);
                  }
                }}
                disabled={loading}
                className="w-full text-left px-3 py-2 bg-white hover:bg-emerald-50 border border-emerald-200 rounded-md text-xs transition-colors"
              >
                <span className="font-semibold text-emerald-700">👨‍🏫 Faculty:</span>
                <span className="text-gray-600 ml-1">faculty@test.com / Faculty@123</span>
              </button>
              <button
                type="button"
                onClick={async () => {
                  setError('');
                  setLoading(true);
                  try {
                    localStorage.setItem('demoMode', 'true');
                    const { mockLogin } = await import('../../api/mockApi');
                    const response = await mockLogin('student@test.com', 'Student@123');
                    login(response);
                    navigate(ROUTES.STUDENT_DASHBOARD, { replace: true });
                  } catch (err) {
                    console.error('Demo login error:', err);
                    setError('Demo login failed. Please try again.');
                  } finally {
                    setLoading(false);
                  }
                }}
                disabled={loading}
                className="w-full text-left px-3 py-2 bg-white hover:bg-amber-50 border border-amber-200 rounded-md text-xs transition-colors"
              >
                <span className="font-semibold text-amber-700">🎓 Student:</span>
                <span className="text-gray-600 ml-1">student@test.com / Student@123</span>
              </button>
            </div>
          </div>

          <div className="mt-4 text-center">
            <p className="text-gray-600 text-sm">
              Don't have an account?{' '}
              <Link to={ROUTES.REGISTER} className="text-blue-600 hover:text-blue-700 font-medium">
                Register here
              </Link>
            </p>
          </div>
        </div>

        <p className="text-center text-gray-400 text-xs mt-6">
          © 2026 ResearchAtlas. All rights reserved.
        </p>
      </div>
    </div>
  );
};

export default LoginPage;
